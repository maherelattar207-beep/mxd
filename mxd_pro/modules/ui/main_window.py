from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QApplication, QAction, QMenu, QVBoxLayout
from PyQt5.QtGui import QIcon

from .optimizer_panel import OptimizerPanel
from .sysinfo_panel import SystemInfoPanel
from .security_panel import SecurityPanel
from .settings_panel import SettingsPanel
from .logs_panel import LogsPanel

class MainWindow(QMainWindow):
    def __init__(self, hardware, games, settings, logger, perf_manager, response_manager, ai_optimizer):
        super().__init__()
        self.hardware = hardware
        self.games = games
        self.settings = settings
        self.logger = logger
        self.perf_manager = perf_manager
        self.response_manager = response_manager
        self.ai_optimizer = ai_optimizer
        self.setWindowTitle("MXD Pro - Multi-GPU Game Optimizer")
        self.setMinimumSize(1024, 720)
        self.setWindowIcon(QIcon("assets/icons/app_icon.png"))

        self._init_ui()

    def _init_ui(self):
        self.tabs = QTabWidget()

        # Instantiate panels with all required dependencies
        self.optimizer_panel = OptimizerPanel(
            self.hardware, self.games, self.settings, self.perf_manager,
            self.response_manager, self.ai_optimizer, self.logger
        )
        self.sysinfo_panel = SystemInfoPanel(self.hardware, self.logger)
        self.security_panel = SecurityPanel(self.logger) # Placeholder
        self.settings_panel = SettingsPanel(self.settings, self.logger) # Placeholder
        self.logs_panel = LogsPanel(self.settings, self.logger)

        # Add tabs
        self.tabs.addTab(self.optimizer_panel, "Optimizer")
        self.tabs.addTab(self.sysinfo_panel, "System Info")
        self.tabs.addTab(self.security_panel, "Security")
        self.tabs.addTab(self.settings_panel, "Settings")
        self.tabs.addTab(self.logs_panel, "Logs & Recovery")

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