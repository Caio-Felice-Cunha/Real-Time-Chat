import socket

HOST = '127.0.0.1'
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


message = client.recv(1014)

if message == b'SALA':
    client.send(b'Dota')
    client.send(b'Caio')

