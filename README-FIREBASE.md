# Firebase Authentication Setup Guide

## 🚀 Quick Start

### 1. Test Your Firebase Setup
Open `test-auth.html` in your browser to test the Firebase authentication:

```bash
# Start a simple HTTP server (recommended)
python -m http.server 8000
# Then visit: http://localhost:8000/test-auth.html
```

### 2. Enable Email/Password Authentication
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `chatbot-51009`
3. Go to **Authentication** → **Sign-in method**
4. Enable **Email/Password** provider
5. Click **Save**

### 3. Test the Authentication
Use the test page to:
- ✅ Create a test user
- ✅ Login with the test user
- ✅ Logout the user
- ✅ Check real-time auth status

## 📁 How to Use in Your Project

### Login Page
Visit `login.html`:
- Users can login with email/password
- Real-time validation
- Auto-redirect on success
- Toast notifications

### Signup Page
Visit `templates/signup.html`:
- Users can create new accounts
- Password confirmation
- Validation for minimum 6 characters
- Stores user data in Firestore

### Integration with Existing Pages
Add this to any HTML page to show user info:

```html
<!-- Add to your <head> -->
<script type="module" src="static/auth-ui.js"></script>

<!-- Add to your HTML where you want to show username -->
<span class="username-display">Guest</span>

<!-- Add login/logout buttons -->
<button class="login-btn">Login</button>
<button class="logout-btn hidden">Logout</button>
```

## 🔧 File Structure

```
├── static/
│   ├── firebase-config.js     # Firebase configuration
│   ├── firebase-auth.js       # Authentication service
│   └── auth-ui.js            # UI management
├── login.html                # Login page
├── templates/
│   └── signup.html           # Signup page
└── test-auth.html           # Test page
```

## 📊 Data Storage

### Firebase Authentication
- User credentials (email, password)
- User ID and basic profile

### Firestore Database
- Collection: `users`
- Documents: User ID as document name
- Fields:
  ```javascript
  {
    username: "string",
    email: "string", 
    createdAt: "timestamp",
    lastLogin: "timestamp"
  }
  ```

## 🛠 Common Usage Examples

### Check if User is Logged In
```javascript
import authService from './static/firebase-auth.js';

const user = authService.getCurrentUser();
if (user) {
  console.log('User is logged in:', user.email);
} else {
  console.log('No user logged in');
}
```

### Get User Data from Firestore
```javascript
const userData = await authService.getUserData(user.uid);
if (userData.success) {
  console.log('User data:', userData.data);
}
```

### Handle Logout
```javascript
const result = await authService.signOut();
if (result.success) {
  window.location.href = '/login.html';
}
```

## 🔒 Security Notes

- ✅ Passwords are securely stored by Firebase
- ✅ Authentication tokens are managed automatically
- ✅ Firestore rules should be configured for production

## 🐛 Troubleshooting

### "auth/operation-not-allowed"
- Go to Firebase Console → Authentication → Sign-in method
- Enable Email/Password provider

### "auth/network-request-failed"
- Check your internet connection
- Verify Firebase project configuration

### CORS Issues
- Use a local HTTP server instead of opening files directly
- `python -m http.server 8000` or `npx serve .`

### Module Import Errors
- Ensure you're using a modern browser
- Use `type="module"` in script tags
- Serve files via HTTP, not file://

## 📱 Mobile Usage

The same Firebase setup works for mobile apps. Just include the same config files and use the same authentication service.

## 🚀 Next Steps

1. Test with `test-auth.html`
2. Enable Email/Password in Firebase Console
3. Try login/signup pages
4. Integrate with your existing pages
5. Configure Firestore security rules for production
