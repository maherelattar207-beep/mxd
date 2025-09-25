import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QGridLayout,
    QGroupBox, QCheckBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from datetime import datetime

from ..core.optimizer import UpscalingTechnology, AIMode, GameProfile, OptimizationLevel
from ..core.performance_manager import PerformanceMode
from ..core.response_manager import ResponseMode

class OptimizerPanel(QWidget):
    """
    The main game optimizer panel, fully functional with all advanced controls.
    """
    def __init__(self, hardware, games, settings, perf_manager, response_manager, ai_optimizer, logger):
        super().__init__()
        self.hardware = hardware
        self.games = games
        self.settings = settings
        self.perf_manager = perf_manager
        self.response_manager = response_manager
        self.ai_optimizer = ai_optimizer
        self.logger = logger

        self.detected_gpus = self.hardware.detect_gpus()
        self.detected_games = list(self.games.game_profiles.keys())

        self.current_game_name = self.detected_games[0] if self.detected_games else None
        self.current_gpu = self.detected_gpus[0] if self.detected_gpus else None

        self._init_ui()
        if self.current_game_name:
            self._on_game_changed(0)
        self.logger.info("OptimizerPanel initialized and fully connected.")

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self._create_selection_group())
        main_layout.addWidget(self._create_upscaling_group())
        main_layout.addWidget(self._create_graphics_group())
        main_layout.addWidget(self._create_response_time_group())
        main_layout.addWidget(self._create_fps_boost_group())
        main_layout.addWidget(self._create_actions_group())
        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_selection_group(self):
        group_box = QGroupBox("Game & GPU Selection")
        layout = QHBoxLayout()
        self.game_combo = QComboBox()
        if self.detected_games: self.game_combo.addItems(self.detected_games)
        self.game_combo.currentIndexChanged.connect(self._on_game_changed)
        layout.addWidget(QLabel("Game:"))
        layout.addWidget(self.game_combo)
        self.gpu_combo = QComboBox()
        if self.detected_gpus:
            for gpu in self.detected_gpus: self.gpu_combo.addItem(f"{gpu.name} ({gpu.vendor})", userData=gpu)
        self.gpu_combo.currentIndexChanged.connect(self._on_gpu_changed)
        layout.addWidget(QLabel("GPU:"))
        layout.addWidget(self.gpu_combo)
        group_box.setLayout(layout)
        return group_box

    def _create_upscaling_group(self):
        group_box = QGroupBox("Upscaling & Frame Generation")
        layout = QGridLayout()
        self.upscaling_combos = {}
        upscaling_map = {"DLSS": [e for e in UpscalingTechnology if "DLSS" in e.name], "FSR": [e for e in UpscalingTechnology if "FSR" in e.name], "XeSS": [e for e in UpscalingTechnology if "XESS" in e.name]}
        for i, (tech, enums) in enumerate(upscaling_map.items()):
            combo = QComboBox()
            combo.addItem("Off", userData=UpscalingTechnology.NONE)
            for e in enums: combo.addItem(e.name.replace(f"{tech}_", "").replace("2_", "2 "), userData=e)
            layout.addWidget(QLabel(f"{tech}:"), i, 0)
            layout.addWidget(combo, i, 1)
            self.upscaling_combos[tech] = combo
        self.frame_gen_checkbox = QCheckBox("Enable Frame Generation")
        layout.addWidget(self.frame_gen_checkbox, len(upscaling_map), 0, 1, 2)
        group_box.setLayout(layout)
        return group_box

    def _create_graphics_group(self):
        group_box = QGroupBox("Advanced Graphics")
        layout = QVBoxLayout()
        self.reflex_checkbox = QCheckBox("NVIDIA Reflex Low Latency")
        layout.addWidget(self.reflex_checkbox)
        self.drs_checkbox = QCheckBox("Enable Dynamic Resolution Scaling")
        layout.addWidget(self.drs_checkbox)
        self.rt_checkbox = QCheckBox("Enable Ray Tracing")
        layout.addWidget(self.rt_checkbox)
        group_box.setLayout(layout)
        return group_box

    def _create_response_time_group(self):
        group_box = QGroupBox("Response Time Optimization")
        layout = QHBoxLayout()
        self.response_mode_combo = QComboBox()
        for mode in ResponseMode: self.response_mode_combo.addItem(mode.value, mode)
        current_mode_str = self.settings.get("response_time.mode", ResponseMode.SAFE.value)
        self.response_mode_combo.setCurrentIndex(self.response_mode_combo.findData(ResponseMode(current_mode_str)))
        self.response_mode_combo.currentIndexChanged.connect(self._on_response_mode_changed)
        layout.addWidget(QLabel("Latency Reduction Mode:"))
        layout.addWidget(self.response_mode_combo)
        group_box.setLayout(layout)
        return group_box

    def _create_fps_boost_group(self):
        group_box = QGroupBox("Advanced FPS Boosting (Use with Caution)")
        layout = QVBoxLayout()
        self.high_prio_checkbox = QCheckBox("Set High Priority for Game Process")
        layout.addWidget(self.high_prio_checkbox)
        self.close_apps_checkbox = QCheckBox("Close Unnecessary Background Apps")
        layout.addWidget(self.close_apps_checkbox)
        group_box.setLayout(layout)
        return group_box

    def _create_actions_group(self):
        group_box = QGroupBox("Actions")
        layout = QVBoxLayout()
        profile_layout = QHBoxLayout()
        self.import_btn, self.export_btn = QPushButton("Import Profile(s)"), QPushButton("Export Profile(s)")
        self.import_btn.clicked.connect(self._import_profiles); self.export_btn.clicked.connect(self._export_profiles)
        profile_layout.addWidget(self.import_btn); profile_layout.addWidget(self.export_btn)
        layout.addLayout(profile_layout)
        ai_layout = QHBoxLayout()
        self.ai_mode_combo = QComboBox()
        for mode in AIMode: self.ai_mode_combo.addItem(mode.value, mode)
        self.auto_btn = QPushButton("Auto-Optimize")
        self.auto_btn.clicked.connect(self._auto_detect_settings)
        ai_layout.addWidget(QLabel("AI Mode:")); ai_layout.addWidget(self.ai_mode_combo); ai_layout.addWidget(self.auto_btn)
        layout.addLayout(ai_layout)
        self.apply_btn = QPushButton("Apply Settings")
        self.apply_btn.clicked.connect(self._apply_settings)
        layout.addWidget(self.apply_btn)
        self.status_label = QLabel("Welcome to MXD Pro!")
        layout.addWidget(self.status_label)
        group_box.setLayout(layout)
        return group_box

    def _update_controls_state(self):
        if not self.current_gpu: return
        self.upscaling_combos["DLSS"].setEnabled(self.current_gpu.supports_dlss)
        self.upscaling_combos["FSR"].setEnabled(self.current_gpu.supports_fsr)
        self.upscaling_combos["XeSS"].setEnabled(self.current_gpu.supports_xess)
        fg_unlocked = (self.current_gpu.supports_dlss or "FSR3" in "".join([c.currentText() for c in self.upscaling_combos.values()])) and self.perf_manager.is_feature_unlocked(PerformanceMode.HIGH_END)
        self.frame_gen_checkbox.setEnabled(fg_unlocked)
        self.reflex_checkbox.setEnabled(self.current_gpu.vendor == "NVIDIA")
        self.rt_checkbox.setEnabled(self.current_gpu.supports_rt and self.perf_manager.is_feature_unlocked(PerformanceMode.HIGH_END))
        self.drs_checkbox.setEnabled(self.perf_manager.is_feature_unlocked(PerformanceMode.NORMAL))

    def _on_gpu_changed(self, index):
        if index < 0: return
        self.current_gpu = self.gpu_combo.itemData(index)
        self._update_controls_state()

    def _on_game_changed(self, index):
        if index < 0: return
        self.current_game_name = self.game_combo.itemText(index)
        profile = self.games.game_profiles.get(self.current_game_name)
        if profile: self._populate_ui_from_profile(profile)

    def _populate_ui_from_profile(self, profile: GameProfile):
        self.rt_checkbox.setChecked(profile.ray_tracing)
        self.drs_checkbox.setChecked(profile.dynamic_resolution)
        self.frame_gen_checkbox.setChecked(profile.frame_generation)
        self.reflex_checkbox.setChecked(profile.low_latency_mode)
        for combo in self.upscaling_combos.values(): combo.setCurrentIndex(0)
        upscaling_tech_str = profile.upscaling.name
        for tech, combo in self.upscaling_combos.items():
            if tech in upscale_tech_str:
                index = combo.findData(profile.upscaling)
                if index != -1: combo.setCurrentIndex(index)
        self.status_label.setText(f"Loaded profile for {profile.name}.")
        self._update_controls_state()

    def _import_profiles(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Profiles", "", "JSON Files (*.json)")
        if path and self.games.import_game_profiles(path):
            self.game_combo.clear(); self.game_combo.addItems(self.games.game_profiles.keys())
            QMessageBox.information(self, "Success", "Profiles imported.")
        elif path: QMessageBox.critical(self, "Error", "Failed to import profiles.")

    def _export_profiles(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Profiles", "mxd_profiles.json", "JSON Files (*.json)")
        if path and self.games.export_game_profiles(path): QMessageBox.information(self, "Success", "Profiles exported.")
        elif path: QMessageBox.critical(self, "Error", "Failed to export profiles.")

    def _on_response_mode_changed(self, index):
        selected_mode = self.response_mode_combo.itemData(index)
        self.response_manager.set_mode(selected_mode)

    def _apply_settings(self):
        if not self.current_game_name: return
        if self.high_prio_checkbox.isChecked() or self.close_apps_checkbox.isChecked():
            game_profile = self.games.game_profiles.get(self.current_game_name)
            if game_profile: self.ai_optimizer.run_system_optimizations(game_profile=game_profile, boost_priority=self.high_prio_checkbox.isChecked(), close_apps=self.close_apps_checkbox.isChecked())
        selected_upscaling = next((c.itemData(c.currentIndex()) for c in self.upscaling_combos.values() if c.currentIndex() > 0), UpscalingTechnology.NONE)
        existing = self.games.game_profiles.get(self.current_game_name)
        new_profile = GameProfile(name=self.current_game_name, executable_paths=existing.executable_paths, config_files=existing.config_files, resolution=existing.resolution, target_fps=existing.target_fps, upscaling=selected_upscaling, frame_generation=self.frame_gen_checkbox.isChecked(), dynamic_resolution=self.drs_checkbox.isChecked(), ray_tracing=self.rt_checkbox.isChecked(), variable_rate_shading=existing.variable_rate_shading, low_latency_mode=self.reflex_checkbox.isChecked(), optimization_level=existing.optimization_level, custom_settings=existing.custom_settings, created_date=existing.created_date, last_modified=datetime.now().isoformat())
        self.games.game_profiles[self.current_game_name] = new_profile
        self.games._save_game_profiles()
        self.games.apply_game_optimization(self.current_game_name, self.hardware.get_system_summary())
        self.status_label.setText(f"Settings for {self.current_game_name} applied successfully!")
        QMessageBox.information(self, "Success", f"Settings for {self.current_game_name} have been applied.")

    def _auto_detect_settings(self):
        self.status_label.setText("Auto-detecting optimal settings...")
        mode = self.ai_mode_combo.itemData(self.ai_mode_combo.currentIndex())
        analysis = self.ai_optimizer.analyze_system_performance(self.hardware.get_system_summary(), mode)
        for rec in analysis.get("recommendations", []):
            rec_lower = rec.lower()
            if "disable ray tracing" in rec_lower: self.rt_checkbox.setChecked(False)
            elif "enable ray tracing" in rec_lower: self.rt_checkbox.setChecked(True)
            if "upscaling" in rec_lower:
                for quality in ["performance", "quality", "balanced"]:
                    if quality in rec_lower:
                        for combo in self.upscaling_combos.values():
                            if combo.isEnabled():
                                index = combo.findText(quality, Qt.MatchContains | Qt.MatchCaseInsensitive)
                                if index != -1: combo.setCurrentIndex(index); break
        self.status_label.setText("Optimal settings have been applied to the UI.")
        QMessageBox.information(self, "Auto-Detect Complete", "Optimal settings have been applied to the UI. Review and click 'Apply Settings' to save.")