import socket
import threading

def handle(client):
    name = client.recv(1024).decode("utf8")
    welcome = "Welcome %s! Have fun." % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s ist teehee!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(1024)
        if msg != bytes("quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s broadcast." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8080))
server.listen()

print("Chatroom-Server started")

while True:
    client, addr = server.accept()
    print("%s teehee." % str(addr))
    client.send(bytes("nickname:", "utf8"))
    client_thread = threading.Thread(target=handle, args=(client,))
    client_thread.start()

server.close()
