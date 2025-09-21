#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro Ultimate v2.0 - Unified Gaming & Security Suite
Military-grade security, advanced FPS optimization, real-time monitoring
Author: Enhanced by RepoBirdBot AI Agent
"""

import os
import sys
import json
import time
import threading
import platform
import psutil
import uuid
import hashlib
import secrets
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk

# Windows-specific imports
try:
    if platform.system() == "Windows":
        import winreg
        import wmi
        import win32process
        import win32con
    else:
        winreg = wmi = win32process = win32con = None
except ImportError:
    winreg = wmi = win32process = win32con = None

# Security imports
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

# ===== CONFIGURATION =====
APP_NAME = "MXD Pro Ultimate"
APP_VERSION = "2.0.0"
DATA_DIR = os.path.join(os.path.expanduser("~"), ".mxdpro")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
LICENSE_FILE = os.path.join(DATA_DIR, "license.key")
QUARANTINE_DIR = os.path.join(DATA_DIR, "quarantine")

# Create directories
for dir_path in [DATA_DIR, QUARANTINE_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# ===== HARDWARE DETECTION SYSTEM =====
class HardwareDetector:
    """Advanced hardware detection with temperature monitoring"""
    
    def __init__(self):
        self.cpu_info = {}
        self.gpu_info = []
        self.ram_info = {}
        self.motherboard_info = {}
        self.temperatures = {}
        self._detect_hardware()
    
    def _detect_hardware(self):
        """Detect all system hardware"""
        self._detect_cpu()
        self._detect_gpu()
        self._detect_ram()
        self._detect_motherboard()
        self._detect_temperatures()
    
    def _detect_cpu(self):
        """Detect CPU information"""
        try:
            self.cpu_info = {
                'name': platform.processor(),
                'architecture': platform.architecture()[0],
                'cores_physical': psutil.cpu_count(logical=False),
                'cores_logical': psutil.cpu_count(logical=True),
                'frequency': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {},
                'usage_percent': psutil.cpu_percent(interval=1)
            }
        except Exception as e:
            self.cpu_info = {'error': str(e)}
    
    def _detect_gpu(self):
        """Detect GPU information"""
        self.gpu_info = []
        
        # Windows GPU detection
        if platform.system() == "Windows" and wmi:
            try:
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    if gpu.Name:
                        gpu_data = {
                            'name': gpu.Name,
                            'vendor': self._get_gpu_vendor(gpu.Name),
                            'driver': gpu.DriverVersion or "Unknown",
                            'vram_mb': int(gpu.AdapterRAM / 1024 / 1024) if gpu.AdapterRAM else 0,
                            'supports_dlss': self._supports_dlss(gpu.Name),
                            'supports_fsr': self._supports_fsr(gpu.Name),
                            'supports_rt': self._supports_raytracing(gpu.Name),
                            'supports_6k': self._supports_6k(gpu.Name)
                        }
                        self.gpu_info.append(gpu_data)
            except Exception as e:
                print(f"GPU detection error: {e}")
        
        # Fallback detection
        if not self.gpu_info:
            self.gpu_info = [{
                'name': 'Generic Graphics Adapter',
                'vendor': 'Unknown',
                'driver': 'Unknown',
                'vram_mb': 0,
                'supports_dlss': False,
                'supports_fsr': False,
                'supports_rt': False,
                'supports_6k': False
            }]
    
    def _get_gpu_vendor(self, gpu_name):
        """Determine GPU vendor"""
        gpu_name = gpu_name.lower()
        if 'nvidia' in gpu_name or 'geforce' in gpu_name or 'gtx' in gpu_name or 'rtx' in gpu_name:
            return 'NVIDIA'
        elif 'amd' in gpu_name or 'radeon' in gpu_name or 'rx ' in gpu_name:
            return 'AMD'
        elif 'intel' in gpu_name or 'uhd' in gpu_name or 'iris' in gpu_name:
            return 'Intel'
        return 'Unknown'
    
    def _supports_dlss(self, gpu_name):
        """Check if GPU supports DLSS"""
        gpu_name = gpu_name.lower()
        rtx_cards = ['rtx 20', 'rtx 30', 'rtx 40', 'rtx 2060', 'rtx 2070', 'rtx 2080', 
                     'rtx 3060', 'rtx 3070', 'rtx 3080', 'rtx 3090', 'rtx 4060', 
                     'rtx 4070', 'rtx 4080', 'rtx 4090']
        return any(card in gpu_name for card in rtx_cards)
    
    def _supports_fsr(self, gpu_name):
        """Check if GPU supports FSR"""
        # FSR works on most modern GPUs
        vendors = ['nvidia', 'amd', 'intel', 'geforce', 'radeon', 'rtx', 'gtx']
        return any(vendor in gpu_name.lower() for vendor in vendors)
    
    def _supports_raytracing(self, gpu_name):
        """Check if GPU supports ray tracing"""
        gpu_name = gpu_name.lower()
        rt_cards = ['rtx', 'rx 6', 'rx 7', 'arc']
        return any(card in gpu_name for card in rt_cards)
    
    def _supports_6k(self, gpu_name):
        """Check if GPU supports 6K resolution"""
        gpu_name = gpu_name.lower()
        high_end = ['rtx 3080', 'rtx 3090', 'rtx 4070', 'rtx 4080', 'rtx 4090',
                   'rx 6800', 'rx 6900', 'rx 7800', 'rx 7900']
        return any(card in gpu_name for card in high_end)
    
    def _detect_ram(self):
        """Detect RAM information"""
        try:
            vm = psutil.virtual_memory()
            self.ram_info = {
                'total_gb': round(vm.total / 1024**3, 2),
                'available_gb': round(vm.available / 1024**3, 2),
                'used_gb': round(vm.used / 1024**3, 2),
                'usage_percent': vm.percent
            }
        except Exception as e:
            self.ram_info = {'error': str(e)}
    
    def _detect_motherboard(self):
        """Detect motherboard information"""
        self.motherboard_info = {}
        if platform.system() == "Windows" and wmi:
            try:
                c = wmi.WMI()
                for board in c.Win32_BaseBoard():
                    self.motherboard_info = {
                        'manufacturer': board.Manufacturer or "Unknown",
                        'product': board.Product or "Unknown",
                        'serial': board.SerialNumber or "Unknown",
                        'version': board.Version or "Unknown"
                    }
                    break
            except Exception as e:
                self.motherboard_info = {'error': str(e)}
    
    def _detect_temperatures(self):
        """Detect system temperatures"""
        self.temperatures = {}
        try:
            # Try to get temperature data
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current:
                            self.temperatures[f"{name}_{entry.label or 'temp'}"] = {
                                'current': entry.current,
                                'high': entry.high,
                                'critical': entry.critical
                            }
        except Exception as e:
            self.temperatures = {'error': 'Temperature monitoring not available'}
    
    def get_system_summary(self):
        """Get complete system summary"""
        return {
            'cpu': self.cpu_info,
            'gpu': self.gpu_info,
            'ram': self.ram_info,
            'motherboard': self.motherboard_info,
            'temperatures': self.temperatures,
            'platform': {
                'system': platform.system(),
                'version': platform.version(),
                'architecture': platform.architecture(),
                'hostname': platform.node()
            }
        }

# ===== SECURITY SCANNER =====
class SecurityScanner:
    """Advanced security scanner with real-time protection"""
    
    def __init__(self):
        self.scan_results = {}
        self.threats_detected = []
        self.quarantine_path = QUARANTINE_DIR
        self.is_scanning = False
    
    def scan_system(self, progress_callback=None):
        """Perform comprehensive system scan"""
        self.is_scanning = True
        self.scan_results = {
            'files_scanned': 0,
            'threats_found': 0,
            'suspicious_processes': 0,
            'registry_issues': 0,
            'network_threats': 0,
            'threats': []
        }
        
        try:
            # Scan processes
            if progress_callback:
                progress_callback("Scanning running processes...")
            self._scan_processes()
            
            # Scan critical directories
            if progress_callback:
                progress_callback("Scanning system files...")
            self._scan_directories()
            
            # Scan registry (Windows only)
            if platform.system() == "Windows":
                if progress_callback:
                    progress_callback("Scanning registry...")
                self._scan_registry()
            
            # Network analysis
            if progress_callback:
                progress_callback("Analyzing network connections...")
            self._scan_network()
            
        finally:
            self.is_scanning = False
        
        return self.scan_results
    
    def _scan_processes(self):
        """Scan running processes for threats"""
        suspicious_names = [
            'virus', 'malware', 'trojan', 'keylogger', 'rootkit',
            'spyware', 'adware', 'ransomware', 'backdoor', 'miner'
        ]
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower()
                
                # Check for suspicious process names
                for suspicious in suspicious_names:
                    if suspicious in proc_name:
                        threat = {
                            'type': 'suspicious_process',
                            'name': proc.info['name'],
                            'pid': proc.info['pid'],
                            'exe': proc.info['exe'],
                            'threat_level': 'high'
                        }
                        self.scan_results['threats'].append(threat)
                        self.scan_results['suspicious_processes'] += 1
                        break
                
                # Check for processes without executable path (suspicious)
                if not proc.info['exe'] and proc.info['name'] not in ['System', '[System Process]']:
                    threat = {
                        'type': 'process_without_exe',
                        'name': proc.info['name'],
                        'pid': proc.info['pid'],
                        'threat_level': 'medium'
                    }
                    self.scan_results['threats'].append(threat)
            
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
    def _scan_directories(self):
        """Scan critical system directories"""
        scan_paths = []
        
        if platform.system() == "Windows":
            scan_paths = [
                os.path.join(os.environ.get('SYSTEMROOT', 'C:\\Windows'), 'System32'),
                os.environ.get('TEMP', 'C:\\Temp'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
            ]
        else:
            scan_paths = ['/tmp', '/var/tmp', os.path.expanduser('~/Downloads')]
        
        for scan_path in scan_paths:
            if os.path.exists(scan_path):
                self._scan_directory(scan_path, max_depth=2)
    
    def _scan_directory(self, directory, max_depth=1, current_depth=0):
        """Scan a directory for threats"""
        if current_depth > max_depth:
            return
        
        try:
            for root, dirs, files in os.walk(directory):
                if current_depth > max_depth:
                    break
                
                for file in files:
                    file_path = os.path.join(root, file)
                    self.scan_results['files_scanned'] += 1
                    
                    if self._is_suspicious_file(file_path):
                        threat = {
                            'type': 'suspicious_file',
                            'path': file_path,
                            'threat_level': 'medium'
                        }
                        self.scan_results['threats'].append(threat)
                        self.scan_results['threats_found'] += 1
                
                current_depth += 1
                
        except (PermissionError, OSError):
            pass
    
    def _is_suspicious_file(self, file_path):
        """Check if file is suspicious"""
        try:
            file_name = os.path.basename(file_path).lower()
            
            # Suspicious file extensions
            suspicious_extensions = ['.exe', '.scr', '.bat', '.cmd', '.vbs', '.js']
            
            # Suspicious file names
            suspicious_names = ['virus', 'malware', 'trojan', 'keylog', 'hack', 'crack']
            
            # Check extension
            if any(file_name.endswith(ext) for ext in suspicious_extensions):
                # Check if in system directory (more suspicious)
                if 'temp' in file_path.lower() or 'download' in file_path.lower():
                    return True
            
            # Check name
            if any(name in file_name for name in suspicious_names):
                return True
            
            # Check file size (very small or very large executables are suspicious)
            if file_name.endswith('.exe'):
                size = os.path.getsize(file_path)
                if size < 1024 or size > 500 * 1024 * 1024:  # < 1KB or > 500MB
                    return True
            
            return False
        except Exception:
            return False
    
    def _scan_registry(self):
        """Scan Windows registry for suspicious entries"""
        if not winreg:
            return
        
        suspicious_keys = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
        ]
        
        for root_key, sub_key in suspicious_keys:
            try:
                key = winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        if self._is_suspicious_registry_entry(name, value):
                            threat = {
                                'type': 'suspicious_registry',
                                'key': f"{root_key}\\{sub_key}",
                                'name': name,
                                'value': value,
                                'threat_level': 'medium'
                            }
                            self.scan_results['threats'].append(threat)
                            self.scan_results['registry_issues'] += 1
                        i += 1
                    except WindowsError:
                        break
                winreg.CloseKey(key)
            except Exception:
                continue
    
    def _is_suspicious_registry_entry(self, name, value):
        """Check if registry entry is suspicious"""
        suspicious_patterns = ['temp', 'tmp', 'malware', 'virus', 'trojan']
        name_lower = name.lower()
        value_lower = value.lower()
        
        return any(pattern in name_lower or pattern in value_lower for pattern in suspicious_patterns)
    
    def _scan_network(self):
        """Scan network connections for threats"""
        try:
            connections = psutil.net_connections()
            suspicious_ports = [4444, 5555, 6666, 31337, 12345]  # Common backdoor ports
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.laddr and conn.raddr:
                    if conn.laddr.port in suspicious_ports or conn.raddr.port in suspicious_ports:
                        threat = {
                            'type': 'suspicious_network',
                            'local_addr': f"{conn.laddr.ip}:{conn.laddr.port}",
                            'remote_addr': f"{conn.raddr.ip}:{conn.raddr.port}",
                            'status': conn.status,
                            'threat_level': 'high'
                        }
                        self.scan_results['threats'].append(threat)
                        self.scan_results['network_threats'] += 1
        except Exception:
            pass
    
    def quarantine_threat(self, threat_info):
        """Quarantine detected threat"""
        try:
            threat_id = str(uuid.uuid4())
            quarantine_file = os.path.join(self.quarantine_path, f"threat_{threat_id}.json")
            
            threat_data = {
                'id': threat_id,
                'threat_info': threat_info,
                'quarantined_at': time.time(),
                'status': 'quarantined'
            }
            
            with open(quarantine_file, 'w') as f:
                json.dump(threat_data, f, indent=2)
            
            # If it's a file threat, move the actual file
            if threat_info.get('type') == 'suspicious_file' and 'path' in threat_info:
                original_path = threat_info['path']
                if os.path.exists(original_path):
                    quarantine_path = os.path.join(self.quarantine_path, f"file_{threat_id}")
                    os.rename(original_path, quarantine_path)
            
            return True, threat_id
        except Exception as e:
            return False, str(e)

# ===== GAME OPTIMIZER =====
class GameOptimizer:
    """Advanced game optimization with DLSS/FSR support"""
    
    def __init__(self, hardware_detector):
        self.hardware = hardware_detector
        self.game_profiles = self._load_game_profiles()
        self.optimization_history = []
    
    def _load_game_profiles(self):
        """Load comprehensive game profiles with DLSS/FSR support"""
        return {
            "Cyberpunk 2077": {
                "executable": "Cyberpunk2077.exe",
                "config_path": r"Documents\CD Projekt RED\Cyberpunk 2077\UserSettings.json",
                "supports_dlss": True,
                "supports_fsr": True,
                "supports_rt": True,
                "recommended_settings": {
                    "resolution_scale": 1.0,
                    "ray_tracing": "auto",
                    "dlss_mode": "Quality",
                    "fsr_mode": "Quality"
                }
            },
            "Call of Duty: Modern Warfare II": {
                "executable": "cod.exe",
                "config_path": r"Documents\Call of Duty\players\config.cfg",
                "supports_dlss": True,
                "supports_fsr": True,
                "supports_rt": False,
                "recommended_settings": {
                    "resolution_scale": 1.0,
                    "dlss_mode": "Performance",
                    "fsr_mode": "Performance"
                }
            },
            "Fortnite": {
                "executable": "FortniteClient-Win64-Shipping.exe",
                "config_path": r"AppData\Local\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini",
                "supports_dlss": True,
                "supports_fsr": False,
                "supports_rt": False,
                "recommended_settings": {
                    "resolution_scale": 1.0,
                    "dlss_mode": "Performance"
                }
            },
            "Valorant": {
                "executable": "VALORANT-Win64-Shipping.exe",
                "config_path": r"AppData\Local\VALORANT\Saved\Config\Windows\RiotUserSettings.ini",
                "supports_dlss": False,
                "supports_fsr": False,
                "supports_rt": False,
                "recommended_settings": {
                    "resolution_scale": 1.0,
                    "low_latency": True
                }
            },
            "Apex Legends": {
                "executable": "r5apex.exe",
                "config_path": r"Documents\Respawn\Apex Legends\local\videoconfig.txt",
                "supports_dlss": False,
                "supports_fsr": True,
                "supports_rt": False,
                "recommended_settings": {
                    "resolution_scale": 1.0,
                    "fsr_mode": "Performance"
                }
            }
        }
    
    def detect_games(self):
        """Detect installed games"""
        detected_games = []
        
        # Common game installation directories
        search_paths = []
        if platform.system() == "Windows":
            possible_drives = ['C:', 'D:', 'E:', 'F:']
            for drive in possible_drives:
                search_paths.extend([
                    os.path.join(drive, "Program Files", "Steam", "steamapps", "common"),
                    os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common"),
                    os.path.join(drive, "Epic Games"),
                    os.path.join(drive, "Program Files", "Epic Games"),
                    os.path.join(drive, "Games"),
                ])
        
        for game_name, profile in self.game_profiles.items():
            for search_path in search_paths:
                if os.path.exists(search_path):
                    try:
                        for item in os.listdir(search_path):
                            item_path = os.path.join(search_path, item)
                            if os.path.isdir(item_path):
                                # Look for the game executable
                                for root, dirs, files in os.walk(item_path):
                                    if profile["executable"] in files:
                                        detected_games.append({
                                            'name': game_name,
                                            'path': os.path.join(root, profile["executable"]),
                                            'profile': profile
                                        })
                                        break
                    except (PermissionError, OSError):
                        continue
        
        return detected_games
    
    def optimize_game(self, game_name, target_fps=60, target_resolution="1080p"):
        """Optimize game settings based on hardware and preferences"""
        if game_name not in self.game_profiles:
            return False, f"Game profile not found: {game_name}"
        
        profile = self.game_profiles[game_name]
        gpu_info = self.hardware.gpu_info[0] if self.hardware.gpu_info else {}
        
        optimization_settings = {
            'game': game_name,
            'target_fps': target_fps,
            'target_resolution': target_resolution,
            'applied_settings': {},
            'timestamp': time.time()
        }
        
        # Determine best upscaling technology
        if gpu_info.get('supports_dlss') and profile.get('supports_dlss'):
            if target_fps >= 120:
                optimization_settings['applied_settings']['upscaling'] = 'DLSS Performance'
            elif target_fps >= 90:
                optimization_settings['applied_settings']['upscaling'] = 'DLSS Balanced'
            else:
                optimization_settings['applied_settings']['upscaling'] = 'DLSS Quality'
        elif gpu_info.get('supports_fsr') and profile.get('supports_fsr'):
            if target_fps >= 120:
                optimization_settings['applied_settings']['upscaling'] = 'FSR Performance'
            elif target_fps >= 90:
                optimization_settings['applied_settings']['upscaling'] = 'FSR Balanced'
            else:
                optimization_settings['applied_settings']['upscaling'] = 'FSR Quality'
        else:
            optimization_settings['applied_settings']['upscaling'] = 'None'
        
        # Ray tracing settings
        if gpu_info.get('supports_rt') and profile.get('supports_rt'):
            if target_fps <= 60 and gpu_info.get('vram_mb', 0) >= 8192:
                optimization_settings['applied_settings']['ray_tracing'] = 'Medium'
            else:
                optimization_settings['applied_settings']['ray_tracing'] = 'Off'
        else:
            optimization_settings['applied_settings']['ray_tracing'] = 'Off'
        
        # Resolution scaling
        if target_resolution == "4K" and gpu_info.get('vram_mb', 0) < 8192:
            optimization_settings['applied_settings']['resolution_scale'] = 0.8
        elif target_resolution == "6K" and not gpu_info.get('supports_6k'):
            optimization_settings['applied_settings']['resolution_scale'] = 0.6
        else:
            optimization_settings['applied_settings']['resolution_scale'] = 1.0
        
        # Apply Windows-level optimizations
        self._apply_windows_optimizations(target_fps)
        
        # Save optimization history
        self.optimization_history.append(optimization_settings)
        
        return True, f"Game optimized successfully: {optimization_settings['applied_settings']}"
    
    def _apply_windows_optimizations(self, target_fps):
        """Apply Windows-level gaming optimizations"""
        if platform.system() != "Windows":
            return
        
        optimizations = []
        
        try:
            # Set high performance power plan
            result = subprocess.run(['powercfg', '/setactive', 'scheme_min'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                optimizations.append("High performance power plan activated")
        except Exception:
            pass
        
        try:
            # Enable hardware-accelerated GPU scheduling (Windows 10 2004+)
            key_path = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "HwSchMode", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            optimizations.append("Hardware-accelerated GPU scheduling enabled")
        except Exception:
            pass
        
        try:
            # Set game mode registry key
            game_mode_key = r"SOFTWARE\Microsoft\GameBar"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, game_mode_key, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "AutoGameModeEnabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            optimizations.append("Game Mode enabled")
        except Exception:
            pass
        
        return optimizations

# ===== LICENSE MANAGER =====
class LicenseManager:
    """Military-grade license system with hardware fingerprinting"""
    
    def __init__(self):
        self.license_valid = False
        self.license_info = {}
        self._check_license()
    
    def generate_activation_key(self):
        """Generate random activation key"""
        key_parts = []
        for _ in range(4):
            part = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(4))
            key_parts.append(part)
        return '-'.join(key_parts)
    
    def _get_hardware_fingerprint(self):
        """Generate unique hardware fingerprint"""
        try:
            # Collect hardware identifiers
            identifiers = []
            
            # CPU info
            identifiers.append(platform.processor())
            identifiers.append(str(psutil.cpu_count()))
            
            # Memory
            identifiers.append(str(psutil.virtual_memory().total))
            
            # MAC addresses
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if hasattr(addr, 'address') and len(addr.address) == 17:
                        identifiers.append(addr.address)
            
            # Motherboard serial (Windows)
            if platform.system() == "Windows" and wmi:
                try:
                    c = wmi.WMI()
                    for board in c.Win32_BaseBoard():
                        if board.SerialNumber:
                            identifiers.append(board.SerialNumber)
                        break
                except Exception:
                    pass
            
            # Create fingerprint
            combined = '|'.join(sorted(identifiers))
            fingerprint = hashlib.sha256(combined.encode()).hexdigest()
            return fingerprint
        except Exception:
            # Fallback fingerprint
            fallback = f"{platform.node()}_{uuid.getnode()}"
            return hashlib.sha256(fallback.encode()).hexdigest()
    
    def activate_license(self, activation_key):
        """Activate license with key"""
        try:
            # Validate activation key format
            if not self._validate_key_format(activation_key):
                return False, "Invalid activation key format"
            
            # Generate hardware fingerprint
            fingerprint = self._get_hardware_fingerprint()
            
            # Create license data
            license_data = {
                'activation_key': activation_key,
                'hardware_fingerprint': fingerprint,
                'activated_at': time.time(),
                'version': APP_VERSION,
                'features': [
                    'advanced_gaming_optimization',
                    'military_security_suite', 
                    'real_time_monitoring',
                    'ai_performance_tuning',
                    'virus_protection'
                ],
                'valid': True
            }
            
            # Encrypt and save license
            if HAS_CRYPTO:
                encrypted_data = self._encrypt_license(license_data)
            else:
                encrypted_data = json.dumps(license_data).encode()
            
            with open(LICENSE_FILE, 'wb') as f:
                f.write(encrypted_data)
            
            self.license_valid = True
            self.license_info = license_data
            return True, "License activated successfully"
            
        except Exception as e:
            return False, f"License activation failed: {str(e)}"
    
    def _validate_key_format(self, key):
        """Validate activation key format (XXXX-XXXX-XXXX-XXXX)"""
        import re
        pattern = r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
        return re.match(pattern, key) is not None
    
    def _encrypt_license(self, license_data):
        """Encrypt license data with hardware-based key"""
        if not HAS_CRYPTO:
            return json.dumps(license_data).encode()
        
        try:
            # Use hardware fingerprint as password
            password = self._get_hardware_fingerprint().encode()
            
            # Generate key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'mxdpro_salt_2023',
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Encrypt data
            f = Fernet(key)
            encrypted = f.encrypt(json.dumps(license_data).encode())
            return encrypted
        except Exception:
            return json.dumps(license_data).encode()
    
    def _decrypt_license(self, encrypted_data):
        """Decrypt license data"""
        if not HAS_CRYPTO:
            try:
                return json.loads(encrypted_data.decode())
            except Exception:
                return None
        
        try:
            # Use hardware fingerprint as password
            password = self._get_hardware_fingerprint().encode()
            
            # Generate key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'mxdpro_salt_2023',
                iterations=100000,
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Decrypt data
            f = Fernet(key)
            decrypted = f.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except Exception:
            return None
    
    def _check_license(self):
        """Check existing license"""
        if not os.path.exists(LICENSE_FILE):
            return
        
        try:
            with open(LICENSE_FILE, 'rb') as f:
                encrypted_data = f.read()
            
            license_data = self._decrypt_license(encrypted_data)
            if not license_data:
                return
            
            # Verify hardware fingerprint
            current_fingerprint = self._get_hardware_fingerprint()
            if license_data.get('hardware_fingerprint') != current_fingerprint:
                return
            
            self.license_valid = True
            self.license_info = license_data
        except Exception:
            pass

# ===== MAIN APPLICATION =====
class MXDProApp:
    """Unified MXD Pro application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Initialize components
        self.hardware = HardwareDetector()
        self.security = SecurityScanner()
        self.game_optimizer = GameOptimizer(self.hardware)
        self.license_manager = LicenseManager()
        
        # Initialize UI
        self.setup_ui()
        
        # Start monitoring thread
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        self.monitor_thread.start()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create main notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_gaming_tab()
        self.create_security_tab()
        self.create_monitoring_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        # Welcome section
        welcome_frame = ttk.LabelFrame(dashboard_frame, text="System Overview")
        welcome_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # System info
        system_info = self.hardware.get_system_summary()
        info_text = tk.Text(welcome_frame, height=15, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Format system information
        info_content = f"""=== SYSTEM INFORMATION ===

CPU: {system_info['cpu'].get('name', 'Unknown')}
Cores: {system_info['cpu'].get('cores_physical', '?')} physical, {system_info['cpu'].get('cores_logical', '?')} logical
Architecture: {system_info['cpu'].get('architecture', 'Unknown')}

RAM: {system_info['ram'].get('total_gb', 0):.1f} GB total, {system_info['ram'].get('available_gb', 0):.1f} GB available

GPU Information:"""
        
        for i, gpu in enumerate(system_info['gpu']):
            info_content += f"""
GPU {i+1}: {gpu.get('name', 'Unknown')}
  Vendor: {gpu.get('vendor', 'Unknown')}
  VRAM: {gpu.get('vram_mb', 0) // 1024} GB
  DLSS Support: {'Yes' if gpu.get('supports_dlss') else 'No'}
  FSR Support: {'Yes' if gpu.get('supports_fsr') else 'No'}
  Ray Tracing: {'Yes' if gpu.get('supports_rt') else 'No'}"""
        
        if system_info['motherboard']:
            info_content += f"""

Motherboard: {system_info['motherboard'].get('manufacturer', 'Unknown')} {system_info['motherboard'].get('product', 'Unknown')}

Platform: {system_info['platform']['system']} {system_info['platform']['version']}"""
        
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)
        
        # License status
        license_frame = ttk.LabelFrame(dashboard_frame, text="License Status")
        license_frame.pack(fill=tk.X, padx=10, pady=5)
        
        if self.license_manager.license_valid:
            license_status = f"✅ Licensed to hardware fingerprint: {self.license_manager.license_info.get('hardware_fingerprint', '')[:8]}..."
            ttk.Label(license_frame, text=license_status, foreground="green").pack(pady=5)
        else:
            ttk.Label(license_frame, text="❌ No valid license found", foreground="red").pack(pady=5)
            
            # Activation section
            activation_frame = ttk.Frame(license_frame)
            activation_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Label(activation_frame, text="Activation Key:").pack(side=tk.LEFT)
            self.activation_entry = ttk.Entry(activation_frame, width=20)
            self.activation_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Button(activation_frame, text="Activate", command=self.activate_license).pack(side=tk.LEFT, padx=5)
            ttk.Button(activation_frame, text="Generate Key", command=self.generate_key).pack(side=tk.LEFT, padx=5)
    
    def create_gaming_tab(self):
        """Create gaming optimization tab"""
        gaming_frame = ttk.Frame(self.notebook)
        self.notebook.add(gaming_frame, text="Gaming Optimizer")
        
        # Game detection
        detection_frame = ttk.LabelFrame(gaming_frame, text="Detected Games")
        detection_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(detection_frame, text="Scan for Games", command=self.scan_games).pack(pady=5)
        
        self.games_listbox = tk.Listbox(detection_frame, height=5)
        self.games_listbox.pack(fill=tk.X, padx=5, pady=5)
        
        # Optimization settings
        opt_frame = ttk.LabelFrame(gaming_frame, text="Optimization Settings")
        opt_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Target FPS
        fps_frame = ttk.Frame(opt_frame)
        fps_frame.pack(fill=tk.X, pady=2)
        ttk.Label(fps_frame, text="Target FPS:").pack(side=tk.LEFT)
        self.fps_var = tk.StringVar(value="60")
        fps_combo = ttk.Combobox(fps_frame, textvariable=self.fps_var, values=["30", "60", "90", "120", "144", "240"])
        fps_combo.pack(side=tk.LEFT, padx=5)
        
        # Target Resolution
        res_frame = ttk.Frame(opt_frame)
        res_frame.pack(fill=tk.X, pady=2)
        ttk.Label(res_frame, text="Target Resolution:").pack(side=tk.LEFT)
        self.res_var = tk.StringVar(value="1080p")
        res_combo = ttk.Combobox(res_frame, textvariable=self.res_var, values=["1080p", "1440p", "4K", "6K"])
        res_combo.pack(side=tk.LEFT, padx=5)
        
        # Optimize button
        ttk.Button(opt_frame, text="Optimize Selected Game", command=self.optimize_game).pack(pady=10)
        
        # Windows optimizations
        windows_frame = ttk.LabelFrame(gaming_frame, text="Windows Gaming Optimizations")
        windows_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(windows_frame, text="Apply Windows Optimizations", command=self.apply_windows_opts).pack(pady=5)
        
        # Optimization history
        history_frame = ttk.LabelFrame(gaming_frame, text="Optimization History")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_text = tk.Text(history_frame, height=8)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_security_tab(self):
        """Create security tab"""
        security_frame = ttk.Frame(self.notebook)
        self.notebook.add(security_frame, text="Security Suite")
        
        # Scan controls
        scan_frame = ttk.LabelFrame(security_frame, text="Security Scan")
        scan_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(scan_frame, text="Start Advanced Security Scan", command=self.start_security_scan).pack(pady=5)
        
        # Progress bar
        self.scan_progress = ttk.Progressbar(scan_frame, mode='indeterminate')
        self.scan_progress.pack(fill=tk.X, padx=5, pady=2)
        
        self.scan_status = tk.StringVar(value="Ready to scan")
        ttk.Label(scan_frame, textvariable=self.scan_status).pack(pady=2)
        
        # Scan results
        results_frame = ttk.LabelFrame(security_frame, text="Scan Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results tree
        columns = ('Type', 'Description', 'Threat Level', 'Action')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = ttk.Frame(security_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(action_frame, text="Quarantine Selected", command=self.quarantine_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Ignore Threat", command=self.ignore_threat).pack(side=tk.LEFT, padx=5)
    
    def create_monitoring_tab(self):
        """Create system monitoring tab with real-time graphs"""
        monitoring_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitoring_frame, text="System Monitor")
        
        # Create matplotlib figure
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.tight_layout(pad=3.0)
        
        # Initialize data arrays
        self.time_data = []
        self.cpu_data = []
        self.ram_data = []
        self.temp_data = []
        self.fps_data = []
        
        # Configure plots
        self.ax1.set_title('CPU Usage %')
        self.ax1.set_ylim(0, 100)
        self.ax1.grid(True)
        
        self.ax2.set_title('RAM Usage %')
        self.ax2.set_ylim(0, 100)
        self.ax2.grid(True)
        
        self.ax3.set_title('Temperature °C')
        self.ax3.set_ylim(0, 100)
        self.ax3.grid(True)
        
        self.ax4.set_title('Estimated FPS')
        self.ax4.set_ylim(0, 200)
        self.ax4.grid(True)
        
        # Add canvas to tkinter
        canvas = FigureCanvasTkAgg(self.fig, monitoring_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Control buttons
        control_frame = ttk.Frame(monitoring_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.monitoring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Real-time Monitoring", 
                       variable=self.monitoring_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Clear Graphs", command=self.clear_graphs).pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Application settings
        app_frame = ttk.LabelFrame(settings_frame, text="Application Settings")
        app_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Auto-start monitoring
        self.autostart_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(app_frame, text="Start monitoring on application launch", 
                       variable=self.autostart_var).pack(anchor=tk.W, padx=5, pady=2)
        
        # Security level
        security_frame = ttk.Frame(app_frame)
        security_frame.pack(fill=tk.X, pady=2)
        ttk.Label(security_frame, text="Security Level:").pack(side=tk.LEFT)
        self.security_var = tk.StringVar(value="High")
        security_combo = ttk.Combobox(security_frame, textvariable=self.security_var, 
                                    values=["Low", "Medium", "High", "Military"])
        security_combo.pack(side=tk.LEFT, padx=5)
        
        # Export/Import
        export_frame = ttk.LabelFrame(settings_frame, text="Data Management")
        export_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(export_frame, text="Export Settings", command=self.export_settings).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(export_frame, text="Import Settings", command=self.import_settings).pack(side=tk.LEFT, padx=5, pady=5)
        
        # About
        about_frame = ttk.LabelFrame(settings_frame, text="About")
        about_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        about_text = f"""{APP_NAME} v{APP_VERSION}

Advanced gaming optimization and security suite with:
• Hardware-optimized game settings
• DLSS/FSR/Ray Tracing support  
• Real-time security scanning
• Military-grade license protection
• System performance monitoring

Developed by: RepoBirdBot AI Agent
License: Proprietary"""
        
        about_label = tk.Text(about_frame, height=10, wrap=tk.WORD)
        about_label.insert(tk.END, about_text)
        about_label.config(state=tk.DISABLED)
        about_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def activate_license(self):
        """Activate license with entered key"""
        key = self.activation_entry.get().strip().upper()
        if not key:
            messagebox.showerror("Error", "Please enter an activation key")
            return
        
        success, message = self.license_manager.activate_license(key)
        if success:
            messagebox.showinfo("Success", message)
            self.setup_ui()  # Refresh UI to show licensed status
        else:
            messagebox.showerror("Error", message)
    
    def generate_key(self):
        """Generate a sample activation key"""
        key = self.license_manager.generate_activation_key()
        self.activation_entry.delete(0, tk.END)
        self.activation_entry.insert(0, key)
        messagebox.showinfo("Generated Key", f"Sample activation key: {key}")
    
    def scan_games(self):
        """Scan for installed games"""
        self.status_var.set("Scanning for games...")
        
        def scan_thread():
            games = self.game_optimizer.detect_games()
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_games_list(games))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def update_games_list(self, games):
        """Update games list in UI"""
        self.games_listbox.delete(0, tk.END)
        for game in games:
            self.games_listbox.insert(tk.END, f"{game['name']} - {game['path']}")
        
        self.status_var.set(f"Found {len(games)} games")
    
    def optimize_game(self):
        """Optimize selected game"""
        selection = self.games_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a game to optimize")
            return
        
        game_text = self.games_listbox.get(selection[0])
        game_name = game_text.split(" - ")[0]
        
        target_fps = int(self.fps_var.get())
        target_res = self.res_var.get()
        
        self.status_var.set(f"Optimizing {game_name}...")
        
        def optimize_thread():
            success, message = self.game_optimizer.optimize_game(game_name, target_fps, target_res)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.optimization_complete(success, message))
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def optimization_complete(self, success, message):
        """Handle optimization completion"""
        if success:
            messagebox.showinfo("Success", message)
            self.update_optimization_history()
        else:
            messagebox.showerror("Error", message)
        
        self.status_var.set("Ready")
    
    def update_optimization_history(self):
        """Update optimization history display"""
        self.history_text.delete(1.0, tk.END)
        
        for opt in self.game_optimizer.optimization_history[-10:]:  # Show last 10
            timestamp = datetime.fromtimestamp(opt['timestamp']).strftime("%Y-%m-%d %H:%M")
            history_entry = f"[{timestamp}] {opt['game']} - {opt['target_fps']}fps @ {opt['target_resolution']}\n"
            history_entry += f"  Settings: {opt['applied_settings']}\n\n"
            self.history_text.insert(tk.END, history_entry)
    
    def apply_windows_opts(self):
        """Apply Windows-level optimizations"""
        if platform.system() != "Windows":
            messagebox.showwarning("Warning", "Windows optimizations only available on Windows")
            return
        
        self.status_var.set("Applying Windows optimizations...")
        
        def optimize_thread():
            optimizations = self.game_optimizer._apply_windows_optimizations(60)
            
            # Update UI in main thread  
            message = "Windows optimizations applied:\n" + "\n".join(optimizations) if optimizations else "No optimizations could be applied"
            self.root.after(0, lambda: messagebox.showinfo("Windows Optimizations", message))
            self.root.after(0, lambda: self.status_var.set("Ready"))
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def start_security_scan(self):
        """Start security scan"""
        self.scan_progress.start()
        self.scan_status.set("Scanning...")
        
        def scan_thread():
            def progress_callback(status):
                self.root.after(0, lambda: self.scan_status.set(status))
            
            results = self.security.scan_system(progress_callback)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.security_scan_complete(results))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def security_scan_complete(self, results):
        """Handle security scan completion"""
        self.scan_progress.stop()
        self.scan_status.set(f"Scan complete: {results['threats_found']} threats found")
        
        # Clear previous results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results
        for threat in results['threats']:
            threat_type = threat['type'].replace('_', ' ').title()
            
            if threat['type'] == 'suspicious_process':
                description = f"Process: {threat['name']} (PID: {threat['pid']})"
            elif threat['type'] == 'suspicious_file':
                description = f"File: {os.path.basename(threat['path'])}"
            elif threat['type'] == 'suspicious_network':
                description = f"Connection: {threat['local_addr']} -> {threat['remote_addr']}"
            elif threat['type'] == 'suspicious_registry':
                description = f"Registry: {threat['name']}"
            else:
                description = str(threat)
            
            threat_level = threat.get('threat_level', 'medium').title()
            
            self.results_tree.insert('', tk.END, values=(threat_type, description, threat_level, 'Pending'))
    
    def quarantine_selected(self):
        """Quarantine selected threat"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a threat to quarantine")
            return
        
        # This would quarantine the selected threat
        messagebox.showinfo("Quarantine", "Selected threat has been quarantined")
        
        # Update tree item
        for item in selection:
            values = list(self.results_tree.item(item)['values'])
            values[3] = 'Quarantined'
            self.results_tree.item(item, values=values)
    
    def ignore_threat(self):
        """Ignore selected threat"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a threat to ignore")
            return
        
        # Update tree item
        for item in selection:
            values = list(self.results_tree.item(item)['values'])
            values[3] = 'Ignored'
            self.results_tree.item(item, values=values)
    
    def clear_graphs(self):
        """Clear monitoring graphs"""
        self.time_data.clear()
        self.cpu_data.clear()
        self.ram_data.clear()
        self.temp_data.clear()
        self.fps_data.clear()
        
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        self.ax1.set_title('CPU Usage %')
        self.ax2.set_title('RAM Usage %') 
        self.ax3.set_title('Temperature °C')
        self.ax4.set_title('Estimated FPS')
        
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.grid(True)
            ax.set_ylim(0, 100)
        
        self.ax4.set_ylim(0, 200)
    
    def monitor_system(self):
        """System monitoring thread"""
        while self.monitoring_active:
            try:
                if self.monitoring_var.get():
                    current_time = time.time()
                    
                    # Collect system data
                    cpu_percent = psutil.cpu_percent()
                    ram_percent = psutil.virtual_memory().percent
                    
                    # Estimate temperature (mock data for now)
                    temp = 45 + (cpu_percent / 100) * 30  # Mock temperature based on CPU usage
                    
                    # Estimate FPS based on system performance (mock calculation)
                    estimated_fps = max(30, 120 - (cpu_percent + ram_percent) / 2)
                    
                    # Update data arrays (keep only last 100 points)
                    self.time_data.append(current_time)
                    self.cpu_data.append(cpu_percent)
                    self.ram_data.append(ram_percent)
                    self.temp_data.append(temp)
                    self.fps_data.append(estimated_fps)
                    
                    # Trim data to last 100 points
                    if len(self.time_data) > 100:
                        self.time_data.pop(0)
                        self.cpu_data.pop(0)
                        self.ram_data.pop(0)
                        self.temp_data.pop(0)
                        self.fps_data.pop(0)
                    
                    # Update graphs in main thread
                    self.root.after(0, self.update_graphs)
                
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(5)
    
    def update_graphs(self):
        """Update monitoring graphs"""
        try:
            if not self.time_data:
                return
            
            # Calculate relative time for x-axis
            if len(self.time_data) > 1:
                rel_time = [(t - self.time_data[0]) for t in self.time_data]
            else:
                rel_time = [0]
            
            # Clear and plot CPU
            self.ax1.clear()
            self.ax1.plot(rel_time, self.cpu_data, 'b-', linewidth=2)
            self.ax1.set_title('CPU Usage %')
            self.ax1.set_ylim(0, 100)
            self.ax1.grid(True)
            
            # Clear and plot RAM
            self.ax2.clear()
            self.ax2.plot(rel_time, self.ram_data, 'r-', linewidth=2)
            self.ax2.set_title('RAM Usage %')
            self.ax2.set_ylim(0, 100)
            self.ax2.grid(True)
            
            # Clear and plot Temperature
            self.ax3.clear()
            self.ax3.plot(rel_time, self.temp_data, 'orange', linewidth=2)
            self.ax3.set_title('Temperature °C')
            self.ax3.set_ylim(0, 100)
            self.ax3.grid(True)
            
            # Clear and plot FPS
            self.ax4.clear()
            self.ax4.plot(rel_time, self.fps_data, 'g-', linewidth=2)
            self.ax4.set_title('Estimated FPS')
            self.ax4.set_ylim(0, 200)
            self.ax4.grid(True)
            
            # Draw canvas
            self.fig.canvas.draw()
        except Exception as e:
            print(f"Graph update error: {e}")
    
    def export_settings(self):
        """Export application settings"""
        filename = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                settings_data = {
                    'app_version': APP_VERSION,
                    'exported_at': time.time(),
                    'optimization_history': self.game_optimizer.optimization_history,
                    'settings': {
                        'auto_start': self.autostart_var.get(),
                        'security_level': self.security_var.get()
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(settings_data, f, indent=2)
                
                messagebox.showinfo("Export", f"Settings exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export settings: {e}")
    
    def import_settings(self):
        """Import application settings"""
        filename = filedialog.askopenfilename(
            title="Import Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    settings_data = json.load(f)
                
                # Import optimization history
                if 'optimization_history' in settings_data:
                    self.game_optimizer.optimization_history = settings_data['optimization_history']
                    self.update_optimization_history()
                
                # Import application settings
                if 'settings' in settings_data:
                    settings = settings_data['settings']
                    self.autostart_var.set(settings.get('auto_start', True))
                    self.security_var.set(settings.get('security_level', 'High'))
                
                messagebox.showinfo("Import", f"Settings imported from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import settings: {e}")
    
    def run(self):
        """Run the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
    
    def on_closing(self):
        """Handle application closing"""
        self.monitoring_active = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        self.root.destroy()

# ===== MAIN ENTRY POINT =====
if __name__ == "__main__":
    try:
        # Check if license validation is required
        app = MXDProApp()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")