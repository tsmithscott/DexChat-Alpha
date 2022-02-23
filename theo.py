from modules.communication import VoiceNetwork
import threading


app = VoiceNetwork("82.0.10.30", 25000)

threading.Thread(target=app.server_receive(), daemon=True).start()
threading.Thread(target=app.client_send, daemon=True).start()
