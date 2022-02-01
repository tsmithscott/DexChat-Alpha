from modules.crypto import Crypto
import base64


handler = Crypto(windows=True)

chat = open("crypt/chat.enc", "wb")

with chat:
    chat.write(base64.b64encode(handler.encrypt("Hello World!")))
