#!/usr/bin/env python3
"""
Version Update Script for Desktop Cat
Easily update version numbers and create new distribution packages
"""

import re
import os
import sys
from pathlib import Path
import subprocess

class VersionUpdater:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.version_file = self.project_root / "VERSION"
        self.setup_file = self.project_root / "setup.py"
        
        # Initialize version file if it doesn't exist
        if not self.version_file.exists():
            self.version_file.write_text("1.0.0")
            
    def get_current_version(self):
        """Get current version from VERSION file"""
        try:
            return self.version_file.read_text().strip()
        except Exception as e:
            print(f"❌ Error reading version: {e}")
            return "1.0.0"
            
    def update_version(self, version_type="patch"):
        """Update version number"""
        current = self.get_current_version()
        major, minor, patch = map(int, current.split('.'))
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            print(f"❌ Invalid version type: {version_type}")
            return None
            
        new_version = f"{major}.{minor}.{patch}"
        
        # Update VERSION file
        self.version_file.write_text(new_version)
        
        # Update setup.py if it exists
        if self.setup_file.exists():
            self._update_setup_py(new_version)
            
        # Update README if it mentions version
        self._update_readme_version(current, new_version)
        
        print(f"✅ Version updated: {current} → {new_version}")
        return new_version
        
    def _update_setup_py(self, new_version):
        """Update version in setup.py"""
        try:
            content = self.setup_file.read_text()
            # Update version line
            content = re.sub(
                r'version="[^"]*"',
                f'version="{new_version}"',
                content
            )
            self.setup_file.write_text(content)
            print(f"✅ Updated setup.py to version {new_version}")
        except Exception as e:
            print(f"⚠️ Could not update setup.py: {e}")
            
    def _update_readme_version(self, old_version, new_version):
        """Update version references in README"""
        readme_file = self.project_root / "README.md"
        if readme_file.exists():
            try:
                content = readme_file.read_text()
                # Update version references
                content = content.replace(old_version, new_version)
                readme_file.write_text(content)
                print(f"✅ Updated README.md version references")
            except Exception as e:
                print(f"⚠️ Could not update README.md: {e}")
                
    def create_versioned_package(self, version_type="patch"):
        """Create a new versioned distribution package"""
        print("🚀 Creating New Versioned Package")
        print("=" * 40)
        
        # Update version
        new_version = self.update_version(version_type)
        if not new_version:
            return False
            
        # Clean previous builds
        print("🧹 Cleaning previous builds...")
        self._clean_builds()
        
        # Build new package
        print("🔨 Building new package...")
        try:
            subprocess.run([sys.executable, "build.py"], check=True)
            print("✅ Build successful!")
            
            # Rename distribution package with version
            self._rename_package(new_version)
            
            print(f"🎉 New version {new_version} package created!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False
            
    def _clean_builds(self):
        """Clean build artifacts"""
        build_dirs = ["build", "__pycache__"]
        for dir_name in build_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                import shutil
                shutil.rmtree(dir_path)
                print(f"  ✅ Cleaned: {dir_name}/")
                
    def _rename_package(self, version):
        """Rename distribution package with version number"""
        dist_dir = self.project_root / "dist"
        if not dist_dir.exists():
            return
            
        # Find the main distribution folder
        for item in dist_dir.iterdir():
            if item.is_dir() and "DesktopCat" in item.name:
                # Create versioned name
                new_name = f"DesktopCat-v{version}-{item.name.split('-', 1)[1]}"
                new_path = dist_dir / new_name
                
                # Rename
                try:
                    item.rename(new_path)
                    print(f"✅ Renamed package to: {new_name}")
                except Exception as e:
                    print(f"⚠️ Could not rename package: {e}")
                break
                
    def show_version_info(self):
        """Show current version information"""
        current_version = self.get_current_version()
        print("📋 Version Information")
        print("=" * 40)
        print(f"Current Version: {current_version}")
        
        # Check for existing packages
        dist_dir = self.project_root / "dist"
        if dist_dir.exists():
            packages = list(dist_dir.glob("*"))
            if packages:
                print(f"\n📦 Distribution Packages:")
                for package in packages:
                    if package.is_dir():
                        print(f"  📁 {package.name}/")
                    else:
                        print(f"  📄 {package.name}")
            else:
                print("\n📦 No distribution packages found")
        else:
            print("\n📦 No dist directory found")
            
        # Show version file content
        print(f"\n📄 VERSION file content:")
        print(f"  {self.version_file.read_text().strip()}")
        
    def interactive_update(self):
        """Interactive version update"""
        print("🔄 Interactive Version Update")
        print("=" * 40)
        
        current = self.get_current_version()
        print(f"Current version: {current}")
        print("\nVersion types:")
        print("1. Patch (1.0.0 → 1.0.1) - Bug fixes, small changes")
        print("2. Minor (1.0.0 → 1.1.0) - New features, backward compatible")
        print("3. Major (1.0.0 → 2.0.0) - Breaking changes, major updates")
        
        choice = input("\n🎯 Choose version type (1-3): ").strip()
        
        version_types = {
            "1": "patch",
            "2": "minor", 
            "3": "major"
        }
        
        if choice in version_types:
            version_type = version_types[choice]
            print(f"\n🔄 Updating to {version_type} version...")
            
            if self.create_versioned_package(version_type):
                print(f"\n🎉 Successfully created version {self.get_current_version()}!")
            else:
                print("\n❌ Version update failed")
        else:
            print("❌ Invalid choice")
            
    def main_menu(self):
        """Main menu for version management"""
        while True:
            print("\n🚀 Desktop Cat Version Manager")
            print("=" * 40)
            print("1. 📋 Show Version Info")
            print("2. 🔄 Interactive Version Update")
            print("3. 🚀 Quick Patch Update (1.0.0 → 1.0.1)")
            print("4. 🚀 Quick Minor Update (1.0.0 → 1.1.0)")
            print("5. 🚀 Quick Major Update (1.0.0 → 2.0.0)")
            print("6. 🧹 Clean Build Files")
            print("0. ❌ Exit")
            print("=" * 40)
            
            choice = input("🎯 Choose an option (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.show_version_info()
            elif choice == "2":
                self.interactive_update()
            elif choice == "3":
                self.create_versioned_package("patch")
            elif choice == "4":
                self.create_versioned_package("minor")
            elif choice == "5":
                self.create_versioned_package("major")
            elif choice == "6":
                self._clean_builds()
            else:
                print("❌ Invalid choice. Please enter 0-6.")
                
            if choice != "0":
                input("\n⏸️ Press Enter to continue...")

if __name__ == "__main__":
    updater = VersionUpdater()
    
    if len(sys.argv) > 1:
        # Command line usage
        command = sys.argv[1]
        if command == "patch":
            updater.create_versioned_package("patch")
        elif command == "minor":
            updater.create_versioned_package("minor")
        elif command == "major":
            updater.create_versioned_package("major")
        elif command == "info":
            updater.show_version_info()
        else:
            print(f"Usage: {sys.argv[0]} [patch|minor|major|info]")
    else:
        # Interactive mode
        updater.main_menu()