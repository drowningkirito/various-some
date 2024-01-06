import tkinter as tk
import ttkbootstrap as ttk
import socket
from threading import Thread

def receive_messages():
    while True:
        try:
            message = socket_client.recv(1024).decode("utf-8")
            chat_display.insert(tk.END, f"{message}\n")
            chat_display.see(tk.END)  # Scroll to the end
        except ConnectionAbortedError:
            break

# Create a Tkinter window
window = ttk.Window(themename="superhero")
photoimage = tk.PhotoImage(file="chat.png")
window.title("ChatApp")
window.iconphoto(False, photoimage)
window.geometry("600x650+400+0")
window.resizable(width=False, height=False)

# Create a socket for the client
socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((socket.gethostbyname(socket.gethostname()), 8888))

# Function to handle sending messages
def send_message():
    msg_server = enter_msg.get()
    socket_client.sendall(msg_server.encode("utf-8"))
    chat_display.insert(tk.END, f"You: {msg_server}\n")
    chat_display.see(tk.END)  # Scroll to the end
    enter_msg.delete(0, tk.END)  # Clear the entry after sending

# Configure window layout
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
# window.rowconfigure(1, weight=1)

# Create a Text widget for displaying messages
chat_display = tk.Text(window, wrap="word", state="normal", width=70, height=20)
chat_display.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Create an Entry widget for entering messages
enter_msg = ttk.Entry(window, width=70)
enter_msg.grid(row=1, column=0, sticky="sw")

# Create a Button for sending messages
send_button = ttk.Button(window, text="SEND", width=30, command=send_message)
send_button.grid(row=1, column=1, sticky="se")

# Create a thread to continuously receive messages from the server
receive_thread = Thread(target=receive_messages)
receive_thread.start()

# Main event loop
window.mainloop()
