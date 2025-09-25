import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QGroupBox, QFrame, QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

class SystemInfoPanel(QWidget):
    """
    Displays detailed system info, AI diagnostics, and real-time monitoring with alerts.
    """
    def __init__(self, hardware, perf_manager, ai_optimizer, response_manager, logger):
        super().__init__()
        self.hardware = hardware
        self.perf_manager = perf_manager
        self.ai_optimizer = ai_optimizer
        self.response_manager = response_manager
        self.logger = logger

        self.static_hardware_info = self.hardware.get_system_summary()
        self.realtime_labels = {}
        self.alert_triggered = set()
        self.high_cpu_counter = 0

        self._init_ui()
        self._setup_timer()
        self.logger.info("SystemInfoPanel initialized.")

        self._update_static_info()
        self._update_realtime_info()
        self._update_ai_diagnostics()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self._create_realtime_group())
        main_layout.addWidget(self._create_static_group())
        main_layout.addWidget(self._create_diagnostics_group())
        self.setLayout(main_layout)

    def _create_realtime_group(self):
        group_box = QGroupBox("Real-Time Monitoring")
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.addWidget(QLabel("<b>CPU</b>"), 0, 0); layout.addWidget(QLabel("<b>GPU</b>"), 0, 2); layout.addWidget(QLabel("<b>System</b>"), 0, 4)
        cpu_metrics = {"utilization": "Overall Usage:", "current_frequency": "Current Speed:"}
        gpu_metrics = {"utilization": "GPU Usage:", "vram_usage_percent": "VRAM Usage:", "temperature": "Temperature:", "core_clock_mhz": "Core Clock:", "mem_clock_mhz": "Memory Clock:", "power_draw_w": "Power Draw:"}
        for i, (key, text) in enumerate(cpu_metrics.items(), 1):
            layout.addWidget(QLabel(text), i, 0); self.realtime_labels[f"cpu_{key}"] = QLabel("N/A"); layout.addWidget(self.realtime_labels[f"cpu_{key}"], i, 1)
        for i, (key, text) in enumerate(gpu_metrics.items(), 1):
            layout.addWidget(QLabel(text), i, 2); self.realtime_labels[f"gpu_{key}"] = QLabel("N/A"); layout.addWidget(self.realtime_labels[f"gpu_{key}"], i, 3)
        layout.addWidget(QLabel("Simulated Latency:"), 1, 4); self.realtime_labels["system_latency"] = QLabel("N/A"); layout.addWidget(self.realtime_labels["system_latency"], 1, 5)
        group_box.setLayout(layout)
        return group_box

    def _create_static_group(self):
        group_box = QGroupBox("System Summary")
        layout = QGridLayout()
        self.static_cpu_label = QLabel("N/A"); self.static_gpu_label = QLabel("N/A"); self.static_ram_label = QLabel("N/A")
        layout.addWidget(QLabel("<b>Processor:</b>"), 0, 0); layout.addWidget(self.static_cpu_label, 0, 1)
        layout.addWidget(QLabel("<b>Graphics Card:</b>"), 1, 0); layout.addWidget(self.static_gpu_label, 1, 1)
        layout.addWidget(QLabel("<b>Memory (RAM):</b>"), 2, 0); layout.addWidget(self.static_ram_label, 2, 1)
        group_box.setLayout(layout)
        return group_box

    def _create_diagnostics_group(self):
        group_box = QGroupBox("AI Diagnostics & Recommendations")
        layout = QVBoxLayout()
        self.diagnostics_text = QTextEdit(); self.diagnostics_text.setReadOnly(True); self.diagnostics_text.setText("Analyzing system..."); self.diagnostics_text.setFixedHeight(100)
        layout.addWidget(self.diagnostics_text)
        group_box.setLayout(layout)
        return group_box

    def _setup_timer(self):
        self.timer = QTimer(self); self.timer.setInterval(3000); self.timer.timeout.connect(self._update_realtime_info); self.timer.start()

    def _update_static_info(self):
        cpu = self.static_hardware_info.get("cpu"); gpu = self.static_hardware_info.get("gpus")[0] if self.static_hardware_info.get("gpus") else None; mem = self.static_hardware_info.get("memory")
        if cpu: self.static_cpu_label.setText(f"{cpu.name} ({cpu.cores} Cores, {cpu.threads} Threads)")
        if gpu: self.static_gpu_label.setText(f"{gpu.name} ({gpu.vram_mb} MB VRAM)")
        if mem: self.static_ram_label.setText(f"{mem.total_mb / 1024:.1f} GB")

    def _update_ai_diagnostics(self):
        analysis = self.ai_optimizer.analyze_system_performance(self.static_hardware_info)
        report = f"<b>AI System Analysis:</b><br>CPU: {analysis['cpu_performance_class'].upper()} | GPU: {analysis['gpu_performance_class'].upper()} | Memory: {analysis['memory_adequacy'].upper()}<br><br>"
        report += "<b>Potential Bottlenecks:</b><br>" + "<br>".join([f"- {item}" for item in analysis['bottlenecks']]) if analysis['bottlenecks'] else "<b>No major bottlenecks detected.</b>"
        self.diagnostics_text.setText(report)

    def _show_alert(self, alert_type: str, title: str, message: str):
        if alert_type not in self.alert_triggered:
            self.logger.warning(f"Health Alert Triggered: {alert_type} - {message}")
            QMessageBox.critical(self, title, message)
            self.alert_triggered.add(alert_type)

    def _update_realtime_info(self):
        stats = self.hardware.get_realtime_stats(); cpu_stats = stats.get("cpu", {}); gpu_stats = stats.get("gpu", {})
        self.realtime_labels["cpu_utilization"].setText(f"{cpu_stats.get('utilization', 0.0):.1f} %")
        self.realtime_labels["cpu_current_frequency"].setText(f"{cpu_stats.get('current_frequency', 0.0):.0f} MHz")
        self.realtime_labels["gpu_utilization"].setText(f"{gpu_stats.get('utilization', 0.0):.1f} %")
        self.realtime_labels["gpu_vram_usage_percent"].setText(f"{gpu_stats.get('vram_usage_percent', 0.0):.1f} %")
        self.realtime_labels["gpu_temperature"].setText(f"{gpu_stats.get('temperature', 0.0):.1f} °C")
        self.realtime_labels["gpu_core_clock_mhz"].setText(f"{gpu_stats.get('core_clock_mhz', 0.0):.0f} MHz")
        self.realtime_labels["gpu_mem_clock_mhz"].setText(f"{gpu_stats.get('mem_clock_mhz', 0.0):.0f} MHz")
        self.realtime_labels["gpu_power_draw_w"].setText(f"{gpu_stats.get('power_draw_w', 0.0):.1f} W")
        self.realtime_labels["system_latency"].setText(f"{self.response_manager.get_simulated_latency():.2f} ms")

        # Check for alert conditions
        if gpu_stats.get('temperature', 0.0) > 90.0:
            self._show_alert("gpu_temp", "High GPU Temperature", "GPU temperature has exceeded 90°C. Please check your cooling system to prevent damage.")

        if cpu_stats.get('utilization', 0.0) > 95.0:
            self.high_cpu_counter += 1
            if self.high_cpu_counter >= 3: # Trigger alert after 3 consecutive high readings
                self._show_alert("cpu_load", "High CPU Usage", "CPU usage has been over 95% for an extended period, which may cause performance issues.")
        else:
            self.high_cpu_counter = 0 # Reset counter if usage drops
