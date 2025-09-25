import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QGroupBox, QCheckBox, QProgressBar, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ScanThread(QThread):
    """
    Worker thread to run the security scan without freezing the UI.
    """
    scan_complete = pyqtSignal(list)

    def __init__(self, security_manager):
        super().__init__()
        self.security_manager = security_manager

    def run(self):
        threats = self.security_manager.scan_for_threats()
        self.scan_complete.emit(threats)

class SecurityPanel(QWidget):
    """
    UI Panel for the AI Security Scanner.
    """
    def __init__(self, security_manager, logger):
        super().__init__()
        self.security_manager = security_manager
        self.logger = logger
        self.scan_thread = None
        self._init_ui()
        self.logger.info("SecurityPanel initialized.")

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self._create_scan_group())
        main_layout.addWidget(self._create_results_group())
        main_layout.addWidget(self._create_options_group())

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_scan_group(self):
        group_box = QGroupBox("Security Scan")
        layout = QVBoxLayout()

        self.scan_status_label = QLabel("Status: Ready to scan.")
        layout.addWidget(self.scan_status_label)

        self.scan_progress_bar = QProgressBar()
        self.scan_progress_bar.setRange(0, 0) # Indeterminate progress
        self.scan_progress_bar.setVisible(False)
        layout.addWidget(self.scan_progress_bar)

        self.start_scan_btn = QPushButton("Start System Scan")
        self.start_scan_btn.clicked.connect(self._start_scan)
        layout.addWidget(self.start_scan_btn)

        group_box.setLayout(layout)
        return group_box

    def _create_results_group(self):
        group_box = QGroupBox("Scan Results")
        layout = QVBoxLayout()

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        group_box.setLayout(layout)
        return group_box

    def _create_options_group(self):
        group_box = QGroupBox("Options")
        layout = QVBoxLayout()

        self.rtp_checkbox = QCheckBox("Enable Real-Time Protection")
        self.rtp_checkbox.setChecked(self.security_manager.real_time_protection_enabled)
        self.rtp_checkbox.toggled.connect(self._toggle_rtp)
        layout.addWidget(self.rtp_checkbox)

        self.vt_checkbox = QCheckBox("Enable Optional VirusTotal Checks")
        vt_enabled = self.security_manager.settings.get("security_suite.virus_total_check", True)
        self.vt_checkbox.setChecked(vt_enabled)
        self.vt_checkbox.toggled.connect(self._toggle_vt)
        layout.addWidget(self.vt_checkbox)

        group_box.setLayout(layout)
        return group_box

    def _start_scan(self):
        if self.scan_thread and self.scan_thread.isRunning():
            return

        self.start_scan_btn.setEnabled(False)
        self.scan_status_label.setText("Status: Scanning in progress...")
        self.scan_progress_bar.setVisible(True)
        self.results_list.clear()

        self.scan_thread = ScanThread(self.security_manager)
        self.scan_thread.scan_complete.connect(self._on_scan_complete)
        self.scan_thread.start()

    def _on_scan_complete(self, threats):
        self.scan_progress_bar.setVisible(False)
        self.start_scan_btn.setEnabled(True)

        if not threats:
            self.scan_status_label.setText("Status: Scan complete. No threats found.")
            self.results_list.addItem(QListWidgetItem("No threats were detected on your system."))
        else:
            self.scan_status_label.setText(f"Status: Scan complete. Found {len(threats)} threat(s).")
            for threat, path in threats:
                item = QListWidgetItem(f"Threat: {threat} | Path: {path}")
                self.results_list.addItem(item)

        self.scan_thread = None

    def _toggle_rtp(self, checked):
        self.security_manager.toggle_real_time_protection(checked)
        QMessageBox.information(self, "Real-Time Protection", f"Real-Time Protection has been {'enabled' if checked else 'disabled'}.")

    def _toggle_vt(self, checked):
        self.security_manager.settings.set("security_suite.virus_total_check", checked)
        QMessageBox.information(self, "VirusTotal Integration", f"VirusTotal integration has been {'enabled' if checked else 'disabled'}.")
