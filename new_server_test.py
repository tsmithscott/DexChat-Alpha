import threading

from modules.networking.node import Node


handler = Node()
server = handler.s_node
while True:
    try:
        conn, addr = server.server.accept()
        handler.add_peer((conn, addr))
        client = handler.c_node
        t = threading.Thread(target=server.listen, args=(conn, addr))
        t.setDaemon(True)
        t.start()
    except KeyboardInterrupt:
        break
print("\nExiting...")
