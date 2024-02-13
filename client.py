import tkinter as tk
import socket
import threading

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:  # Have fun
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # English
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

top = tk.Tk()
top.title("Talky")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()
my_msg.set("input.")
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'
PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
tk.mainloop()
