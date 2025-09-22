#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MXD Pro - Licensing System Module
Handles one-time license key verification and storage
"""

import os
import sys
import hashlib
import uuid
import base64
import json
import platform
from datetime import datetime, timedelta
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
        # Generate a consistent secret based on app identity
        app_id = "MXDPro_v1.0_Licensing_System"
        return hashlib.sha256(app_id.encode()).digest()

    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        try:
            # Create machine ID from multiple system characteristics
            system_info = [
                platform.system(),
                platform.machine(),
                platform.processor(),
                str(uuid.getnode())  # MAC address
            ]

            # Add Windows-specific info if available
            if platform.system() == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                       r"SOFTWARE\Microsoft\Cryptography")
                    machine_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                    system_info.append(machine_guid)
                    winreg.CloseKey(key)
                except:
                    pass

            # Create hash of system info
            combined = "|".join(system_info)
            machine_id = hashlib.sha256(combined.encode()).hexdigest()[:32]
            return machine_id

        except Exception as e:
            self._log(f"Error generating machine ID: {e}")
            # Fallback machine ID
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def _encrypt_data(self, data: str, password: str) -> bytes:
        """Encrypt data with password"""
        try:
            # Generate salt
            salt = os.urandom(16)

            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode())

            # Generate IV
            iv = os.urandom(16)

            # Encrypt data
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            # Pad data
            pad_length = 16 - (len(data.encode()) % 16)
            padded_data = data.encode() + bytes([pad_length] * pad_length)

            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

            # Combine salt + iv + encrypted_data
            return salt + iv + encrypted_data

        except Exception as e:
            self._log(f"Error encrypting data: {e}")
            return b""

    def _decrypt_data(self, encrypted_data: bytes, password: str) -> str:
        """Decrypt data with password"""
        try:
            # Extract components
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]

            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(password.encode())

            # Decrypt data
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            pad_length = padded_data[-1]
            data = padded_data[:-pad_length]

            return data.decode()

        except Exception as e:
            self._log(f"Error decrypting data: {e}")
            return ""

    def _generate_license_key(self, user_info: str = "") -> str:
        """Generate a license key format (for display purposes)"""
        # This is just for format demonstration - real keys would come from server
        prefix = "MXD"
        user_hash = hashlib.md5(user_info.encode()).hexdigest()[:8].upper()
        timestamp = datetime.now().strftime("%y%m")
        suffix = hashlib.sha256(f"{user_hash}{timestamp}".encode()).hexdigest()[:8].upper()

        return f"{prefix}-{user_hash}-{timestamp}-{suffix}"

    def _validate_license_key_format(self, license_key: str) -> bool:
        """Validate license key format"""
        try:
            # Basic format validation: MXD-XXXXXXXX-YYYY-XXXXXXXX
            parts = license_key.split('-')
            if len(parts) != 4:
                return False

            if parts[0] != "MXD":
                return False

            if len(parts[1]) != 8 or not parts[1].isalnum():
                return False

            if len(parts[2]) != 4 or not parts[2].isdigit():
                return False

            if len(parts[3]) != 8 or not parts[3].isalnum():
                return False

            return True

        except:
            return False

    def is_first_run(self) -> bool:
        """Check if this is the first run (no license data exists)"""
        return not (self.license_file.exists() and self.license_data_file.exists())

    def request_license_key(self) -> str:
        """Request license key from user (to be called by GUI)"""
        if self.is_first_run():
            self._log("First run detected - license key required")
            machine_id = self._get_machine_id()
            self._log(f"Machine ID: {machine_id}")

            # For demo purposes, show expected format
            demo_key = self._generate_license_key(machine_id)
            self._log(f"Expected license key format: {demo_key}")

            return ""  # GUI will handle the actual input
        else:
            self._log("License already exists")
            return self.get_current_license_key()

    def validate_and_store_license(self, license_key: str) -> Tuple[bool, str]:
        """Validate and store license key"""
        try:
            # Validate format
            if not self._validate_license_key_format(license_key):
                return False, "Invalid license key format"

            # Get machine information
            machine_id = self._get_machine_id()

            # Create license data
            license_data = {
                "key": license_key,
                "machine_id": machine_id,
                "activation_date": datetime.now().isoformat(),
                "version": "1.0.0",
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

            # Store license key in plain text file (as requested)
            with open(self.license_file, 'w', encoding='utf-8') as f:
                f.write(license_key)

            # Store encrypted license data
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
            # Check if license files exist
            if not (self.license_file.exists() and self.license_data_file.exists()):
                return False, "No license found", {}

            # Read license key
            with open(self.license_file, 'r', encoding='utf-8') as f:
                license_key = f.read().strip()

            # Read and decrypt license data
            with open(self.license_data_file, 'rb') as f:
                encrypted_data = f.read()

            machine_id = self._get_machine_id()
            license_json = self._decrypt_data(encrypted_data, machine_id)

            if not license_json:
                return False, "License data corrupted", {}

            license_data = json.loads(license_json)

            # Verify machine ID
            if license_data.get("machine_id") != machine_id:
                return False, "License not valid for this machine", {}

            # Verify license key format
            if not self._validate_license_key_format(license_key):
                return False, "Invalid license key", {}

            # Verify stored key matches file
            if license_data.get("key") != license_key:
                return False, "License key mismatch", {}

            self._log("License verified successfully")
            return True, "License valid", license_data

        except Exception as e:
            error_msg = f"License verification error: {e}"
            self._log(error_msg)
            return False, error_msg, {}

    def get_current_license_key(self) -> str:
        """Get current license key"""
        try:
            if self.license_file.exists():
                with open(self.license_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except:
            pass
        return ""

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
                "machine_id": license_data.get("machine_id", "")[:16] + "...",  # Partial machine ID for security
                "status": "Active"
            }
        else:
            return {
                "valid": False,
                "status": "Invalid",
                "message": message
            }

    def revoke_license(self) -> bool:
        """Revoke current license (for testing/reset purposes)"""
        try:
            if self.license_file.exists():
                os.remove(self.license_file)

            if self.license_data_file.exists():
                os.remove(self.license_data_file)

            self._log("License revoked successfully")
            return True

        except Exception as e:
            self._log(f"Error revoking license: {e}")
            return False

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a specific feature is enabled"""
        valid, _, license_data = self.verify_license()

        if not valid:
            return False

        features = license_data.get("features", {})
        return features.get(feature_name, False)

    def get_demo_license_key(self) -> str:
        """Generate a demo license key for testing"""
        machine_id = self._get_machine_id()
        return self._generate_license_key(machine_id)

