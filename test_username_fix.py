#!/usr/bin/env python3
"""
Test script to verify the username fix in home.html template
"""

from flask import Flask, render_template, session
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_username_rendering():
    """Test that username is properly passed to template"""
    
    with app.test_client() as client:
        # Test with a logged-in user
        with app.test_request_context():
            # Simulate a logged-in user session
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['username'] = 'TestUser'
            
            # Get the home page
            response = client.get('/home')
            
            # Check if the response is successful
            assert response.status_code == 200
            
            # Get the HTML content
            html_content = response.get_data(as_text=True)
            
            # Check if the username is properly rendered in the data-username attribute
            if 'data-username="TestUser"' in html_content:
                print("✅ SUCCESS: Username is properly passed to template!")
                print("✅ The 'welcome undefined' issue should be fixed.")
                return True
            else:
                print("❌ FAILED: Username not found in template")
                print("❌ Checking for data-username attribute...")
                
                # Show a snippet around where username should be
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'usernameDisplay' in line:
                        print(f"Line {i+1}: {line.strip()}")
                        break
                return False

def test_guest_user():
    """Test with guest user (not logged in)"""
    
    with app.test_client() as client:
        with app.test_request_context():
            # No session data (guest user)
            response = client.get('/home')
            
            html_content = response.get_data(as_text=True)
            
            if 'data-username="Guest"' in html_content:
                print("✅ SUCCESS: Guest user properly handled!")
                return True
            else:
                print("❌ FAILED: Guest user not handled properly")
                return False

if __name__ == "__main__":
    print("🧪 Testing username fix...")
    print("=" * 50)
    
    try:
        success1 = test_username_rendering()
        success2 = test_guest_user()
        
        print("=" * 50)
        if success1 and success2:
            print("🎉 All tests passed! The username fix is working correctly.")
        else:
            print("⚠️  Some tests failed. Please check the implementation.")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
