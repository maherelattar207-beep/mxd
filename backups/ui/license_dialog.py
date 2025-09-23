import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QDesktopWidget, QFormLayout
)
from PyQt5.QtCore import Qt

class LicenseDialog(QDialog):
    """
    A dialog to prompt for license activation via email or a direct key.
    """
    def __init__(self, license_manager, logger):
        super().__init__()
        self.license_manager = license_manager
        self.logger = logger
        self.setWindowTitle("MXD Pro - Product Activation")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)
        self.setMinimumWidth(450)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        main_layout.addWidget(QLabel("<h2>Activate Your Product</h2>"))
        main_layout.addWidget(QLabel("Please activate using your purchase email or a provided license key."))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("e.g., user@example.com")
        form_layout.addRow("Purchase Email:", self.email_input)

        self.verify_btn = QPushButton("Verify Purchase & Activate")
        self.verify_btn.clicked.connect(self._verify_purchase)
        main_layout.addWidget(self.verify_btn)

        main_layout.addWidget(QLabel("<hr>")) # Separator

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter emergency master key or a provided key")
        form_layout.addRow("License Key:", self.key_input)

        main_layout.addLayout(form_layout)

        self.activate_key_btn = QPushButton("Activate with Key")
        self.activate_key_btn.clicked.connect(self._activate_with_key)
        main_layout.addWidget(self.activate_key_btn)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #C0392B;") # Red for errors
        main_layout.addWidget(self.status_label)

        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.reject)
        main_layout.addWidget(quit_btn, 0, Qt.AlignRight)

        self.setLayout(main_layout)

    def _verify_purchase(self):
        email = self.email_input.text().strip()
        if not email:
            self.status_label.setText("Please enter an email address.")
            return

        self.status_label.setText("Verifying purchase... (simulated)")
        QApplication.processEvents() # Update UI

        success, message = self.license_manager.verify_purchase_and_activate(email)

        if success:
            QMessageBox.information(self, "Activation Successful", message)
            self.accept()
        else:
            self.status_label.setText(f"Failed: {message}")
            QMessageBox.warning(self, "Activation Failed", message)

    def _activate_with_key(self):
        key = self.key_input.text().strip()
        if not key:
            self.status_label.setText("Please enter a license key.")
            return

        self.status_label.setText("Validating key...")
        QApplication.processEvents()

        success, message = self.license_manager.validate_and_store_license(key)

        if success:
            QMessageBox.information(self, "Activation Successful", message)
            self.accept()
        else:
            self.status_label.setText(f"Failed: {message}")
            QMessageBox.warning(self, "Activation Failed", message)
