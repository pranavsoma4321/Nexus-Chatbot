# Firebase Connectivity Troubleshooting Guide

## 🚨 Error: "Failed to get document because the client is offline"

This error indicates Firebase cannot connect to your project. Follow these steps to resolve:

## 🔧 Quick Fixes

### 1. Check Internet Connection
- Ensure you have a stable internet connection
- Try loading other websites to verify connectivity
- If on WiFi, try switching to mobile data or vice versa

### 2. Firebase Project Settings
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `chatbot-51009`
3. Go to **Project Settings** → **General**
4. Verify your **Project ID** matches: `chatbot-51009`

### 3. Enable Firestore Database
1. In Firebase Console, go to **Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (for development)
4. Select a location (choose closest to your users)
5. Click **Create**

### 4. Check Security Rules
In Firestore → **Rules** tab, ensure you have:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 5. Clear Browser Cache
- Press `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Or clear cache in browser settings

## 🛠 Advanced Solutions

### Check Firebase Configuration
Verify your `firebase-config.js` has correct settings:
- `projectId`: "chatbot-51009"
- `apiKey`: Should match your Firebase project

### Network Issues
If you're behind a corporate firewall:
- Contact IT to allow Firebase domains:
  - `*.firebaseio.com`
  - `*.googleapis.com`
  - `*.google.com`

### Browser Console Debugging
1. Open Developer Tools (F12)
2. Go to **Console** tab
3. Look for additional error messages
4. Check **Network** tab for failed requests

## 🧪 Test Your Connection

Use the test page to diagnose:
1. Open `test-auth.html`
2. Check authentication status
3. Open `test-assignments.html`
4. Verify assignment loading

## 📱 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Permission denied" | Update Firestore security rules |
| "Project not found" | Verify project ID in config |
| "API key invalid" | Regenerate API key in Firebase Console |
| Intermittent connection | Check network stability |

## 🔄 Automatic Retry System

The app now includes:
- **Automatic retries** (up to 3 attempts)
- **Exponential backoff** (delays between retries)
- **Network status monitoring**
- **Offline detection**

## 📞 Still Having Issues?

1. **Check Firebase Status**: [status.firebase.google.com](https://status.firebase.google.com)
2. **Verify Project**: Ensure project exists and is active
3. **Regenerate Keys**: Create new API keys if needed
4. **Contact Support**: Reach out to Firebase support

## ✅ Success Checklist

When everything works, you should see:
- ✅ Green "Logged in" status
- ✅ Username displayed in navigation
- ✅ Assignments load without errors
- ✅ Can create new assignments
- ✅ No console errors

---

**Last Updated**: January 2024
**Firebase SDK Version**: 10.7.1
