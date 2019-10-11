import socket
import random
import os,sys
import tkinter as tk
import threading
import msvcrt

class Client():
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.counter = 0
        self.me = random.randint(1,100)

    def cnct_server(self):
        print('YOUR ID is : {}'.format(self.me))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # サーバを指定
        self.sock.connect((self.host, self.port))
        thread = threading.Thread(target=self.send_massage,args=())
        thread.start()
        while True:
            try:
                data = self.sock.recv(4096)
                if data:
                    print(data.decode())
            except KeyboardInterrupt:
                break

    def send_massage(self):
        while True:
            key = ord(msvcrt.getch())
            if key == 13:
                self.counter += 1
                massage = 'This is CLIENT ID:' + "{0:02d}".format(self.me) + 'count: {}'.format(self.counter)
                # サーバにメッセージを送る
                #print(massage)
                self.sock.sendall(massage.encode())
            elif key == 27:
                break

#ローカル動作確認用
if __name__ == "__main__":
    host = 'localhost'
    port = 3000
    client = Client(host,port)
    client.cnct_server()