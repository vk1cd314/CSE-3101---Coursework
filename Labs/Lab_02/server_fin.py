import socket
import random
import threading
from threading import Timer
import time
import queue

users = {
    1:"password",
    2:"password2"
}
taka = {
    1: 1000,
    2: 2000
}
requests = {
    0: "" 
}

requestID = 1

THRESHOLD = 1000
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

global count_time 
count_time = 5
tOut = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

timer_active = False

def send(conn, msg):
    conn.send(msg.encode())
    #print(msg)

def sendTimed(conn, msg):
    timer_active = True
    conn.send(msg.encode())
    print(msg)

def start():
    server.listen()
    print(f"server is listening on {SERVER}, PORT::{PORT}")
    conn, addr = server.accept()
    connected = True
    print(f"{addr} connected.")
    #timer1 = RepeatTimer(2, sendTimed, [conn, "Withdrawn"])
    logged = False
    useridInp = False 
    prompted = False
    optSel = False
    timer_active = False
    while connected:
        print(useridInp, logged, prompted, optSel)
        if useridInp == False:
            send(conn, "Please enter your UserID")
        if logged == False or prompted == True: 
            data = conn.recv(1024).decode()
                
        if data:
            if "," in data:
                req_data = data.split(",")
                if int(req_data[0].strip()) in requests.keys():
                    send(conn, requests[int(req_data[0])])
                    continue
                else :
                    data = req_data[1]
            if data == "bye":
                connected = False
                print(f"{addr} disconnected.")
                conn.close()
            print(f"user {addr} input {data}")

            if useridInp == False:
                id = int(data)
                print(data)
                if id in users.keys():
                    useridInp = True
                else:
                    send(conn, "sorry wrong userId")
                send(conn, "pls type pass")
                continue
            
            if logged == False:
                print(data)
                if users[id] == data:
                    logged = True
                    send(conn, "Logged In\n")
                else:
                    send(conn, "sorry wrong password")
                continue
            
            if prompted == False:
                prompt = f"""You have {taka[id]} in account.
                What do you want to do?
                (1) withdraw money
                (2) deposit money
                (bye) exit
                """
                send(conn, prompt)
                prompted = True
                print("prompt for withdraw")
                continue
            
            if optSel == False:
                requestID = max(k for k, v in requests.items()) + 1
                optSel = True
                opt = int(data)
                if opt == 1:
                    send(conn, "Enter amount to withdraw ")
                    send(conn, f"requestId: {requestID}")
                else :
                    send(conn, "Enter amount to deposit")
                    send(conn, f" requestId: {requestID}")
                continue
            optSel = False
            prompted = False 
            
            if opt == 1:
                amount = float(data)
                if amount <= taka[id]:
                    taka[id] -= amount
                    confirmation = f"{amount} Withdrawn. Current Balance {taka[id]}"
                    requests.update({requestID : confirmation})
                    rando = random.randint(0,99)
                    if rando > THRESHOLD:
                        continue
                    send(conn, confirmation)
                else:
                    confirmation = "insufficeint funds"
                    send(conn, confirmation)
                    rando = random.randint(0,99)
                    if rando > THRESHOLD:
                        continue
                    requests.update({requestID : confirmation})
            else:
                amount = float(data)
                taka[id] += amount
                confirmation = f"{amount} Deposited. Current Balance {taka[id]}"
                requests.update({requestID : confirmation})
                rando = random.randint(0,99)
                if rando > THRESHOLD:
                    continue
                send(conn, confirmation)
    conn.close()

print("starting server")
start()