#!/usr/bin/env python3
"""
MP4 to MP3 Converter
A desktop application for converting MP4 video files to MP3 audio files.
Built with PySide6 and moviepy.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional
import traceback

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit, QFileDialog,
    QGroupBox, QListWidget, QMessageBox, QSplitter
)
from PySide6.QtCore import QThread, Signal, QObject, Qt
from PySide6.QtGui import QFont, QIcon

try:
    from moviepy import VideoFileClip
except ImportError:
    VideoFileClip = None


class ConversionWorker(QThread):
    """Worker thread for handling MP4 to MP3 conversion."""
    
    progress_updated = Signal(int)  # Progress percentage (0-100)
    status_updated = Signal(str)    # Status message
    file_completed = Signal(str, bool)  # filename, success
    conversion_finished = Signal()
    
    def __init__(self, input_files: List[str], output_dir: str):
        super().__init__()
        self.input_files = input_files
        self.output_dir = output_dir
        self.is_cancelled = False
    
    def cancel(self):
        """Cancel the conversion process."""
        self.is_cancelled = True
    
    def run(self):
        """Main conversion process."""
        if not VideoFileClip:
            self.status_updated.emit("ERROR: moviepy library not found. Please install requirements.")
            return
        
        total_files = len(self.input_files)
        
        for i, input_file in enumerate(self.input_files):
            if self.is_cancelled:
                self.status_updated.emit("Conversion cancelled by user.")
                break
            
            try:
                # Update status
                filename = os.path.basename(input_file)
                self.status_updated.emit(f"Converting: {filename}")
                
                # Load video file
                video = VideoFileClip(input_file)
                
                # Extract audio
                audio = video.audio
                
                if audio is None:
                    self.status_updated.emit(f"WARNING: No audio track found in {filename}")
                    self.file_completed.emit(filename, False)
                    continue
                
                # Generate output filename
                output_filename = Path(input_file).stem + ".mp3"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Convert to MP3
                audio.write_audiofile(
                    output_path,
                    logger=None  # Suppress moviepy logs
                )
                
                # Clean up
                audio.close()
                video.close()
                
                self.status_updated.emit(f"✓ Completed: {filename}")
                self.file_completed.emit(filename, True)
                
            except Exception as e:
                error_msg = f"✗ Failed: {filename} - {str(e)}"
                self.status_updated.emit(error_msg)
                self.file_completed.emit(filename, False)
            
            # Update overall progress
            progress = int((i + 1) / total_files * 100)
            self.progress_updated.emit(progress)
        
        self.conversion_finished.emit()


class MP4ToMP3Converter(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.input_files = []
        self.output_directory = ""
        self.conversion_worker = None
        
        self.init_ui()
        self.setWindowTitle("MP4 to MP3 Converter")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
    
    def init_ui(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("MP4 to MP3 Converter")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Input files section
        input_group = QGroupBox("Input Files")
        input_layout = QVBoxLayout(input_group)
        
        # File selection buttons
        file_buttons_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add MP4 Files")
        self.add_files_btn.clicked.connect(self.add_files)
        self.clear_files_btn = QPushButton("Clear List")
        self.clear_files_btn.clicked.connect(self.clear_files)
        
        file_buttons_layout.addWidget(self.add_files_btn)
        file_buttons_layout.addWidget(self.clear_files_btn)
        file_buttons_layout.addStretch()
        
        input_layout.addLayout(file_buttons_layout)
        
        # File list
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(150)
        input_layout.addWidget(self.file_list)
        
        splitter.addWidget(input_group)
        
        # Output directory section
        output_group = QGroupBox("Output Directory")
        output_layout = QVBoxLayout(output_group)
        
        output_buttons_layout = QHBoxLayout()
        self.select_output_btn = QPushButton("Select Output Directory")
        self.select_output_btn.clicked.connect(self.select_output_directory)
        self.output_label = QLabel("No directory selected")
        
        output_buttons_layout.addWidget(self.select_output_btn)
        output_buttons_layout.addWidget(self.output_label, 1)
        
        output_layout.addLayout(output_buttons_layout)
        splitter.addWidget(output_group)
        
        # Progress section
        progress_group = QGroupBox("Conversion Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Control buttons
        control_layout = QHBoxLayout()
        self.convert_btn = QPushButton("Start Conversion")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_conversion)
        self.cancel_btn.setEnabled(False)
        
        control_layout.addWidget(self.convert_btn)
        control_layout.addWidget(self.cancel_btn)
        control_layout.addStretch()
        
        progress_layout.addLayout(control_layout)
        splitter.addWidget(progress_group)
        
        # Status/Log section
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        status_layout.addWidget(self.status_text)
        
        splitter.addWidget(status_group)
        
        # Set splitter proportions
        splitter.setSizes([150, 80, 120, 200])
        
        # Initial status message
        self.add_status_message("Ready. Please select MP4 files and output directory.")
    
    def add_status_message(self, message: str):
        """Add a message to the status text area."""
        self.status_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.status_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def add_files(self):
        """Open file dialog to select MP4 files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select MP4 Files",
            "",
            "Video Files (*.mp4 *.MP4);;All Files (*)"
        )
        
        if files:
            # Add new files to the list (avoid duplicates)
            new_files = [f for f in files if f not in self.input_files]
            self.input_files.extend(new_files)
            
            # Update the display
            self.update_file_list()
            self.update_convert_button_state()
            
            self.add_status_message(f"Added {len(new_files)} file(s). Total: {len(self.input_files)}")
    
    def clear_files(self):
        """Clear the input files list."""
        self.input_files.clear()
        self.update_file_list()
        self.update_convert_button_state()
        self.add_status_message("File list cleared.")
    
    def update_file_list(self):
        """Update the file list display."""
        self.file_list.clear()
        for file_path in self.input_files:
            filename = os.path.basename(file_path)
            self.file_list.addItem(filename)
    
    def select_output_directory(self):
        """Open dialog to select output directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory"
        )
        
        if directory:
            self.output_directory = directory
            self.output_label.setText(f"Output: {directory}")
            self.update_convert_button_state()
            self.add_status_message(f"Output directory set to: {directory}")
    
    def update_convert_button_state(self):
        """Enable/disable convert button based on current state."""
        can_convert = (
            len(self.input_files) > 0 and
            bool(self.output_directory) and
            (self.conversion_worker is None or not self.conversion_worker.isRunning())
        )
        self.convert_btn.setEnabled(bool(can_convert))
    
    def start_conversion(self):
        """Start the conversion process."""
        if not VideoFileClip:
            QMessageBox.critical(
                self,
                "Missing Dependency",
                "The moviepy library is required for conversion.\n"
                "Please install it using: pip install moviepy"
            )
            return
        
        # Validate inputs
        if not self.input_files:
            QMessageBox.warning(self, "No Files", "Please select MP4 files to convert.")
            return
        
        if not self.output_directory:
            QMessageBox.warning(self, "No Output Directory", "Please select an output directory.")
            return
        
        # Check if output directory exists and is writable
        if not os.path.exists(self.output_directory):
            QMessageBox.warning(self, "Invalid Directory", "Output directory does not exist.")
            return
        
        if not os.access(self.output_directory, os.W_OK):
            QMessageBox.warning(self, "Permission Error", "Cannot write to output directory.")
            return
        
        # Start conversion
        self.add_status_message(f"Starting conversion of {len(self.input_files)} file(s)...")
        
        self.conversion_worker = ConversionWorker(self.input_files, self.output_directory)
        self.conversion_worker.progress_updated.connect(self.update_progress)
        self.conversion_worker.status_updated.connect(self.add_status_message)
        self.conversion_worker.file_completed.connect(self.on_file_completed)
        self.conversion_worker.conversion_finished.connect(self.on_conversion_finished)
        
        self.conversion_worker.start()
        
        # Update UI state
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
    
    def cancel_conversion(self):
        """Cancel the ongoing conversion."""
        if self.conversion_worker and self.conversion_worker.isRunning():
            self.conversion_worker.cancel()
            self.add_status_message("Cancelling conversion...")
    
    def update_progress(self, value: int):
        """Update the progress bar."""
        self.progress_bar.setValue(value)
    
    def on_file_completed(self, filename: str, success: bool):
        """Handle completion of individual file conversion."""
        # This is already handled by status updates in the worker
        pass
    
    def on_conversion_finished(self):
        """Handle completion of all conversions."""
        self.add_status_message("Conversion process completed.")
        
        # Reset UI state
        self.progress_bar.setVisible(False)
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.update_convert_button_state()
        
        # Show completion message
        QMessageBox.information(
            self,
            "Conversion Complete",
            "All files have been processed. Check the status log for details."
        )


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MP4 to MP3 Converter")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("MP4MP3Converter")
    
    # Create and show main window
    window = MP4ToMP3Converter()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
