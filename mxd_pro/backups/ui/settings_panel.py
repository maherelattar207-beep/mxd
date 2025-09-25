import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QComboBox, QCheckBox, QLabel,
    QMessageBox
)
from PyQt5.QtCore import Qt

from ..core.performance_manager import PerformanceMode
from ..core.utils import SystemUtils

class SettingsPanel(QWidget):
    """
    UI Panel for managing all application settings.
    """
    def __init__(self, settings, perf_manager, loc_manager, logger):
        super().__init__()
        self.settings = settings
        self.perf_manager = perf_manager
        self.loc_manager = loc_manager
        self.logger = logger
        self._init_ui()
        self.logger.info("SettingsPanel initialized.")

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        main_layout.addWidget(self._create_performance_group())
        main_layout.addWidget(self._create_language_group())
        main_layout.addWidget(self._create_general_settings_group())
        main_layout.addWidget(self._create_data_group())

        main_layout.addStretch()
        self.setLayout(main_layout)

    def _create_performance_group(self):
        group_box = QGroupBox("Performance Settings")
        layout = QVBoxLayout()

        # Performance Mode Override
        layout.addWidget(QLabel("Manually override the application's performance mode:"))
        self.perf_mode_combo = QComboBox()
        for mode in PerformanceMode:
            self.perf_mode_combo.addItem(mode.value, mode)

        # Set initial value from settings
        current_mode_str = self.settings.get("performance_mode", PerformanceMode.NORMAL.value)
        current_mode = PerformanceMode(current_mode_str)
        self.perf_mode_combo.setCurrentIndex(self.perf_mode_combo.findData(current_mode))

        self.perf_mode_combo.currentIndexChanged.connect(self._on_perf_mode_changed)
        layout.addWidget(self.perf_mode_combo)

        group_box.setLayout(layout)
        return group_box

    def _create_language_group(self):
        group_box = QGroupBox("Language Settings")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select application language (requires restart):"))
        self.lang_combo = QComboBox()

        # As per requirements, support for 16 languages
        languages = {
            "en": "English", "es": "Español (Spanish)", "fr": "Français (French)",
            "de": "Deutsch (German)", "it": "Italiano (Italian)", "pt": "Português (Portuguese)",
            "ru": "Русский (Russian)", "ja": "日本語 (Japanese)", "ko": "한국어 (Korean)",
            "zh": "中文 (Chinese)", "ar": "العربية (Arabic)", "hi": "हिन्दी (Hindi)",
            "pl": "Polski (Polish)", "tr": "Türkçe (Turkish)", "nl": "Nederlands (Dutch)",
            "sv": "Svenska (Swedish)"
        }
        for code, name in languages.items():
            self.lang_combo.addItem(name, code)

        current_lang = self.settings.get("language", "en")
        self.lang_combo.setCurrentIndex(self.lang_combo.findData(current_lang))

        self.lang_combo.currentIndexChanged.connect(self._on_lang_changed)
        layout.addWidget(self.lang_combo)

        group_box.setLayout(layout)
        return group_box

    def _create_general_settings_group(self):
        group_box = QGroupBox("General & AI Settings")
        layout = QVBoxLayout()

        # AI Learning
        self.ai_learning_checkbox = QCheckBox("Enable AI Learning Mode")
        is_checked = self.settings.get("ai_optimizer.learning_mode", True)
        self.ai_learning_checkbox.setChecked(is_checked)
        self.ai_learning_checkbox.toggled.connect(
            lambda checked: self.settings.set("ai_optimizer.learning_mode", checked)
        )
        layout.addWidget(self.ai_learning_checkbox)

        # Auto Updates
        self.auto_updates_checkbox = QCheckBox("Enable Automatic Updates")
        is_checked = self.settings.get("auto_updates", True)
        self.auto_updates_checkbox.setChecked(is_checked)
        self.auto_updates_checkbox.toggled.connect(
            lambda checked: self.settings.set("auto_updates", checked)
        )
        layout.addWidget(self.auto_updates_checkbox)

        group_box.setLayout(layout)
        return group_box

    def _on_perf_mode_changed(self, index):
        selected_mode = self.perf_mode_combo.itemData(index)
        self.settings.set("performance_mode", selected_mode.value)
        self.perf_manager.mode = selected_mode # Update the manager instance
        self.logger.info(f"Performance mode manually changed to: {selected_mode.value}")
        QMessageBox.information(self, "Performance Mode Changed",
            f"Performance mode has been set to {selected_mode.value}. "
            "UI controls will be updated. A restart may be required for all changes to take effect.")
        # In a fully-fledged app, we'd emit a signal here to tell other panels to update.

    def _on_lang_changed(self, index):
        selected_lang_code = self.lang_combo.itemData(index)
        self.loc_manager.change_language(selected_lang_code)
        self.logger.info(f"Language changed to: {selected_lang_code}")
        QMessageBox.information(self, "Language Changed",
            "The language has been changed. Please restart the application for the changes to take full effect.")

    def _create_data_group(self):
        group_box = QGroupBox("User Data")
        layout = QVBoxLayout()

        self.clear_data_btn = QPushButton("Clear Caches, Logs, and Settings")
        self.clear_data_btn.setToolTip("This will reset the application to its first-run state. Cannot be undone.")
        self.clear_data_btn.clicked.connect(self._confirm_and_clear_data)
        layout.addWidget(self.clear_data_btn)

        group_box.setLayout(layout)
        return group_box

    def _confirm_and_clear_data(self):
        reply = QMessageBox.warning(self, "Confirm Data Deletion",
            "This will delete all logs, settings, and user profiles, resetting the application to its factory state. This action cannot be undone.\n\nAre you sure you want to continue?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.logger.info("User confirmed data deletion.")
            SystemUtils.clear_all_user_data(self.logger)
            QMessageBox.information(self, "Data Cleared",
                "All user data has been cleared. The application will now close. Please restart it.")
            # Quit the application
            QApplication.instance().quit()
