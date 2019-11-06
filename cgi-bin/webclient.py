import time
from websocket import create_connection
import threading

ws = create_connection("ws://localhost:3000/")


def res_msg():
    result = ws.recv()
    print("Received '%s'" % result)


while True:
    thread = threading.Thread(target=res_msg)
    thread.start()
    msg = input()
    ws.send(msg)


ws.close()
