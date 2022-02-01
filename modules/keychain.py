import keyring


class Keychain:
    def __init__(self):
        try:
            keyring.get_keyring()
        except RuntimeError as error:
            print(error)

    @staticmethod
    def store_keys(pub_key: str, priv_key: str) -> bool:
        try:
            keyring.set_password("sfe-cw1", pub_key, priv_key)

            with open("crypt/pub.enc", "w") as enc_file:
                enc_file.write(pub_key)

            return True
        except RuntimeError as error:
            print(error)

    @staticmethod
    def fetch_pub() -> str:
        try:
            with open("crypt/pub.enc", "r") as enc_file:
                return enc_file.read()
        except RuntimeError as error:
            print(error)

    @staticmethod
    def fetch_priv(pub_key: str):
        try:
            return keyring.get_password("sfe-cw1", pub_key)
        except RuntimeError as error:
            return False

    @staticmethod
    def add_auth(username: str, password_hash: str) -> bool:
        try:
            keyring.set_password("sfe-cw1", username, password_hash)
            return True
        except RuntimeError as error:
            print(error)

    @staticmethod
    def fetch_auth(username: str) -> str:
        try:
            return keyring.get_password("sfe-cw1", username)
        except RuntimeError as error:
            print(error)
