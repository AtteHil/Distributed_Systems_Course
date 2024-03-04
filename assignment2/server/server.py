import socket
import threading
HEADER = 64
HOST = "127.0.0.1" #Localhost
PORT = 3570
DISCONNECT_MESSAGE = "!Quit"
ADDR = (HOST, PORT)
FORMAT = 'UTF-8'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_input(conn,addr):
    print(f"[CONNECTED] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Receive the full message
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                
                connected = False
            print(f"[{addr}] {msg}") # print out the message
            conn.send("Msg received".encode(FORMAT))
    print(f"[DISCONNECT] {addr} disconnected")
    conn.close()

def main():
    server.listen()
    print(f"[LISTENING] Server listening on {HOST}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_input, args=(conn, addr)) ## make new thread for incoming connection. 
        thread.start()
        print(f"[ACTIVE] {threading.active_count()-1}")


main()
