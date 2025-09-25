from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QPushButton, QGroupBox, QHeaderView
)
from .theme import Theme

class QuarantinePanel(QWidget):
    """UI panel to manage quarantined files."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Theme.STYLESHEET)
        self._init_ui()
        self._populate_dummy_data()

    def _init_ui(self):
        main_layout = QVBoxLayout()

        # Quarantine Table
        table_group = QGroupBox("Quarantined Items")
        table_layout = QVBoxLayout()
        self.quarantine_table = QTableWidget()
        self.quarantine_table.setColumnCount(4)
        self.quarantine_table.setHorizontalHeaderLabels([
            "Threat Name", "Original Path", "Date Quarantined", "Risk Score"
        ])
        self.quarantine_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_layout.addWidget(self.quarantine_table)
        table_group.setLayout(table_layout)
        main_layout.addWidget(table_group)

        # Action Buttons
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        restore_btn = QPushButton("Restore Selected")
        delete_btn = QPushButton("Delete Selected")
        actions_layout.addWidget(restore_btn)
        actions_layout.addWidget(delete_btn)
        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        self.setLayout(main_layout)

    def _populate_dummy_data(self):
        """Populates the table with placeholder data for demonstration."""
        dummy_items = [
            ("Trojan.Generic.12345", "C:/Users/Test/Downloads/installer.exe", "2025-09-24 18:05:10", "85"),
            ("Adware.InstallCore.789", "C:/Users/Test/AppData/Local/Temp/adware.dll", "2025-09-24 18:06:22", "40")
        ]
        for item in dummy_items:
            row_position = self.quarantine_table.rowCount()
            self.quarantine_table.insertRow(row_position)
            self.quarantine_table.setItem(row_position, 0, QTableWidgetItem(item[0]))
            self.quarantine_table.setItem(row_position, 1, QTableWidgetItem(item[1]))
            self.quarantine_table.setItem(row_position, 2, QTableWidgetItem(item[2]))
            self.quarantine_table.setItem(row_position, 3, QTableWidgetItem(item[3]))