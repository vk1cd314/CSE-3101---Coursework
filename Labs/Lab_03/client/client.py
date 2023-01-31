import socket
import tqdm
import os
import pickle

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 
host = "localhost"

port = 5002

s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")
data = s.recv(BUFFER_SIZE).decode()
data = s.recv(BUFFER_SIZE).decode()
if data :
    print(data)
fn = input("select file by name ->")
s.send(fn.encode())
received = s.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        bytes_read = s.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

s.close()