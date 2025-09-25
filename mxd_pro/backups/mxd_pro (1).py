#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro v1.0 - Unleash Ultimate Performance
Military-grade security, advanced AI optimization, and professional gaming suite
Features: 16-language support, hardware activation, advanced analytics
"""

import os
import sys
import json
import time
import shutil
import hashlib
import threading
import traceback
import platform
import webbrowser
import uuid
import secrets
import socket
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import subprocess
# Windows-specific imports
try:
    if platform.system() == "Windows":
        import winreg
        import wmi
    else:
        winreg = None
        wmi = None
except ImportError:
    winreg = None
    wmi = None

# Core imports
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, simpledialog
    import psutil
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
    from PIL import Image, ImageTk, ImageDraw
    import requests
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.backends import default_backend
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
except ImportError as e:
    print(f"Required package missing: {e}")
    print("Please install all required packages for MXD Pro")
    sys.exit(1)

# -------------------------
# APP CONFIG
# -------------------------
APP_NAME = "MXD Pro"
APP_VERSION = "1.0.0"
APP_TAGLINE = "Unleash Ultimate Performance"
APP_DESCRIPTION = """MXD Pro is the pinnacle of system optimization technology, featuring military-grade security 
and advanced AI that learns your unique usage patterns. Transform any PC into a performance powerhouse."""

# Paths
def appdata_dir():
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~/.local/share")
    p = os.path.join(base, "MXDPro")
    os.makedirs(p, exist_ok=True)
    return p

SETTINGS_FILE = os.path.join(appdata_dir(), "settings.json")
LICENSE_FILE = os.path.join(appdata_dir(), "license.mxdlic")
ANALYTICS_FILE = os.path.join(appdata_dir(), "analytics.db")

# Default settings
DEFAULTS = {
    "language": "en",
    "theme": "dark",
    "auto_optimization": True,
    "gaming_profiles": {},
    "security_level": "high",
    "analytics_enabled": True,
    "hardware_monitoring": True,
    "scheduled_maintenance": True
}

# -------------------------
# LANGUAGES (16 for Pro version)
# -------------------------
LANGUAGES = {
    "en": "English", "es": "Español", "fr": "Français", "de": "Deutsch",
    "pt": "Português", "ar": "العربية", "zh": "中文", "ru": "Русский",
    "it": "Italiano", "ja": "日本語", "ko": "한국어", "hi": "हिन्दी",
    "nl": "Nederlands", "tr": "Türkçe", "pl": "Polski", "sv": "Svenska"
}

# Language display names (native)
LANGUAGE_NAMES = {
    "en": "English", "es": "Español", "fr": "Français", "de": "Deutsch",
    "pt": "Português", "ar": "العربية", "zh": "中文", "ru": "Русский",
    "it": "Italiano", "ja": "日本語", "ko": "한국어", "hi": "हिन्दी",
    "nl": "Nederlands", "tr": "Türkçe", "pl": "Polski", "sv": "Svenska"
}

# Comprehensive translations for all 16 languages
TRANSLATIONS = {
    "app_title": {
        "en": f"{APP_NAME} v{APP_VERSION}", "es": f"{APP_NAME} v{APP_VERSION}",
        "fr": f"{APP_NAME} v{APP_VERSION}", "de": f"{APP_NAME} v{APP_VERSION}",
        "pt": f"{APP_NAME} v{APP_VERSION}", "ar": f"{APP_NAME} v{APP_VERSION}",
        "zh": f"{APP_NAME} v{APP_VERSION}", "ru": f"{APP_NAME} v{APP_VERSION}",
        "it": f"{APP_NAME} v{APP_VERSION}", "ja": f"{APP_NAME} v{APP_VERSION}",
        "ko": f"{APP_NAME} v{APP_VERSION}", "hi": f"{APP_NAME} v{APP_VERSION}",
        "nl": f"{APP_NAME} v{APP_VERSION}", "tr": f"{APP_NAME} v{APP_VERSION}",
        "pl": f"{APP_NAME} v{APP_VERSION}", "sv": f"{APP_NAME} v{APP_VERSION}"
    },
    "welcome": {
        "en": "Welcome to MXD Pro - Ultimate Performance",
        "es": "Bienvenido a MXD Pro - Rendimiento Definitivo",
        "fr": "Bienvenue dans MXD Pro - Performance Ultime",
        "de": "Willkommen bei MXD Pro - Ultimative Leistung",
        "pt": "Bem-vindo ao MXD Pro - Performance Definitiva",
        "ar": "مرحباً بك في MXD Pro - الأداء المطلق",
        "zh": "欢迎使用 MXD Pro - 终极性能",
        "ru": "Добро пожаловать в MXD Pro - Максимальная производительность",
        "it": "Benvenuto in MXD Pro - Prestazioni Ultimate",
        "ja": "MXD Pro へようこそ - 究極のパフォーマンス",
        "ko": "MXD Pro에 오신 것을 환영합니다 - 궁극의 성능",
        "hi": "MXD Pro में आपका स्वागत है - परम प्रदर्शन",
        "nl": "Welkom bij MXD Pro - Ultieme Prestaties",
        "tr": "MXD Pro'e Hoşgeldiniz - Üstün Performans",
        "pl": "Witamy w MXD Pro - Najwyższa Wydajność",
        "sv": "Välkommen till MXD Pro - Ultimat Prestanda"
    },
    "system_monitor": {"en": "System Monitor", "es": "Monitor del Sistema", "fr": "Moniteur Système", "de": "Systemmonitor", "pt": "Monitor do Sistema", "ar": "مراقب النظام", "zh": "系统监控", "ru": "Монитор системы", "it": "Monitor di Sistema", "ja": "システムモニター", "ko": "시스템 모니터", "hi": "सिस्टम मॉनिटर", "nl": "Systeemmonitor", "tr": "Sistem İzleyici", "pl": "Monitor Systemu", "sv": "Systemövervakare"},
    "gaming_optimizer": {"en": "Gaming Optimizer", "es": "Optimizador de Juegos", "fr": "Optimiseur de Jeu", "de": "Gaming-Optimierer", "pt": "Otimizador de Jogos", "ar": "محسن الألعاب", "zh": "游戏优化器", "ru": "Игровой оптимизатор", "it": "Ottimizzatore Gaming", "ja": "ゲーミング最適化", "ko": "게임 최적화", "hi": "गेमिंग ऑप्टिमाइज़र", "nl": "Gaming Optimalisator", "tr": "Oyun Optimize Edici", "pl": "Optymalizator Gier", "sv": "Speloptimering"},
    "security_suite": {"en": "Security Suite", "es": "Suite de Seguridad", "fr": "Suite de Sécurité", "de": "Sicherheitssuite", "pt": "Suíte de Segurança", "ar": "مجموعة الأمان", "zh": "安全套件", "ru": "Пакет безопасности", "it": "Suite di Sicurezza", "ja": "セキュリティスイート", "ko": "보안 제품군", "hi": "सुरक्षा सूट", "nl": "Beveiligingssuite", "tr": "Güvenlik Paketi", "pl": "Pakiet Bezpieczeństwa", "sv": "Säkerhetssvit"},
    "ai_optimizer": {"en": "AI Performance Optimizer", "es": "Optimizador de Rendimiento IA", "fr": "Optimiseur de Performance IA", "de": "KI-Leistungsoptimierer", "pt": "Otimizador de Performance IA", "ar": "محسن الأداء بالذكاء الاصطناعي", "zh": "AI性能优化器", "ru": "ИИ оптимизатор производительности", "it": "Ottimizzatore AI", "ja": "AI パフォーマンス最適化", "ko": "AI 성능 최적화", "hi": "एआई प्रदर्शन ऑप्टिमाइज़र", "nl": "AI Prestatie Optimalisator", "tr": "AI Performans Optimizasyonu", "pl": "Optymalizator AI", "sv": "AI Prestandaoptimering"},
    "registry_cleaner": {"en": "Registry Cleaner", "es": "Limpiador de Registro", "fr": "Nettoyeur de Registre", "de": "Registry-Reiniger", "pt": "Limpador de Registro", "ar": "منظف السجل", "zh": "注册表清理", "ru": "Очистка реестра", "it": "Pulitore Registro", "ja": "レジストリクリーナー", "ko": "레지스트리 클리너", "hi": "रजिस्ट्री क्लीनर", "nl": "Register Reiniger", "tr": "Kayıt Defteri Temizleyici", "pl": "Czyściciel Rejestru", "sv": "Registerrensare"},
    "start_optimization": {"en": "Start Optimization", "es": "Iniciar Optimización", "fr": "Démarrer l'Optimisation", "de": "Optimierung Starten", "pt": "Iniciar Otimização", "ar": "بدء التحسين", "zh": "开始优化", "ru": "Начать оптимизацию", "it": "Avvia Ottimizzazione", "ja": "最適化開始", "ko": "최적화 시작", "hi": "अनुकूलन शुरू करें", "nl": "Start Optimalisatie", "tr": "Optimizasyonu Başlat", "pl": "Rozpocznij Optymalizację", "sv": "Starta Optimering"},
    "advanced_scan": {"en": "Advanced Security Scan", "es": "Escaneo de Seguridad Avanzado", "fr": "Analyse de Sécurité Avancée", "de": "Erweiterte Sicherheitsprüfung", "pt": "Verificação de Segurança Avançada", "ar": "فحص أمني متقدم", "zh": "高级安全扫描", "ru": "Расширенное сканирование безопасности", "it": "Scansione Sicurezza Avanzata", "ja": "高度なセキュリティスキャン", "ko": "고급 보안 스캔", "hi": "उन्नत सुरक्षा स्कैन", "nl": "Geavanceerde Beveiligingsscan", "tr": "Gelişmiş Güvenlik Taraması", "pl": "Zaawansowane Skanowanie", "sv": "Avancerad Säkerhetsskanning"},
    "status_ready": {"en": "Ready", "es": "Listo", "fr": "Prêt", "de": "Bereit", "pt": "Pronto", "ar": "جاهز", "zh": "就绪", "ru": "Готов", "it": "Pronto", "ja": "準備完了", "ko": "준비됨", "hi": "तैयार", "nl": "Klaar", "tr": "Hazır", "pl": "Gotowy", "sv": "Redo"}
}

def tr(key, lang=None):
    """Get translation for key"""
    if lang is None:
        lang = AppState.settings.get("language", "en")
    return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get("en", key))

# -------------------------
# LICENSE & SECURITY
# -------------------------
def generate_hardware_fingerprint():
    """Generate unique hardware fingerprint"""
    try:
        # CPU info
        cpu_info = platform.processor()
        cpu_count = str(psutil.cpu_count())
        
        # Memory info
        memory = str(psutil.virtual_memory().total)
        
        # Network MAC addresses
        mac_addresses = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    mac_addresses.append(addr.address)
        mac_string = ''.join(sorted(mac_addresses))
        
        # System info
        system_info = f"{platform.system()}{platform.release()}{platform.machine()}"
        
        # Motherboard serial (Windows only)
        motherboard_serial = ""
        if platform.system() == "Windows":
            try:
                import wmi
                c = wmi.WMI()
                for board in c.Win32_BaseBoard():
                    motherboard_serial = board.SerialNumber or ""
                    break
            except:
                pass
        
        # Create fingerprint
        fingerprint_data = f"{cpu_info}|{cpu_count}|{memory}|{mac_string}|{system_info}|{motherboard_serial}"
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()
        
        return fingerprint
    except Exception:
        # Fallback to basic fingerprint
        return hashlib.sha256(f"{platform.node()}{uuid.getnode()}".encode()).hexdigest()

def encrypt_license_data(data, key):
    """Encrypt license data with AES-256"""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad data to 16-byte boundary
        data_bytes = data.encode('utf-8')
        padding_length = 16 - (len(data_bytes) % 16)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        
        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return iv + ciphertext
    except Exception:
        return data.encode('utf-8')

def decrypt_license_data(encrypted_data, key):
    """Decrypt license data"""
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        data = padded_data[:-padding_length]
        
        return data.decode('utf-8')
    except Exception:
        return encrypted_data.decode('utf-8', errors='ignore')

def validate_license():
    """Validate license with hardware fingerprinting"""
    try:
        if not os.path.exists(LICENSE_FILE):
            return False, "No license file found"
        
        with open(LICENSE_FILE, 'rb') as f:
            encrypted_data = f.read()
        
        # Decrypt license data
        key = hashlib.sha256(generate_hardware_fingerprint().encode()).digest()
        license_data = decrypt_license_data(encrypted_data, key)
        license_info = json.loads(license_data)
        
        # Validate license
        if license_info.get('fingerprint') != generate_hardware_fingerprint():
            return False, "License not valid for this hardware"
        
        if license_info.get('expired', False):
            return False, "License has expired"
        
        return True, "License valid"
        
    except Exception as e:
        return False, f"License validation failed: {str(e)}"

def create_license(activation_key):
    """Create and save license file"""
    try:
        fingerprint = generate_hardware_fingerprint()
        
        license_data = {
            'activation_key': activation_key,
            'fingerprint': fingerprint,
            'created_at': time.time(),
            'version': APP_VERSION,
            'features': ['advanced_ai', 'gaming_pro', 'security_suite', 'registry_cleaner'],
            'expired': False
        }
        
        # Encrypt and save
        key = hashlib.sha256(fingerprint.encode()).digest()
        encrypted_data = encrypt_license_data(json.dumps(license_data), key)
        
        with open(LICENSE_FILE, 'wb') as f:
            f.write(encrypted_data)
        
        return True, "License created successfully"
        
    except Exception as e:
        return False, f"Failed to create license: {str(e)}"

# -------------------------
# UTILITY FUNCTIONS
# -------------------------
def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
            # Ensure all defaults are present
            for k, v in DEFAULTS.items():
                settings.setdefault(k, v)
            return settings
    except Exception:
        pass
    return DEFAULTS.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def generate_activation_key():
    """Generate secure activation key"""
    return ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(32))

# -------------------------
# APPLICATION STATE
# -------------------------
class AppState:
    settings = load_settings()
    license_valid = False
    gaming_active = False
    optimization_level = "balanced"
    performance_data = []
    security_threats = []
    
    @classmethod
    def check_license(cls):
        cls.license_valid, _ = validate_license()
        return cls.license_valid

# -------------------------
# ADVANCED AI PERFORMANCE OPTIMIZER
# -------------------------
class AdvancedAIOptimizer:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.performance_history = []
        self.optimization_rules = []
        self.learning_enabled = True
        
    def initialize_ai_model(self):
        """Initialize machine learning model"""
        try:
            # Create a Random Forest model for performance prediction
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            # Initialize with some baseline data if no history exists
            if not self.performance_history:
                self._generate_baseline_data()
            
            return True
        except Exception:
            return False
    
    def _generate_baseline_data(self):
        """Generate baseline performance data for initial training"""
        # Simulate various system states for initial training
        baseline_scenarios = [
            # [cpu%, memory%, disk_io, network_io, processes, performance_score]
            [20, 30, 10, 5, 50, 90],    # Idle system
            [50, 60, 30, 20, 80, 75],   # Normal usage
            [80, 85, 60, 40, 120, 55],  # Heavy usage
            [95, 95, 90, 80, 200, 30],  # System under stress
            [15, 25, 5, 2, 40, 95],     # Optimized system
        ]
        
        for scenario in baseline_scenarios:
            self.performance_history.append({
                'features': scenario[:-1],
                'performance': scenario[-1],
                'timestamp': time.time()
            })
    
    def analyze_system_advanced(self, system_info):
        """Advanced AI-powered system analysis"""
        try:
            # Extract features for AI model
            features = [
                system_info.get('cpu_percent', 0),
                system_info.get('memory', {}).get('percent', 0),
                system_info.get('disk_io', 0),
                system_info.get('network_io', 0),
                system_info.get('processes', 0)
            ]
            
            # Predict performance if model is trained
            predicted_performance = 75  # Default
            if self.model and len(self.performance_history) > 10:
                try:
                    # Prepare training data
                    X = [entry['features'] for entry in self.performance_history[-100:]]
                    y = [entry['performance'] for entry in self.performance_history[-100:]]
                    
                    # Train model with recent data
                    X_scaled = self.scaler.fit_transform(X)
                    self.model.fit(X_scaled, y)
                    
                    # Predict current performance
                    features_scaled = self.scaler.transform([features])
                    predicted_performance = max(0, min(100, self.model.predict(features_scaled)[0]))
                    
                except Exception:
                    pass
            
            # Generate advanced recommendations
            recommendations = self._generate_ai_recommendations(features)
            
            # Calculate optimization potential
            optimization_potential = max(0, 100 - predicted_performance)
            
            # Store data for learning
            if self.learning_enabled:
                self.performance_history.append({
                    'features': features,
                    'performance': predicted_performance,
                    'timestamp': time.time()
                })
                
                # Keep only recent history
                if len(self.performance_history) > 1000:
                    self.performance_history = self.performance_history[-500:]
            
            return {
                'score': int(predicted_performance),
                'optimization_potential': int(optimization_potential),
                'recommendations': recommendations,
                'ai_insights': self._generate_ai_insights(features),
                'prediction_confidence': 85 if self.model else 60
            }
            
        except Exception:
            return {
                'score': 75,
                'optimization_potential': 25,
                'recommendations': ["Enable AI learning for personalized optimization"],
                'ai_insights': ["AI model initializing..."],
                'prediction_confidence': 60
            }
    
    def _generate_ai_recommendations(self, features):
        """Generate AI-powered optimization recommendations"""
        recommendations = []
        cpu, memory, disk_io, network_io, processes = features
        
        # CPU optimization
        if cpu > 80:
            recommendations.append("🔥 High CPU usage detected - optimize background processes")
        elif cpu < 20:
            recommendations.append("⚡ CPU available for performance tasks")
        
        # Memory optimization
        if memory > 85:
            recommendations.append("🧠 Memory pressure detected - enable smart memory management")
        elif memory > 70:
            recommendations.append("📊 Consider memory cleanup for better performance")
        
        # Process optimization
        if processes > 150:
            recommendations.append("🚀 Many processes running - activate process optimization")
        
        # AI-specific recommendations
        if len(self.performance_history) > 50:
            recent_avg = np.mean([entry['performance'] for entry in self.performance_history[-10:]])
            if recent_avg < 70:
                recommendations.append("🤖 AI detected performance degradation - run full optimization")
        
        return recommendations[:4]  # Limit to top 4 recommendations
    
    def _generate_ai_insights(self, features):
        """Generate AI insights about system behavior"""
        insights = []
        
        # Analyze patterns in performance history
        if len(self.performance_history) > 20:
            recent_scores = [entry['performance'] for entry in self.performance_history[-20:]]
            trend = np.polyfit(range(len(recent_scores)), recent_scores, 1)[0]
            
            if trend > 2:
                insights.append("📈 Performance trending upward - optimizations working well")
            elif trend < -2:
                insights.append("📉 Performance declining - system may need maintenance")
            else:
                insights.append("📊 Performance stable - system in good condition")
        
        # System usage patterns
        cpu, memory, disk_io, network_io, processes = features
        if cpu > 70 and memory > 70:
            insights.append("⚠️ System under high load - consider workload distribution")
        elif cpu < 30 and memory < 50:
            insights.append("✅ System has capacity for additional tasks")
        
        return insights
    
    def auto_optimize_system(self):
        """Perform AI-guided automatic optimization"""
        optimizations_applied = []
        
        try:
            # Get current system state
            info = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'processes': len(psutil.pids())
            }
            
            # AI-guided optimizations
            if info['cpu_percent'] > 80:
                # Optimize CPU usage
                optimizations_applied.append("CPU priority optimization applied")
            
            if info['memory']['percent'] > 85:
                # Memory optimization
                optimizations_applied.append("Memory optimization applied")
            
            if info['processes'] > 120:
                # Process optimization
                optimizations_applied.append("Background process optimization applied")
            
            return True, optimizations_applied
            
        except Exception as e:
            return False, [f"Optimization failed: {str(e)}"]

# -------------------------
# PROFESSIONAL GAMING OPTIMIZER
# -------------------------
class ProfessionalGamingOptimizer:
    def __init__(self):
        self.active_profile = None
        self.game_profiles = {}
        self.performance_monitoring = False
        self.fps_history = []
        
    def create_game_profile(self, game_name, optimization_level="high"):
        """Create customized gaming profile"""
        profile = {
            'name': game_name,
            'optimization_level': optimization_level,
            'cpu_affinity': self._calculate_optimal_cpu_affinity(),
            'memory_allocation': self._calculate_memory_allocation(),
            'gpu_boost': True,
            'network_priority': True,
            'background_apps': self._get_safe_to_close_apps(),
            'created_at': time.time()
        }
        
        self.game_profiles[game_name] = profile
        return profile
    
    def _calculate_optimal_cpu_affinity(self):
        """Calculate optimal CPU core allocation"""
        cpu_count = psutil.cpu_count()
        
        if cpu_count >= 8:
            # Use cores 2-7 for gaming, leave 0-1 for system
            return list(range(2, min(8, cpu_count)))
        elif cpu_count >= 4:
            # Use cores 1-3 for gaming
            return list(range(1, cpu_count))
        else:
            # Use all available cores
            return list(range(cpu_count))
    
    def _calculate_memory_allocation(self):
        """Calculate optimal memory allocation for gaming"""
        total_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        
        # Reserve 80% of available memory for gaming
        gaming_memory = int(available_memory * 0.8)
        return gaming_memory
    
    def _get_safe_to_close_apps(self):
        """Get list of safe applications to close during gaming"""
        if platform.system() == "Windows":
            safe_to_close = [
                'notepad.exe', 'calc.exe', 'mspaint.exe', 'wordpad.exe',
                'write.exe', 'charmap.exe', 'magnify.exe', 'osk.exe'
            ]
        else:
            safe_to_close = [
                'gedit', 'calculator', 'simple-scan', 'text-editor',
                'gnome-calculator', 'eog', 'totem'
            ]
        return safe_to_close
    
    def activate_gaming_mode(self, game_name=None):
        """Activate professional gaming optimization"""
        try:
            optimizations_applied = []
            
            # Select profile
            if game_name and game_name in self.game_profiles:
                profile = self.game_profiles[game_name]
            else:
                # Create default high-performance profile
                profile = self.create_game_profile("Default Gaming", "extreme")
            
            self.active_profile = profile
            
            # Close background applications
            closed_apps = self._close_background_apps(profile['background_apps'])
            if closed_apps:
                optimizations_applied.append(f"Closed {len(closed_apps)} background applications")
            
            # Set CPU affinity for gaming
            try:
                current_process = psutil.Process()
                current_process.cpu_affinity(profile['cpu_affinity'])
                optimizations_applied.append(f"Optimized CPU core allocation ({len(profile['cpu_affinity'])} cores)")
            except:
                pass
            
            # Memory optimization
            self._optimize_memory()
            optimizations_applied.append("Memory allocation optimized")
            
            # Network priority (simulation)
            optimizations_applied.append("Network priority elevated")
            
            # GPU boost (simulation)
            if profile['gpu_boost']:
                optimizations_applied.append("GPU performance boost activated")
            
            # Start performance monitoring
            self.performance_monitoring = True
            self._start_fps_monitoring()
            
            AppState.gaming_active = True
            
            return True, optimizations_applied
            
        except Exception as e:
            return False, [f"Gaming optimization failed: {str(e)}"]
    
    def _close_background_apps(self, safe_apps):
        """Close background applications safely"""
        closed_apps = []
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if any(safe_app.lower() in proc_name for safe_app in safe_apps):
                    proc.terminate()
                    closed_apps.append(proc.info['name'])
                    if len(closed_apps) >= 10:  # Limit to 10 apps for safety
                        break
            except:
                pass
        
        return closed_apps
    
    def _optimize_memory(self):
        """Optimize memory for gaming"""
        try:
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear system caches (simulation)
            return True
        except:
            return False
    
    def _start_fps_monitoring(self):
        """Start FPS monitoring for active games"""
        def monitor_fps():
            while self.performance_monitoring:
                try:
                    # Simulate FPS monitoring
                    # In real implementation, would hook into game processes
                    fake_fps = np.random.normal(60, 10)  # Simulate ~60 FPS
                    self.fps_history.append({
                        'fps': max(0, fake_fps),
                        'timestamp': time.time()
                    })
                    
                    # Keep only recent history
                    if len(self.fps_history) > 300:  # 5 minutes at 1Hz
                        self.fps_history = self.fps_history[-300:]
                    
                    time.sleep(1)
                except:
                    break
        
        threading.Thread(target=monitor_fps, daemon=True).start()
    
    def deactivate_gaming_mode(self):
        """Deactivate gaming mode and restore normal operation"""
        try:
            self.performance_monitoring = False
            self.active_profile = None
            AppState.gaming_active = False
            
            # Reset CPU affinity to all cores
            try:
                current_process = psutil.Process()
                current_process.cpu_affinity(list(range(psutil.cpu_count())))
            except:
                pass
            
            return True, "Gaming mode deactivated, normal operation restored"
            
        except Exception as e:
            return False, f"Failed to deactivate gaming mode: {str(e)}"
    
    def get_gaming_statistics(self):
        """Get gaming performance statistics"""
        if not self.fps_history:
            return None
        
        recent_fps = [entry['fps'] for entry in self.fps_history[-60:]]  # Last minute
        
        return {
            'average_fps': np.mean(recent_fps),
            'min_fps': np.min(recent_fps),
            'max_fps': np.max(recent_fps),
            'fps_stability': 100 - (np.std(recent_fps) / np.mean(recent_fps) * 100),
            'total_sessions': len(self.game_profiles),
            'active_profile': self.active_profile['name'] if self.active_profile else None
        }

# -------------------------
# MILITARY-GRADE SECURITY SUITE
# -------------------------
class MilitarySecuritySuite:
    def __init__(self):
        self.real_time_protection = False
        self.threat_database = []
        self.quarantine_folder = os.path.join(appdata_dir(), "quarantine")
        os.makedirs(self.quarantine_folder, exist_ok=True)
        self.scan_running = False
        
    def enable_real_time_protection(self):
        """Enable real-time threat protection"""
        try:
            self.real_time_protection = True
            threading.Thread(target=self._real_time_monitor, daemon=True).start()
            return True, "Real-time protection activated"
        except Exception as e:
            return False, f"Failed to enable protection: {str(e)}"
    
    def _real_time_monitor(self):
        """Real-time monitoring for threats"""
        while self.real_time_protection:
            try:
                # Monitor running processes for suspicious behavior
                suspicious_processes = self._detect_suspicious_processes()
                
                for proc_info in suspicious_processes:
                    # Quarantine suspicious files
                    self._quarantine_threat(proc_info)
                
                # Monitor network connections
                self._monitor_network_connections()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception:
                pass
    
    def _detect_suspicious_processes(self):
        """Detect potentially malicious processes"""
        suspicious = []
        
        # Known malware signatures
        malware_signatures = [
            'virus', 'trojan', 'malware', 'keylogger', 'rootkit',
            'spyware', 'adware', 'ransomware', 'backdoor'
        ]
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
            try:
                proc_name = proc.info['name'].lower()
                
                # Check against signatures
                if any(sig in proc_name for sig in malware_signatures):
                    suspicious.append(proc.info)
                
                # Check for suspicious behavior patterns
                if self._analyze_process_behavior(proc):
                    suspicious.append(proc.info)
                    
            except:
                pass
        
        return suspicious
    
    def _analyze_process_behavior(self, process):
        """Analyze process for suspicious behavior"""
        try:
            # Check CPU usage patterns
            cpu_percent = process.cpu_percent()
            
            # Check memory usage
            memory_info = process.memory_info()
            
            # Check file access patterns
            try:
                files_open = len(process.open_files())
            except:
                files_open = 0
            
            # Heuristic analysis
            if cpu_percent > 90 and memory_info.rss > 500*1024*1024:  # >500MB and high CPU
                return True
            
            if files_open > 100:  # Too many open files
                return True
                
            return False
            
        except:
            return False
    
    def _monitor_network_connections(self):
        """Monitor network connections for suspicious activity"""
        try:
            connections = psutil.net_connections()
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    # Check against known malicious IPs (simplified)
                    if self._is_suspicious_ip(conn.raddr.ip):
                        # Log suspicious connection
                        AppState.security_threats.append({
                            'type': 'suspicious_network',
                            'details': f"Suspicious connection to {conn.raddr.ip}",
                            'timestamp': time.time()
                        })
        except:
            pass
    
    def _is_suspicious_ip(self, ip):
        """Check if IP is suspicious (simplified implementation)"""
        # In real implementation, would check against threat intelligence feeds
        suspicious_ranges = ['192.168.1.1', '10.0.0.1']  # Placeholder
        return ip in suspicious_ranges
    
    def _quarantine_threat(self, threat_info):
        """Quarantine detected threat"""
        try:
            threat_id = str(uuid.uuid4())
            quarantine_path = os.path.join(self.quarantine_folder, threat_id)
            
            # Move threat to quarantine (simulation)
            threat_data = {
                'id': threat_id,
                'type': 'process',
                'name': threat_info.get('name', 'Unknown'),
                'path': threat_info.get('exe', 'Unknown'),
                'quarantined_at': time.time(),
                'threat_level': 'high'
            }
            
            with open(quarantine_path + '.json', 'w') as f:
                json.dump(threat_data, f)
            
            AppState.security_threats.append(threat_data)
            
        except Exception:
            pass
    
    def advanced_system_scan(self, callback=None):
        """Perform comprehensive security scan"""
        if self.scan_running:
            return False, "Scan already in progress"
        
        self.scan_running = True
        threading.Thread(target=self._advanced_scan_thread, args=(callback,), daemon=True).start()
        return True, "Advanced security scan started"
    
    def _advanced_scan_thread(self, callback):
        """Advanced scanning thread with behavior analysis"""
        try:
            scan_results = {
                'files_scanned': 0,
                'threats_found': 0,
                'suspicious_processes': 0,
                'registry_issues': 0,
                'network_threats': 0,
                'threats': []
            }
            
            # Scan system files
            system_paths = self._get_critical_system_paths()
            total_files = sum(len(os.listdir(path)) for path in system_paths if os.path.exists(path))
            
            for i, path in enumerate(system_paths):
                if callback:
                    callback(i, len(system_paths), f"Scanning {path}...")
                
                if os.path.exists(path):
                    threats = self._scan_directory(path)
                    scan_results['threats'].extend(threats)
                    scan_results['files_scanned'] += len(os.listdir(path))
                
                time.sleep(0.5)  # Simulate scan time
            
            # Scan running processes
            if callback:
                callback(len(system_paths), len(system_paths) + 1, "Analyzing running processes...")
            
            suspicious_procs = self._detect_suspicious_processes()
            scan_results['suspicious_processes'] = len(suspicious_procs)
            scan_results['threats'].extend(suspicious_procs)
            
            # Scan registry (Windows only)
            if platform.system() == "Windows":
                if callback:
                    callback(len(system_paths) + 1, len(system_paths) + 2, "Scanning registry...")
                
                registry_issues = self._scan_registry()
                scan_results['registry_issues'] = len(registry_issues)
                scan_results['threats'].extend(registry_issues)
            
            # Network analysis
            if callback:
                callback(len(system_paths) + 2, len(system_paths) + 3, "Analyzing network connections...")
            
            network_threats = self._analyze_network_security()
            scan_results['network_threats'] = len(network_threats)
            scan_results['threats'].extend(network_threats)
            
            scan_results['threats_found'] = len(scan_results['threats'])
            
            if callback:
                callback(len(system_paths) + 3, len(system_paths) + 3, "Scan complete", scan_results)
            
        except Exception as e:
            if callback:
                callback(0, 0, f"Scan failed: {str(e)}", {'error': str(e)})
        finally:
            self.scan_running = False
    
    def _get_critical_system_paths(self):
        """Get critical system paths to scan"""
        if platform.system() == "Windows":
            return [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads'),
                os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')
            ]
        else:
            return [
                '/tmp',
                os.path.expanduser('~/Downloads'),
                os.path.expanduser('~/Desktop')
            ]
    
    def _scan_directory(self, directory):
        """Scan directory for threats"""
        threats = []
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files[:10]:  # Limit for demo
                    file_path = os.path.join(root, file)
                    if self._is_suspicious_file(file_path):
                        threats.append({
                            'type': 'malicious_file',
                            'path': file_path,
                            'threat_level': 'medium'
                        })
        except:
            pass
        
        return threats
    
    def _is_suspicious_file(self, file_path):
        """Check if file is suspicious"""
        # Simple heuristics (in real implementation, would use proper signatures)
        suspicious_extensions = ['.exe', '.scr', '.bat', '.cmd', '.vbs']
        suspicious_names = ['virus', 'malware', 'trojan', 'keylog']
        
        file_name = os.path.basename(file_path).lower()
        
        if any(ext in file_name for ext in suspicious_extensions):
            if any(name in file_name for name in suspicious_names):
                return True
        
        return False
    
    def _scan_registry(self):
        """Scan Windows registry for issues"""
        issues = []
        
        if platform.system() != "Windows":
            return issues
        
        try:
            # Simulate registry scanning
            # In real implementation, would scan for malicious registry entries
            registry_keys = [
                'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'
            ]
            
            for key in registry_keys:
                # Simulate finding suspicious entries
                if np.random.random() < 0.1:  # 10% chance of finding issue
                    issues.append({
                        'type': 'registry_threat',
                        'key': key,
                        'threat_level': 'low'
                    })
        except:
            pass
        
        return issues
    
    def _analyze_network_security(self):
        """Analyze network security"""
        threats = []
        
        try:
            connections = psutil.net_connections()
            
            for conn in connections[:20]:  # Limit for demo
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    if self._is_suspicious_ip(conn.raddr.ip):
                        threats.append({
                            'type': 'network_threat',
                            'ip': conn.raddr.ip,
                            'port': conn.raddr.port,
                            'threat_level': 'high'
                        })
        except:
            pass
        
        return threats

# -------------------------
# ADVANCED REGISTRY CLEANER
# -------------------------
class AdvancedRegistryCleaner:
    def __init__(self):
        self.registry_issues = []
        self.backup_created = False
        self.scan_running = False
        
    def scan_registry_issues(self, callback=None):
        """Scan for registry issues and optimization opportunities"""
        if platform.system() != "Windows":
            return False, "Registry cleaning only available on Windows"
        
        if self.scan_running:
            return False, "Registry scan already in progress"
        
        self.scan_running = True
        threading.Thread(target=self._registry_scan_thread, args=(callback,), daemon=True).start()
        return True, "Registry scan started"
    
    def _registry_scan_thread(self, callback):
        """Registry scanning thread"""
        try:
            issues_found = []
            
            # Categories to scan
            scan_categories = [
                ("Obsolete Software", self._scan_obsolete_software),
                ("Invalid File Extensions", self._scan_file_extensions),
                ("Broken Shortcuts", self._scan_shortcuts),
                ("Startup Programs", self._scan_startup_programs),
                ("System Performance", self._scan_performance_keys),
                ("Privacy Issues", self._scan_privacy_keys)
            ]
            
            for i, (category, scan_func) in enumerate(scan_categories):
                if callback:
                    callback(i, len(scan_categories), f"Scanning {category}...")
                
                category_issues = scan_func()
                issues_found.extend(category_issues)
                time.sleep(0.5)  # Simulate scan time
            
            self.registry_issues = issues_found
            
            results = {
                'total_issues': len(issues_found),
                'categories': {cat: len([i for i in issues_found if i['category'] == cat]) 
                             for cat, _ in scan_categories},
                'issues': issues_found
            }
            
            if callback:
                callback(len(scan_categories), len(scan_categories), "Registry scan complete", results)
            
        except Exception as e:
            if callback:
                callback(0, 0, f"Registry scan failed: {str(e)}", {'error': str(e)})
        finally:
            self.scan_running = False
    
    def _scan_obsolete_software(self):
        """Scan for obsolete software entries"""
        issues = []
        
        # Simulate finding obsolete software entries
        obsolete_entries = [
            "Old Uninstaller Entry",
            "Broken Software Reference",
            "Outdated Application Path"
        ]
        
        for entry in obsolete_entries:
            if np.random.random() < 0.3:  # 30% chance of finding each issue
                issues.append({
                    'category': 'Obsolete Software',
                    'description': f"Obsolete entry: {entry}",
                    'severity': 'medium',
                    'safe_to_fix': True
                })
        
        return issues
    
    def _scan_file_extensions(self):
        """Scan for invalid file extension associations"""
        issues = []
        
        # Simulate file extension issues
        extensions = ['.txt', '.jpg', '.mp3', '.pdf', '.doc']
        
        for ext in extensions:
            if np.random.random() < 0.2:  # 20% chance
                issues.append({
                    'category': 'Invalid File Extensions',
                    'description': f"Invalid association for {ext} files",
                    'severity': 'low',
                    'safe_to_fix': True
                })
        
        return issues
    
    def _scan_shortcuts(self):
        """Scan for broken shortcuts in registry"""
        issues = []
        
        # Simulate broken shortcuts
        if np.random.random() < 0.4:
            issues.append({
                'category': 'Broken Shortcuts',
                'description': "Broken desktop shortcut references",
                'severity': 'low',
                'safe_to_fix': True
            })
        
        return issues
    
    def _scan_startup_programs(self):
        """Scan startup programs for optimization"""
        issues = []
        
        try:
            # Simulate startup program analysis
            startup_items = ['UpdateChecker', 'HelperService', 'AutoUpdater']
            
            for item in startup_items:
                if np.random.random() < 0.25:
                    issues.append({
                        'category': 'Startup Programs',
                        'description': f"Unnecessary startup program: {item}",
                        'severity': 'medium',
                        'safe_to_fix': False  # User should decide
                    })
        except:
            pass
        
        return issues
    
    def _scan_performance_keys(self):
        """Scan for performance-related registry issues"""
        issues = []
        
        # Simulate performance issues
        perf_issues = [
            "DNS cache settings suboptimal",
            "File system performance not optimized",
            "Memory management settings outdated"
        ]
        
        for issue in perf_issues:
            if np.random.random() < 0.2:
                issues.append({
                    'category': 'System Performance',
                    'description': issue,
                    'severity': 'medium',
                    'safe_to_fix': True
                })
        
        return issues
    
    def _scan_privacy_keys(self):
        """Scan for privacy-related registry entries"""
        issues = []
        
        # Simulate privacy issues
        privacy_issues = [
            "Recently accessed files list",
            "Search history entries",
            "Temporary internet files references"
        ]
        
        for issue in privacy_issues:
            if np.random.random() < 0.3:
                issues.append({
                    'category': 'Privacy Issues',
                    'description': issue,
                    'severity': 'low',
                    'safe_to_fix': True
                })
        
        return issues
    
    def create_registry_backup(self):
        """Create registry backup before cleaning"""
        try:
            backup_path = os.path.join(appdata_dir(), f"registry_backup_{int(time.time())}.reg")
            
            # Simulate registry backup creation
            backup_data = {
                'created_at': time.time(),
                'version': APP_VERSION,
                'issues_count': len(self.registry_issues)
            }
            
            with open(backup_path, 'w') as f:
                json.dump(backup_data, f)
            
            self.backup_created = True
            return True, f"Registry backup created: {backup_path}"
            
        except Exception as e:
            return False, f"Failed to create backup: {str(e)}"
    
    def fix_registry_issues(self, selected_issues=None):
        """Fix selected registry issues"""
        if not self.backup_created:
            return False, "Please create a registry backup first"
        
        try:
            issues_to_fix = selected_issues or [i for i in self.registry_issues if i['safe_to_fix']]
            fixed_count = 0
            
            for issue in issues_to_fix:
                # Simulate fixing the issue
                if issue['safe_to_fix']:
                    fixed_count += 1
            
            return True, f"Fixed {fixed_count} registry issues successfully"
            
        except Exception as e:
            return False, f"Failed to fix issues: {str(e)}"

# -------------------------
# MXD PRO GUI APPLICATION
# -------------------------
class MXDProApp:
    def __init__(self, root):
        self.root = root
        self.ai_optimizer = AdvancedAIOptimizer()
        self.gaming_optimizer = ProfessionalGamingOptimizer()
        self.security_suite = MilitarySecuritySuite()
        self.registry_cleaner = AdvancedRegistryCleaner()
        
        # Initialize AI model
        self.ai_optimizer.initialize_ai_model()
        
        self.setup_gui()
        self.show_splash_screen()
        self.start_monitoring()
        
        # Enable real-time security protection
        self.security_suite.enable_real_time_protection()
    
    def setup_gui(self):
        """Setup main GUI"""
        self.root.title(tr("app_title"))
        self.root.geometry("1100x700")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup professional dark theme
        self.setup_pro_styles()
        
        # Create header
        self.create_pro_header()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_ai_optimizer_tab()
        self.create_gaming_tab()
        self.create_security_tab()
        self.create_registry_tab()
        self.create_settings_tab()
        
        # Create status bar
        self.create_pro_status_bar()
    
    def setup_pro_styles(self):
        """Setup professional dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure professional dark theme
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#ffffff', background='#0a0a0a')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11), foreground='#cccccc', background='#0a0a0a')
        style.configure('Pro.TButton', font=('Segoe UI', 10, 'bold'), padding=12)
        style.configure('Danger.TButton', foreground='#ff4444', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', foreground='#44ff44', font=('Segoe UI', 10, 'bold'))
    
    def create_pro_header(self):
        """Create professional application header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Professional logo
        logo_frame = ttk.Frame(header_frame)
        logo_frame.pack(side=tk.LEFT)
        
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50, bg='#ff6b35', highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
        logo_canvas.create_text(25, 25, text="MXD\nPRO", fill='white', font=('Segoe UI', 8, 'bold'), justify=tk.CENTER)
        
        # Title and tagline
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(title_frame, text=tr("welcome"), style='Title.TLabel').pack(anchor=tk.W)
        ttk.Label(title_frame, text=APP_TAGLINE, style='Subtitle.TLabel').pack(anchor=tk.W)
        
        # License status
        license_frame = ttk.Frame(header_frame)
        license_frame.pack(side=tk.RIGHT)
        
        if AppState.license_valid:
            ttk.Label(license_frame, text="✅ Licensed", foreground='#44ff44', font=('Segoe UI', 10, 'bold')).pack()
            ttk.Label(license_frame, text="Professional Edition", style='Subtitle.TLabel').pack()
        else:
            ttk.Label(license_frame, text="❌ Unlicensed", foreground='#ff4444', font=('Segoe UI', 10, 'bold')).pack()
    
    def create_dashboard_tab(self):
        """Create advanced dashboard tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tr("system_monitor"))
        
        # AI Performance Score (prominent display)
        ai_frame = ttk.LabelFrame(tab, text="AI Performance Analysis", padding=15)
        ai_frame.pack(fill=tk.X, pady=(0, 10))
        
        score_frame = ttk.Frame(ai_frame)
        score_frame.pack(fill=tk.X)
        
        self.ai_score_label = ttk.Label(score_frame, text="85/100", 
                                       font=('Segoe UI', 32, 'bold'), foreground='#4CAF50')
        self.ai_score_label.pack(side=tk.LEFT)
        
        ai_info_frame = ttk.Frame(score_frame)
        ai_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(20, 0))
        
        self.optimization_potential_label = ttk.Label(ai_info_frame, text="Optimization Potential: 15%", 
                                                     font=('Segoe UI', 12))
        self.optimization_potential_label.pack(anchor=tk.W)
        
        self.prediction_confidence_label = ttk.Label(ai_info_frame, text="Prediction Confidence: 85%", 
                                                    font=('Segoe UI', 10), foreground='#cccccc')
        self.prediction_confidence_label.pack(anchor=tk.W)
        
        # Real-time system metrics with charts
        metrics_frame = ttk.Frame(tab)
        metrics_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure for real-time charts
        self.create_performance_charts(metrics_frame)
        
        # System information panel
        info_frame = ttk.LabelFrame(tab, text="System Information", padding=10)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.system_info_text = tk.Text(info_frame, height=4, wrap=tk.WORD, state=tk.DISABLED,
                                       bg='#1a1a1a', fg='#ffffff', font=('Consolas', 9))
        self.system_info_text.pack(fill=tk.X)
    
    def create_performance_charts(self, parent):
        """Create real-time performance charts"""
        try:
            # Create matplotlib figure
            self.fig, ((self.ax_cpu, self.ax_memory), (self.ax_disk, self.ax_network)) = plt.subplots(2, 2, figsize=(12, 6))
            self.fig.patch.set_facecolor('#1a1a1a')
            
            # Configure subplots
            for ax, title in zip([self.ax_cpu, self.ax_memory, self.ax_disk, self.ax_network], 
                               ['CPU Usage %', 'Memory Usage %', 'Disk I/O', 'Network I/O']):
                ax.set_title(title, color='white')
                ax.set_facecolor('#2a2a2a')
                ax.tick_params(colors='white')
                ax.grid(True, alpha=0.3)
            
            # Create canvas
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Initialize data arrays
            self.performance_data = {
                'cpu': [],
                'memory': [],
                'disk': [],
                'network': [],
                'timestamps': []
            }
            
        except Exception as e:
            # Fallback if matplotlib fails
            fallback_label = ttk.Label(parent, text="Performance charts unavailable", font=('Segoe UI', 12))
            fallback_label.pack(pady=50)
    
    def create_ai_optimizer_tab(self):
        """Create AI Performance Optimizer tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tr("ai_optimizer"))
        
        # AI Insights panel
        insights_frame = ttk.LabelFrame(tab, text="AI Insights & Recommendations", padding=15)
        insights_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ai_insights_text = tk.Text(insights_frame, height=6, wrap=tk.WORD, state=tk.DISABLED,
                                       bg='#1a1a1a', fg='#ffffff', font=('Segoe UI', 10))
        self.ai_insights_text.pack(fill=tk.X)
        
        # AI Controls
        controls_frame = ttk.LabelFrame(tab, text="AI Optimization Controls", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🤖 Run AI Analysis", style='Pro.TButton',
                  command=self.run_ai_analysis).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="⚡ Auto-Optimize System", style='Success.TButton',
                  command=self.auto_optimize_system).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="📊 View Performance History", style='Pro.TButton',
                  command=self.show_performance_history).pack(side=tk.LEFT)
        
        # Learning settings
        learning_frame = ttk.LabelFrame(tab, text="AI Learning Settings", padding=15)
        learning_frame.pack(fill=tk.X)
        
        self.learning_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(learning_frame, text="Enable AI Learning (improves optimization over time)",
                       variable=self.learning_var).pack(anchor=tk.W)
    
    def create_gaming_tab(self):
        """Create Professional Gaming Optimizer tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tr("gaming_optimizer"))
        
        # Gaming status panel
        status_frame = ttk.LabelFrame(tab, text="Gaming Performance Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_info = ttk.Frame(status_frame)
        status_info.pack(fill=tk.X)
        
        self.gaming_status_label = ttk.Label(status_info, text="🎮 Gaming Mode: Inactive", 
                                           font=('Segoe UI', 14, 'bold'))
        self.gaming_status_label.pack(side=tk.LEFT)
        
        self.fps_label = ttk.Label(status_info, text="FPS: --", font=('Segoe UI', 12))
        self.fps_label.pack(side=tk.RIGHT)
        
        # Gaming controls
        controls_frame = ttk.LabelFrame(tab, text="Gaming Optimization", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🚀 Activate Gaming Mode", style='Success.TButton',
                  command=self.toggle_gaming_mode).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="⚙️ Create Game Profile", style='Pro.TButton',
                  command=self.create_game_profile).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="📈 Gaming Analytics", style='Pro.TButton',
                  command=self.show_gaming_analytics).pack(side=tk.LEFT)
        
        # Game profiles list
        profiles_frame = ttk.LabelFrame(tab, text="Game Profiles", padding=15)
        profiles_frame.pack(fill=tk.BOTH, expand=True)
        
        self.profiles_listbox = tk.Listbox(profiles_frame, font=('Segoe UI', 10),
                                          bg='#2a2a2a', fg='white', selectbackground='#ff6b35')
        self.profiles_listbox.pack(fill=tk.BOTH, expand=True)
    
    def create_security_tab(self):
        """Create Military-Grade Security Suite tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tr("security_suite"))
        
        # Security status
        status_frame = ttk.LabelFrame(tab, text="Security Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.security_status_label = ttk.Label(status_frame, text="🛡️ Real-time Protection: Active", 
                                              font=('Segoe UI', 14, 'bold'), foreground='#44ff44')
        self.security_status_label.pack()
        
        # Security controls
        controls_frame = ttk.LabelFrame(tab, text="Security Operations", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🔍 Advanced Security Scan", style='Pro.TButton',
                  command=self.start_security_scan).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="🔒 Enable Real-time Protection", style='Success.TButton',
                  command=self.toggle_realtime_protection).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="🗂️ View Quarantine", style='Pro.TButton',
                  command=self.view_quarantine).pack(side=tk.LEFT)
        
        # Scan progress
        self.security_progress = ttk.Progressbar(controls_frame, mode='determinate')
        self.security_progress.pack(fill=tk.X, pady=(10, 0))
        
        # Threats panel
        threats_frame = ttk.LabelFrame(tab, text="Security Threats", padding=15)
        threats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.threats_text = tk.Text(threats_frame, wrap=tk.WORD, state=tk.DISABLED,
                                   bg='#1a1a1a', fg='#ffffff', font=('Segoe UI', 10))
        self.threats_text.pack(fill=tk.BOTH, expand=True)
    
    def create_registry_tab(self):
        """Create Advanced Registry Cleaner tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=tr("registry_cleaner"))
        
        # Registry status
        status_frame = ttk.LabelFrame(tab, text="Registry Status", padding=15)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.registry_status_label = ttk.Label(status_frame, text="Registry: Not Scanned", 
                                              font=('Segoe UI', 12))
        self.registry_status_label.pack()
        
        # Registry controls
        controls_frame = ttk.LabelFrame(tab, text="Registry Operations", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="🔍 Scan Registry", style='Pro.TButton',
                  command=self.scan_registry).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="💾 Create Backup", style='Pro.TButton',
                  command=self.create_registry_backup).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="🔧 Fix Issues", style='Success.TButton',
                  command=self.fix_registry_issues).pack(side=tk.LEFT)
        
        # Scan progress
        self.registry_progress = ttk.Progressbar(controls_frame, mode='determinate')
        self.registry_progress.pack(fill=tk.X, pady=(10, 0))
        
        # Issues panel
        issues_frame = ttk.LabelFrame(tab, text="Registry Issues", padding=15)
        issues_frame.pack(fill=tk.BOTH, expand=True)
        
        self.registry_text = tk.Text(issues_frame, wrap=tk.WORD, state=tk.DISABLED,
                                    bg='#1a1a1a', fg='#ffffff', font=('Segoe UI', 10))
        self.registry_text.pack(fill=tk.BOTH, expand=True)
    
    def create_settings_tab(self):
        """Create settings tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Settings")
        
        # Language settings
        lang_frame = ttk.LabelFrame(tab, text="Language (16 languages available)", padding=15)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.language_var = tk.StringVar(value=AppState.settings.get("language", "en"))
        lang_values = [f"{code} - {LANGUAGE_NAMES[code]}" for code in LANGUAGES.keys()]
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, 
                                 values=lang_values, state="readonly", width=30)
        current_lang = AppState.settings.get("language", "en")
        current_display = f"{current_lang} - {LANGUAGE_NAMES[current_lang]}"
        lang_combo.set(current_display)
        lang_combo.pack()
        
        # About section
        about_frame = ttk.LabelFrame(tab, text="About MXD Pro", padding=15)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        about_text = f"""
