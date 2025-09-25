from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QApplication, QAction, QMenu, QVBoxLayout
from PyQt5.QtGui import QIcon

from .optimizer_panel import OptimizerPanel
from .sysinfo_panel import SystemInfoPanel
from .security_panel import SecurityPanel
from .settings_panel import SettingsPanel
from .logs_panel import LogsPanel

class MainWindow(QMainWindow):
    def __init__(self, hardware, games, settings, perf_manager, ai_optimizer, security_manager, loc_manager, response_manager, logger):
        super().__init__()
        self.hardware = hardware
        self.games = games
        self.settings = settings
        self.perf_manager = perf_manager
        self.ai_optimizer = ai_optimizer
        self.security_manager = security_manager
        self.loc_manager = loc_manager
        self.response_manager = response_manager
        self.logger = logger
        self.setWindowTitle("MXD Pro - Multi-GPU Game Optimizer")
        self.setMinimumSize(1024, 720)
        self.setWindowIcon(QIcon("assets/icons/app_icon.png"))

        self._init_ui()

        # Connect signals from backend managers to UI slots
        self.games.instability_reverted.connect(self._show_rollback_notification)

    def _init_ui(self):
        self.setWindowTitle(self.loc_manager.get_string("app_title", "MXD Pro"))

        self.tabs = QTabWidget()
        self.optimizer_panel = OptimizerPanel(self.hardware, self.games, self.settings, self.perf_manager, self.response_manager, self.logger)
        self.sysinfo_panel = SystemInfoPanel(self.hardware, self.perf_manager, self.ai_optimizer, self.response_manager, self.logger)
        self.security_panel = SecurityPanel(self.security_manager, self.logger)
        self.settings_panel = SettingsPanel(self.settings, self.perf_manager, self.loc_manager, self.logger)
        self.logs_panel = LogsPanel(self.logger)

        self.tabs.addTab(self.optimizer_panel, self.loc_manager.get_string("tab_optimizer", "Optimizer"))
        self.tabs.addTab(self.sysinfo_panel, self.loc_manager.get_string("tab_system_info", "System Info"))
        self.tabs.addTab(self.security_panel, self.loc_manager.get_string("tab_security", "Security"))
        self.tabs.addTab(self.settings_panel, self.loc_manager.get_string("tab_settings", "Settings"))
        self.tabs.addTab(self.logs_panel, self.loc_manager.get_string("tab_logs_recovery", "Logs & Recovery"))

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "About MXD Pro",
            "MXD Pro\nMulti-GPU, Multi-Game Optimizer\n\n"
            "by maherelattar207-beep and contributors\n"
            "https://github.com/maherelattar207-beep\n"
            "MIT License"
        )

    def _show_rollback_notification(self, game_name, message):
        """Displays a warning message when a rollback occurs."""
        from PyQt5.QtWidgets import QMessageBox
        self.logger.warning(f"Displaying rollback notification for {game_name}")
        QMessageBox.warning(self, "Optimization Rolled Back",
            f"<b>Instability Detected for {game_name}!</b><br><br>"
            f"{message}<br><br>"
            "Your previous settings for this game have been restored.")