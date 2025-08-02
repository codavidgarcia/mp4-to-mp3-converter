#!/usr/bin/env python3
"""
Setup script for MP4 to MP3 Converter
This script helps users set up the application with all dependencies.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✓ Dependencies installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def test_imports():
    """Test if all required modules can be imported."""
    print("\nTesting imports...")
    
    modules = [
        ("PySide6", "PySide6.QtWidgets"),
        ("moviepy", "moviepy.editor"),
    ]
    
    all_good = True
    for module_name, import_name in modules:
        try:
            __import__(import_name)
            print(f"✓ {module_name} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module_name}: {e}")
            all_good = False
    
    return all_good


def create_run_script():
    """Create a simple run script."""
    script_content = """#!/usr/bin/env python3
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the application
from mp4_to_mp3_converter import main

if __name__ == "__main__":
    main()
"""
    
    with open("run_converter.py", "w") as f:
        f.write(script_content)
    
    # Make executable on Unix-like systems
    if os.name != 'nt':
        os.chmod("run_converter.py", 0o755)
    
    print("✓ Created run_converter.py script")


def main():
    """Main setup function."""
    print("MP4 to MP3 Converter Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nSetup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\nSome modules failed to import. Please check the installation.")
        sys.exit(1)
    
    # Create run script
    create_run_script()
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("\nTo run the application:")
    print("  python mp4_to_mp3_converter.py")
    print("  or")
    print("  python run_converter.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
