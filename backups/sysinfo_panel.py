from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QGroupBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class SystemInfoPanel(QWidget):
    """
    Displays detailed, read-only system and hardware info.
    GPU list, monitors, CPU, RAM, OS, and summary.
    """
    def __init__(self, hardware, logger):
        super().__init__()
        self.hardware = hardware
        self.logger = logger
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>System Information Overview</h2>"))

        # Summary box
        summary_box = QGroupBox("Summary")
        summary_layout = QVBoxLayout()
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setText(self.hardware.summary())
        summary_layout.addWidget(self.summary_text)
        summary_box.setLayout(summary_layout)
        layout.addWidget(summary_box)

        # GPU Table
        gpu_box = QGroupBox("Detected GPUs")
        gpu_layout = QVBoxLayout()
        self.gpu_table = QTableWidget()
        gpus = self.hardware.gpus
        self.gpu_table.setRowCount(len(gpus))
        self.gpu_table.setColumnCount(6)
        self.gpu_table.setHorizontalHeaderLabels([
            "Name", "Vendor", "VRAM (MB)", "Driver", "6K Capable", "Ray Tracing"
        ])
        for idx, gpu in enumerate(gpus):
            self.gpu_table.setItem(idx, 0, QTableWidgetItem(gpu.name))
            self.gpu_table.setItem(idx, 1, QTableWidgetItem(gpu.vendor))
            self.gpu_table.setItem(idx, 2, QTableWidgetItem(str(gpu.vram_mb)))
            self.gpu_table.setItem(idx, 3, QTableWidgetItem(gpu.driver))
            self.gpu_table.setItem(idx, 4, QTableWidgetItem("Yes" if gpu.supports_6k else "No"))
            self.gpu_table.setItem(idx, 5, QTableWidgetItem("Yes" if gpu.supports_rt else "No"))
        self.gpu_table.resizeColumnsToContents()
        gpu_layout.addWidget(self.gpu_table)
        gpu_box.setLayout(gpu_layout)
        layout.addWidget(gpu_box)

        # Monitor Table
        mon_box = QGroupBox("Connected Monitors")
        mon_layout = QVBoxLayout()
        monitors = self.hardware.monitors
        self.mon_table = QTableWidget()
        self.mon_table.setRowCount(len(monitors))
        self.mon_table.setColumnCount(4)
        self.mon_table.setHorizontalHeaderLabels([
            "Model", "Width", "Height", "Frequency (Hz)"
        ])
        for idx, mon in enumerate(monitors):
            self.mon_table.setItem(idx, 0, QTableWidgetItem(str(mon.name)))
            self.mon_table.setItem(idx, 1, QTableWidgetItem(str(mon.width)))
            self.mon_table.setItem(idx, 2, QTableWidgetItem(str(mon.height)))
            self.mon_table.setItem(idx, 3, QTableWidgetItem(str(mon.frequency)))
        self.mon_table.resizeColumnsToContents()
        mon_layout.addWidget(self.mon_table)
        mon_box.setLayout(mon_layout)
        layout.addWidget(mon_box)

        # CPU/RAM/OS Box
        cpu_box = QGroupBox("CPU, RAM, OS")
        cpu_layout = QVBoxLayout()
        cpu = self.hardware.cpu
        cpu_info = f"CPU: {cpu.get('name', 'Unknown')} ({cpu.get('arch', '?')})\n"
        cpu_info += f"Cores (Physical/Logical): {cpu.get('cores_physical', '?')} / {cpu.get('cores_logical', '?')}\n"
        cpu_info += f"Clock: {cpu.get('freq_mhz', '?')} MHz\n"
        cpu_info += f"RAM: {self.hardware.ram_gb} GB\n"
        cpu_info += f"Disk: {self.hardware.disk_gb} GB\n"
        cpu_info += f"OS: {self.hardware.os} {self.hardware.os_version}\n"
        cpu_info += f"Hostname: {self.hardware.hostname}\n"
        cpu_label = QLabel(cpu_info)
        cpu_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        cpu_layout.addWidget(cpu_label)
        cpu_box.setLayout(cpu_layout)
        layout.addWidget(cpu_box)

        layout.addStretch()
        self.setLayout(layout)