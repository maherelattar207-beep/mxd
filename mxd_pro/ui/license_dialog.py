from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LicenseDialog(QDialog):
    """A dialog to prompt the user for a license key."""
    def __init__(self, license_manager, parent=None):
        super().__init__(parent)
        self.license_manager = license_manager
        self.setWindowTitle("MXD Pro Activation")
        self.setModal(True)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Please enter your license key to activate MXD Pro:"))
        self.key_input = QLineEdit()
        layout.addWidget(self.key_input)
        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self._on_activate_clicked)
        layout.addWidget(self.activate_button)
        self.setLayout(layout)

    def _on_activate_clicked(self):
        key = self.key_input.text().strip()
        if self.license_manager.activate(key):
            QMessageBox.information(self, "Success", "MXD Pro has been activated!")
            self.accept()
        else:
            QMessageBox.warning(self, "Activation Failed", "The provided license key is invalid.")