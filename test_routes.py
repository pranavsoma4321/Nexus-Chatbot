#!/usr/bin/env python3
"""
Test script to verify all Flask routes are working
"""

import requests
import time

# Base URL for testing
BASE_URL = "http://localhost:5000"

def test_route(route_name, url):
    """Test a single route"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {route_name}: {url} - OK ({response.status_code})")
            return True
        else:
            print(f"❌ {route_name}: {url} - Failed ({response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {route_name}: {url} - Error: {e}")
        return False

def main():
    """Test all routes"""
    print("🧪 Testing NexusBot Flask Routes...")
    print("=" * 50)
    
    routes = [
        ("Home", f"{BASE_URL}/"),
        ("Home Page", f"{BASE_URL}/home"),
        ("Login", f"{BASE_URL}/login"),
        ("Signup", f"{BASE_URL}/signup"),
        ("Customize Upload", f"{BASE_URL}/customize_upload"),
        ("Choose Model", f"{BASE_URL}/choose_model"),
        ("Customize Chatbot", f"{BASE_URL}/customize_chatbot"),
        ("Bot Builder", f"{BASE_URL}/bot_builder"),
        ("Templates", f"{BASE_URL}/templates"),
        ("My Bots", f"{BASE_URL}/my_bots"),
        ("Assignments", f"{BASE_URL}/assignments"),
    ]
    
    success_count = 0
    total_count = len(routes)
    
    for route_name, url in routes:
        if test_route(route_name, url):
            success_count += 1
        time.sleep(0.1)  # Small delay between requests
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_count} routes working")
    
    if success_count == total_count:
        print("🎉 All routes are working correctly!")
    else:
        print("⚠️  Some routes are not working. Check the Flask app.")

if __name__ == "__main__":
    main()
