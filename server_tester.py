from modules.networking.server import Server

c = Server("172.21.1.6", 25000)

while True:
    c.receive_message()
