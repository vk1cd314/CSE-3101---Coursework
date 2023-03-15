import socket
import tqdm
import os

SERVER_HOST = ""
SERVER_PORT = 5002
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

arr = os.listdir('.')
print(arr)

client_socket.send(str(len(arr)).encode())

for str in arr:
    str = str + "\n"
    client_socket.send(str.encode())

filename = client_socket.recv(BUFFER_SIZE).decode()
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
s.close()