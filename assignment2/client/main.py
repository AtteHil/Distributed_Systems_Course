import socket
#Server information
HOST="127.0.0.1"
PORT = 3570
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!Quit"
HEADER = 64

ADDR = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect to server
client.connect(ADDR)



 
def main(msg): ## sneds msg to server
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

    


    
main("Hello World")
input()
main("Hello Matt")
input()
main("Hello Everyone")
input()
main(DISCONNECT_MESSAGE)