from modules.communication import Network
import threading


app = Network("82.0.10.30", 25000)

threading.Thread(target=app.server_accept, daemon=True).start()
threading.Thread(target=app.client_send).start()
