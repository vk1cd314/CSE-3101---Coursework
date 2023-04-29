import socket
from queue import PriorityQueue
import threading
import time
import random
ERR = False
CNGTIME = 15
ME = 5005

graph = {
        5005 : [(5001, 12),(5002, 33)],
        5001 : [(5005, 12)],
        5002 : [(5005, 33)]
        }
dist = {}

def dijkstra():
    pq = PriorityQueue()
    dist.clear()
    for i in range(5001, 5006):
        dist[i] = 100000
    dist[ME] = 0
    pq.put((dist[ME], ME))
    while pq.qsize():
        d, u = pq.get()
        if dist[u] != d:
            continue
        # print(f"graph={graph}")
        # print(f"dist={dist}")
        for (v, w) in graph[u]:
            if v not in dist or dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pq.put((dist[v], v))
    
    print(f'Updated Distance Array {dist}')

def update_edge_cost(u, v, w):
    #print(f"keys{graph.keys()}")
    change = False
    if u not in graph.keys():
        graph[u] = []
        if (v, w) not in graph[u]:
            graph[u].append((v, w))
            change = True
    else:
        if (v, w) not in graph[u]:
            graph[u].append((v, w))
            change = True
        # elif w != graph[u][graph[u].index((v, w))][1]:
        #     graph[u][graph[u].index((v, w))][1] = w
        else:
            for (x, y) in graph[u]:
                if x == v:
                    if w != y:
                        change = True
                        graph[u][graph[u].index((x,y))] = (v, w)
            
    if v not in graph.keys():
        graph[v] = []
        if (u, w) not in graph[v]:
            graph[v].append((u, w))
            change = True
    else:
        if (u, w) not in graph[v]:
            graph[v].append((u, w))
            change = True
        else:
            for (x, y) in graph[v]:
                if x == u:
                    if w != y:
                        change = True
                        graph[v][graph[v].index((x,y))] = (u, w)

    if change:
        dijkstra()

def send():
    #print(f"graph={graph}")
    for (u, w) in graph[ME]:
        to_send = ''
        for v in graph.keys():
            for (x, y) in graph[v]:
                to_send += f'{x},{v},{y}\n'
        #print(f'{u} , {ME}')
        if u != ME:
            #print(f'Sending to {u} with {to_send}')
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
            #print(int(u))
                client.connect(('127.0.0.1',int(u)))
                client.send(to_send.encode())
                client.close()
            except:
                print("client conn refused")
                client.close()
            #sock.sendto(to_send.encode(), ('127.0.0.1', int(u)))

def receive(conn, addr):
    # try:
    #data, addr = sock.recvfrom(1024)
    data = conn.recv(1024).decode()
    lst = data.splitlines()
    #print(f"recieved{lst}")
    for info in lst:
        u, v, w = info.split(',')
        update_edge_cost(int(u), int(v), int(w))
    # except socket.timeout:
        # send(sock)
        # print(f'Timed Out')
def sent():
    while True:
        #print("in sent thread")
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

# sock.settimeout(5)
recThread = threading.Thread(target=recvt, args=())
recThread.start()
time.sleep(5)
senThread = threading.Thread(target=sent, args=())
senThread.start()

startTim = time.time()

while True:
    currTim = time.time()
    if ERR:
        if (currTim - startTim > CNGTIME):
            rankey = random.randint(5001, 5005)
            ranWt = random.randint(10, 100)
            startTim = time.time()
            for (u, v) in graph[ME]:
                if u == rankey:
                    graph[ME][graph[ME].index((u, v))] = (u, ranWt)
                    graph[u][graph[u].index((ME, v))] = (ME, ranWt)
    