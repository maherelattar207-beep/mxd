from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QMessageBox
)
from PyQt5.QtCore import Qt
from .widgets import ToolTipLabel

class SecurityPanel(QWidget):
    """The main user interface for the Security Engine."""
    def __init__(self, security_engine, logger):
        super().__init__()
        self.security_engine = security_engine
        self.logger = logger
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Main Status
        status_group = QGroupBox("Protection Status")
        status_layout = QHBoxLayout()
        self.status_label = QLabel("ACTIVE")
        self.status_label.setStyleSheet("color: #27AE60; font-size: 24pt; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        # Scan Controls
        scan_group = QGroupBox("Manual Scans")
        scan_layout = QHBoxLayout()
        scan_layout.addWidget(QPushButton("Quick Scan"))
        scan_layout.addWidget(QPushButton("Full System Scan"))
        scan_layout.addWidget(QPushButton("Custom Scan..."))
        scan_group.setLayout(scan_layout)
        main_layout.addWidget(scan_group)

        # Progress Bar
        self.scan_progress = QProgressBar()
        self.scan_progress.setVisible(False) # Hide until a scan is active
        main_layout.addWidget(self.scan_progress)

        # Threats Table
        threats_group = QGroupBox("Detected Threats")
        threats_layout = QVBoxLayout()
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(5)
        self.threats_table.setHorizontalHeaderLabels(["Threat Name", "Risk Level", "Status", "Date", "Path"])
        self.threats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        threats_layout.addWidget(self.threats_table)

        # Threat Actions
        actions_layout = QHBoxLayout()
        actions_layout.addWidget(QPushButton("Quarantine Selected"))
        actions_layout.addWidget(QPushButton("Delete Selected"))
        actions_layout.addWidget(QPushButton("Allow Selected"))
        actions_layout.addStretch()
        actions_layout.addWidget(ToolTipLabel("Manage detected items.\n'Allow' will add the item to an exclusion list."))
        threats_layout.addLayout(actions_layout)

        threats_group.setLayout(threats_layout)
        main_layout.addWidget(threats_group)

        self.setLayout(main_layout)