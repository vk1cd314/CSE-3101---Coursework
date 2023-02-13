import socket
import tqdm
import os
import threading

SERVER_HOST = ""
SERVER_PORT = 5002
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))

def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    while connected:
        arr = os.listdir('.')
        print(arr)

        client_socket.send(str(len(arr)).encode())

        for st in arr:
            st = st + "\n"
            client_socket.send(st.encode())

        filename = client_socket.recv(BUFFER_SIZE).decode()
        if filename == "quit": 
            connected = False
            break
        filesize = os.path.getsize(filename)

        print(filename, filesize)

        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
                progress.update(len(bytes_read))
    client_socket.close()

def start():
    s.listen()
    print(f"[LISTENING] Server is listening on {SERVER_HOST}:{SERVER_PORT}")    
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()