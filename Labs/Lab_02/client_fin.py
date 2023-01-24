import socket
import time
import threading
from threading import Timer
import random

THRESHOLD = 50
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5000
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

def send(msg):
    message = msg.encode()
    client.send(message)
    # print(msg)

while True:
    #thread = threading.Thread(target=display)
    #thread.start()
    data = client.recv(1024).decode()
    if data:
        if "requestId" in data:
            print(data)
            rID = data.partition("requestId:")[2]
            #print(rID+"requestID")
            inp = input('->')
            req = f"{rID},{inp}"
            #t = time.process_time()
            start = time.time()
            sendTd = RepeatTimer(1, send, [req])
            sendTd.start()
            reqLoop = True
            while reqLoop:
                data = client.recv(1024).decode()
                if data:
                    rando = random.randint(0,99)
                    if rando > THRESHOLD:
                        continue
                    sendTd.cancel()
                    print(data)
                    end = time.time()
                    #elapsed_time = time.process_time()-t
                    print(f"elapsed time: {end - start}")
                    reqLoop = False
            continue
        if ("Logged" in data) or ("Withdrawn" in data) or ("Deposited" in data) or (("Enter" in data)):
            print(data+"\n")
            continue
        else:
            print(data)
            inp = input('->')
            send(inp)