#!/usr/bin/env python3
"""
Test script to verify that all dependencies are properly installed
and the application can be imported without errors.
"""

import sys
import traceback


def test_python_version():
    """Test Python version compatibility."""
    print("Testing Python version...")
    if sys.version_info < (3, 7):
        print(f"✗ Python 3.7+ required, found {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} is compatible")
    return True


def test_imports():
    """Test all required imports."""
    print("\nTesting imports...")
    
    tests = [
        ("PySide6.QtWidgets", "PySide6 GUI framework"),
        ("PySide6.QtCore", "PySide6 core components"),
        ("PySide6.QtGui", "PySide6 GUI components"),
        ("moviepy", "moviepy video processing"),
        ("pathlib", "pathlib for file handling"),
        ("os", "os module"),
        ("sys", "sys module"),
    ]
    
    all_passed = True
    
    for module, description in tests:
        try:
            __import__(module)
            print(f"✓ {description}")
        except ImportError as e:
            print(f"✗ {description}: {e}")
            all_passed = False
        except Exception as e:
            print(f"✗ {description}: Unexpected error - {e}")
            all_passed = False
    
    return all_passed


def test_application_import():
    """Test importing the main application."""
    print("\nTesting application import...")
    
    try:
        # Try to import the main application module
        import mp4_to_mp3_converter
        print("✓ Main application module imported successfully")
        
        # Test if main classes can be instantiated (without showing GUI)
        # We'll just check if the classes exist
        if hasattr(mp4_to_mp3_converter, 'MP4ToMP3Converter'):
            print("✓ Main application class found")
        else:
            print("✗ Main application class not found")
            return False
            
        if hasattr(mp4_to_mp3_converter, 'ConversionWorker'):
            print("✓ Conversion worker class found")
        else:
            print("✗ Conversion worker class not found")
            return False
            
        return True
        
    except ImportError as e:
        print(f"✗ Failed to import application: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing application: {e}")
        traceback.print_exc()
        return False


def test_moviepy_functionality():
    """Test basic moviepy functionality."""
    print("\nTesting moviepy functionality...")
    
    try:
        from moviepy import VideoFileClip
        print("✓ VideoFileClip can be imported")
        
        # Test if we can access basic moviepy functions
        # (We won't actually process a file, just check if the class works)
        print("✓ moviepy appears to be working correctly")
        return True
        
    except ImportError as e:
        print(f"✗ moviepy import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ moviepy test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("MP4 to MP3 Converter - Installation Test")
    print("=" * 45)
    
    tests = [
        ("Python Version", test_python_version),
        ("Required Imports", test_imports),
        ("Application Import", test_application_import),
        ("Moviepy Functionality", test_moviepy_functionality),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            all_passed = False
    
    print("\n" + "=" * 45)
    
    if all_passed:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("  python mp4_to_mp3_converter.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure you've installed all dependencies:")
        print("   pip install -r requirements.txt")
        print("2. Check that you're using Python 3.7 or higher")
        print("3. Try running the setup script: python setup.py")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
