import socket
import threading
import struct

mp = {
    'cs.du.ac.bd' : '192.0.2.3'
}

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def make_dns_packet(host_name):
    query_id = 0x0001
    flags = 0x0100
    questions = 1
    answer_rrs = 1
    authority_rrs = 0
    additional_rrs = 0

    hostname = host_name.encode()
    qtype = 1
    qclass = 1

    answer_name = hostname
    answer_type = 1
    answer_class = 1
    answer_ttl = 60
    answer_rdlength = 4
    answer_rdata = socket.inet_aton(mp[host_name])

    packet = struct.pack("!HHHHHH", query_id, flags, questions, answer_rrs, authority_rrs, additional_rrs) + hostname + struct.pack("!HH", qtype, qclass) + answer_name + struct.pack("!HHIH4s", answer_type, answer_class, answer_ttl, answer_rdlength, answer_rdata)
    return packet

def handle_client():
    connected = True
    while connected:
        msg, addr = server.recvfrom(512)
        if msg:
            print(f'yooo {mp[msg.decode()]}')
            print(f'{msg} from {addr}')
            server.sendto(make_dns_packet(msg.decode()), addr)

def start():
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        thread = threading.Thread(target=handle_client)
        thread.start()

print("Server is starting")
start()