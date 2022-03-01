#!/usr/bin/env python3

#TCP used over UDP as for this purpose we need an established connection whereas UDP sockets are helpful for actions without any active connections, for example, emails
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

#Setting up constants for later use       
clients = {}
addresses = {}

HOST = '127.0.0.1' # It is the local host (local system IP), so the chat works locally, not on the Internet; 
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# This funtion is continuously running and accepting the new clients
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings MCSBT! Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

# This funtion takes the client socket as an argument and enables the client to join the chat
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    #saving the name of the client
    name = client.recv(BUFSIZ).decode("utf8")
    #sending a welcome message to the client
    welcome = 'Welcome %s! If you ever want to quit, type exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))  # broadcasts the message to all the other clients
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("exit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("exit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

# This funtion is responsible for broadcasting the message to all the clients 
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

# This part connects the server and the client together by assigning the HOST IP and PORT to the server through sockets
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
