from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QGroupBox, QComboBox, QCheckBox, QPushButton, QHBoxLayout
from .theme import Theme, ToolTip

class SettingsPanel(QWidget):
    """A comprehensive settings panel with multiple tabs and tooltips."""
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setStyleSheet(Theme.STYLESHEET)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create and add tabs
        self.tabs.addTab(self._create_defense_tab(), "Defense Modes")
        self.tabs.addTab(self._create_scheduling_tab(), "Scheduling")
        self.tabs.addTab(self._create_beta_tab(), "Beta Features")
        self.tabs.addTab(self._create_account_tab(), "Account")

        self.setLayout(main_layout)

    def _create_defense_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Autonomous Defense Mode")

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QComboBox())
        mode_layout.itemAt(0).widget().addItems(["Balanced", "High Sensitivity", "Maximum Protection", "Gamer Mode"])
        mode_layout.addWidget(ToolTip("Select the AI's sensitivity level.\n- Balanced: Recommended for most users.\n- Gamer Mode: Suspends alerts during fullscreen gaming."))
        group.setLayout(mode_layout)

        layout.addWidget(group)
        tab.setLayout(layout)
        return tab

    def _create_scheduling_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Automatic Scans")

        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QComboBox())
        freq_layout.itemAt(0).widget().addItems(["Daily", "Weekly", "Monthly"])
        freq_layout.addWidget(ToolTip("How often to run a full system scan automatically."))

        smart_scan_layout = QHBoxLayout()
        smart_scan_layout.addWidget(QCheckBox("Enable Smart Scan (AI-scheduled)"))
        smart_scan_layout.addWidget(ToolTip("Lets the AI learn your usage patterns to schedule scans at the most convenient times."))

        v_layout = QVBoxLayout()
        v_layout.addLayout(freq_layout)
        v_layout.addLayout(smart_scan_layout)
        group.setLayout(v_layout)

        layout.addWidget(group)
        tab.setLayout(layout)
        return tab

    def _create_beta_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Experimental Features (Beta)")

        temp_cleaner_layout = QHBoxLayout()
        temp_cleaner_layout.addWidget(QCheckBox("Enable Advanced Temporary Files Cleaner"))
        temp_cleaner_layout.addWidget(ToolTip("Uses advanced algorithms to safely detect and remove junk files."))

        task_killer_layout = QHBoxLayout()
        task_killer_layout.addWidget(QCheckBox("Enable Safe Background Task Killer"))
        task_killer_layout.addWidget(ToolTip("Identifies and closes non-essential tasks to free up resources. 100% safe."))

        v_layout = QVBoxLayout()
        v_layout.addLayout(temp_cleaner_layout)
        v_layout.addLayout(task_killer_layout)
        group.setLayout(v_layout)

        layout.addWidget(group)
        tab.setLayout(layout)
        return tab

    def _create_account_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("License Management")
        deactivate_btn = QPushButton("Deactivate & Reactivate MXD Pro")
        layout.addWidget(deactivate_btn)
        group.setLayout(layout)
        layout.addWidget(group)
        tab.setLayout(layout)
        return tab