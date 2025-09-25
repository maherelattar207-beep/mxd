from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QGroupBox, QCheckBox, QMessageBox, QFileDialog, QGridLayout
)
from PyQt5.QtCore import Qt
from .widgets import ToolTipLabel

class OptimizerPanel(QWidget):
    """The main game optimizer panel with all advanced controls."""
    def __init__(self, hardware, games, settings, perf_manager, ai_optimizer, logger):
        super().__init__()
        self.hardware = hardware
        self.games = games
        self.settings = settings
        self.perf_manager = perf_manager
        self.ai_optimizer = ai_optimizer
        self.logger = logger
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Create and add all the control groups
        main_layout.addWidget(self._create_selection_group())
        main_layout.addWidget(self._create_upscaling_group())
        main_layout.addWidget(self._create_graphics_group())
        main_layout.addWidget(self._create_fps_boost_group())
        main_layout.addWidget(self._create_actions_group())

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_selection_group(self):
        group_box = QGroupBox("Game & GPU Selection")
        layout = QHBoxLayout()
        self.game_combo = QComboBox()
        # self.game_combo.addItems(self.games.get_game_list()) # To be connected later
        layout.addWidget(QLabel("Game:"))
        layout.addWidget(self.game_combo)
        # ... (GPU selection would go here)
        group_box.setLayout(layout)
        return group_box

    def _create_upscaling_group(self):
        group_box = QGroupBox("Upscaling & Frame Generation")
        layout = QGridLayout()
        # DLSS
        layout.addWidget(QLabel("NVIDIA DLSS:"), 0, 0)
        self.dlss_combo = QComboBox()
        self.dlss_combo.addItems(["Off", "Quality", "Balanced", "Performance", "Ultra Performance"])
        layout.addWidget(self.dlss_combo, 0, 1)
        layout.addWidget(ToolTipLabel("Deep Learning Super Sampling for NVIDIA RTX GPUs."), 0, 2)
        # FSR
        layout.addWidget(QLabel("AMD FSR:"), 1, 0)
        self.fsr_combo = QComboBox()
        self.fsr_combo.addItems(["Off", "FSR 2 Quality", "FSR 2 Balanced", "FSR 3 Performance"])
        layout.addWidget(self.fsr_combo, 1, 1)
        layout.addWidget(ToolTipLabel("FidelityFX Super Resolution, works on most GPUs."), 1, 2)
        # XeSS
        layout.addWidget(QLabel("Intel XeSS:"), 2, 0)
        self.xess_combo = QComboBox()
        self.xess_combo.addItems(["Off", "Quality", "Balanced", "Performance"])
        layout.addWidget(self.xess_combo, 2, 1)
        layout.addWidget(ToolTipLabel("Xe Super Sampling for Intel Arc and other modern GPUs."), 2, 2)
        # Frame Gen
        self.frame_gen_checkbox = QCheckBox("Enable Frame Generation")
        layout.addWidget(self.frame_gen_checkbox, 3, 0, 1, 2)
        layout.addWidget(ToolTipLabel("Generates intermediate frames for smoother gameplay.\nRequires DLSS 3 or FSR 3."), 3, 2)
        group_box.setLayout(layout)
        return group_box

    def _create_graphics_group(self):
        group_box = QGroupBox("Advanced Graphics")
        layout = QVBoxLayout()
        # ... (Reflex, DRS, Ray Tracing checkboxes with tooltips)
        layout.addWidget(QCheckBox("Enable NVIDIA Reflex Low Latency"))
        layout.addWidget(QCheckBox("Enable Dynamic Resolution Scaling"))
        layout.addWidget(QCheckBox("Enable Ray Tracing"))
        group_box.setLayout(layout)
        return group_box

    def _create_fps_boost_group(self):
        group_box = QGroupBox("FPS Boost+")
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Set High Priority for Game Process"))
        layout.addWidget(QCheckBox("Close Unnecessary Background Apps (Safe Mode)"))
        group_box.setLayout(layout)
        return group_box

    def _create_actions_group(self):
        group_box = QGroupBox("Actions")
        layout = QVBoxLayout()

        ai_layout = QHBoxLayout()
        ai_layout.addWidget(QLabel("AI Mode:"))
        self.ai_mode_combo = QComboBox()
        self.ai_mode_combo.addItems(["Performance", "Graphics", "Balanced"])
        ai_layout.addWidget(self.ai_mode_combo)
        ai_layout.addWidget(QPushButton("Auto-Optimize"))
        layout.addLayout(ai_layout)

        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QPushButton("Import Profile"))
        profile_layout.addWidget(QPushButton("Export Profile"))
        layout.addLayout(profile_layout)

        layout.addWidget(QPushButton("Apply Settings"))
        group_box.setLayout(layout)
        return group_box