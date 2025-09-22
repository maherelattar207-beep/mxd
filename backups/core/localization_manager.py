import json
from pathlib import Path

class LocalizationManager:
    """
    Manages loading and retrieving translated strings for the UI.
    """
    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings
        self.lang_dir = Path("backups/languages")
        self.strings = {}
        self.load_language()

    def load_language(self):
        """
        Loads the language file specified in the settings.
        Defaults to 'en' if the specified language is not found.
        """
        lang_code = self.settings.get("language", "en")
        lang_file = self.lang_dir / f"{lang_code}.json"

        if not lang_file.exists():
            self.logger.warning(f"Language file not found: {lang_file}. Defaulting to English.")
            lang_file = self.lang_dir / "en.json"
            if not lang_file.exists():
                self.logger.error("Default language file 'en.json' is missing. UI text will be empty.")
                self.strings = {}
                return

        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
            self.logger.info(f"Successfully loaded language: {lang_code}")
        except Exception as e:
            self.logger.error(f"Failed to load or parse language file {lang_file}: {e}")
            self.strings = {}

    def get_string(self, key, default_text=""):
        """
        Retrieves a translated string for a given key.
        Returns a default text if the key is not found.
        """
        return self.strings.get(key, default_text)

    def change_language(self, lang_code):
        """
        Changes the current language, saves it to settings, and reloads strings.
        """
        self.settings.set("language", lang_code)
        self.load_language()
