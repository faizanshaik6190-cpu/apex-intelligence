import sys
import subprocess
import os
import time
import webbrowser
import json
from pathlib import Path
from datetime import datetime
import threading
import requests

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
        QComboBox, QSpinBox, QLineEdit, QMessageBox, QStatusBar, QProgressBar
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
    from PyQt6.QtGui import QIcon, QColor, QFont
except ImportError:
    print("Installing PyQt6...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt6"])
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem,
        QComboBox, QSpinBox, QLineEdit, QMessageBox, QStatusBar, QProgressBar
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
    from PyQt6.QtGui import QIcon, QColor, QFont

class ServerWorker(QThread):
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    
    def __init__(self, project_path):
        super().__init__()
        self.project_path = project_path
        self.running = False
    
    def run(self):
        try:
            os.chdir(self.project_path)
            self.log_signal.emit("[INFO] Starting Docker services...")
            self.status_signal.emit("Starting...")
            
            # Start Docker Compose
            process = subprocess.Popen(
                ["docker-compose", "up", "-d"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.log_signal.emit("[SUCCESS] Docker services started")
                self.status_signal.emit("Running")
                
                # Wait for API to be ready
                self.log_signal.emit("[INFO] Waiting for API to be ready...")
                for i in range(30):
                    try:
                        response = requests.get("http://localhost:8000/health", timeout=1)
                        if response.status_code == 200:
                            self.log_signal.emit("[SUCCESS] API is ready!")
                            self.status_signal.emit("Ready")
                            break
                    except:
                        pass
                    time.sleep(1)
            else:
                self.log_signal.emit(f"[ERROR] {stderr}")
                self.status_signal.emit("Error")
        
        except Exception as e:
            self.log_signal.emit(f"[ERROR] {str(e)}")
            self.status_signal.emit("Error")

class ApexIntelligenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_path = Path(__file__).parent
        self.server_running = False
        self.server_worker = None
        self.init_ui()
        self.check_requirements()
    
    def init_ui(self):
        self.setWindowTitle("Apex Intelligence - Private Server")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Title
        title = QLabel("Apex Intelligence - AI-Powered Growth Agency")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # === TAB 1: DASHBOARD ===
        dashboard_widget = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_widget)
        
        # Status section
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Server Status:"))
        self.status_label = QLabel("Stopped")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        dashboard_layout.addLayout(status_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Start Server")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setStyleSheet("background-color: green; color: white; font-weight: bold; padding: 10px;")
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop Server")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; padding: 10px;")
        button_layout.addWidget(self.stop_btn)
        
        self.restart_btn = QPushButton("🔄 Restart")
        self.restart_btn.clicked.connect(self.restart_server)
        self.restart_btn.setEnabled(False)
        button_layout.addWidget(self.restart_btn)
        
        self.api_btn = QPushButton("📖 Open API Docs")
        self.api_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/docs"))
        button_layout.addWidget(self.api_btn)
        
        dashboard_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        dashboard_layout.addWidget(self.progress)
        
        # Logs
        dashboard_layout.addWidget(QLabel("📋 Logs:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(400)
        dashboard_layout.addWidget(self.log_text)
        
        tabs.addTab(dashboard_widget, "Dashboard")
        
        # === TAB 2: API TESTER ===
        api_widget = QWidget()
        api_layout = QVBoxLayout(api_widget)
        
        api_layout.addWidget(QLabel("🧪 API Tester"))
        
        # Endpoint selector
        endpoint_layout = QHBoxLayout()
        endpoint_layout.addWidget(QLabel("Endpoint:"))
        self.endpoint_combo = QComboBox()
        self.endpoint_combo.addItems([
            "/health",
            "/ceo/summary",
            "/leads",
            "/deals",
            "/clients",
            "/audits",
            "/tickets"
        ])
        endpoint_layout.addWidget(self.endpoint_combo)
        
        self.test_btn = QPushButton("Test")
        self.test_btn.clicked.connect(self.test_api)
        endpoint_layout.addWidget(self.test_btn)
        api_layout.addLayout(endpoint_layout)
        
        # Response
        api_layout.addWidget(QLabel("Response:"))
        self.response_text = QTextEdit()
        self.response_text.setReadOnly(True)
        api_layout.addWidget(self.response_text)
        
        tabs.addTab(api_widget, "API Tester")
        
        # === TAB 3: LEAD GENERATOR ===
        leads_widget = QWidget()
        leads_layout = QVBoxLayout(leads_widget)
        
        leads_layout.addWidget(QLabel("🎯 Generate Leads"))
        
        # Form
        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("City:"))
        self.city_input = QLineEdit("Austin, TX")
        form_layout.addWidget(self.city_input)
        
        form_layout.addWidget(QLabel("Category:"))
        self.category_input = QLineEdit("dental")
        form_layout.addWidget(self.category_input)
        
        form_layout.addWidget(QLabel("Limit:"))
        self.limit_spin = QSpinBox()
        self.limit_spin.setValue(5)
        self.limit_spin.setMaximum(100)
        form_layout.addWidget(self.limit_spin)
        
        self.generate_btn = QPushButton("Generate Leads")
        self.generate_btn.clicked.connect(self.generate_leads)
        form_layout.addWidget(self.generate_btn)
        
        leads_layout.addLayout(form_layout)
        
        # Results
        leads_layout.addWidget(QLabel("Results:"))
        self.leads_text = QTextEdit()
        self.leads_text.setReadOnly(True)
        leads_layout.addWidget(self.leads_text)
        
        tabs.addTab(leads_widget, "Lead Generator")
        
        # === TAB 4: SERVICES ===
        services_widget = QWidget()
        services_layout = QVBoxLayout(services_widget)
        
        services_layout.addWidget(QLabel("🔗 External Services"))
        
        services_buttons = QVBoxLayout()
        
        api_docs_btn = QPushButton("📖 API Documentation (http://localhost:8000/docs)")
        api_docs_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/docs"))
        services_buttons.addWidget(api_docs_btn)
        
        supervisor_btn = QPushButton("👨‍💼 Supervisor (http://localhost:9001)")
        supervisor_btn.clicked.connect(lambda: webbrowser.open("http://localhost:9001"))
        services_buttons.addWidget(supervisor_btn)
        
        flower_btn = QPushButton("🌸 Celery Flower (http://localhost:5555)")
        flower_btn.clicked.connect(lambda: webbrowser.open("http://localhost:5555"))
        services_buttons.addWidget(flower_btn)
        
        api_btn = QPushButton("🌐 API Health (http://localhost:8000/health)")
        api_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/health"))
        services_buttons.addWidget(api_btn)
        
        ceo_btn = QPushButton("📊 CEO Summary (http://localhost:8000/ceo/summary)")
        ceo_btn.clicked.connect(lambda: webbrowser.open("http://localhost:8000/ceo/summary"))
        services_buttons.addWidget(ceo_btn)
        
        services_layout.addLayout(services_buttons)
        services_layout.addStretch()
        
        tabs.addTab(services_widget, "Services")
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Timer for checking server status
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_server_status)
        self.timer.start(5000)  # Check every 5 seconds
    
    def check_requirements(self):
        """Check if Docker is installed"""
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            self.add_log("[SUCCESS] Docker is installed")
        except FileNotFoundError:
            self.add_log("[ERROR] Docker is not installed")
            reply = QMessageBox.critical(
                self,
                "Docker Not Found",
                "Docker Desktop is required.\n\nDownload from: https://www.docker.com/products/docker-desktop",
                QMessageBox.StandardButton.Ok
            )
    
    def start_server(self):
        """Start the server"""
        if self.server_running:
            QMessageBox.warning(self, "Server Running", "Server is already running")
            return
        
        self.add_log("Starting server...")
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate
        self.start_btn.setEnabled(False)
        
        self.server_worker = ServerWorker(self.project_path)
        self.server_worker.log_signal.connect(self.add_log)
        self.server_worker.status_signal.connect(self.update_status)
        self.server_worker.start()
    
    def stop_server(self):
        """Stop the server"""
        try:
            os.chdir(self.project_path)
            self.add_log("Stopping server...")
            subprocess.run(["docker-compose", "down"], capture_output=True)
            self.add_log("[SUCCESS] Server stopped")
            self.server_running = False
            self.update_ui_state()
        except Exception as e:
            self.add_log(f"[ERROR] {str(e)}")
    
    def restart_server(self):
        """Restart the server"""
        self.stop_server()
        time.sleep(2)
        self.start_server()
    
    def check_server_status(self):
        """Check if server is running"""
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                if not self.server_running:
                    self.server_running = True
                    self.update_ui_state()
        except:
            if self.server_running:
                self.server_running = False
                self.update_ui_state()
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)
        if status == "Ready":
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.server_running = True
            self.progress.setVisible(False)
            self.start_btn.setEnabled(False)
            self.update_ui_state()
        elif status == "Running":
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        elif status == "Error":
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.progress.setVisible(False)
            self.start_btn.setEnabled(True)
    
    def update_ui_state(self):
        """Update button states based on server status"""
        self.stop_btn.setEnabled(self.server_running)
        self.restart_btn.setEnabled(self.server_running)
        self.api_btn.setEnabled(self.server_running)
        self.test_btn.setEnabled(self.server_running)
        self.generate_btn.setEnabled(self.server_running)
    
    def add_log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def test_api(self):
        """Test API endpoint"""
        if not self.server_running:
            QMessageBox.warning(self, "Server Not Running", "Start the server first")
            return
        
        endpoint = self.endpoint_combo.currentText()
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            self.response_text.setText(json.dumps(response.json(), indent=2))
        except Exception as e:
            self.response_text.setText(f"Error: {str(e)}")
    
    def generate_leads(self):
        """Generate leads"""
        if not self.server_running:
            QMessageBox.warning(self, "Server Not Running", "Start the server first")
            return
        
        try:
            city = self.city_input.text()
            category = self.category_input.text()
            limit = self.limit_spin.value()
            
            payload = {
                "city": city,
                "category": category,
                "limit": limit
            }
            
            response = requests.post(
                "http://localhost:8000/leads/generate",
                json=payload,
                timeout=10
            )
            
            self.leads_text.setText(json.dumps(response.json(), indent=2))
        except Exception as e:
            self.leads_text.setText(f"Error: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = ApexIntelligenceApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
