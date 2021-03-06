#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

# This funtion is responsible for receiving the messages 
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "exit":
        client_socket.close()
        top.quit()

# This funtion is responsible for closing the chat window
def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("exit")
    send()

#Following is the graphical aspect of the chat box:
#Header of the chat box
top = tkinter.Tk()
top.title("Chat app!")

#Message frames
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=30, width=150, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

#Following is for the space to enter the message and send it through the "send" button
entry_field = tkinter.Entry(top, textvariable=my_msg, width=150)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(text="Send", command=send)
send_button.pack()

#Following is for the action on pressing the close button on the chat box
top.protocol("WM_DELETE_WINDOW", on_closing)

# This is the sockets part that connects the server and the client through sockets
HOST = '127.0.0.1' # local host (IP of the host)
PORT = 33000 #port of the host
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024 #Buffersize
ADDR = (HOST, PORT) #Assigning host Ip and port to ADDR as the variable

client_socket = socket(AF_INET, SOCK_STREAM) #Getting the client socket using AF_INET and SOCK_STREAM
client_socket.connect(ADDR)

#Initiating the Receive function
receive_thread = Thread(target=receive)
receive_thread.start()

# Starts GUI execution.
tkinter.mainloop()  
