import socket
from queue import PriorityQueue
import threading
import time
import random

CNGTIME = 15

ME = 7001

localPrefTable = {
    1 : 100,
    2 : 100,
    3 : 100,
    4 : 100
}

forwardingTable = {
        # graph ta dekhtesi pore ;-;
        }

prefixTable = {

}
ASpaths = {
}
eLinks = [5001]
iLinks = [7002, 7003, 7004]

ADPREF = 7000
ASN = 3


def query(dest):
    dest_pref = (dest//1000) * 1000
    if dest_pref == ADPREF:
        print(f"in the same AS, nexthop = {forwardingTable[dest]}\n")
    if dest_pref in ASpaths.keys():
        print(f"In a connected AS, path to which is = {ASpaths[dest]}\n")
    else :
        print("host is unreachable\n")


    
def send(origin, dest, path, link_list):
    brk = "\n"
    next_hop = str(ME)
    to_send = str(dest) + brk + origin + brk + path + brk + next_hop
    for u in link_list:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('127.0.0.1',int(u)))
            client.send(to_send.encode())
            client.close()
        except:
            print("client conn refused")
            client.close()


def sendPref(dest, path, localPref):
    brk = "\n"
    next_hop = str(ME)
    to_send = str(dest) + brk + "iBGP" + brk + path + brk + next_hop + brk + str(localPref)
    for u in iLinks:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(('127.0.0.1',int(u)))
            client.send(to_send.encode())
            client.close()
        except:
            print("client conn refused")
            client.close()

def update(dest, path, localpref, nexthop):
    prefixTable[dest] = (nexthop, localpref)
    ASpaths[dest] = path


def handleBGP(msg):
    hasPref = False
    origin = msg[1]
    dest = msg[0]
    path = msg[2]
    nexthop = msg[3]
    localpref = 100
    if msg[1] != "iBGP":
        src = int(msg[2][0])
        if src in localPrefTable.keys():
            if localPrefTable[src] != 100:
                localpref = localPrefTable[src]
                hasPref = True
    if len(msg) >= 5:
        localpref = int(msg[4])
        hasPref = True
    print(f"Destination: {dest}\nOrigin: {origin}\nASpath: {path}\nNextHop: {nexthop}\nlocalPreference: {localpref}\n")
    if dest in prefixTable.keys():
        if ASpaths[dest] == path:
            return
        print(prefixTable)
        if int(prefixTable[dest][1]) < localpref:
            update(dest, path, localpref, nexthop)
        elif len(ASpaths[dest]) > len(path):
            update(dest, path, localpref, nexthop)
    else :
        prefixTable[dest] = (nexthop, localpref)
        ASpaths[dest] = path
    print(ASpaths)
    print(prefixTable)
    if origin == "eBGP":
        if len(iLinks):
            print("sending ebgp info to iLinks")
            if hasPref:
                sendPref(dest, path,  localpref)
            else:
                send("iBGP", dest, path, iLinks)
        if len(eLinks):
            print("sending ebgp to other eLinks")
            send("eBGP", dest, str(ASN)+" "+path, eLinks)

    else :
        if len(eLinks):
            print("sending to eLinks cause it is ibgp")
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
send("eBGP", ADPREF, str(ASN), eLinks)



        