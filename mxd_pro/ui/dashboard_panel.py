import pyqtgraph as pg
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from .theme import Theme
from core.real_time_monitor import RealTimeMonitor

class DashboardPanel(QWidget):
    """The main security dashboard panel with professional styling and live charts."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Theme.STYLESHEET)
        self._init_ui()
        self._init_charts()
        self._start_monitoring()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        # Left side: Status and Scans
        left_v_layout = QVBoxLayout()
        status_group = self._create_status_group()
        left_v_layout.addWidget(status_group)
        scan_group = self._create_scan_group()
        left_v_layout.addWidget(scan_group)
        top_layout.addLayout(left_v_layout)

        # Right side: Performance Chart
        performance_group = self._create_performance_group()
        top_layout.addWidget(performance_group)
        main_layout.addLayout(top_layout)

        # Bottom: Threats table
        threats_group = self._create_threats_group()
        main_layout.addWidget(threats_group)

        self.setLayout(main_layout)

    def _create_status_group(self):
        group_box = QGroupBox("System Status")
        layout = QVBoxLayout()
        self.status_label = QLabel("PROTECTED")
        font = QFont("Segoe UI", 28, QFont.Bold)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet(f"color: {Theme.RED};")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        group_box.setLayout(layout)
        return group_box

    def _create_scan_group(self):
        group_box = QGroupBox("Manual Scans")
        layout = QHBoxLayout()
        quick_scan_btn = QPushButton("Quick Scan")
        full_scan_btn = QPushButton("Full System Scan")
        layout.addWidget(quick_scan_btn)
        layout.addWidget(full_scan_btn)
        group_box.setLayout(layout)
        return group_box

    def _create_performance_group(self):
        group_box = QGroupBox("Real-Time Performance Impact")
        layout = QVBoxLayout()
        pg.setConfigOption('background', Theme.DARK_GREY)
        pg.setConfigOption('foreground', Theme.LIGHT_GREY)
        self.perf_chart = pg.PlotWidget()
        self.perf_chart.showGrid(x=True, y=True, alpha=0.3)
        self.perf_chart.setLabel('left', 'Usage', units='%')
        self.perf_chart.setLabel('bottom', 'Time', units='s')
        self.perf_chart.addLegend()
        self.cpu_curve = self.perf_chart.plot(pen=pg.mkPen(Theme.RED, width=2), name="CPU")
        self.ram_curve = self.perf_chart.plot(pen=pg.mkPen(Theme.GOLD, width=2), name="RAM")
        layout.addWidget(self.perf_chart)
        group_box.setLayout(layout)
        return group_box

    def _create_threats_group(self):
        group_box = QGroupBox("Detected Threats")
        layout = QVBoxLayout()
        self.threats_table = QTableWidget()
        self.threats_table.setColumnCount(4)
        self.threats_table.setHorizontalHeaderLabels(["Timestamp", "Threat Name", "Type", "Risk Score"])
        self.threats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.threats_table)
        group_box.setLayout(layout)
        return group_box

    def _init_charts(self):
        self.time_data = list(range(30))
        self.cpu_data = [0] * 30
        self.ram_data = [0] * 30
        self.chart_timer = QTimer()
        self.chart_timer.setInterval(1000)
        self.chart_timer.timeout.connect(self._update_charts)
        self.chart_timer.start()

    def _update_charts(self):
        import psutil
        self.cpu_data.pop(0)
        self.cpu_data.append(psutil.cpu_percent())
        self.ram_data.pop(0)
        self.ram_data.append(psutil.virtual_memory().percent)
        self.cpu_curve.setData(self.time_data, self.cpu_data)
        self.ram_curve.setData(self.time_data, self.ram_data)

    def _start_monitoring(self):
        self.monitor_thread = RealTimeMonitor(self)
        self.monitor_thread.threat_detected.connect(self._on_threat_detected)
        self.monitor_thread.start()

    def _on_threat_detected(self, threat_info):
        from datetime import datetime
        QMessageBox.critical(
            self,
            "Threat Detected!",
            f"A high-risk threat has been detected:\n\n"
            f"Name: {threat_info['name']}\n"
            f"Type: {threat_info['type']}\n"
            f"Risk Score: {threat_info['risk_score']}\n\n"
            "The file has been automatically quarantined."
        )
        # Add to table
        row_position = self.threats_table.rowCount()
        self.threats_table.insertRow(row_position)
        self.threats_table.setItem(row_position, 0, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.threats_table.setItem(row_position, 1, QTableWidgetItem(threat_info['name']))
        self.threats_table.setItem(row_position, 2, QTableWidgetItem(threat_info['type']))
        self.threats_table.setItem(row_position, 3, QTableWidgetItem(str(threat_info['risk_score'])))

    def closeEvent(self, event):
        self.monitor_thread.stop()
        self.monitor_thread.wait()
        super().closeEvent(event)