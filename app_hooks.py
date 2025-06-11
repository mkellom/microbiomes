from threading import Thread
from . import data_load

def on_server_loaded(server_context):
    t = Thread(target=data_load, args=(), daemon=True)
    t.start()