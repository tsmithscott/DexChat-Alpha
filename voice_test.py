import threading
import multiprocessing

from modules.network.voicenetwork import VoiceNetwork


app = VoiceNetwork("100.67.164.33", 25000)

sr = threading.Thread(target=app.server_receive, daemon=True)
cs = threading.Thread(target=app.client_send, daemon=True)
pv = threading.Thread(target=app.play_voice)

sr.start()
cs.start()
pv.start()

print(sr.ident)
