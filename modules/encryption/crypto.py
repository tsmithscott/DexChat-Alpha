import os
import sys

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from modules.encryption.keychain import Keychain


class Crypto:
    def __init__(self):
        self.pub_key = None
        self.pub_key_instance = None

        try:
            self.keychain = Keychain()

            if self.key_exists():
                self.pub_key = self.keychain.fetch_pub()
            else:
                if sys.platform == "win32":
                    self.generate_key(1024)
                else:
                    self.generate_key(4096)
        except RuntimeError as error:
            print(error)

    def generate_key(self, size: int):
        # Generate key objects
        priv_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=size,
            backend=default_backend()
        )

        self.pub_key_instance = priv_key.public_key()

        # Generate key strings
        priv_key = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        self.pub_key = self.pub_key_instance.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        ).decode()

        self.keychain.store_keys(self.pub_key, priv_key)

        del priv_key

    @staticmethod
    def key_exists() -> bool:
        if os.path.exists("crypt/pub.enc"):
            with open("crypt/pub.enc", "r") as enc_file:
                if len(enc_file.read()) > 1:
                    return True
                else:
                    return False
        else:
            return False

    def load_pub_key(self):
        if not self.pub_key_instance:
            self.pub_key_instance = serialization.load_pem_public_key(
                self.pub_key.encode(),
                backend=default_backend()
            )
        else:
            pass

    def load_priv_key(self):
        priv_key = serialization.load_pem_private_key(
            self.keychain.fetch_priv(self.pub_key).encode(),
            password=None,
            backend=default_backend()
        )

        return priv_key

    def encrypt(self, data: str) -> bytes:
        self.load_pub_key()

        data = self.pub_key_instance.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return data

    def decrypt(self, data: bytes) -> bytes:
        key = self.load_priv_key()
        data = key.decrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return data
