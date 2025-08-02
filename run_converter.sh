#!/bin/bash
# MP4 to MP3 Converter - Unix Shell Script
# This script runs the MP4 to MP3 converter application

echo "Starting MP4 to MP3 Converter..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH"
        echo "Please install Python 3.7 or higher"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "Using Python version: $PYTHON_VERSION"

# Check if the main script exists
if [ ! -f "mp4_to_mp3_converter.py" ]; then
    echo "Error: mp4_to_mp3_converter.py not found"
    echo "Please ensure you're running this from the correct directory"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the application
echo "Launching application..."
$PYTHON_CMD mp4_to_mp3_converter.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "Application exited with an error"
    echo "Check the error messages above for troubleshooting"
fi
