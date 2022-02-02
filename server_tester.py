from modules.networking.server import Server

s = Server("172.21.1.6", 25000)

while True:
    s.accept()
