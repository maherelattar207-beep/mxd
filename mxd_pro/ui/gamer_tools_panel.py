from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton
from .theme import Theme

class GamerToolsPanel(QWidget):
    """UI panel for gamer-focused performance tools."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Theme.STYLESHEET)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()

        # Response Time Optimization
        response_group = QGroupBox("Response Time Optimization")
        response_layout = QVBoxLayout()
        response_layout.addWidget(QCheckBox("Enable Aggressive Latency Tuning (Experimental)"))
        response_layout.addWidget(QPushButton("Apply Latency Optimization"))
        response_group.setLayout(response_layout)
        main_layout.addWidget(response_group)

        # FPS Boost+
        fps_group = QGroupBox("FPS Boost+")
        fps_layout = QVBoxLayout()
        fps_layout.addWidget(QCheckBox("Auto-close unnecessary background applications before gaming"))
        fps_layout.addWidget(QPushButton("Activate FPS Boost"))
        fps_group.setLayout(fps_layout)
        main_layout.addWidget(fps_group)

        main_layout.addStretch()
        self.setLayout(main_layout)