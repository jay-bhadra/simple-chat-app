import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

#Creating a server where AF_INET is Internet socket and SOCK_STREAM is a TCP Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Binding the servver address to the Host and Port created earlier
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#Broadcast function - To send message to all the connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#Handle function - Individual handling connection after connected
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


#Receive function - Listen to new connections
def receive():
    while True:
        #creating a loop to accept newer client connections
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        #Requesting for nickname from the client
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        
        #Appending the nickname and client to the existing list
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start


print("Server running....")
receive()