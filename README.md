# Dre Eyes Only Finance - MVP Banking System

A functional MVP banking system for testing and demonstration purposes.

## Features

### Client Features
- ✅ Login/Logout
- ✅ View Accounts
- ✅ Send Money (Mock Transfers)
- ✅ View Transaction History

### Admin Features
- ✅ Admin Login
- ✅ View All Accounts
- ✅ View All Users
- ✅ View All Transactions
- ✅ Put Account on Hold
- ✅ Release Account from Hold
- ✅ Delete Account (Soft Delete)

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

The server will start on `http://localhost:3000`

### 3. Access the Application

- **Frontend**: http://localhost:3000/index.html
- **Login Page**: http://localhost:3000/secure/customer_login.html

## Test Credentials

### Client Login
- **Email**: `client@drebank.com`
- **Password**: `client123`

### Admin Login
- **Email**: `admin@drebank.com`
- **Password**: `admin123`

## Project Structure

```
bankclone/
├── server.js              # Backend API server
├── package.json           # Node.js dependencies
├── drebank/              # Frontend files
│   ├── index.html        # Landing page
│   └── secure/
│       ├── customer_login.html    # Login page
│       ├── client-dashboard.html  # Client dashboard
│       └── admin-dashboard.html   # Admin dashboard
└── README.md             # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register new user
- `GET /api/auth/verify` - Verify token

### Accounts
- `GET /api/accounts` - Get user's accounts
- `GET /api/accounts/:id` - Get account by ID

### Transactions
- `POST /api/transactions/send` - Send money
- `GET /api/transactions` - Get transaction history

### Admin
- `GET /api/admin/accounts` - Get all accounts
- `GET /api/admin/users` - Get all users
- `GET /api/admin/transactions` - Get all transactions
- `POST /api/admin/accounts/:id/hold` - Put account on hold
- `POST /api/admin/accounts/:id/release` - Release account
- `DELETE /api/admin/accounts/:id` - Delete account

## Important Notes

⚠️ **This is an MVP for testing only:**
- No real money is involved
- Data is stored in memory (resets on server restart)
- Simple password authentication (not production-ready)
- For production use, implement:
  - Real database (MySQL/PostgreSQL)
  - Proper password hashing
  - HTTPS/SSL
  - Rate limiting
  - Input validation
  - Security best practices

## Deployment

### Local Development
Just run `npm start` and access at `http://localhost:3000`

### Production Deployment
1. Update `API_BASE_URL` in dashboard files to your production URL
2. Set environment variables for JWT_SECRET
3. Deploy to Vercel, Heroku, Railway, or your preferred platform

## Support

For issues or questions, contact: support@drebabanla.com
