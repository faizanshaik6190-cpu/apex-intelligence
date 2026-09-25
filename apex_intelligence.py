import sys
import subprocess
import os
import time
import webbrowser
import json
import shutil
from pathlib import Path
from datetime import datetime
import threading

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QMessageBox, QProgressBar, QFrame
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
    from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QMessageBox, QProgressBar, QFrame
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize
    from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap

class ServerSetupWorker(QThread):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    complete_signal = pyqtSignal(bool)
    
    def run(self):
        try:
            # Check if Docker is installed
            self.log_signal.emit("[CHECK] Looking for Docker...")
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            
            if result.returncode != 0:
                self.log_signal.emit("[ERROR] Docker not found. Please install Docker Desktop first.")
                self.log_signal.emit("[INFO] Download from: https://www.docker.com/products/docker-desktop")
                self.status_signal.emit("Docker Required")
                self.complete_signal.emit(False)
                return
            
            self.log_signal.emit(f"[SUCCESS] {result.stdout.strip()}")
            
            # Find project directory
            self.log_signal.emit("[CHECK] Locating project files...")
            project_dir = Path(__file__).parent.absolute()
            docker_compose_file = project_dir / "docker-compose.yml"
            
            if not docker_compose_file.exists():
                self.log_signal.emit("[ERROR] docker-compose.yml not found")
                self.status_signal.emit("Setup Failed")
                self.complete_signal.emit(False)
                return
            
            self.log_signal.emit(f"[SUCCESS] Project found at {project_dir}")
            
            # Start Docker Compose
            self.log_signal.emit("[START] Launching services...")
            self.status_signal.emit("Starting Services...")
            
            os.chdir(project_dir)
            
            process = subprocess.Popen(
                ["docker-compose", "up", "-d"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_signal.emit(f"[ERROR] Failed to start services")
                self.log_signal.emit(f"[ERROR] {stderr}")
                self.status_signal.emit("Setup Failed")
                self.complete_signal.emit(False)
                return
            
            self.log_signal.emit("[SUCCESS] Services launched")
            self.log_signal.emit("[WAIT] Waiting for API to be ready (this takes ~30 seconds)...")
            self.status_signal.emit("Waiting for API...")
            
            # Wait for API to be ready
            max_attempts = 60
            for attempt in range(max_attempts):
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        self.log_signal.emit(f"[SUCCESS] API is ready! (Attempt {attempt+1}/{max_attempts})")
                        self.status_signal.emit("Ready")
                        self.complete_signal.emit(True)
                        return
                except:
                    pass
                
                if attempt % 10 == 0:
                    self.log_signal.emit(f"[WAIT] Still waiting... ({attempt+1}/{max_attempts})")
                time.sleep(1)
            
            self.log_signal.emit("[ERROR] API did not start in time")
            self.status_signal.emit("Timeout")
            self.complete_signal.emit(False)
        
        except Exception as e:
            self.log_signal.emit(f"[ERROR] {str(e)}")
            self.status_signal.emit("Error")
            self.complete_signal.emit(False)

class ApexApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_path = Path(__file__).parent.absolute()
        self.server_running = False
        self.setup_worker = None
        self.init_ui()
        self.check_server_on_startup()
    
    def init_ui(self):
        self.setWindowTitle("Apex Intelligence")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; }
            QLabel { color: white; }
            QPushButton { 
                background-color: #0d7377; 
                color: white; 
                border: none; 
                border-radius: 5px; 
                padding: 12px; 
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #14919b; }
            QPushButton:pressed { background-color: #0a5460; }
            QPushButton:disabled { background-color: #666; }
            QTextEdit { 
                background-color: #2d2d2d; 
                color: #00ff00; 
                border: 1px solid #444;
                border-radius: 3px;
                font-family: Consolas, monospace;
                font-size: 10px;
            }
            QProgressBar {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #0d7377;
            }
        """)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("APEX INTELLIGENCE")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #00ff00;")
        layout.addWidget(title)
        
        subtitle = QLabel("AI-Powered Growth Agency Private Server")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888;")
        layout.addWidget(subtitle)
        
        # Status section
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 5px; padding: 10px;")
        status_layout = QVBoxLayout(status_frame)
        
        status_label_title = QLabel("Server Status:")
        status_label_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        status_layout.addWidget(status_label_title)
        
        self.status_label = QLabel("Checking...")
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ffaa00;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_frame)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.start_btn = QPushButton("▶ START SERVER")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setStyleSheet("""
            QPushButton { background-color: #4CAF50; }
            QPushButton:hover { background-color: #45a049; }
        """)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ STOP")
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton { background-color: #f44336; }
            QPushButton:hover { background-color: #da190b; }
        """)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        # Service buttons
        service_layout = QHBoxLayout()
        service_layout.setSpacing(10)
        
        api_btn = QPushButton("📖 API DOCS")
        api_btn.setMinimumHeight(40)
        api_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/docs"))
        service_layout.addWidget(api_btn)
        
        ceo_btn = QPushButton("📊 CEO DASHBOARD")
        ceo_btn.setMinimumHeight(40)
        ceo_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/ceo/summary"))
        service_layout.addWidget(ceo_btn)
        
        flower_btn = QPushButton("🌸 TASKS")
        flower_btn.setMinimumHeight(40)
        flower_btn.clicked.connect(lambda: webbrowser.open("http://localhost:5555"))
        service_layout.addWidget(flower_btn)
        
        layout.addLayout(service_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(25)
        layout.addWidget(self.progress)
        
        # Logs
        log_label = QLabel("📋 Logs:")
        log_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(300)
        layout.addWidget(self.log_text)
        
        # Timer for checking status
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_server_status)
        self.timer.start(5000)
    
    def add_log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())
    
    def check_server_on_startup(self):
        """Check if server is already running on startup"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                self.server_running = True
                self.update_status("✓ READY", "#00ff00")
                self.add_log("[INFO] Server is already running")
                self.update_ui_state()
                return
        except:
            pass
        
        self.server_running = False
        self.update_status("✗ STOPPED", "#ff3333")
    
    def start_server(self):
        """Start the server"""
        if self.server_running:
            QMessageBox.information(self, "Info", "Server is already running")
            return
        
        self.add_log("Starting server...")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.start_btn.setEnabled(False)
        self.update_status("◐ STARTING", "#ffaa00")
        
        self.setup_worker = ServerSetupWorker()
        self.setup_worker.log_signal.connect(self.add_log)
        self.setup_worker.status_signal.connect(lambda s: self.update_status(f"◐ {s}", "#ffaa00"))
        self.setup_worker.complete_signal.connect(self.on_setup_complete)
        self.setup_worker.start()
    
    def on_setup_complete(self, success):
        """Called when setup completes"""
        self.progress.setVisible(False)
        self.start_btn.setEnabled(True)
        
        if success:
            self.server_running = True
            self.update_status("✓ READY", "#00ff00")
            self.add_log("\n[SUCCESS] Server is ready!")
            self.add_log("[INFO] Open API Docs to start using the server")
            self.update_ui_state()
        else:
            self.server_running = False
            self.update_status("✗ FAILED", "#ff3333")
            self.add_log("\n[ERROR] Failed to start server")
    
    def stop_server(self):
        """Stop the server"""
        try:
            self.add_log("Stopping server...")
            self.update_status("◐ STOPPING", "#ffaa00")
            os.chdir(self.project_path)
            subprocess.run(["docker-compose", "down"], capture_output=True, timeout=30)
            self.server_running = False
            self.update_status("✗ STOPPED", "#ff3333")
            self.add_log("[SUCCESS] Server stopped")
            self.update_ui_state()
        except Exception as e:
            self.add_log(f"[ERROR] {str(e)}")
            self.update_status("✗ ERROR", "#ff3333")
    
    def check_server_status(self):
        """Periodically check if server is running"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200 and not self.server_running:
                self.server_running = True
                self.update_status("✓ READY", "#00ff00")
                self.update_ui_state()
        except:
            if self.server_running:
                self.server_running = False
                self.update_status("✗ STOPPED", "#ff3333")
                self.update_ui_state()
    
    def update_status(self, status_text, color):
        """Update status label"""
        self.status_label.setText(status_text)
        self.status_label.setStyleSheet(f"color: {color};")
    
    def update_ui_state(self):
        """Update button states based on server status"""
        self.stop_btn.setEnabled(self.server_running)
        self.start_btn.setEnabled(not self.server_running)

def main():
    app = QApplication(sys.argv)
    window = ApexApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
