import threading

from modules.networking.node import Node
from modules.networking.server.node_server import NodeServer


handler = Node()
server = NodeServer(handler)
while True:
    try:
        conn, addr = server.sock.accept()
        handler.add_peer((conn, addr))
        t = threading.Thread(target=server.receive_message, args=(conn, addr))
        t.setDaemon(True)
        t.start()
    except KeyboardInterrupt:
        break
print("\nExiting...")
