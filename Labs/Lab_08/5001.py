import socket
from queue import PriorityQueue
import threading
import time
import random

ERR=False
INF = 100000
CNGTIME = 15

ME = 5001

cost = {}
dist_all = {}
broken_links = []

def init():
    for i in range(5001, 5006):
        cost[i] = {}
        dist_all[i] = {}
        for j in range(5001, 5006):
            cost[i][j] = INF
            cost[i][i] = 0
            dist_all[i][j] = INF
            dist_all[i][i] = 0
    
    cost[5001][5002] = 10

    cost[5001][5003] = 11
    
    cost[5001][5005] = 12

def bellman_ford():
    print(f'Updating the Distance array')
    cng = False
    for y in range(5001, 5006):
        for v in range(5001, 5006):
            cur = dist_all[ME][y]
            dist_all[ME][y] = min(dist_all[ME][y], cost[ME][v] + dist_all[v][y])
            if cur != dist_all[ME][y]:
                cng = True
    print(f'We now have {dist_all}')
    if cng:
        send()

def update_distance_vector(new_dist):
    sender = int(new_dist[0])
    old = dist_all[sender]
    for i in range(5001, 5006):
        dist_all[sender][i] = int(new_dist[i - 5000])

    for i in range(5001, 5006):
        if (cost[ME][i] != 0 or cost[ME][i] != INF) and i not in broken_links:
            if dist_all[i][ME] == INF:
                dist_all[i][sender] = INF
    
    bellman_ford()

def send():
    print('Sending')
    to_send = ''
    to_send += f'{ME} '
    for i in range(5001, 5006):
        if i != 5005:
            to_send += f'{dist_all[ME][i]} '
        else:
            to_send += f'{dist_all[ME][i]}'
    
    for u in range(5001, 5006):
        if (cost[ME][u] != 0 or cost[ME][u] != INF) and u not in broken_links:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client.connect(('127.0.0.1', int(u)))
                client.send(to_send.encode())
                client.close()
            except:
                print("client conn refused")
                for j in range(5001, 5006):
                    dist_all[j][u] = INF
                    dist_all[u][j] = INF
                broken_links.append(u)
                send()
                broken_links.pop()
            client.close()

def receive(conn, addr):
    data = conn.recv(1024).decode().split(' ')
    update_distance_vector(data)

def sent():
    while True:
        send()
        time.sleep(5)

def recvt():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', ME))
    sock.listen()
    print(f"server at{ME}")
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=receive, args=(conn, addr))
        thread.start()

init()

recThread = threading.Thread(target=recvt, args=())
recThread.start()
time.sleep(5)

bellman_ford()

startTim = time.time()

while True:
    currTim = time.time()
    if ERR:
        if (currTim - startTim > CNGTIME):
            rankey = random.randint(5001, 5005)
            ranWt = random.randint(1, 9)
            startTim = time.time()
            if rankey not in broken_links and cost[ME][rankey] != INF:
                cost[ME][rankey] = ranWt
                cost[rankey][ME] = ranWt
                bellman_ford()