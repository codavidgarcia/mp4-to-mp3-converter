#!/usr/bin/env python3
"""
Demo script for MP4 to MP3 Converter
This script demonstrates the basic functionality without requiring actual video files.
"""

import sys
import os
from pathlib import Path

def create_sample_files():
    """Create some sample files for demonstration (empty files with .mp4 extension)."""
    sample_dir = Path("sample_files")
    sample_dir.mkdir(exist_ok=True)
    
    sample_files = [
        "sample_video_1.mp4",
        "sample_video_2.mp4", 
        "sample_video_3.mp4"
    ]
    
    for filename in sample_files:
        sample_path = sample_dir / filename
        if not sample_path.exists():
            sample_path.touch()
            print(f"Created sample file: {sample_path}")
    
    return sample_dir

def demo_info():
    """Display demo information."""
    print("MP4 to MP3 Converter - Demo")
    print("=" * 40)
    print()
    print("This demo shows the MP4 to MP3 converter application.")
    print()
    print("Features demonstrated:")
    print("• File selection dialog for MP4 files")
    print("• Output directory selection")
    print("• Batch conversion support")
    print("• Progress tracking")
    print("• Error handling")
    print("• User-friendly interface")
    print()
    print("Note: For this demo, we'll create empty .mp4 files.")
    print("In real usage, you would select actual MP4 video files.")
    print()

def main():
    """Run the demo."""
    demo_info()
    
    # Create sample files
    sample_dir = create_sample_files()
    
    print(f"Sample files created in: {sample_dir.absolute()}")
    print()
    print("To test the application:")
    print("1. Run: python mp4_to_mp3_converter.py")
    print("2. Click 'Add MP4 Files' and select the sample files")
    print("3. Click 'Select Output Directory' and choose a folder")
    print("4. Click 'Start Conversion' to begin")
    print()
    print("Note: The sample files are empty, so conversion will fail,")
    print("but you can see how the interface works.")
    print()
    print("For real usage, replace the sample files with actual MP4 videos.")

if __name__ == "__main__":
    main()
