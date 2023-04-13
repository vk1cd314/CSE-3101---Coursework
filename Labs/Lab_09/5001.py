import socket
from queue import PriorityQueue
import threading
import time
import random

CNGTIME = 15

ME = 5001

forwardingTable = {
        # graph ta dekhtesi pore ;-;
        5002 : 5002,
        5003 : 5002
        }

ganjaTableKaronPrefix = {

}
ASpaths = {
    5002 : "1",
    5003 : "1"
}
eLinks = [6001]
iLinks = [5002, 5003]

ADPREF = 5000
ASN = 1


def query(dest):
    dest_pref = ((dest//1000) % 10) * 1000
    if dest_pref == ADPREF:
        print(f"in the same AS, nexthop = {forwardingTable[dest]}\n")
    if dest_pref in ASpaths.keys():
        print(f"In a connected AS, path to which is = {ASpaths[dest]}\n")
    else :
        print("host is unreachable\n")


    
def send(origin, dest, path, link_list):
    brk = "\n"
    next_hop = str(ME)
    to_send = dest + brk + origin + brk + path + brk + next_hop
    for u in link_list:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('127.0.0.1',int(u)))
            client.send(to_send.encode())
            client.close()
        except:
            print("client conn refused")
            client.close()

def update(dest, path, localpref, nexthop):
    ganjaTableKaronPrefix[dest] = (nexthop, localpref)
    ASpaths[dest] = path


def handleBGP(msg):
    origin = msg[1]
    dest = msg[0]
    path = msg[2]
    nexthop = msg[3]
    localpref = 100
    if msg.length() >= 5:
        localpref = msg[4]
    if dest in ganjaTableKaronPrefix.keys():
        if ganjaTableKaronPrefix[dest][1] < localpref:
            update(dest, path, localpref, nexthop)
        if len(ASpaths[dest]) > len(path):
            update(dest, path, localpref, nexthop)
    else :
        ganjaTableKaronPrefix[dest] = (msg[3], localpref)
        ASpaths[dest] = path
    if origin == "eBGP":
        if len(iLinks):
            send("iBGP", dest, path, iLinks)

    else :
        if len(eLinks):
            send("eBGP", dest, str(ASN)+" "+path, eLinks)
    
            

def receive(conn, addr):
    data = conn.recv(1024).decode()
    msg = data.splitlines()

    if str(ASN) in msg[2]:
        return 
    handleBGP(msg)



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



        