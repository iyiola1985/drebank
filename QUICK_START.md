# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Node.js
If you don't have Node.js installed, download it from: https://nodejs.org/

### Step 2: Install Dependencies
Open terminal in this folder and run:
```bash
npm install
```

### Step 3: Start the Server
```bash
npm start
```

You should see:
```
🚀 MVP Server running on http://localhost:3000
📧 Test Login Credentials:
   Client: client@drebank.com / client123
   Admin: admin@drebank.com / admin123
```

## 🌐 Access the Application

1. **Landing Page**: http://localhost:3000/index.html
2. **Login Page**: http://localhost:3000/secure/customer_login.html

## 🔑 Test Credentials

### Client Account
- Email: `client@drebank.com`
- Password: `client123`
- Features: View accounts, send money, view transactions

### Admin Account
- Email: `admin@drebank.com`
- Password: `admin123`
- Features: View all accounts, put on hold, delete accounts, view all transactions

## ✨ What You Can Test

### As Client:
1. Login with client credentials
2. View your accounts and balances
3. Send money to other accounts (mock transfers)
4. View transaction history

### As Admin:
1. Login with admin credentials
2. View all accounts in the system
3. Put any account on hold
4. Release accounts from hold
5. Delete accounts (soft delete)
6. View all transactions

## 📝 Notes

- All data is stored in memory (resets when server restarts)
- No real money is involved - this is for testing only
- The server must be running for the dashboards to work
- If you see connection errors, make sure the server is running on port 3000

## 🛠️ Troubleshooting

**Port 3000 already in use?**
- Change the PORT in `server.js` or stop the other application

**Can't connect to API?**
- Make sure server is running: `npm start`
- Check that you're accessing via `http://localhost:3000`

**Login not working?**
- Make sure server is running
- Check browser console for errors
- Verify you're using the correct credentials
