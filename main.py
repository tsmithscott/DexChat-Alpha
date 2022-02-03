from modules.encryption.crypto import Crypto
import base64

# ( os.name == "nt" ) will return True if host OS is Windows
handler = Crypto(windows=True)

chat = open("crypt/chat.enc", "rb")

with chat:
    data = chat.read()

print(data)
print(base64.b64encode(data))
print(handler.decrypt(data))


