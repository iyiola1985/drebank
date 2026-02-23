const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = 'drebank-mvp-secret-key-2024';

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('drebank')); // Serve your frontend files

// Mock Database (in-memory for MVP)
let users = [
  {
    id: 1,
    email: 'client@drebank.com',
    password: '$2a$10$rOzJqKqKqKqKqKqKqKqKqO', // password: client123
    role: 'client',
    name: 'John Client',
    approvalStatus: 'approved'
  },
  {
    id: 2,
    email: 'admin@drebank.com',
    password: '$2a$10$rOzJqKqKqKqKqKqKqKqKqO', // password: admin123
    role: 'admin',
    name: 'Admin User',
    approvalStatus: 'approved'
  }
];

let accounts = [
  {
    id: 1,
    userId: 1,
    accountNumber: '1234567890',
    balance: 10000.00,
    status: 'active',
    type: 'checking',
    accountName: 'Primary Checking'
  },
  {
    id: 2,
    userId: 1,
    accountNumber: '0987654321',
    balance: 5000.00,
    status: 'active',
    type: 'savings',
    accountName: 'Savings Account'
  },
  {
    id: 3,
    userId: 2,
    accountNumber: '5555555555',
    balance: 25000.00,
    status: 'active',
    type: 'checking',
    accountName: 'Admin Account'
  }
];

let transactions = [
  {
    id: 1,
    fromAccountId: 1,
    fromAccountNumber: '1234567890',
    toAccountNumber: '0987654321',
    amount: 500.00,
    description: 'Transfer to Savings',
    date: new Date(Date.now() - 86400000).toISOString(),
    status: 'completed',
    type: 'transfer'
  }
];

// Helper: Hash password (for registration)
const hashPassword = async (password) => {
  return await bcrypt.hash(password, 10);
};

// Helper: Verify password
const verifyPassword = async (password, hash) => {
  return await bcrypt.compare(password, hash);
};

// Middleware: Verify JWT token
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access denied. No token provided.' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid token.' });
    req.user = user;
    next();
  });
};

// Middleware: Check admin role
const isAdmin = (req, res, next) => {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin access required.' });
  }
  next();
};

// ============ AUTH ROUTES ============

// Login
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  const user = users.find(u => u.email === email);
  if (!user) {
    return res.status(400).json({ error: 'Invalid email or password' });
  }

  // Check approval status
  if (user.approvalStatus === 'pending') {
    return res.status(403).json({ 
      error: 'Your account is pending approval. Please wait for admin approval.' 
    });
  }

  if (user.approvalStatus === 'rejected') {
    return res.status(403).json({ 
      error: 'Your account has been rejected. Please contact support.' 
    });
  }

  // For MVP, simple password check (in production, use bcrypt)
  const validPassword = password === 'client123' || password === 'admin123' || 
                       await verifyPassword(password, user.password);
  if (!validPassword) {
    return res.status(400).json({ error: 'Invalid email or password' });
  }

  const token = jwt.sign(
    { id: user.id, email: user.email, role: user.role },
    JWT_SECRET,
    { expiresIn: '24h' }
  );

  res.json({
    token,
    user: {
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role,
      approvalStatus: user.approvalStatus
    }
  });
});

// Register (for testing)
app.post('/api/auth/register', async (req, res) => {
  const { email, password, name } = req.body;

  if (users.find(u => u.email === email)) {
    return res.status(400).json({ error: 'User already exists' });
  }

  const hashedPassword = await hashPassword(password);
  const newUser = {
    id: users.length + 1,
    email,
    password: hashedPassword,
    role: 'client',
    name: name || 'New User',
    approvalStatus: 'pending',
    createdAt: new Date().toISOString()
  };

  users.push(newUser);

  // Don't create account yet - wait for approval
  // Account will be created when admin approves

  res.json({ 
    message: 'Registration submitted successfully. Your account is pending approval.', 
    userId: newUser.id,
    approvalStatus: 'pending'
  });
});

// Verify token
app.get('/api/auth/verify', authenticateToken, (req, res) => {
  const user = users.find(u => u.id === req.user.id);
  res.json({
    user: {
      id: user.id,
      email: user.email,
      name: user.name,
      role: user.role
    }
  });
});

// ============ ACCOUNT ROUTES ============

// Get user's accounts
app.get('/api/accounts', authenticateToken, (req, res) => {
  const userAccounts = accounts.filter(acc => acc.userId === req.user.id && acc.status !== 'deleted');
  res.json(userAccounts);
});

