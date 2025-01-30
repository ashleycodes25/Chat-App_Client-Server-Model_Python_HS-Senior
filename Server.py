import socket
import threading
import logging
import time

class Client:
    def __init__(self, socket, name):
        self.socket = socket
        self.name = name


def broadcast(message):
    for c in clients:
        c.socket.sendall(message.encode())


def broadcast_users():
    user_lst = "USERS: "
    for c in clients:
        user_lst += c.name+", "
    for c in clients:
        c.socket.sendall(user_lst.encode())

def broadcast_user(user):
    for c in clients:
        c.socket.sendall(user.encode())


def talk_thread():
    while True:
        temp = input()
        if not temp:
            break
        msg = "Server: "+temp
        broadcast(msg)


def listen_thread(client):
    while True:
        try:
            data = client.socket.recv(1024).decode()
            temp = client.name+":"+" "+data
            print(temp)
            broadcast(temp)
        except Exception as e:
            # if not data:
            msg = "DISCONNECTED: " + client.name
            print(msg)
            clients.remove(client)
            broadcast(msg)
            broadcast_users()
            break

def accept_thread(server):
    server.listen()
    while True:
        conn, ip = server.accept();
        username = conn.recv(1024).decode()
        c = Client(conn, username)
        clients.append(c)
        broadcast_users()
        t3 = threading.Thread(target=listen_thread, args=(c,))
        t3.start()



clients = []
host = socket.gethostname()
port = 50000
IP = socket.gethostbyname(host)
server_socket = socket.socket()
print("Server on:", IP, port)
server_socket.bind((IP, port))
t1 = threading.Thread(target=accept_thread, args=(server_socket,))
t2 = threading.Thread(target=talk_thread, args=())
t1.start()
t2.start()
t1.join()
t2.join()