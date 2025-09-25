from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QLabel, QGroupBox
)
from PyQt5.QtCore import Qt

class LogsPanel(QWidget):
    """
    Logs and Recovery panel:
    - Shows last N lines of app log
    - Allows export, clear, and import/export of settings
    - Provides quick links to log file and backup directory
    """
    def __init__(self, settings, logger):
        super().__init__()
        self.settings = settings
        self.logger = logger
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # Log viewer group
        log_group = QGroupBox("MXD Pro Activity Log")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)

        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh Logs")
        self.refresh_btn.clicked.connect(self._refresh_logs)
        btn_layout.addWidget(self.refresh_btn)

        self.export_btn = QPushButton("Export Logs")
        self.export_btn.clicked.connect(self._export_logs)
        btn_layout.addWidget(self.export_btn)

        self.clear_btn = QPushButton("Clear Logs")
        self.clear_btn.clicked.connect(self._clear_logs)
        btn_layout.addWidget(self.clear_btn)

        log_layout.addLayout(btn_layout)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # Settings import/export
        settings_group = QGroupBox("Settings Export/Import & Backups")
        settings_layout = QHBoxLayout()
        self.export_settings_btn = QPushButton("Export All Settings")
        self.export_settings_btn.clicked.connect(self._export_settings)
        settings_layout.addWidget(self.export_settings_btn)

        self.import_settings_btn = QPushButton("Import Settings")
        self.import_settings_btn.clicked.connect(self._import_settings)
        settings_layout.addWidget(self.import_settings_btn)

        self.show_logfile_btn = QPushButton("Open Log File Location")
        self.show_logfile_btn.clicked.connect(self._show_logfile)
        settings_layout.addWidget(self.show_logfile_btn)

        self.show_backup_dir_btn = QPushButton("Open Backups Directory")
        self.show_backup_dir_btn.clicked.connect(self._show_backup_dir)
        settings_layout.addWidget(self.show_backup_dir_btn)

        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        # Recovery note
        note = QLabel(
            "If your settings become corrupted, use 'Import Settings' to restore a backup, or 'Restore Last Settings' in the Optimizer panel.\n"
            "For support, you can export logs/settings and send them to support."
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        layout.addStretch()
        self.setLayout(layout)
        self._refresh_logs()

    def _refresh_logs(self):
        logs = self.logger.get_logs(500)
        self.log_text.setPlainText(logs)

    def _export_logs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Logs", "mxd_pro.log", "Log Files (*.log);;All Files (*)")
        if path:
            try:
                with open(self.logger.get_logfile_path(), "r", encoding="utf-8") as src, open(path, "w", encoding="utf-8") as dst:
                    dst.write(src.read())
                QMessageBox.information(self, "Export Logs", f"Logs exported to {path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export logs: {e}")

    def _clear_logs(self):
        self.logger.clear_logs()
        self._refresh_logs()
        QMessageBox.information(self, "Logs Cleared", "Log file cleared.")

    def _export_settings(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Settings", "mxdpro_settings_export.json", "JSON Files (*.json);;All Files (*)")
        if path:
            if self.settings.export_all_settings(path):
                QMessageBox.information(self, "Export Settings", f"Settings exported to {path}")
            else:
                QMessageBox.critical(self, "Export Failed", "Failed to export settings.")

    def _import_settings(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Settings", "", "JSON Files (*.json);;All Files (*)")
        if path:
            if self.settings.import_all_settings(path):
                QMessageBox.information(self, "Import Settings", f"Settings imported from {path}")
                self._refresh_logs()
            else:
                QMessageBox.critical(self, "Import Failed", "Failed to import settings.")

    def _show_logfile(self):
        import subprocess
        import os
        path = self.logger.get_logfile_path()
        if os.path.exists(path):
            if os.name == 'nt':
                os.startfile(os.path.dirname(path))
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', os.path.dirname(path)])
        else:
            QMessageBox.warning(self, "Not Found", "Log file not found.")

    def _show_backup_dir(self):
        import subprocess
        import os
        backup_dir = "mxdpro_backups"
        if os.path.exists(backup_dir):
            if os.name == 'nt':
                os.startfile(os.path.abspath(backup_dir))
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', os.path.abspath(backup_dir)])
        else:
            QMessageBox.warning(self, "Not Found", "Backup directory not found.")