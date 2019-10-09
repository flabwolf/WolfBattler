import socket
import time
import os,sys

#とりあえずの確認(あらかじめ建てた鯖とつなげるか？))
if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバを指定
        s.connect(('localhost', 3000))
        # サーバにメッセージを送る
        s.sendall(b'hello')
        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        data = s.recv(1024)
        #
        print(repr(data))
        time.sleep(3)