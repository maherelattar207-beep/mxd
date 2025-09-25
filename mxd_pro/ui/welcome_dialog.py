from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class WelcomeDialog(QDialog):
    """A dialog to welcome the user."""
    def __init__(self, user_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Welcome, {user_name}!")
        self.setModal(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Welcome, {user_name}!\n\nMXD Pro is now ready for you."))
        ok_button = QPushButton("Get Started")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)