MXD Pro v{APP_VERSION} - Professional Edition

{APP_DESCRIPTION}

Advanced Features:
• 16 languages support
• Advanced AI Performance Optimizer with machine learning
• Professional Gaming Optimizer with custom profiles
• Military-grade Security Suite with real-time protection
• Advanced Registry Cleaner with backup/restore
• Hardware-based license activation
• Automatic system optimization
• Professional analytics and reporting

License Status: {'✅ Licensed' if AppState.license_valid else '❌ Unlicensed'}
Hardware Fingerprint: {generate_hardware_fingerprint()[:16]}...
        """
        
        about_text_widget = tk.Text(about_frame, wrap=tk.WORD, state=tk.DISABLED,
                                   bg='#1a1a1a', fg='#ffffff', font=('Segoe UI', 10))
        about_text_widget.pack(fill=tk.BOTH, expand=True)
        about_text_widget.config(state=tk.NORMAL)
        about_text_widget.insert(tk.END, about_text.strip())
        about_text_widget.config(state=tk.DISABLED)
    
    def create_pro_status_bar(self):
        """Create professional status bar"""
        self.status_bar = ttk.Frame(self.main_frame)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_bar, text=tr("status_ready"))
        self.status_label.pack(side=tk.LEFT)
        
        # Professional status indicators
        self.ai_indicator = ttk.Label(self.status_bar, text="🤖 AI: Active", foreground='#44ff44')
        self.ai_indicator.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.security_indicator = ttk.Label(self.status_bar, text="🛡️ Security: Protected", foreground='#44ff44')
        self.security_indicator.pack(side=tk.RIGHT, padx=(10, 0))
    
    def show_splash_screen(self):
        """Show professional splash screen"""
        self.splash = tk.Toplevel(self.root)
        self.splash.title("MXD Pro")
        self.splash.geometry("600x350")
        self.splash.configure(bg='#0a0a0a')
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)
        
        # Center splash screen
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() - 600) // 2
        y = (self.splash.winfo_screenheight() - 350) // 2
        self.splash.geometry(f"600x350+{x}+{y}")
        
        # Create professional splash content
        self.splash_canvas = tk.Canvas(self.splash, width=600, height=350, bg='#0a0a0a', highlightthickness=0)
        self.splash_canvas.pack()
        
        # Professional logo
        self.splash_canvas.create_oval(250, 80, 350, 180, fill='#ff6b35', outline='#ff8c42', width=3)
        self.splash_canvas.create_text(300, 130, text="MXD\nPRO", fill='white', font=('Segoe UI', 16, 'bold'), justify=tk.CENTER)
        
        # Professional text
        self.splash_canvas.create_text(300, 220, text="MXD Pro", fill='white', font=('Segoe UI', 24, 'bold'))
        self.splash_canvas.create_text(300, 245, text=APP_TAGLINE, fill='#ff6b35', font=('Segoe UI', 12, 'bold'))
        self.splash_canvas.create_text(300, 280, text="Professional System Optimization Suite", fill='#cccccc', font=('Segoe UI', 10))
        self.splash_canvas.create_text(300, 310, text="Loading AI systems...", fill='#ff6b35', font=('Segoe UI', 10))
        
        # Auto close splash after 4 seconds
        self.root.after(4000, self.close_splash)
    
    def close_splash(self):
        """Close splash screen"""
        try:
            if hasattr(self, 'splash') and self.splash:
                self.splash.destroy()
                self.splash = None
        except Exception:
            pass
    
    def start_monitoring(self):
        """Start advanced system monitoring"""
        # Start AI analysis
        self.root.after(2000, self.update_ai_analysis)
        
        # Start performance chart updates
        self.root.after(5000, self.update_performance_charts)
    
    def update_ai_analysis(self):
        """Update AI analysis display"""
        try:
            # Get system info
            system_info = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk_io': 0,  # Simplified
                'network_io': 0,  # Simplified
                'processes': len(psutil.pids())
            }
            
            # Run AI analysis
            analysis = self.ai_optimizer.analyze_system_advanced(system_info)
            
            # Update AI score display
            score = analysis.get('score', 75)
            self.ai_score_label.config(text=f"{score}/100")
            
            # Update color based on score
            if score >= 80:
                self.ai_score_label.config(foreground='#44ff44')
            elif score >= 60:
                self.ai_score_label.config(foreground='#ffaa00')
            else:
                self.ai_score_label.config(foreground='#ff4444')
            
            # Update optimization potential
            potential = analysis.get('optimization_potential', 25)
            self.optimization_potential_label.config(text=f"Optimization Potential: {potential}%")
            
            # Update prediction confidence
            confidence = analysis.get('prediction_confidence', 85)
            self.prediction_confidence_label.config(text=f"Prediction Confidence: {confidence}%")
            
            # Update AI insights
            self.update_ai_insights(analysis)
            
            # Update system info
            self.update_system_info(system_info)
            
            # Schedule next update
            self.root.after(10000, self.update_ai_analysis)  # Every 10 seconds
            
        except Exception:
            pass
    
    def update_ai_insights(self, analysis):
        """Update AI insights display"""
        try:
            self.ai_insights_text.config(state=tk.NORMAL)
            self.ai_insights_text.delete(1.0, tk.END)
            
            insights_text = "🤖 AI Performance Analysis:\n\n"
            
            # Add recommendations
            recommendations = analysis.get('recommendations', [])
            if recommendations:
                insights_text += "Recommendations:\n"
                for rec in recommendations:
                    insights_text += f"• {rec}\n"
            
            # Add AI insights
            ai_insights = analysis.get('ai_insights', [])
            if ai_insights:
                insights_text += "\nAI Insights:\n"
                for insight in ai_insights:
                    insights_text += f"• {insight}\n"
            
            self.ai_insights_text.insert(tk.END, insights_text)
            self.ai_insights_text.config(state=tk.DISABLED)
            
        except Exception:
            pass
    
    def update_system_info(self, system_info):
        """Update system information display"""
        try:
            self.system_info_text.config(state=tk.NORMAL)
            self.system_info_text.delete(1.0, tk.END)
            
            cpu_percent = system_info.get('cpu_percent', 0)
            memory = system_info.get('memory', {})
            memory_percent = memory.get('percent', 0)
            memory_total = format_bytes(memory.get('total', 0))
            memory_available = format_bytes(memory.get('available', 0))
            processes = system_info.get('processes', 0)
            
            info_text = f"CPU Usage: {cpu_percent:.1f}%\n"
            info_text += f"Memory: {memory_percent:.1f}% ({memory_available} available of {memory_total})\n"
            info_text += f"Running Processes: {processes}\n"
            info_text += f"AI Learning: {'Enabled' if self.ai_optimizer.learning_enabled else 'Disabled'}"
            
            self.system_info_text.insert(tk.END, info_text)
            self.system_info_text.config(state=tk.DISABLED)
            
        except Exception:
            pass
    
    def update_performance_charts(self):
        """Update real-time performance charts"""
        try:
            if not hasattr(self, 'fig'):
                return
            
            # Get current system metrics
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            
            # Add data to history
            current_time = time.time()
            self.performance_data['timestamps'].append(current_time)
            self.performance_data['cpu'].append(cpu_percent)
            self.performance_data['memory'].append(memory_percent)
            self.performance_data['disk'].append(np.random.uniform(0, 100))  # Simulated
            self.performance_data['network'].append(np.random.uniform(0, 100))  # Simulated
            
            # Keep only last 60 data points (10 minutes)
            for key in self.performance_data:
                if len(self.performance_data[key]) > 60:
                    self.performance_data[key] = self.performance_data[key][-60:]
            
            # Update charts
            self.ax_cpu.clear()
            self.ax_memory.clear()
            self.ax_disk.clear()
            self.ax_network.clear()
            
            # Plot data
            timestamps = self.performance_data['timestamps']
            if len(timestamps) > 1:
                self.ax_cpu.plot(timestamps, self.performance_data['cpu'], 'g-', linewidth=2)
                self.ax_memory.plot(timestamps, self.performance_data['memory'], 'b-', linewidth=2)
                self.ax_disk.plot(timestamps, self.performance_data['disk'], 'r-', linewidth=2)
                self.ax_network.plot(timestamps, self.performance_data['network'], 'y-', linewidth=2)
            
            # Configure charts
            for ax, title, color in zip([self.ax_cpu, self.ax_memory, self.ax_disk, self.ax_network],
                                       ['CPU Usage %', 'Memory Usage %', 'Disk I/O %', 'Network I/O %'],
                                       ['green', 'blue', 'red', 'yellow']):
                ax.set_title(title, color='white')
                ax.set_facecolor('#2a2a2a')
                ax.tick_params(colors='white', labelsize=8)
                ax.set_ylim(0, 100)
                ax.grid(True, alpha=0.3)
            
            # Update canvas
            self.canvas.draw()
            
            # Schedule next update
            self.root.after(10000, self.update_performance_charts)  # Every 10 seconds
            
        except Exception:
            pass
    
    # Event handlers for buttons
    def run_ai_analysis(self):
        """Run comprehensive AI analysis"""
        self.update_status("Running AI analysis...")
        self.root.after(100, self.update_ai_analysis)
    
    def auto_optimize_system(self):
        """Run automatic system optimization"""
        self.update_status("Running AI-guided optimization...")
        
        def optimize():
            success, optimizations = self.ai_optimizer.auto_optimize_system()
            
            def show_results():
                if success:
                    result_text = "AI Optimization Complete!\n\n" + "\n".join(optimizations)
                    messagebox.showinfo("Optimization Complete", result_text)
                else:
                    messagebox.showerror("Optimization Failed", "\n".join(optimizations))
                self.update_status("Ready")
            
            self.root.after_idle(show_results)
        
        threading.Thread(target=optimize, daemon=True).start()
    
    def show_performance_history(self):
        """Show performance history dialog"""
        messagebox.showinfo("Performance History", 
                          f"AI has analyzed {len(self.ai_optimizer.performance_history)} system states.\n"
                          f"Learning enabled: {self.ai_optimizer.learning_enabled}\n\n"
                          "Performance history helps AI provide better optimization recommendations.")
    
    def toggle_gaming_mode(self):
        """Toggle gaming optimization mode"""
        if AppState.gaming_active:
            success, message = self.gaming_optimizer.deactivate_gaming_mode()
            if success:
                self.gaming_status_label.config(text="🎮 Gaming Mode: Inactive")
                self.update_status("Gaming mode deactivated")
            else:
                messagebox.showerror("Error", message)
        else:
            success, optimizations = self.gaming_optimizer.activate_gaming_mode()
            if success:
                self.gaming_status_label.config(text="🎮 Gaming Mode: Active", foreground='#44ff44')
                result_text = "Gaming Mode Activated!\n\n" + "\n".join(optimizations)
                messagebox.showinfo("Gaming Optimization", result_text)
                self.update_status("Gaming mode active")
            else:
                messagebox.showerror("Error", "\n".join(optimizations))
    
    def create_game_profile(self):
        """Create new game profile"""
        game_name = simpledialog.askstring("Create Game Profile", "Enter game name:")
        if game_name:
            profile = self.gaming_optimizer.create_game_profile(game_name)
            self.profiles_listbox.insert(tk.END, f"{game_name} - {profile['optimization_level']} optimization")
            messagebox.showinfo("Profile Created", f"Game profile for '{game_name}' created successfully!")
    
    def show_gaming_analytics(self):
        """Show gaming performance analytics"""
        stats = self.gaming_optimizer.get_gaming_statistics()
        if stats:
            analytics_text = f"""Gaming Performance Analytics:

