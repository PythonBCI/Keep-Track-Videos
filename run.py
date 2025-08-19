#!/usr/bin/env python3
"""
Simple launcher for Desktop Cat - Video Quest Game
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from desktop_cat import DesktopCat
    
    print("🚀 Starting Desktop Cat - Video Quest Game...")
    app = DesktopCat()
    app.run()
    
except ImportError as e:
    print(f"❌ Error importing DesktopCat: {e}")
    print("Make sure desktop_cat.py is in the same directory")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error running DesktopCat: {e}")
    sys.exit(1)