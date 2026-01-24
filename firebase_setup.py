"""
Firebase Setup Instructions
==========================

1. Install Firebase Admin SDK:
pip install firebase-admin

2. Set up Firebase Project:
   - Go to https://console.firebase.google.com
   - Create a new project or use existing one
   - Enable Authentication (Email/Password)
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file and save as 'serviceAccountKey.json'

3. Add to your app.py:
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Get Firestore database
db = firestore.client()

# Example User Operations:
def create_firebase_user(email, password, username):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )
        # Store additional user data in Firestore
        db.collection('users').document(user.uid).set({
            'username': username,
            'email': email,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def login_firebase_user(email, password):
    try:
        # Note: Firebase Admin SDK doesn't support password verification
        # You'll need to use Firebase Client SDK on frontend
        # Or use Firebase REST API for authentication
        pass
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None
"""
