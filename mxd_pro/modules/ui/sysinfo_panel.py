from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QGroupBox, QPushButton,
    QHeaderView
)
from PyQt5.QtCore import Qt
import json

class SystemInfoPanel(QWidget):
    """
    Displays a detailed, read-only tree view of the system hardware information.
    """
    def __init__(self, hardware, logger):
        super().__init__()
        self.hardware = hardware
        self.logger = logger
        self.system_summary = self.hardware.get_system_summary()
        self._init_ui()
        self.logger.info("SystemInfoPanel initialized.")

    def _init_ui(self):
        layout = QVBoxLayout()

        # Action Buttons
        actions_group = QGroupBox("Actions")
        actions_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh Hardware Info")
        self.refresh_button.clicked.connect(self.refresh_info)
        actions_layout.addWidget(self.refresh_button)
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        # Tree Widget for System Info
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Component", "Details"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.tree)

        self.setLayout(layout)
        self.populate_tree()

    def populate_tree(self):
        """Populates the tree widget with hardware information."""
        self.tree.clear()

        # CPU Info
        cpu_info = self.system_summary.get('cpu', {})
        cpu_item = self._add_tree_item(self.tree, "CPU")
        self._add_tree_item(cpu_item, "Name", cpu_info.get('name', 'N/A'))
        self._add_tree_item(cpu_item, "Cores", f"{cpu_info.get('cores', 0)} ({cpu_info.get('threads', 0)} threads)")
        self._add_tree_item(cpu_item, "Frequency", f"{cpu_info.get('frequency_mhz', 0) / 1000:.2f} GHz")
        self._add_tree_item(cpu_item, "Architecture", cpu_info.get('architecture', 'N/A'))

        # GPU Info
        gpu_info_list = self.system_summary.get('gpus', [])
        gpu_item = self._add_tree_item(self.tree, "GPUs")
        for i, gpu in enumerate(gpu_info_list):
            gpu_sub_item = self._add_tree_item(gpu_item, f"GPU #{i+1}", gpu.get('name', 'N/A'))
            self._add_tree_item(gpu_sub_item, "Vendor", gpu.get('vendor', 'N/A'))
            self._add_tree_item(gpu_sub_item, "VRAM", f"{gpu.get('vram_mb', 0)} MB")
            self._add_tree_item(gpu_sub_item, "Driver Version", gpu.get('driver_version', 'N/A'))

            # Supported Features
            features_item = self._add_tree_item(gpu_sub_item, "Features")
            self._add_tree_item(features_item, "DLSS", "Supported" if gpu.get('supports_dlss') else "Not Supported")
            self._add_tree_item(features_item, "FSR", "Supported" if gpu.get('supports_fsr') else "Not Supported")
            self._add_tree_item(features_item, "XeSS", "Supported" if gpu.get('supports_xess') else "Not Supported")
            self._add_tree_item(features_item, "Ray Tracing", "Supported" if gpu.get('supports_rt') else "Not Supported")

        # Memory Info
        mem_info = self.system_summary.get('memory', {})
        mem_item = self._add_tree_item(self.tree, "Memory (RAM)")
        self._add_tree_item(mem_item, "Total", f"{mem_info.get('total_gb', 0):.2f} GB")
        self._add_tree_item(mem_item, "Available", f"{mem_info.get('available_gb', 0):.2f} GB")

        # Storage Info
        storage_info_list = self.system_summary.get('storage', [])
        storage_item = self._add_tree_item(self.tree, "Storage Devices")
        for i, disk in enumerate(storage_info_list):
            disk_sub_item = self._add_tree_item(storage_item, f"Disk #{i+1}", f"{disk.get('device', 'N/A')} ({disk.get('type', 'N/A')})")
            self._add_tree_item(disk_sub_item, "Size", f"{disk.get('total_gb', 0):.2f} GB")
            self._add_tree_item(disk_sub_item, "Free Space", f"{disk.get('free_gb', 0):.2f} GB")

        # OS Info
        os_info = self.system_summary.get('os', {})
        os_item = self._add_tree_item(self.tree, "Operating System")
        self._add_tree_item(os_item, "Name", os_info.get('name', 'N/A'))
        self._add_tree_item(os_item, "Version", os_info.get('version', 'N/A'))
        self._add_tree_item(os_item, "Build", os_info.get('build', 'N/A'))

        self.tree.expandAll()

    def _add_tree_item(self, parent, primary_text, secondary_text=""):
        """Helper to add an item to the tree."""
        item = QTreeWidgetItem([str(primary_text), str(secondary_text)])
        parent.addChild(item)
        return item

    def refresh_info(self):
        """Reloads hardware information and repopulates the view."""
        self.logger.info("Refreshing system hardware information...")
        self.system_summary = self.hardware.get_system_summary(force_rescan=True)
        self.populate_tree()
        self.logger.info("System information view refreshed.")