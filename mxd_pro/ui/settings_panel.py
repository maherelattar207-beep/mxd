from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QGroupBox, QComboBox,
    QCheckBox, QPushButton, QHBoxLayout, QApplication
)
from .widgets import ToolTipLabel

class SettingsPanel(QWidget):
    """The main settings panel with integrated help tooltips."""
    def __init__(self, settings_manager, license_manager, logger):
        super().__init__()
        self.settings = settings_manager
        self.license_manager = license_manager
        self.logger = logger
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tabs.addTab(self._create_defense_tab(), "Defense")
        self.tabs.addTab(self._create_scheduling_tab(), "Scheduling")
        self.tabs.addTab(self._create_beta_tab(), "Beta Features")
        self.tabs.addTab(self._create_account_tab(), "Account")

        self.setLayout(main_layout)

    def _create_defense_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        mode_group = QGroupBox("Autonomous Defense Mode")
        mode_layout = QHBoxLayout()
        mode_combo = QComboBox()
        mode_combo.addItems(["Balanced", "High Sensitivity", "Maximum Protection", "Gamer Mode"])
        mode_layout.addWidget(mode_combo)
        mode_layout.addWidget(ToolTipLabel("Select the AI's sensitivity.\n- Gamer Mode suspends alerts during fullscreen gaming."))
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        perf_group = QGroupBox("Performance Mode")
        perf_layout = QHBoxLayout()
        perf_combo = QComboBox()
        perf_combo.addItems(["Auto-Detect", "Low-End", "Normal", "High-End"])
        perf_layout.addWidget(perf_combo)
        perf_layout.addWidget(ToolTipLabel("Manually override the auto-detected hardware performance tier."))
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def _create_scheduling_tab(self):
        tab = QWidget()
        # ... (Layout with scheduling options and tooltips)
        return tab

    def _create_beta_tab(self):
        tab = QWidget()
        beta_layout = QVBoxLayout()
        group = QGroupBox("Experimental Features (BETA)")
        layout = QVBoxLayout()

        cleaner_layout = QHBoxLayout()
        cleaner_layout.addWidget(QCheckBox("Advanced Temp File Cleaner"))
        cleaner_layout.addWidget(ToolTipLabel("Safely scans and removes junk files to free up space."))
        layout.addLayout(cleaner_layout)

        booster_layout = QHBoxLayout()
        booster_layout.addWidget(QCheckBox("Offline System Booster"))
        booster_layout.addWidget(ToolTipLabel("Applies various tweaks to improve system responsiveness."))
        layout.addLayout(booster_layout)

        group.setLayout(layout)
        beta_layout.addWidget(group)
        beta_layout.addStretch()
        tab.setLayout(beta_layout)
        return tab

    def _create_account_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("License Management")

        deactivate_btn = QPushButton("Deactivate & Reactivate MXD Pro")
        deactivate_btn.clicked.connect(self._deactivate_and_restart)

        h_layout = QHBoxLayout()
        h_layout.addWidget(deactivate_btn)
        h_layout.addWidget(ToolTipLabel("Deactivates the current license and restarts the app to allow for a new key to be entered."))
        group.setLayout(h_layout)

        layout.addWidget(group)
        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def _deactivate_and_restart(self):
        self.logger.info("Deactivating and preparing for restart.")
        self.license_manager.deactivate()
        QApplication.quit() # A more robust implementation would use QProcess to restart