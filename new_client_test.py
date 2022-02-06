import threading

from modules.networking.node import Node


handler = Node()
client = handler.c_node
client.connect(("172.21.3.218", 25574))
t = threading.Thread(target=client.listen)
t.setDaemon(True)
t.start()

