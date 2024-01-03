import socket
import threading
socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket_server.bind((socket.gethostbyname(socket.gethostname()),8888))
clients_socket=[]#appending mutiple client socket
clients_address=[]#appending multiple client address
socket_server.listen()
def handle_clients(client_socket,client_address):#handle clients runs as an argument using thread
    try:
        while True:
            msg=client_socket.recv(1024).decode("utf-8")
            if msg.lower()=="quit":
                clients_socket.sendall("Quting..".encode("utf-8"))
                break;

            send_msg(msg,client_socket,client_address)#taking every client message, address,socket for sending
        
    except Exception as e:
        print(f"{e}")
    finally:
        client_socket.close()
             
def connecting_clients():#connecting every clients
    while True:
        client_socket,client_address=socket_server.accept()
        clients_socket.append(client_socket)
        clients_address.append(client_address)
        print(f"Succesfullly connected to {client_address[0]}:{client_address[1]}")
        t1=threading.Thread(target=handle_clients,args=(client_socket,client_address)) 
        t1.start()  

def broadcast_msg():# use this function for broadcasting message to all clients
    for client in clients_socket:
        client.sendall("Hello".encode("utf-8"))

def send_msg(msg,client_socket,client_address):#for sending message from client to clients
    for sending in clients_socket:
        if client_socket!=sending:
            sending.sendall(f"{client_address[0]}:{msg}".encode("utf-8"))

if __name__=="__main__":
    connecting_clients()    
    