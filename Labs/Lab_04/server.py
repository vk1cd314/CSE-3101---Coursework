import socket
import threading

mp = {
    'cs.du.ac.bd' : '192.0.2.3, A'
}

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def make_packet(dns_server_name):
    

def handle_client():
    connected = True
    while connected:
        msg, addr = server.recvfrom(512)
        if msg:
            print(f'yooo {mp[msg.decode()]}')
            print(f'{msg} from {addr}')
            server.sendto(f'{mp[msg.decode()]}'.encode(), addr)
    conn.close()

def start():
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        #conn, addr = server.accept()
        thread = threading.Thread(target=handle_client)
        thread.start()

print("Server is starting")
start()