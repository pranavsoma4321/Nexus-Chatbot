#!/usr/bin/env python3
"""
Script to check authentication state and debug login issues
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, User, db
from werkzeug.security import generate_password_hash

def check_database():
    """Check database and create test user if needed"""
    with app.app_context():
        # Check if users exist
        users = User.query.all()
        print(f"📊 Found {len(users)} users in database:")
        
        for user in users:
            print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        
        # Create test user if no users exist
        if len(users) == 0:
            print("\n🔧 Creating test user...")
            test_user = User(
                username='testuser',
                email='test@example.com',
                password_hash=generate_password_hash('testpass123')
            )
            
            try:
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created successfully!")
                print("   Email: test@example.com")
                print("   Password: testpass123")
            except Exception as e:
                print(f"❌ Failed to create test user: {e}")
                db.session.rollback()
        
        return users

def test_login():
    """Test login functionality"""
    with app.app_context():
        # Test login with test user
        user = User.query.filter_by(email='test@example.com').first()
        
        if user:
            print(f"\n🔐 Testing login for user: {user.username}")
            print(f"   User exists: {user is not None}")
            print(f"   Password check: {user.check_password('testpass123')}")
            
            # Simulate session
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['user_id'] = user.id
                    sess['username'] = user.username
                
                # Test home page access
                response = client.get('/home')
                print(f"   Home page status: {response.status_code}")
                
                if response.status_code == 200:
                    html = response.get_data(as_text=True)
                    if f'data-username="{user.username}"' in html:
                        print("   ✅ Username properly passed to template!")
                    else:
                        print("   ❌ Username not found in template")
                        # Show relevant lines
                        lines = html.split('\n')
                        for i, line in enumerate(lines):
                            if 'usernameDisplay' in line:
                                print(f"      Line {i+1}: {line.strip()}")
                                break
        else:
            print("❌ No test user found")

if __name__ == "__main__":
    print("🔍 Checking authentication setup...")
    print("=" * 50)
    
    try:
        users = check_database()
        test_login()
        
        print("\n" + "=" * 50)
        print("📋 Summary:")
        print("1. Make sure you're using Flask login (not Firebase)")
        print("2. Test credentials: test@example.com / testpass123")
        print("3. After login, you should see 'Welcome, testuser!' and logout button")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
