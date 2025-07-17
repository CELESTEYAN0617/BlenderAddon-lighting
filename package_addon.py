#!/usr/bin/env python3
"""
Packaging Script for Procedural Lighting System Addon
This script creates a properly structured ZIP file for Blender addon installation.
"""

import os
import zipfile
import shutil
import datetime
from pathlib import Path

# Addon information
ADDON_NAME = "procedural_lighting_system"
ADDON_VERSION = "1.0.0"
ADDON_FILES = [
    "__init__.py",
    "properties.py", 
    "operators.py",
    "ui.py",
    "presets.py",
    "utils.py"
]

DOCUMENTATION_FILES = [
    "README.md",
    "sample_scene.py"
]

OPTIONAL_FILES = [
    "LICENSE",
    "CHANGELOG.md"
]

def create_addon_directory():
    """Create the addon directory structure"""
    addon_dir = Path(ADDON_NAME)
    
    # Remove existing directory if it exists
    if addon_dir.exists():
        shutil.rmtree(addon_dir)
    
    # Create the addon directory
    addon_dir.mkdir()
    
    return addon_dir

def copy_addon_files(addon_dir):
    """Copy addon files to the directory"""
    current_dir = Path(".")
    
    print("Copying addon files...")
    for file_name in ADDON_FILES:
        src_file = current_dir / file_name
        if src_file.exists():
            dst_file = addon_dir / file_name
            shutil.copy2(src_file, dst_file)
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} (missing)")
            return False
    
    print("\nCopying documentation files...")
    for file_name in DOCUMENTATION_FILES:
        src_file = current_dir / file_name
        if src_file.exists():
            dst_file = addon_dir / file_name
            shutil.copy2(src_file, dst_file)
            print(f"  ✓ {file_name}")
    
    print("\nCopying optional files...")
    for file_name in OPTIONAL_FILES:
        src_file = current_dir / file_name
        if src_file.exists():
            dst_file = addon_dir / file_name
            shutil.copy2(src_file, dst_file)
            print(f"  ✓ {file_name}")
        else:
            print(f"  - {file_name} (optional, not found)")
    
    return True

def create_license_file(addon_dir):
    """Create a basic MIT license file if it doesn't exist"""
    license_file = addon_dir / "LICENSE"
    if not license_file.exists():
        license_text = """MIT License

Copyright (c) 2024 Procedural Lighting System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        with open(license_file, 'w') as f:
            f.write(license_text)
        print("  ✓ Created LICENSE file")

def create_changelog(addon_dir):
    """Create a basic changelog file if it doesn't exist"""
    changelog_file = addon_dir / "CHANGELOG.md"
    if not changelog_file.exists():
        changelog_text = f"""# Changelog

## [1.0.0] - {datetime.date.today()}

### Added
- Initial release of Procedural Lighting System
- Procedural light generation with 5 pattern types (Circle, Grid, Random, Spiral, Wave)
- Advanced light management with grouping and parenting
- Volumetric lighting support
- Bloom effects integration
- Light animation system
- Preset management with built-in presets
- Performance optimization tools
- Comprehensive user interface
- Sample scene and documentation

### Features
- Compatible with Blender 4.1+
- Cycles render engine integration
- Export/import preset functionality
- Light baking support
- Automatic compositor setup for effects

### Requirements
- Blender 4.1 or higher
- Cycles render engine (for volumetrics)
- Compositor enabled (for bloom effects)
"""
        with open(changelog_file, 'w') as f:
            f.write(changelog_text)
        print("  ✓ Created CHANGELOG.md file")