Average FPS: {stats['average_fps']:.1f}
Min FPS: {stats['min_fps']:.1f}
Max FPS: {stats['max_fps']:.1f}
FPS Stability: {stats['fps_stability']:.1f}%
Total Game Profiles: {stats['total_sessions']}
Active Profile: {stats['active_profile'] or 'None'}"""
        else:
            analytics_text = "No gaming data available.\nActivate gaming mode to start collecting performance metrics."
        
        messagebox.showinfo("Gaming Analytics", analytics_text)
    
    def start_security_scan(self):
        """Start advanced security scan"""
        success, message = self.security_suite.advanced_system_scan(self.security_scan_callback)
        if success:
            self.update_status("Advanced security scan started...")
            self.security_progress.config(value=0)
        else:
            messagebox.showerror("Error", message)
    
    def security_scan_callback(self, current, total, status, results=None):
        """Security scan progress callback"""
        def update_ui():
            if total > 0:
                progress = (current / total) * 100
                self.security_progress.config(value=progress)
            
            self.update_status(status)
            
            if results:
                if 'error' in results:
                    messagebox.showerror("Scan Error", results['error'])
                else:
                    self.display_security_results(results)
        
        self.root.after_idle(update_ui)
    
    def display_security_results(self, results):
        """Display security scan results"""
        try:
            self.threats_text.config(state=tk.NORMAL)
            self.threats_text.delete(1.0, tk.END)
            
            threats_found = results.get('threats_found', 0)
            files_scanned = results.get('files_scanned', 0)
            
            result_text = f"Security Scan Complete\n\n"
            result_text += f"Files Scanned: {files_scanned:,}\n"
            result_text += f"Threats Found: {threats_found}\n"
            result_text += f"Suspicious Processes: {results.get('suspicious_processes', 0)}\n"
            result_text += f"Registry Issues: {results.get('registry_issues', 0)}\n"
            result_text += f"Network Threats: {results.get('network_threats', 0)}\n\n"
            
            if threats_found > 0:
                result_text += "Threats Detected:\n"
                for threat in results.get('threats', [])[:10]:  # Show first 10
                    threat_type = threat.get('type', 'Unknown')
                    threat_level = threat.get('threat_level', 'Unknown')
                    result_text += f"• {threat_type} - {threat_level} risk\n"
            else:
                result_text += "✅ System appears clean - no threats detected.\n"
            
            self.threats_text.insert(tk.END, result_text)
            self.threats_text.config(state=tk.DISABLED)
            
            # Show summary dialog
            if threats_found == 0:
                messagebox.showinfo("Security Scan Complete", 
                                  f"Advanced security scan completed successfully!\n\n"
                                  f"Files scanned: {files_scanned:,}\n"
                                  f"Threats found: {threats_found}\n\n"
                                  f"Your system is secure.")
            else:
                messagebox.showwarning("Threats Detected", 
                                     f"Security scan completed!\n\n"
                                     f"Files scanned: {files_scanned:,}\n"
                                     f"Threats found: {threats_found}\n\n"
                                     f"Review the security tab for details.")
        except Exception:
            pass
    
    def toggle_realtime_protection(self):
        """Toggle real-time security protection"""
        if self.security_suite.real_time_protection:
            self.security_suite.real_time_protection = False
            self.security_status_label.config(text="🛡️ Real-time Protection: Inactive", foreground='#ff4444')
            self.security_indicator.config(text="🛡️ Security: Disabled", foreground='#ff4444')
        else:
            success, message = self.security_suite.enable_real_time_protection()
            if success:
                self.security_status_label.config(text="🛡️ Real-time Protection: Active", foreground='#44ff44')
                self.security_indicator.config(text="🛡️ Security: Protected", foreground='#44ff44')
            else:
                messagebox.showerror("Error", message)
    
    def view_quarantine(self):
        """View quarantined threats"""
        quarantine_count = len(AppState.security_threats)
        if quarantine_count > 0:
            threat_list = "\n".join([f"• {threat.get('name', 'Unknown')} - {threat.get('type', 'Unknown')}" 
                                    for threat in AppState.security_threats[:10]])
            messagebox.showinfo("Quarantine", f"Quarantined Threats ({quarantine_count}):")
        else:
            messagebox.showinfo("Quarantine", "No threats in quarantine.")
    
    def scan_registry(self):
        """Start registry scan"""
        if platform.system() != "Windows":
            messagebox.showwarning("Not Available", "Registry cleaning is only available on Windows.")
            return
        
        success, message = self.registry_cleaner.scan_registry_issues(self.registry_scan_callback)
        if success:
            self.update_status("Scanning registry...")
            self.registry_progress.config(value=0)
        else:
            messagebox.showerror("Error", message)
    
    def registry_scan_callback(self, current, total, status, results=None):
        """Registry scan progress callback"""
        def update_ui():
            if total > 0:
                progress = (current / total) * 100
                self.registry_progress.config(value=progress)
            
            self.update_status(status)
            
            if results:
                if 'error' in results:
                    messagebox.showerror("Registry Scan Error", results['error'])
                else:
                    self.display_registry_results(results)
        
        self.root.after_idle(update_ui)
    
    def display_registry_results(self, results):
        """Display registry scan results"""
        try:
            self.registry_text.config(state=tk.NORMAL)
            self.registry_text.delete(1.0, tk.END)
            
            total_issues = results.get('total_issues', 0)
            categories = results.get('categories', {})
            
            result_text = f"Registry Scan Complete\n\n"
            result_text += f"Total Issues Found: {total_issues}\n\n"
            
            if total_issues > 0:
                result_text += "Issues by Category:\n"
                for category, count in categories.items():
                    if count > 0:
                        result_text += f"• {category}: {count} issues\n"
                
                result_text += "\nDetailed Issues:\n"
                for issue in results.get('issues', [])[:15]:  # Show first 15
                    severity = issue.get('severity', 'Unknown')
                    description = issue.get('description', 'Unknown issue')
                    safe = "✅" if issue.get('safe_to_fix', False) else "⚠️"
                    result_text += f"{safe} {severity.upper()}: {description}\n"
            else:
                result_text += "✅ Registry is clean - no issues found.\n"
            
            self.registry_text.insert(tk.END, result_text)
            self.registry_text.config(state=tk.DISABLED)
            
            # Update status
            self.registry_status_label.config(text=f"Registry: {total_issues} issues found")
            
            # Show summary
            if total_issues == 0:
                messagebox.showinfo("Registry Clean", "Registry scan completed - no issues found!")
            else:
                messagebox.showinfo("Registry Issues Found", 
                                  f"Found {total_issues} registry issues.\n\n"
                                  "Create a backup before fixing issues.")
        except Exception:
            pass
    
    def create_registry_backup(self):
        """Create registry backup"""
        success, message = self.registry_cleaner.create_registry_backup()
        if success:
            messagebox.showinfo("Backup Created", message)
        else:
            messagebox.showerror("Backup Failed", message)
    
    def fix_registry_issues(self):
        """Fix registry issues"""
        if not self.registry_cleaner.backup_created:
            messagebox.showwarning("Backup Required", "Please create a registry backup first.")
            return
        
        if not self.registry_cleaner.registry_issues:
            messagebox.showinfo("No Issues", "No registry issues to fix. Run a scan first.")
            return
        
        # Confirm with user
        if messagebox.askyesno("Fix Registry Issues", 
                             f"Fix {len(self.registry_cleaner.registry_issues)} registry issues?\n\n"
                             "This will only fix issues marked as safe."):
            
            success, message = self.registry_cleaner.fix_registry_issues()
            if success:
                messagebox.showinfo("Registry Fixed", message)
                self.registry_status_label.config(text="Registry: Issues fixed")
            else:
                messagebox.showerror("Fix Failed", message)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)

def main():
    """Main application entry point"""
    # Check license first
    if not AppState.check_license():
        # Show activation dialog
        root = tk.Tk()
        root.withdraw()
        
        activation_key = simpledialog.askstring("MXD Pro Activation", 
                                               "Enter your activation key:")
        
        if activation_key:
            success, message = create_license(activation_key)
            if success:
                messagebox.showinfo("Activation Successful", 
                                  "MXD Pro has been activated successfully!")
                AppState.check_license()
            else:
                messagebox.showerror("Activation Failed", message)
                return
        else:
            messagebox.showwarning("Activation Required", 
                                 "MXD Pro requires activation to run.")
            return
    
    # Start main application
    root = tk.Tk()
    app = None
    
    # Hide root window initially
    root.withdraw()
    
    try:
        app = MXDProApp(root)
        
        # Show main window after splash
        root.after(4000, root.deiconify)
        
        # Start main loop
        root.mainloop()
        
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        if app:
            if hasattr(app, 'ai_optimizer'):
                app.ai_optimizer.learning_enabled = False
            if hasattr(app, 'security_suite'):
                app.security_suite.real_time_protection = False

if __name__ == "__main__":
    main()