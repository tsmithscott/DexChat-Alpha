from modules.communication import SingleConnection
import threading


app = SingleConnection("82.0.10.30", 25000)

threading.Thread(target=app.server_accept).start()
threading.Thread(target=app.client_send).start()
