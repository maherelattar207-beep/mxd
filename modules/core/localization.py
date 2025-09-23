# Localization stub for MXD Pro.
# Extend with real translations as needed.

STRINGS = {
    "en": {
        "OPTIMIZER": "Optimizer",
        "SYSTEM_INFO": "System Info",
        "LOGS_RECOVERY": "Logs & Recovery",
        "APPLY_SETTINGS": "Apply Settings",
        "RESTORE_SETTINGS": "Restore Last Settings",
        "ABOUT": "About MXD Pro",
        "EXIT": "Exit"
    },
    "ar": {
        "OPTIMIZER": "المحسِّن",
        "SYSTEM_INFO": "معلومات النظام",
        "LOGS_RECOVERY": "السجلات والاستعادة",
        "APPLY_SETTINGS": "تطبيق الإعدادات",
        "RESTORE_SETTINGS": "استعادة الإعدادات الأخيرة",
        "ABOUT": "حول MXD Pro",
        "EXIT": "خروج"
    }
}

def t(key, lang="en"):
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)