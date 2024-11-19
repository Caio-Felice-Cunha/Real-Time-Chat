from email import message
import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

rooms = {}

def broadcast(room, message):
    for i in rooms[room]:
        if isinstance(message, str):
            message = message.encode()
        i.send(message)

def sendMessage(name, room, client):
    while True:
        message = client.recv(1024)
        message = f'{name}: {message.decode()}\n'
        broadcast(room, message)

while True:
    client, addr = server.accept()
    
    client.send(b'SALA')
    room = client.recv(1024).decode()
    name = client.recv(1024).decode()
    
    if room not in rooms.keys():
        rooms[room] = []

    rooms[room].append(client)

    print(f'{name} has connected in the room {room}! INFO {addr}')

    broadcast(room, f'{name} just joined the room! \n')

    