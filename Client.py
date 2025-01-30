import socket
import threading
from tkinter import *
from tkinter import ttk

def thread_input(client_socket, client_text):
    while True:
        temp = input().encode()
        if not temp:
            break
        client_socket.sendall(temp)

def broadcast(client_socket, client_text, client_entry, message):
    client_socket.sendall(message.encode())
    client_entry.delete(0, 'end')

def thread_receive(client_socket, client_text, user_text):
    user_lst = []
    temp = []
    connected = []
    dictionary = {}
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        if(data[0:7] == "USERS: "):
            if(len(str(user_text)) > 0):
                user_text.delete(1.0, 'end')
                temp = user_lst
                user_lst.clear()
                user_text.insert(END, "USERS:\n")
            index = 7
            for i in range(7,len(data)):
                if data[i] == ",":
                    user_lst.append(data[index:i])
                    index = i+2
                    i = i+2
            for x in user_lst:
                user_text.insert('end', x + "\n")
            connected = announce_connection(connected, user_lst, client_text)
        elif(data[0:14] == "DISCONNECTED: "):
            connected.remove(data[14:])
            client_text.insert('end', data[14:] + " left the chat.\n")
        else:
            client_text.insert('end', data + "\n")

def announce_connection(connected, user_lst, client_text):
    found = False
    for x in user_lst:
        for y in connected:
            if x == y:
                found = True
        if found == False:
            connected.append(x)
            client_text.insert('end', x + " connected to the server!\n")
        found = False
    return connected

def connect(root, IP, temp, username):
    print("Connecting")
    port = int(temp)
    client_socket = socket.socket()
    root.destroy()
    try:
        client_socket.connect((IP, port))
        client_socket.sendall(username.encode())
    except():
        print("Connection Failed")
    chat(client_socket)

def login():
    root = Tk(className = " Login")
    s = ttk.Style(root)
    s.configure("Pink.TLabel", background = "#fcb8f3")
    frame = ttk.Frame(root, padding = 20, style = "Pink.TLabel")
    frame.grid()
    label_zero = ttk.Label(frame, text = "Ashley's Chat App", style = "Pink.TLabel")
    label_one = ttk.Label(frame, text = "Enter IP:", style = "Pink.TLabel")
    label_two = ttk.Label(frame, text = "Enter Port:", style = "Pink.TLabel")
    label_three = ttk.Label(frame, text = "Username:", style = "Pink.TLabel")
    entry_IP = ttk.Entry(frame)
    entry_Port = ttk.Entry(frame)
    entry_Username = ttk.Entry(frame)
    button_one = ttk.Button(frame, text = "Connect to the Server!", command = lambda: connect(root, entry_IP.get(), entry_Port.get(), entry_Username.get()))

    entry_IP.insert(0, "192.168.1.73")
    entry_Port.insert(0, "50000")
    entry_Username.insert(0, "Ashley")

    label_zero.grid(row = 0, column = 0, columnspan = 2, pady=(0,10))
    label_one.grid(row = 1, column = 0, sticky = W)
    entry_IP.grid(row = 1, column = 1, sticky = E, pady=5)
    label_two.grid(row = 2, column = 0, sticky = W)
    entry_Port.grid(row = 2, column = 1, sticky = E, pady=5)
    label_three.grid(row = 3, column = 0, sticky = W)
    entry_Username.grid(row = 3, column = 1, sticky = E, pady=5)
    button_one.grid(row = 4, column = 0, columnspan = 2, pady = (20,0), sticky = NSEW)

    root.mainloop()

def chat(client_socket):
    root = Tk(className=" Chat")
    root.geometry("500x412")

    s = ttk.Style(root)
    s.configure("Pink.TLabel", background="#fbccfc")
    user_text = Text(root, height=20, width=20, background="#fa96fa", borderwidth=2)
    client_text = Text(root, width=30, background="#fcb3fc", borderwidth=2)
    scroll_bar = ttk.Scrollbar(root, orient=VERTICAL, command=client_text.yview)
    client_text.configure(yscrollcommand=scroll_bar.set)
    client_entry = ttk.Entry(root, width=20, style = "Pink.TLabel")
    client_button = ttk.Button(root, text = "Send", command = lambda: broadcast(client_socket, client_text, client_entry, client_entry.get()))

    user_text.grid(row=0, column=0, sticky="NSEW")
    client_text.grid(row=0, column=1, sticky="NSEW")
    scroll_bar.grid(row=0, column=2, sticky="NS")
    client_entry.grid(row=1, column=0, columnspan = 2, sticky="EW")
    client_button.grid(row=1, column=1, sticky="E")

    Grid.rowconfigure(root, 0, weight=0)
    Grid.rowconfigure(root, 1, weight=1)
    Grid.columnconfigure(root, 0, weight=0)
    Grid.columnconfigure(root, 1, weight=1)

    user_text.insert(END, "USERS:\n")
    client_text.insert(END, "START OF CHAT:\n")

    t1 = threading.Thread(target=thread_input, args=(client_socket, client_text))
    t2 = threading.Thread(target=thread_receive, args=(client_socket, client_text, user_text))
    t1.start()
    t2.start()

    root.mainloop()

login()