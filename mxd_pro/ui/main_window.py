from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout

class MainWindow(QMainWindow):
    """The main application window."""
    def __init__(self, settings_manager, license_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.license_manager = license_manager
        self.setWindowTitle("MXD Pro - AI Antivirus & Security System")
        self.setMinimumSize(1200, 800)
        self._init_ui()

    def _init_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        from .dashboard_panel import DashboardPanel
        self.dashboard_panel = DashboardPanel()
        self.tabs.addTab(self.dashboard_panel, "Dashboard")

        from .settings_panel import SettingsPanel
        self.settings_panel = SettingsPanel(self.settings_manager)
        self.tabs.addTab(self.settings_panel, "Settings")

        from .quarantine_panel import QuarantinePanel
        self.quarantine_panel = QuarantinePanel()
        self.tabs.addTab(self.quarantine_panel, "Quarantine")

        from .scan_history_panel import ScanHistoryPanel
        self.scan_history_panel = ScanHistoryPanel()
        self.tabs.addTab(self.scan_history_panel, "Scan History")

        from .gamer_tools_panel import GamerToolsPanel
        self.gamer_tools_panel = GamerToolsPanel()
        self.tabs.addTab(self.gamer_tools_panel, "Gamer Tools")

        self.show()