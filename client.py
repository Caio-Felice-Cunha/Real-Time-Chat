#from email import message
import os
os.environ['TCL_LIBRARY'] = 'C:/Users/caiof/AppData/Local/Programs/Python/Python313/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Users/caiof/AppData/Local/Programs/Python/Python313/tcl/tk8.6'

import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

class ChatClient:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 55555

        self.root = tk.Tk()
        self.root.title('Chat Application')
        self.root.geometry("800x600")

        self.setup_login()

    def setup_login(self):
        # Login dialog
        self.name = simpledialog.askstring('Name', 'Enter your name', parent=self.root)
        self.room = simpledialog.askstring('Room', 'Enter room name', parent=self.root)
        
        if not self.name or not self.room:
            messagebox.showerror("Error", "Name and Room are required!")
            self.root.quit()
            return

        # Connect to server
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.HOST, self.PORT))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            self.root.quit()
            return

        self.setup_ui()
        self.start_listening()

    def setup_ui(self):
        # Chat display area
        self.text_box = scrolledtext.ScrolledText(self.root, state='disabled')
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Message input area
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.send_message = tk.Entry(input_frame, width=50)
        self.send_message.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        send_btn = tk.Button(input_frame, text='Send', command=self.send_message_handler)
        send_btn.pack(side=tk.RIGHT)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_listening(self):
        # Send room and name
        self.client.send(self.room.encode())
        self.client.send(self.name.encode())

        # Start listening thread
        listen_thread = threading.Thread(target=self.receive_messages, daemon=True)
        listen_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024)
                if not message:
                    break
                
                # Update text box safely
                self.root.after(0, self.update_text_box, message.decode())
            except Exception as e:
                messagebox.showerror("Connection Error", f"Lost connection: {e}")
                break

        self.on_closing()

    def update_text_box(self, message):
        self.text_box.configure(state='normal')
        self.text_box.insert(tk.END, message)
        self.text_box.see(tk.END)
        self.text_box.configure(state='disabled')

    def send_message_handler(self):
        message = self.send_message.get()
        if message:
            try:
                self.client.send(message.encode())
                self.send_message.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Send Error", f"Could not send message: {e}")

    def on_closing(self):
        try:
            self.client.close()
        except:
            pass
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.run()