class LicenseActivationDialog:
    """Simple console-based license activation for testing"""

    def __init__(self, license_manager: LicenseManager):
        self.license_manager = license_manager

    def show_activation_dialog(self) -> bool:
        """Show license activation dialog in console"""
        print("\n" + "="*60)
        print("MXD Pro - License Activation Required")
        print("="*60)

        if not self.license_manager.is_first_run():
            print("License already activated.")
            return True

        print("\nThis is your first run of MXD Pro.")
        print("Please enter your license key to continue.")
        print("\nFormat: MXD-XXXXXXXX-YYYY-XXXXXXXX")

        # Show machine ID for reference
        machine_id = self.license_manager._get_machine_id()
        print(f"\nMachine ID: {machine_id[:16]}...")

        # For demo purposes, show a valid demo key
        demo_key = self.license_manager.get_demo_license_key()
        print(f"Demo key (for testing): {demo_key}")

        while True:
            try:
                license_key = input("\nEnter license key (or 'demo' for demo key): ").strip()

                if license_key.lower() == 'demo':
                    license_key = demo_key

                if license_key.lower() == 'quit':
                    return False

                print("Validating license key...")

                valid, message = self.license_manager.validate_and_store_license(license_key)

                if valid:
                    print(f"✓ {message}")
                    print("License activated successfully!")
                    return True
                else:
                    print(f"✗ {message}")
                    print("Please try again or contact support.")

                    retry = input("Retry? (y/n): ").strip().lower()
                    if retry != 'y':
                        return False

            except KeyboardInterrupt:
                print("\n\nActivation cancelled.")
                return False
            except Exception as e:
                print(f"Error: {e}")
                return False

if __name__ == "__main__":
    # Test licensing system
    from utils import MXDLogger

    logger = MXDLogger("License_Test")
    license_manager = LicenseManager(logger)

    print("Testing MXD Pro Licensing System...")

    # Test first run check
    print(f"First run: {license_manager.is_first_run()}")

    # Test license activation
    if license_manager.is_first_run():
        dialog = LicenseActivationDialog(license_manager)
        if dialog.show_activation_dialog():
            print("License activation successful!")
        else:
            print("License activation failed.")

    # Test license verification
    valid, message, license_data = license_manager.verify_license()
    print(f"\nLicense verification: {valid}")
    print(f"Message: {message}")

    if valid:
        # Show license info
        license_info = license_manager.get_license_info()
        print(f"\nLicense Info:")
        for key, value in license_info.items():
            print(f"  {key}: {value}")

        # Test feature checks
        features = ["ai_optimizer", "gaming_optimizer", "security_suite"]
        print(f"\nFeature availability:")
        for feature in features:
            enabled = license_manager.is_feature_enabled(feature)
            print(f"  {feature}: {'✓' if enabled else '✗'}")

    print("\nLicensing system test completed.")