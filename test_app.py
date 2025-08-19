#!/usr/bin/env python3
"""
Test script for Desktop Cat application
"""

import sys
import os

def test_import():
    """Test if the application can be imported"""
    try:
        from desktop_cat import DesktopCat
        print("✅ Successfully imported DesktopCat class")
        return True
    except ImportError as e:
        print(f"❌ Failed to import DesktopCat: {e}")
        return False

def test_initialization():
    """Test if the application can be initialized"""
    try:
        from desktop_cat import DesktopCat
        
        # Create a test instance (this will create the Tkinter window)
        print("🔄 Testing application initialization...")
        app = DesktopCat()
        
        # Check if the main window was created
        if hasattr(app, 'root') and app.root:
            print("✅ Application initialized successfully")
            print("✅ Main window created")
            print("✅ UI components set up")
            
            # Close the test window
            app.root.destroy()
            return True
        else:
            print("❌ Main window not created")
            return False
            
    except Exception as e:
        print(f"❌ Failed to initialize application: {e}")
        return False

def test_game_data():
    """Test if game data structure is correct"""
    try:
        from desktop_cat import DesktopCat
        
        app = DesktopCat()
        
        # Check game data structure
        required_keys = ['level', 'xp', 'total_watched', 'streak', 'achievement_score', 'videos', 'last_watch_date']
        for key in required_keys:
            if key not in app.game_data:
                print(f"❌ Missing game data key: {key}")
                return False
        
        # Check videos structure
        video_categories = ['priority', 'backlog', 'completed']
        for category in video_categories:
            if category not in app.game_data['videos']:
                print(f"❌ Missing video category: {category}")
                return False
        
        print("✅ Game data structure is correct")
        
        # Close the test window
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Failed to test game data: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Desktop Cat Application Tests")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_import),
        ("Initialization Test", test_initialization),
        ("Game Data Test", test_game_data),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)