def create_installation_guide(addon_dir):
    """Create a quick installation guide"""
    install_file = addon_dir / "INSTALLATION.md"
    install_text = """# Installation Guide

## Quick Install

1. **Download** the ZIP file
2. **Open Blender 4.1+**
3. Go to `Edit` → `Preferences` → `Add-ons`
4. Click `Install...` button
5. Select the downloaded ZIP file
6. **Enable** the "Procedural Lighting System" addon
7. **Done!** Find the addon in the 3D Viewport sidebar under "Lighting" tab

## Manual Install

1. Extract the ZIP file
2. Copy the `procedural_lighting_system` folder to:
   - **Windows**: `%APPDATA%\\Blender Foundation\\Blender\\4.1\\scripts\\addons\\`
   - **macOS**: `~/Library/Application Support/Blender/4.1/scripts/addons/`
   - **Linux**: `~/.config/blender/4.1/scripts/addons/`
3. Restart Blender
4. Enable the addon in preferences

## First Use

1. Open the 3D Viewport sidebar (press `N`)
2. Navigate to the "Lighting" tab
3. Find "Procedural Lighting" panel
4. Try the sample scene: Run `sample_scene.py` in Blender's text editor

## Troubleshooting

- **Addon not showing**: Check Blender version compatibility (4.1+)
- **Volumetrics not working**: Ensure Cycles render engine is selected
- **Bloom not appearing**: Enable compositor in the scene properties
- **Performance issues**: Use fewer lights or enable optimization tools

For more help, see the full README.md file.
"""
    with open(install_file, 'w') as f:
        f.write(install_text)
    print("  ✓ Created INSTALLATION.md file")

def create_zip_package(addon_dir):
    """Create the ZIP package"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{ADDON_NAME}_v{ADDON_VERSION}_{timestamp}.zip"
    
    print(f"\nCreating ZIP package: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files in the addon directory
        for root, dirs, files in os.walk(addon_dir):
            for file in files:
                file_path = Path(root) / file
                # Create the archive path (relative to addon directory)
                archive_path = Path(ADDON_NAME) / file_path.relative_to(addon_dir)
                zipf.write(file_path, archive_path)
                print(f"  + {archive_path}")
    
    return zip_name

def validate_addon_structure(addon_dir):
    """Validate the addon structure"""
    print("\nValidating addon structure...")
    
    # Check for required files
    required_files = ["__init__.py"]
    for file_name in required_files:
        file_path = addon_dir / file_name
        if not file_path.exists():
            print(f"  ✗ Missing required file: {file_name}")
            return False
        print(f"  ✓ {file_name}")
    
    # Check __init__.py for bl_info
    init_file = addon_dir / "__init__.py"
    with open(init_file, 'r') as f:
        content = f.read()
        if 'bl_info' not in content:
            print("  ✗ __init__.py missing bl_info dictionary")
            return False
        print("  ✓ bl_info found in __init__.py")
    
    print("  ✓ Addon structure is valid")
    return True

def cleanup(addon_dir):
    """Clean up temporary files"""
    if addon_dir.exists():
        shutil.rmtree(addon_dir)
        print(f"\nCleaned up temporary directory: {addon_dir}")

def main():
    """Main packaging function"""
    print("=" * 60)
    print("Procedural Lighting System - Addon Packaging Tool")
    print("=" * 60)
    
    try:
        # Create addon directory
        addon_dir = create_addon_directory()
        print(f"Created addon directory: {addon_dir}")
        
        # Copy files
        if not copy_addon_files(addon_dir):
            print("\n❌ Failed to copy addon files!")
            return
        
        # Create additional files
        create_license_file(addon_dir)
        create_changelog(addon_dir)
        create_installation_guide(addon_dir)
        
        # Validate structure
        if not validate_addon_structure(addon_dir):
            print("\n❌ Addon structure validation failed!")
            return
        
        # Create ZIP package
        zip_name = create_zip_package(addon_dir)
        
        # Clean up
        cleanup(addon_dir)
        
        print("\n" + "=" * 60)
        print("✅ PACKAGING SUCCESSFUL!")
        print("=" * 60)
        print(f"📦 Package created: {zip_name}")
        print(f"📁 Size: {os.path.getsize(zip_name)} bytes")
        print("\n🚀 Installation Instructions:")
        print("1. Open Blender 4.1+")
        print("2. Go to Edit → Preferences → Add-ons")
        print("3. Click 'Install...' and select the ZIP file")
        print("4. Enable 'Procedural Lighting System' addon")
        print("5. Find it in 3D Viewport sidebar → Lighting tab")
        print("\n💡 Tip: Run sample_scene.py for a quick demo!")
        
    except Exception as e:
        print(f"\n❌ Error during packaging: {e}")
        if 'addon_dir' in locals():
            cleanup(addon_dir)

if __name__ == "__main__":
    main() 