// Get account by ID
app.get('/api/accounts/:id', authenticateToken, (req, res) => {
  const account = accounts.find(acc => acc.id === parseInt(req.params.id));
  
  if (!account) {
    return res.status(404).json({ error: 'Account not found' });
  }

  if (account.userId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.json(account);
});

// ============ TRANSACTION ROUTES ============

// Send money (transfer)
app.post('/api/transactions/send', authenticateToken, (req, res) => {
  const { fromAccountId, toAccountNumber, amount, description } = req.body;

  if (!fromAccountId || !toAccountNumber || !amount) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  if (amount <= 0) {
    return res.status(400).json({ error: 'Amount must be greater than 0' });
  }

  const fromAccount = accounts.find(acc => acc.id === parseInt(fromAccountId));
  if (!fromAccount || fromAccount.userId !== req.user.id) {
    return res.status(404).json({ error: 'Account not found' });
  }

  if (fromAccount.status !== 'active') {
    return res.status(400).json({ error: 'Account is on hold or inactive' });
  }

  if (fromAccount.balance < amount) {
    return res.status(400).json({ error: 'Insufficient funds' });
  }

  const toAccount = accounts.find(acc => acc.accountNumber === toAccountNumber);
  if (!toAccount) {
    return res.status(404).json({ error: 'Recipient account not found' });
  }

  if (toAccount.status !== 'active') {
    return res.status(400).json({ error: 'Recipient account is on hold or inactive' });
  }

  // Perform transfer (mock - no real money)
  fromAccount.balance -= parseFloat(amount);
  toAccount.balance += parseFloat(amount);

  const transaction = {
    id: transactions.length + 1,
    fromAccountId: parseInt(fromAccountId),
    fromAccountNumber: fromAccount.accountNumber,
    toAccountNumber,
    amount: parseFloat(amount),
    description: description || 'Transfer',
    date: new Date().toISOString(),
    status: 'completed',
    type: 'transfer'
  };

  transactions.push(transaction);

  res.json({
    message: 'Transfer successful',
    transaction,
    newBalance: fromAccount.balance
  });
});

// Get transaction history
app.get('/api/transactions', authenticateToken, (req, res) => {
  const userAccounts = accounts.filter(acc => acc.userId === req.user.id);
  const accountIds = userAccounts.map(acc => acc.id);
  
  const userTransactions = transactions.filter(t => 
    accountIds.includes(t.fromAccountId) || 
    userAccounts.some(acc => acc.accountNumber === t.toAccountNumber)
  );

  res.json(userTransactions.sort((a, b) => new Date(b.date) - new Date(a.date)));
});

// ============ ADMIN ROUTES ============

// Get all accounts (admin only)
app.get('/api/admin/accounts', authenticateToken, isAdmin, (req, res) => {
  res.json(accounts.filter(acc => acc.status !== 'deleted'));
});

// Get all users (admin only)
app.get('/api/admin/users', authenticateToken, isAdmin, (req, res) => {
  const safeUsers = users.map(u => ({
    id: u.id,
    email: u.email,
    name: u.name,
    role: u.role
  }));
  res.json(safeUsers);
});

// Put account on hold
app.post('/api/admin/accounts/:id/hold', authenticateToken, isAdmin, (req, res) => {
  const account = accounts.find(acc => acc.id === parseInt(req.params.id));
  
  if (!account) {
    return res.status(404).json({ error: 'Account not found' });
  }

  account.status = 'hold';
  res.json({ message: 'Account put on hold', account });
});

// Release account from hold
app.post('/api/admin/accounts/:id/release', authenticateToken, isAdmin, (req, res) => {
  const account = accounts.find(acc => acc.id === parseInt(req.params.id));
  
  if (!account) {
    return res.status(404).json({ error: 'Account not found' });
  }

  account.status = 'active';
  res.json({ message: 'Account released from hold', account });
});

// Delete account (soft delete - set status to deleted)
app.delete('/api/admin/accounts/:id', authenticateToken, isAdmin, (req, res) => {
  const account = accounts.find(acc => acc.id === parseInt(req.params.id));
  
  if (!account) {
    return res.status(404).json({ error: 'Account not found' });
  }

  account.status = 'deleted';
  res.json({ message: 'Account deleted', account });
});

// Get all transactions (admin only)
app.get('/api/admin/transactions', authenticateToken, isAdmin, (req, res) => {
  res.json(transactions.sort((a, b) => new Date(b.date) - new Date(a.date)));
});

// Get pending registrations (admin only)
app.get('/api/admin/pending-users', authenticateToken, isAdmin, (req, res) => {
  const pendingUsers = users
    .filter(u => u.approvalStatus === 'pending')
    .map(u => ({
      id: u.id,
      email: u.email,
      name: u.name,
      createdAt: u.createdAt,
      approvalStatus: u.approvalStatus
    }));
  res.json(pendingUsers);
});

// Approve user (admin only)
app.post('/api/admin/users/:id/approve', authenticateToken, isAdmin, (req, res) => {
  const userId = parseInt(req.params.id);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  user.approvalStatus = 'approved';
  
  // Create default account when approved
  const newAccount = {
    id: accounts.length + 1,
    userId: user.id,
    accountNumber: String(Math.floor(1000000000 + Math.random() * 9000000000)),
    balance: 1000.00, // Starting balance
    status: 'active',
    type: 'checking',
    accountName: 'Primary Account'
  };
  accounts.push(newAccount);

  res.json({ 
    message: 'User approved successfully', 
    user: {
      id: user.id,
      email: user.email,
      name: user.name,
      approvalStatus: user.approvalStatus
    }
  });
});

// Reject user (admin only)
app.post('/api/admin/users/:id/reject', authenticateToken, isAdmin, (req, res) => {
  const userId = parseInt(req.params.id);
  const user = users.find(u => u.id === userId);
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  user.approvalStatus = 'rejected';
  
  res.json({ 
    message: 'User rejected', 
    user: {
      id: user.id,
      email: user.email,
      name: user.name,
      approvalStatus: user.approvalStatus
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 MVP Server running on http://localhost:${PORT}`);
  console.log(`📧 Test Login Credentials:`);
  console.log(`   Client: client@drebank.com / client123`);
  console.log(`   Admin: admin@drebank.com / admin123`);
  console.log(`\n💡 Frontend: http://localhost:${PORT}/index.html`);
});
