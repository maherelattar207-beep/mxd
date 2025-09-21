from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider,
    QGroupBox, QCheckBox, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt

class OptimizerPanel(QWidget):
    """
    The main game optimizer panel.
    Allows selection of game, GPU, advanced settings, and applies config changes with full failsafes.
    """
    def __init__(self, hardware, games, settings, logger):
        super().__init__()
        self.hardware = hardware
        self.games = games
        self.settings = settings
        self.logger = logger
        self.current_game = self.games.list_all_games()[0]
        self.current_gpu = 0
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Game selection
        game_group = QGroupBox("Select Game")
        game_layout = QHBoxLayout()
        self.game_combo = QComboBox()
        self.game_combo.addItems(self.games.list_all_games())
        self.game_combo.currentIndexChanged.connect(self._on_game_changed)
        game_layout.addWidget(QLabel("Game:"))
        game_layout.addWidget(self.game_combo)
        game_group.setLayout(game_layout)
        layout.addWidget(game_group)

        # GPU selection (if multiple)
        gpu_group = QGroupBox("Select GPU")
        gpu_layout = QHBoxLayout()
        self.gpu_combo = QComboBox()
        gpus = self.hardware.gpus
        for idx, gpu in enumerate(gpus):
            label = f"{gpu.name} ({gpu.vendor}, {gpu.vram_mb//1024 if gpu.vram_mb>2048 else gpu.vram_mb}GB VRAM)"
            self.gpu_combo.addItem(label)
        self.gpu_combo.setCurrentIndex(self.current_gpu)
        self.gpu_combo.currentIndexChanged.connect(self._on_gpu_changed)
        gpu_layout.addWidget(QLabel("GPU:"))
        gpu_layout.addWidget(self.gpu_combo)
        gpu_group.setLayout(gpu_layout)
        layout.addWidget(gpu_group)

        # Resolution
        res_group = QGroupBox("Resolution (Up to 6K only)")
        res_layout = QHBoxLayout()
        self.res_combo = QComboBox()
        res_options = self.games.get_profile_by_name(self.current_game).supported_resolutions
        for res in res_options:
            self.res_combo.addItem(res)
        res_layout.addWidget(QLabel("Resolution:"))
        res_layout.addWidget(self.res_combo)
        res_group.setLayout(res_layout)
        layout.addWidget(res_group)

        # FPS
        fps_group = QGroupBox("Target FPS")
        fps_layout = QHBoxLayout()
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(30)
        self.fps_slider.setMaximum(240)
        self.fps_slider.setValue(60)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_label = QLabel("60")
        self.fps_slider.valueChanged.connect(lambda v: self.fps_label.setText(str(v)))
        fps_layout.addWidget(self.fps_slider)
        fps_layout.addWidget(self.fps_label)
        fps_group.setLayout(fps_layout)
        layout.addWidget(fps_group)

        # Advanced graphics
        adv_group = QGroupBox("Advanced Graphics")
        adv_layout = QVBoxLayout()
        self.dlss_combo = QComboBox()
        self.dlss_combo.addItems(["Off", "Quality", "Balanced", "Performance", "Ultra Performance"])
        adv_layout.addWidget(QLabel("DLSS/FSR/XeSS:"))
        adv_layout.addWidget(self.dlss_combo)
        self.rtx_checkbox = QCheckBox("Enable Ray Tracing")
        adv_layout.addWidget(self.rtx_checkbox)
        self.vrs_checkbox = QCheckBox("Enable Variable Rate Shading (VRS)")
        adv_layout.addWidget(self.vrs_checkbox)
        adv_group.setLayout(adv_layout)
        layout.addWidget(adv_group)

        # Dynamic scaling & frame pacing
        dyn_group = QGroupBox("Dynamic Scaling & Frame Pacing")
        dyn_layout = QVBoxLayout()
        self.dynres_checkbox = QCheckBox("Enable Dynamic Resolution Scaling")
        self.dynres_min_fps = QSlider(Qt.Horizontal)
        self.dynres_min_fps.setMinimum(30)
        self.dynres_min_fps.setMaximum(120)
        self.dynres_min_fps.setValue(45)
        self.dynres_min_fps.setTickInterval(5)
        self.dynres_min_fps.setTickPosition(QSlider.TicksBelow)
        self.dynres_min_fps_label = QLabel("Min FPS: 45")
        self.dynres_min_fps.valueChanged.connect(lambda v: self.dynres_min_fps_label.setText(f"Min FPS: {v}"))
        dyn_layout.addWidget(self.dynres_checkbox)
        dyn_layout.addWidget(self.dynres_min_fps_label)
        dyn_layout.addWidget(self.dynres_min_fps)
        self.framecap_checkbox = QCheckBox("Enable Frame Capping")
        self.framecap_value = QSlider(Qt.Horizontal)
        self.framecap_value.setMinimum(30)
        self.framecap_value.setMaximum(240)
        self.framecap_value.setValue(120)
        self.framecap_label = QLabel("Cap: 120")
        self.framecap_value.valueChanged.connect(lambda v: self.framecap_label.setText(f"Cap: {v}"))
        dyn_layout.addWidget(self.framecap_checkbox)
        dyn_layout.addWidget(self.framecap_label)
        dyn_layout.addWidget(self.framecap_value)
        dyn_group.setLayout(dyn_layout)
        layout.addWidget(dyn_group)

        # Low latency
        latency_group = QGroupBox("Input Lag Minimizer")
        latency_layout = QHBoxLayout()
        self.low_latency_checkbox = QCheckBox("Enable Ultra Low Latency")
        latency_layout.addWidget(self.low_latency_checkbox)
        latency_group.setLayout(latency_layout)
        layout.addWidget(latency_group)

        # Apply/Restore buttons
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply Settings")
        self.apply_btn.clicked.connect(self._apply_settings)
        self.restore_btn = QPushButton("Restore Last Settings")
        self.restore_btn.clicked.connect(self._restore_settings)
        btn_layout.addWidget(self.apply_btn)
        btn_layout.addWidget(self.restore_btn)
        layout.addLayout(btn_layout)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def _on_game_changed(self, idx):
        self.current_game = self.game_combo.currentText()
        # Update available resolutions for the selected game
        self.res_combo.clear()
        profile = self.games.get_profile_by_name(self.current_game)
        for res in profile.supported_resolutions:
            self.res_combo.addItem(res)
        self.logger.info(f"Game changed to {self.current_game}")

    def _on_gpu_changed(self, idx):
        self.current_gpu = idx
        self.logger.info(f"GPU changed to index {self.current_gpu}")

    def _apply_settings(self):
        game_name = self.current_game
        profile = self.games.get_profile_by_name(game_name)
        schema = profile.settings_schema
        settings = {
            "resolution": self.res_combo.currentText(),
            "fps": self.fps_slider.value(),
            "dlss": self.dlss_combo.currentText(),
            "rtx": self.rtx_checkbox.isChecked(),
            "vrs": self.vrs_checkbox.isChecked(),
            "dynamic_res": self.dynres_checkbox.isChecked(),
            "dynres_min": self.dynres_min_fps.value(),
            "framecap": self.framecap_checkbox.isChecked(),
            "framecap_val": self.framecap_value.value(),
            "low_latency": self.low_latency_checkbox.isChecked()
        }
        # Validate settings
        valid, msg = self.games.validate_settings(game_name, settings)
        if not valid:
            QMessageBox.warning(self, "Invalid Settings", msg)
            self.status_label.setText("Settings not applied: " + msg)
            self.logger.warning(f"Settings not applied: {msg}")
            return
        # Enforce 6K max
        if settings["resolution"] not in ["1080p", "2K", "4K", "5K", "6K"]:
            QMessageBox.critical(self, "Resolution Error", "Only up to 6K allowed for stability.")
            self.status_label.setText("Resolution not allowed.")
            self.logger.warning("User attempted unsupported resolution.")
            return
        # Save to user settings and write config
        self.settings.set_game_settings(game_name, settings)
        from core.config_writer import ConfigWriter
        writer = ConfigWriter(self.logger)
        config_path = profile.config_paths[0]
        writer.write_config(config_path, settings, schema)
        self.status_label.setText("Settings applied successfully.")
        self.logger.info(f"Settings applied for {game_name}: {settings}")

    def _restore_settings(self):
        game_name = self.current_game
        if self.settings.restore_last_backup(game_name):
            settings = self.settings.get_game_settings(game_name)
            # Update UI
            idx = self.res_combo.findText(settings.get("resolution", "4K"))
            if idx != -1:
                self.res_combo.setCurrentIndex(idx)
            self.fps_slider.setValue(settings.get("fps", 60))
            self.dlss_combo.setCurrentText(settings.get("dlss", "Off"))
            self.rtx_checkbox.setChecked(settings.get("rtx", False))
            self.vrs_checkbox.setChecked(settings.get("vrs", False))
            self.dynres_checkbox.setChecked(settings.get("dynamic_res", False))
            self.dynres_min_fps.setValue(settings.get("dynres_min", 45))
            self.framecap_checkbox.setChecked(settings.get("framecap", False))
            self.framecap_value.setValue(settings.get("framecap_val", 120))
            self.low_latency_checkbox.setChecked(settings.get("low_latency", False))
            self.status_label.setText("Restored last settings.")
            self.logger.info(f"Restored last backup for {game_name}")
        else:
            self.status_label.setText("No backup found.")
            self.logger.warning("Restore requested but no backup found.")