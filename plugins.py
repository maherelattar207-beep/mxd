# Simple plugin loader stub for MXD Pro.
import importlib.util
import os

class PluginManager:
    def __init__(self, plugin_dir="plugins", logger=None):
        self.plugin_dir = plugin_dir
        self.logger = logger
        self.plugins = []
        self.load_plugins()

    def _log(self, msg):
        if self.logger:
            self.logger.info(msg)

    def load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
        for fname in os.listdir(self.plugin_dir):
            if fname.endswith(".py"):
                path = os.path.join(self.plugin_dir, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                mod = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(mod)
                    self.plugins.append(mod)
                    self._log(f"Loaded plugin: {fname}")
                except Exception as e:
                    self._log(f"Failed to load plugin {fname}: {e}")

    def get_plugins(self):
        return self.plugins