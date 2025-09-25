import os
import sys
import hashlib
import uuid
import base64
import json
import platform
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class LicenseManager:
    """Professional license management system for MXD Pro."""

    MASTER_KEY = "K!nG0FDr@g0nS"

    def __init__(self, logger=None):
        self.logger = logger
        self.license_file = Path("license.txt")
        self.license_data_file = Path(".license_data")
        self._log("License manager initialized.")

    def _log(self, message: str):
        if self.logger: self.logger.info(message)

    def _get_machine_id(self) -> str:
        try:
            system_info = [platform.system(), platform.machine(), platform.processor(), str(uuid.getnode())]
            if platform.system() == "Windows":
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                    machine_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                    system_info.append(machine_guid)
                    winreg.CloseKey(key)
                except Exception: pass
            return hashlib.sha256("|".join(system_info).encode()).hexdigest()[:32]
        except Exception as e:
            self._log(f"Error generating machine ID: {e}")
            return hashlib.sha256(str(uuid.getnode()).encode()).hexdigest()[:32]

    def _encrypt_data(self, data: str, password: str) -> bytes:
        try:
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(password.encode())
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            pad_length = 16 - (len(data.encode()) % 16)
            padded_data = data.encode() + bytes([pad_length] * pad_length)
            return salt + iv + (encryptor.update(padded_data) + encryptor.finalize())
        except Exception as e:
            self._log(f"Error encrypting data: {e}"); return b""

    def _decrypt_data(self, encrypted_data: bytes, password: str) -> str:
        try:
            salt, iv, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
            key = kdf.derive(password.encode())
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            pad_length = padded_data[-1]
            return padded_data[:-pad_length].decode()
        except Exception as e:
            self._log(f"Error decrypting data: {e}"); return ""

    def _generate_license_key(self, user_info: str = "") -> str:
        prefix = "MXDPRO"
        user_hash = hashlib.md5(user_info.encode()).hexdigest()[:8].upper()
        timestamp = datetime.now().strftime("%y%m%d")
        random_element = hashlib.sha256(os.urandom(16)).hexdigest()[:12].upper()
        return f"{prefix}-{user_hash}-{timestamp}-{random_element}"

    def verify_purchase_and_activate(self, email: str) -> Tuple[bool, str]:
        """Simulates an API call to verify a purchase and activates the product."""
        self._log(f"Simulating purchase verification for email: {email}")
        time.sleep(2) # Simulate network latency

        # In a real application, this would be an HTTPS request to a server.
        # For this simulation, we'll just check for a specific test email.
        if email.lower() == "test@test.com":
            self._log("Test purchase verified successfully.")
            new_key = self._generate_license_key(email)
            success, msg = self.validate_and_store_license(new_key)
            if success:
                return True, "Purchase verified and product activated successfully!"
            else:
                return False, f"Purchase verified, but activation failed: {msg}"
        else:
            self._log("Purchase verification failed for this email.")
            return False, "This email address was not found in our purchase records."

    def validate_and_store_license(self, license_key: str) -> Tuple[bool, str]:
        """Validates a license key (including the master key) and stores it."""

        # Check for the emergency master key
        if license_key == self.MASTER_KEY:
            self._log("Emergency master key used for activation.")
            # We still generate a real license structure for consistency
            return self._generate_and_store_new_license(is_master_key=True)

        if not self._validate_license_key_format(license_key):
            return False, "Invalid license key format."

        return self._store_license(license_key)

    def _generate_and_store_new_license(self, is_master_key=False) -> Tuple[bool, str]:
        """Internal helper to generate and store a new license."""
        user_info = "MASTER" if is_master_key else self._get_machine_id()
        new_key = self._generate_license_key(user_info)
        return self._store_license(new_key, is_master_key)

    def _store_license(self, license_key: str, is_master_key=False) -> Tuple[bool, str]:
        try:
            machine_id = self._get_machine_id()
            license_data = {
                "key": license_key,
                "machine_id": machine_id,
                "activation_date": datetime.now().isoformat(),
                "is_master": is_master_key,
                "version": "2.1.0"
            }
            with open(self.license_file, 'w', encoding='utf-8') as f: f.write(license_key)
            encrypted_data = self._encrypt_data(json.dumps(license_data), machine_id)
            with open(self.license_data_file, 'wb') as f: f.write(encrypted_data)
            self._log(f"License key stored successfully: {license_key}")
            return True, "License key activated successfully."
        except Exception as e:
            return False, f"Error storing license: {e}"

    def _validate_license_key_format(self, license_key: str) -> bool:
        return license_key.startswith("MXDPRO-") and len(license_key.split('-')) == 4

    def verify_license(self) -> bool:
        """Verifies if the stored license is valid for this machine."""
        try:
            if not (self.license_file.exists() and self.license_data_file.exists()): return False
            with open(self.license_file, 'r', encoding='utf-8') as f: license_key = f.read().strip()
            if not (self._validate_license_key_format(license_key) or license_key == self.MASTER_KEY): return False
            with open(self.license_data_file, 'rb') as f: encrypted_data = f.read()
            machine_id = self._get_machine_id()
            license_json = self._decrypt_data(encrypted_data, machine_id)
            if not license_json: return False
            license_data = json.loads(license_json)
            if license_data.get("machine_id") != machine_id: return False
            if license_data.get("key") != license_key: return False
            self._log("License verified successfully.")
            return True
        except Exception as e:
            self._log(f"License verification error: {e}"); return False
