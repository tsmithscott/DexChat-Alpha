from modules.communication import VoiceNetwork
import threading


app = VoiceNetwork("100.118.187.57", 25000)

threading.Thread(target=app.server_receive, daemon=True).start()
threading.Thread(target=app.client_send, daemon=True).start()
threading.Thread(target=app.play_voice).start()

