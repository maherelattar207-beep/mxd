from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from core.licensing import LicenseManager

class LicenseDialog(QDialog):
    """A dialog to prompt the user for a license key."""
    def __init__(self, license_manager: LicenseManager, parent=None):
        super().__init__(parent)
        self.license_manager = license_manager

        self.setWindowTitle("MXD Pro Activation")
        self.setModal(True)
        self.setFixedWidth(400)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("MXD Pro Activation Required")
        title.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Please enter your license key to activate the software."))

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
        layout.addWidget(self.key_input)

        self.activate_button = QPushButton("Activate")
        self.activate_button.clicked.connect(self._on_activate_clicked)
        layout.addWidget(self.activate_button)

        self.setLayout(layout)

    def _on_activate_clicked(self):
        key = self.key_input.text().strip()
        if self.license_manager.activate(key):
            QMessageBox.information(self, "Success", "MXD Pro has been activated successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Activation Failed", "The license key you entered is invalid. Please try again.")
            self.key_input.selectAll()