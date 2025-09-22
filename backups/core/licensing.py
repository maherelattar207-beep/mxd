#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro - Licensing System Module
Handles one-time license key verification and storage.
Auto-generates a license if missing or invalid.
"""

import os
import sys
import hashlib
import uuid
import base64
import json
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class LicenseManager:
    """License management system for MXD Pro"""

    def __init__(self, logger=None):
        self.logger = logger
        self.license_file = Path("license.txt")
        self.license_data_file = Path(".license_data")
        self.app_secret = self._get_app_secret()
        self._log("License manager initialized")

    def _log(self, message: str):
        """Log message if logger is available"""
        if self.logger:
            self.logger.info(message)

    def _get_app_secret(self) -> bytes:
        """Get application secret for encryption"""
        app_id = "MXDPro_v1.0_Licensing_System"
        return hashlib.sha256(app_id.encode()).digest()

    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        try:
            system_info = [
                platform.system(),
                platform.machine(),
                platform.processor(),
                str(uuid.getnode())
            ]
            if platform.system() == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                    machine_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                    system_info.append(machine_guid)
                    winreg.CloseKey(key)
                except Exception:
                    pass
            combined = "|".join(system_info)
            return hashlib.sha256(combined.encode()).hexdigest()[:32]
        except Exception as e:
            self._log(f"Error generating machine ID: {e}")
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def _encrypt_data(self, data: str, password: str) -> bytes:
        """Encrypt data with password"""
        try:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(password.encode())
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            pad_length = 16 - (len(data.encode()) % 16)
            padded_data = data.encode() + bytes([pad_length] * pad_length)
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            return salt + iv + encrypted_data
        except Exception as e:
            self._log(f"Error encrypting data: {e}")
            return b""

    def _decrypt_data(self, encrypted_data: bytes, password: str) -> str:
        """Decrypt data with password"""
        try:
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(password.encode())
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            pad_length = padded_data[-1]
            data = padded_data[:-pad_length]
            return data.decode()
        except Exception as e:
            self._log(f"Error decrypting data: {e}")
            return ""

    def _generate_license_key(self, user_info: str = "") -> str:
        """Generate a valid license key."""
        prefix = "MXD"
        user_hash = hashlib.md5(user_info.encode()).hexdigest()[:8].upper()
        timestamp = datetime.now().strftime("%y%m")
        # Add a random element to ensure uniqueness
        random_element = hashlib.sha256(os.urandom(16)).hexdigest()[:8].upper()
        return f"{prefix}-{user_hash}-{timestamp}-{random_element}"

    def _validate_license_key_format(self, license_key: str) -> bool:
        """Validate license key format"""
        try:
            parts = license_key.split('-')
            return len(parts) == 4 and parts[0] == "MXD" and len(parts[1]) == 8 and len(parts[2]) == 4 and len(parts[3]) == 8
        except:
            return False

    def _generate_and_store_new_license(self) -> Tuple[bool, str]:
        """Generates and stores a new license, making it valid on the spot."""
        self._log("Generating and storing a new license.")
        machine_id = self._get_machine_id()
        new_key = self._generate_license_key(machine_id)
        return self.validate_and_store_license(new_key)

    def ensure_license_is_valid(self):
        """
        Checks for a valid license. If not found or invalid, generates a new one.
        This is the main entry point for the application startup.
        """
        self._log("Ensuring license is valid...")
        is_valid, message, _ = self.verify_license()
        if is_valid:
            self._log("License is valid.")
            return

        self._log(f"License not valid ({message}), generating a new one.")
        success, msg = self._generate_and_store_new_license()
        if success:
            self._log(f"Successfully generated and stored new license: {msg}")
        else:
            self._log(f"CRITICAL: Failed to generate a new license: {msg}")
            # In a real app, we might want to handle this failure more gracefully.
            # For now, we log it as critical.

    def validate_and_store_license(self, license_key: str) -> Tuple[bool, str]:
        """Validate and store license key"""
        try:
            if not self._validate_license_key_format(license_key):
                return False, "Invalid license key format"

            machine_id = self._get_machine_id()
            license_data = {
                "key": license_key,
                "machine_id": machine_id,
                "activation_date": datetime.now().isoformat(),
                "version": "1.1.0", # Updated version
                "features": {
                    "ai_optimizer": True,
                    "gaming_optimizer": True,
                    "security_suite": True,
                    "registry_cleaner": True,
                    "multi_language": True,
                    "real_time_monitoring": True,
                    "auto_updates": True
                }
            }

            with open(self.license_file, 'w', encoding='utf-8') as f:
                f.write(license_key)

            license_json = json.dumps(license_data, indent=2)
            encrypted_data = self._encrypt_data(license_json, machine_id)
            with open(self.license_data_file, 'wb') as f:
                f.write(encrypted_data)

            self._log(f"License key validated and stored: {license_key}")
            return True, "License key activated successfully"

        except Exception as e:
            error_msg = f"Error storing license: {e}"
            self._log(error_msg)
            return False, error_msg

    def verify_license(self) -> Tuple[bool, str, Dict[str, Any]]:
        """Verify current license and return license info"""
        try:
            if not (self.license_file.exists() and self.license_data_file.exists()):
                return False, "No license found", {}

            with open(self.license_file, 'r', encoding='utf-8') as f:
                license_key = f.read().strip()
            if not self._validate_license_key_format(license_key):
                return False, "Invalid license key format", {}

            with open(self.license_data_file, 'rb') as f:
                encrypted_data = f.read()

            machine_id = self._get_machine_id()
            license_json = self._decrypt_data(encrypted_data, machine_id)
            if not license_json:
                return False, "License data corrupted", {}

            license_data = json.loads(license_json)

            if license_data.get("machine_id") != machine_id:
                return False, "License not valid for this machine", {}
            if license_data.get("key") != license_key:
                return False, "License key mismatch", {}

            self._log("License verified successfully")
            return True, "License valid", license_data

        except Exception as e:
            error_msg = f"License verification error: {e}"
            self._log(error_msg)
            return False, error_msg, {}

    def get_license_info(self) -> Dict[str, Any]:
        """Get license information for display"""
        valid, message, license_data = self.verify_license()
        if valid:
            activation_date = license_data.get("activation_date", "")
            try:
                activation_datetime = datetime.fromisoformat(activation_date.replace('Z', '+00:00'))
                formatted_date = activation_datetime.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_date = "Unknown"
            return {
                "valid": True,
                "license_key": license_data.get("key", ""),
                "activation_date": formatted_date,
                "version": license_data.get("version", ""),
                "features": license_data.get("features", {}),
                "machine_id": license_data.get("machine_id", "")[:16] + "...",
                "status": "Active"
            }
        else:
            return {"valid": False, "status": "Invalid", "message": message}

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a specific feature is enabled"""
        valid, _, license_data = self.verify_license()
        if not valid:
            return False
        features = license_data.get("features", {})
        return features.get(feature_name, False)

if __name__ == "__main__":
    # Test the new auto-generating license system
    from .utils import MXDLogger
    logger = MXDLogger("License_Test")

    # Clean up old license files for a clean test
    if os.path.exists("license.txt"):
        os.remove("license.txt")
    if os.path.exists(".license_data"):
        os.remove(".license_data")

    print("--- Testing License Auto-Generation ---")
    license_manager = LicenseManager(logger)
    license_manager.ensure_license_is_valid()

    valid, message, _ = license_manager.verify_license()
    print(f"Verification after auto-generation: {valid}, Message: {message}")

    print("\n--- Testing Existing License ---")
    license_manager_2 = LicenseManager(logger)
    license_manager_2.ensure_license_is_valid()
    valid_2, message_2, _ = license_manager_2.verify_license()
    print(f"Second verification: {valid_2}, Message: {message_2}")

    print("\n--- License Info ---")
    info = license_manager_2.get_license_info()
    for k, v in info.items():
        print(f"{k}: {v}")

    print("\nLicensing system test completed.")
