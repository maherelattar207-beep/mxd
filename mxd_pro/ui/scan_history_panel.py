from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QGroupBox, QHeaderView
)
from .theme import Theme

class ScanHistoryPanel(QWidget):
    """UI panel to display the history of past scans."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Theme.STYLESHEET)
        self._init_ui()
        self._populate_dummy_data()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        group_box = QGroupBox("Scan History")
        layout = QVBoxLayout()
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels([
            "Date & Time", "Scan Type", "Items Scanned", "Threats Found"
        ])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.history_table)
        group_box.setLayout(layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

    def _populate_dummy_data(self):
        """Populates the table with placeholder data for demonstration."""
        dummy_items = [
            ("2025-09-24 18:00:05", "Full System Scan", "1,234,567", "2"),
            ("2025-09-24 14:30:11", "Quick Scan", "15,890", "0"),
            ("2025-09-23 09:05:45", "Full System Scan", "1,198,234", "1")
        ]
        for item in dummy_items:
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(item[0]))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(item[1]))
            self.history_table.setItem(row_position, 2, QTableWidgetItem(item[2]))
            self.history_table.setItem(row_position, 3, QTableWidgetItem(item[3]))