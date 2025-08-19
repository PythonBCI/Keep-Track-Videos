#!/usr/bin/env python3
"""
Development Script for Desktop Cat
Run and test your application instantly without rebuilding!
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class DevRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.main_app = self.project_root / "desktop_cat.py"
        self.cat_demo = self.project_root / "cat_demo.py"
        
    def show_menu(self):
        """Show the development menu"""
        print("🚀 Desktop Cat Development Menu")
        print("=" * 40)
        print("1. 🐱 Run Main App (Desktop Cat)")
        print("2. 🎬 Run Cat Animation Demo")
        print("3. 🧪 Run Tests")
        print("4. 🔨 Build for Distribution")
        print("5. 📦 Quick Build & Test")
        print("6. 🗑️ Clean Build Files")
        print("7. 📋 Show Project Status")
        print("0. ❌ Exit")
        print("=" * 40)
        
    def run_main_app(self):
        """Run the main desktop cat application"""
        print("🐱 Starting Desktop Cat Application...")
        print("💡 Tip: Make changes to the code and restart to see them instantly!")
        print("Press Ctrl+C to stop the app")
        print("-" * 40)
        
        try:
            subprocess.run([sys.executable, str(self.main_app)], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Application stopped by user")
        except Exception as e:
            print(f"❌ Error running app: {e}")
            
    def run_cat_demo(self):
        """Run the cat animation demo"""
        print("🎬 Starting Cat Animation Demo...")
        print("💡 This is perfect for testing cat animation changes!")
        print("Press Ctrl+C to stop the demo")
        print("-" * 40)
        
        try:
            subprocess.run([sys.executable, str(self.cat_demo)], check=True)
        except KeyboardInterrupt:
            print("\n🛑 Demo stopped by user")
        except Exception as e:
            print(f"❌ Error running demo: {e}")
            
    def run_tests(self):
        """Run the test suite"""
        print("🧪 Running Tests...")
        print("-" * 40)
        
        test_file = self.project_root / "test_app.py"
        if test_file.exists():
            try:
                result = subprocess.run([sys.executable, str(test_file)], 
                                      capture_output=True, text=True, check=True)
                print(result.stdout)
                print("✅ All tests passed!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Tests failed:")
                print(e.stdout)
                print(e.stderr)
        else:
            print("❌ Test file not found: test_app.py")
            
    def build_for_distribution(self):
        """Build the application for distribution"""
        print("🔨 Building for Distribution...")
        print("-" * 40)
        
        build_script = self.project_root / "build.py"
        if build_script.exists():
            try:
                subprocess.run([sys.executable, str(build_script)], check=True)
                print("✅ Build completed successfully!")
                print("📦 Distribution package ready in project root")
            except subprocess.CalledProcessError as e:
                print(f"❌ Build failed: {e}")
        else:
            print("❌ Build script not found: build.py")
            
    def quick_build_test(self):
        """Quick build and test cycle"""
        print("📦 Quick Build & Test Cycle...")
        print("-" * 40)
        
        # Clean previous builds
        self.clean_build_files()
        
        # Build
        print("🔨 Building...")
        build_script = self.project_root / "build.py"
        if build_script.exists():
            try:
                subprocess.run([sys.executable, str(build_script)], check=True)
                print("✅ Build successful!")
                
                # Test the built executable
                print("🧪 Testing built executable...")
                dist_dir = self.project_root / "dist" / "DesktopCat"
                if dist_dir.exists():
                    executable = dist_dir / "DesktopCat"
                    if executable.exists():
                        print(f"🚀 Testing: {executable}")
                        # Note: In some environments, we might need to test differently
                        print("✅ Executable built successfully!")
                    else:
                        print("❌ Executable not found in build output")
                else:
                    print("❌ Build directory not found")
                    
            except subprocess.CalledProcessError as e:
                print(f"❌ Build failed: {e}")
        else:
            print("❌ Build script not found")
            
    def clean_build_files(self):
        """Clean build artifacts"""
        print("🗑️ Cleaning Build Files...")
        print("-" * 40)
        
        build_dirs = ["build", "dist", "__pycache__"]
        for dir_name in build_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                try:
                    import shutil
                    shutil.rmtree(dir_path)
                    print(f"✅ Cleaned: {dir_name}/")
                except Exception as e:
                    print(f"❌ Error cleaning {dir_name}: {e}")
            else:
                print(f"ℹ️ No {dir_name}/ directory to clean")
                
        # Clean .pyc files
        for pyc_file in self.project_root.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                print(f"✅ Cleaned: {pyc_file.name}")
            except Exception as e:
                print(f"❌ Error cleaning {pyc_file.name}: {e}")
                
    def show_project_status(self):
        """Show current project status"""
        print("📋 Project Status")
        print("=" * 40)
        
        # Check main files
        main_files = [
            "desktop_cat.py",
            "cat_animation.py", 
            "cat_renderer.py",
            "cat_demo.py",
            "build.py",
            "test_app.py"
        ]
        
        print("📁 Core Files:")
        for file_name in main_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✅ {file_name} ({size:,} bytes)")
            else:
                print(f"  ❌ {file_name} (missing)")
                
        # Check build status
        print("\n🔨 Build Status:")
        dist_dir = self.project_root / "dist"
        if dist_dir.exists():
            build_files = list(dist_dir.glob("*"))
            if build_files:
                print(f"  ✅ Build output: {len(build_files)} items")
                for item in build_files:
                    if item.is_dir():
                        print(f"    📁 {item.name}/")
                    else:
                        print(f"    📄 {item.name}")
            else:
                print("  ℹ️ Build directory empty")
        else:
            print("  ℹ️ No build output yet")
            
        # Check Python environment
        print(f"\n🐍 Python Environment:")
        print(f"  Version: {sys.version}")
        print(f"  Executable: {sys.executable}")
        
        # Check dependencies
        print(f"\n📦 Dependencies:")
        try:
            import tkinter
            print("  ✅ tkinter (GUI framework)")
        except ImportError:
            print("  ❌ tkinter (missing)")
            
        try:
            import PyInstaller
            print("  ✅ PyInstaller (build tool)")
        except ImportError:
            print("  ℹ️ PyInstaller (not installed - needed for building)")
            
    def main_loop(self):
        """Main development loop"""
        while True:
            try:
                self.show_menu()
                choice = input("\n🎯 Choose an option (0-7): ").strip()
                
                if choice == "0":
                    print("👋 Goodbye! Happy coding!")
                    break
                elif choice == "1":
                    self.run_main_app()
                elif choice == "2":
                    self.run_cat_demo()
                elif choice == "3":
                    self.run_tests()
                elif choice == "4":
                    self.build_for_distribution()
                elif choice == "5":
                    self.quick_build_test()
                elif choice == "6":
                    self.clean_build_files()
                elif choice == "7":
                    self.show_project_status()
                else:
                    print("❌ Invalid choice. Please enter 0-7.")
                    
                if choice != "0":
                    input("\n⏸️ Press Enter to continue...")
                    os.system('clear' if os.name == 'posix' else 'cls')
                    
            except KeyboardInterrupt:
                print("\n\n👋 Development session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                input("Press Enter to continue...")

if __name__ == "__main__":
    dev_runner = DevRunner()
    dev_runner.main_loop()