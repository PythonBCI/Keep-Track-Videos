#!/usr/bin/env python3
"""
Build script for Desktop Cat - Video Quest Game
Automatically creates standalone executables for distribution
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ is required")
        return False
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("✅ PyInstaller is available")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    print("✅ All dependencies are satisfied")
    return True

def build_executable():
    """Build the standalone executable"""
    print("🏗️ Building standalone executable...")
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Build using PyInstaller
    if not run_command("pyinstaller desktop_cat.spec", "Building executable"):
        return False
    
    print("✅ Build completed successfully!")
    return True

def create_distribution():
    """Create a distribution package"""
    print("📦 Creating distribution package...")
    
    # Get platform info
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    # Create distribution directory
    dist_name = f"DesktopCat-{system}-{arch}"
    dist_dir = f"dist/{dist_name}"
    
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir, exist_ok=True)
    
    # Copy executable and dependencies
    source_dir = "dist/DesktopCat"
    if os.path.exists(source_dir):
        # Remove destination if it exists
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        shutil.copytree(source_dir, dist_dir)
    
    # Copy README and other files
    if os.path.exists("README.md"):
        shutil.copy("README.md", dist_dir)
    
    # Create a simple launcher script for Linux/Mac
    if system != "windows":
        launcher_content = f"""#!/bin/bash
# Desktop Cat Launcher
cd "$(dirname "$0")"
./DesktopCat
"""
        with open(f"{dist_dir}/run.sh", "w") as f:
            f.write(launcher_content)
        os.chmod(f"{dist_dir}/run.sh", 0o755)
    
    # Create zip archive
    archive_name = f"{dist_name}.zip"
    if os.path.exists(archive_name):
        os.remove(archive_name)
    
    if run_command(f"cd dist && zip -r ../{archive_name} {dist_name}", "Creating zip archive"):
        print(f"✅ Distribution package created: {archive_name}")
        return True
    
    return False

def main():
    """Main build process"""
    print("🚀 Desktop Cat Build Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Build failed due to missing dependencies")
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        print("❌ Build failed")
        sys.exit(1)
    
    # Create distribution
    if not create_distribution():
        print("❌ Distribution creation failed")
        sys.exit(1)
    
    print("\n🎉 Build completed successfully!")
    print("📁 Your executable is ready in the 'dist' folder")
    print("📦 Distribution package created and ready to share!")

if __name__ == "__main__":
    main()