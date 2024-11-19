import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

rooms = {}

def broadcast(room, message):
    """Broadcasts a message to all clients in a given room."""
    for client in rooms.get(room, []):
        try:
            client.send(message.encode() if isinstance(message, str) else message)
        except Exception as e:
            print(f"Failed to send message: {e}")
            continue

def handle_client(name, room, client):
    """Handles messages from a specific client."""
    try:
        while True:
            message = client.recv(1024)
            if not message:
                break  # Client disconnected
            broadcast(room, f"{name}: {message.decode(errors='ignore')}\n")
    except Exception as e:
        print(f"Error handling client {name}: {e}")
    finally:
        remove_client(name, room, client)

def remove_client(name, room, client):
    """Removes a client from the room and closes the socket."""
    if room in rooms:
        rooms[room].remove(client)
        broadcast(room, f"{name} has left the room.\n")
        print(f"{name} disconnected from room {room}.")
    client.close()

def main():
    """Main server loop for accepting and handling clients."""
    print(f"Server is listening on {HOST}:{PORT}...")
    while True:
        try:
            client, addr = server.accept()
            print(f"Connection from {addr}")

            # Initialize client
            client.send(b"ROOM")
            room = client.recv(1024).decode(errors='ignore').strip()
            name = client.recv(1024).decode(errors='ignore').strip()

            # Create room if it doesn't exist
            if room not in rooms:
                rooms[room] = []

            rooms[room].append(client)
            print(f"{name} joined room {room} from {addr}")

            broadcast(room, f"{name} just joined the room!\n")

            # Start thread for client
            threading.Thread(target=handle_client, args=(name, room, client), daemon=True).start()
        except Exception as e:
            print(f"Error accepting client: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.close()