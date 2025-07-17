#!/bin/bash

echo "====================================================="
echo "Procedural Lighting System - Addon Packaging Tool"
echo "====================================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.6+ and try again"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $($PYTHON_CMD --version)"
echo "Running packaging script..."
echo

$PYTHON_CMD package_addon.py

echo
echo "Packaging complete!"
echo "Press Enter to continue..."
read 