import os
import json
import xml.etree.ElementTree as ET
import shutil

class ConfigWriter:
    def __init__(self, logger):
        self.logger = logger

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

    def backup_config(self, config_path):
        if not os.path.exists(config_path):
            return None
        backup_path = config_path + ".mxdpro.bak"
        try:
            shutil.copy2(config_path, backup_path)
            self._log(f"Config backup created: {backup_path}")
            return backup_path
        except Exception as e:
            self._log(f"Failed to backup config {config_path}: {e}")
            return None

    def restore_backup(self, config_path):
        backup_path = config_path + ".mxdpro.bak"
        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, config_path)
                self._log(f"Config restored from backup: {backup_path}")
                return True
            except Exception as e:
                self._log(f"Failed to restore config from backup: {e}")
                return False
        return False

    def write_config(self, config_path, settings, schema):
        ext = os.path.splitext(config_path)[1].lower()
        self.backup_config(config_path)
        try:
            if ext in (".ini", ".cfg", ".ltx"):
                return self._write_ini(config_path, settings)
            elif ext in (".json", ".jsn"):
                return self._write_json(config_path, settings)
            elif ext == ".xml":
                return self._write_xml(config_path, settings)
            else:
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(str(settings))
                self._log(f"Wrote raw config for {config_path}")
                return True
        except Exception as e:
            self._log(f"Failed to write config {config_path}: {e}")
            return False

    def _write_ini(self, config_path, settings):
        lines = []
        for k, v in settings.items():
            lines.append(f"{k}={v}")
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self._log(f"Wrote INI/CFG config: {config_path}")
            return True
        except Exception as e:
            self._log(f"Failed to write INI/CFG: {e}")
            return False

    def _write_json(self, config_path, settings):
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
            self._log(f"Wrote JSON config: {config_path}")
            return True
        except Exception as e:
            self._log(f"Failed to write JSON: {e}")
            return False

    def _write_xml(self, config_path, settings):
        try:
            root = ET.Element("Settings")
            for k, v in settings.items():
                e = ET.SubElement(root, k)
                e.text = str(v)
            tree = ET.ElementTree(root)
            tree.write(config_path, encoding="utf-8", xml_declaration=True)
            self._log(f"Wrote XML config: {config_path}")
            return True
        except Exception as e:
            self._log(f"Failed to write XML: {e}")
            return False

    def validate_settings(self, settings, schema):
        for k, v in settings.items():
            if k not in schema:
                return False, f"Unknown setting: {k}"
            info = schema[k]
            if info["type"] == "int":
                if not isinstance(v, int):
                    return False, f"Setting {k} must be int"
                if "min" in info and v < info["min"]:
                    return False, f"Setting {k} too low"
                if "max" in info and v > info["max"]:
                    return False, f"Setting {k} too high"
            elif info["type"] == "string":
                if not isinstance(v, str):
                    return False, f"Setting {k} must be string"
                if "options" in info and v not in info["options"]:
                    return False, f"Setting {k} invalid value"
            elif info["type"] == "bool":
                if not isinstance(v, bool):
                    return False, f"Setting {k} must be bool"
        return True, ""

    def read_config(self, config_path):
        ext = os.path.splitext(config_path)[1].lower()
        if not os.path.exists(config_path):
            return {}
        try:
            if ext in (".ini", ".cfg", ".ltx"):
                return self._read_ini(config_path)
            elif ext in (".json", ".jsn"):
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            elif ext == ".xml":
                return self._read_xml(config_path)
            else:
                with open(config_path, "r", encoding="utf-8") as f:
                    return {"raw": f.read()}
        except Exception as e:
            self._log(f"Failed to read config {config_path}: {e}")
            return {}

    def _read_ini(self, config_path):
        result = {}
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    k, v = line.split("=", 1)
                    result[k.strip()] = v.strip()
        return result

    def _read_xml(self, config_path):
        result = {}
        try:
            tree = ET.parse(config_path)
            root = tree.getroot()
            for child in root:
                result[child.tag] = child.text
        except Exception:
            pass
        return result