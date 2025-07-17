# Packaging Guide for Procedural Lighting System

This guide explains how to properly package the Blender addon for distribution and installation.

## 🚀 Quick Packaging (Recommended)

### Method 1: Automated Packaging Script

**Windows:**
```batch
# Double-click or run in command prompt
package.bat
```

**Linux/Mac:**
```bash
# Make executable (first time only)
chmod +x package.sh

# Run the script
./package.sh
```

**Manual Python:**
```bash
python package_addon.py
```

This will create a properly structured ZIP file with timestamp, ready for distribution.

## 📦 Package Structure

The automated script creates this structure:
```
procedural_lighting_system_v1.0.0_YYYYMMDD_HHMMSS.zip
└── procedural_lighting_system/
    ├── __init__.py          # Main addon file (required)
    ├── properties.py        # Data structures
    ├── operators.py         # Core functionality  
    ├── ui.py               # User interface
    ├── presets.py          # Preset management
    ├── utils.py            # Utility functions
    ├── README.md           # Documentation
    ├── sample_scene.py     # Demo script
    ├── INSTALLATION.md     # Installation guide
    ├── CHANGELOG.md        # Version history
    └── LICENSE             # MIT License
```

## 🛠️ Manual Packaging Methods

### Method 2: Manual ZIP Creation

1. **Create folder structure:**
   ```
   procedural_lighting_system/
   ├── __init__.py
   ├── properties.py
   ├── operators.py
   ├── ui.py
   ├── presets.py
   ├── utils.py
   └── README.md
   ```

2. **Create ZIP file:**
   - Select the `procedural_lighting_system` folder
   - Right-click → "Send to" → "Compressed folder" (Windows)
   - Or use: `zip -r procedural_lighting_system.zip procedural_lighting_system/`

3. **Important:** The ZIP must contain the folder, not just the files!

### Method 3: Using 7-Zip (Windows)

1. Install 7-Zip if not already installed
2. Select all addon files
3. Right-click → 7-Zip → "Add to archive..."
4. Archive format: ZIP
5. Archive name: `procedural_lighting_system.zip`

### Method 4: Using Terminal

**Linux/Mac:**
```bash
# Create directory
mkdir procedural_lighting_system

# Copy files
cp __init__.py properties.py operators.py ui.py presets.py utils.py README.md procedural_lighting_system/

# Create ZIP
zip -r procedural_lighting_system.zip procedural_lighting_system/
```

**Windows PowerShell:**
```powershell
# Create directory
New-Item -ItemType Directory -Name procedural_lighting_system

# Copy files
Copy-Item @("__init__.py", "properties.py", "operators.py", "ui.py", "presets.py", "utils.py", "README.md") -Destination procedural_lighting_system/

# Create ZIP
Compress-Archive -Path procedural_lighting_system -DestinationPath procedural_lighting_system.zip
```

## ✅ Validation Checklist

Before distributing, ensure your package has:

### Required Files
- [ ] `__init__.py` with proper `bl_info` dictionary
- [ ] All Python modules (properties.py, operators.py, etc.)
- [ ] README.md with usage instructions

### bl_info Validation
The `__init__.py` must contain:
```python
bl_info = {
    "name": "Procedural Lighting System",
    "author": "Your Name", 
    "version": (1, 0, 0),
    "blender": (4, 1, 0),          # Minimum Blender version
    "location": "3D Viewport > Sidebar > Lighting",
    "description": "Advanced procedural lighting system",
    "category": "Lighting",
}
```

### Structure Validation
- [ ] ZIP contains a single folder named `procedural_lighting_system`
- [ ] Folder contains all addon files
- [ ] No extra system files (.DS_Store, Thumbs.db, etc.)
- [ ] File permissions are correct

### Testing
- [ ] Test installation in clean Blender installation
- [ ] Verify addon appears in preferences
- [ ] Check all panels load correctly
- [ ] Test core functionality

## 📋 Installation Methods for Users

### For End Users - ZIP Installation

1. **Download** the ZIP file
2. **Open Blender 4.1+**
3. Go to `Edit` → `Preferences` → `Add-ons`
4. Click `Install...` button
5. Browse and select the ZIP file
6. **Enable** the addon by checking the checkbox
7. **Save Preferences** (optional but recommended)

### For Developers - Manual Installation

1. **Extract** ZIP to Blender addons directory:
   - **Windows**: `%APPDATA%\Blender Foundation\Blender\4.1\scripts\addons\`
   - **macOS**: `~/Library/Application Support/Blender/4.1/scripts/addons/`
   - **Linux**: `~/.config/blender/4.1/scripts/addons/`

2. **Restart Blender**
3. **Enable addon** in preferences

## 🔧 Troubleshooting Packaging Issues

### Common Problems

**ZIP file won't install:**
- Ensure ZIP contains folder, not just files
- Check folder name matches addon identifier
- Verify `__init__.py` has proper `bl_info`

**Files missing after packaging:**
- Check all Python files are copied
- Verify file paths are correct
- Ensure no files are excluded by .gitignore

**Addon doesn't appear in Blender:**
- Check Blender version compatibility
- Verify `bl_info` format is correct
- Look for Python errors in console

**Permission issues:**
- Ensure write permissions to addons directory
- Run Blender as administrator if needed
- Check file permissions in ZIP

### Validation Commands

```bash
# Check ZIP contents
unzip -l procedural_lighting_system.zip

# Verify Python syntax
python -m py_compile __init__.py

# Check for required strings
grep -l "bl_info" __init__.py
```

## 📦 Distribution Best Practices

### Version Control
- Use semantic versioning (1.0.0, 1.1.0, 2.0.0)
- Include version in filename
- Update `bl_info["version"]` in code
- Maintain changelog

### Documentation
- Include comprehensive README
- Provide installation instructions  
- Add usage examples
- Include troubleshooting guide

### Testing
- Test on multiple Blender versions
- Verify on different operating systems
- Check with clean Blender installations
- Test all major features

### Release Process
1. Update version numbers
2. Update changelog
3. Test thoroughly
4. Package using automated script
5. Test installation from ZIP
6. Upload to distribution platform

## 🌐 Distribution Platforms

### Blender Market
- Professional marketplace
- Built-in licensing
- Automatic updates
- Payment processing

### GitHub Releases
- Free hosting
- Version control integration
- Easy collaboration
- Direct download links

### BlenderArtists Forum
- Community-driven
- Free sharing
- Feedback and support
- Wide user base

### Gumroad
- Simple setup
- Payment processing
- Download analytics
- Marketing tools

---

## 🎯 Summary

The **automated packaging script** (`package_addon.py`) is the recommended method as it:
- ✅ Creates proper folder structure
- ✅ Validates addon format
- ✅ Includes all necessary files
- ✅ Generates installation guide
- ✅ Adds version timestamps
- ✅ Creates professional package

For quick packaging, just run:
- **Windows**: `package.bat`
- **Linux/Mac**: `./package.sh`
- **Manual**: `python package_addon.py`

The resulting ZIP file is ready for distribution and will install correctly in Blender 4.1+! 