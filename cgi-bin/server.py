from websocket_server import WebsocketServer
import types
import cgi
import cgitb
# cgitb.enable()
# print("Content-Type: text/html\n\n")
# form = cgi.FieldStorage()

PORT = 80
# PORT = form.getfirst("port")
HOST = "localhost"

# def new_client(client, server):
#     server.send_message_to_all("クライアントが接続されました"")


def send_msg_allclient(client, server, message):
    server.send_message_to_all("{}".format(
        message).encode('iso-8859-1').decode("utf-8"))
    print(message.encode('iso-8859-1').decode("utf-8"))
# print(client)


server = WebsocketServer(PORT, host=HOST)
# server.set_fn_new_client(new_client)
server.set_fn_message_received(send_msg_allclient)
server.run_forever()
