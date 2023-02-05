import socket
import threading

from dnslib import DNSHeader, DNSRecord, QTYPE, RR
from dnslib import * 

def encode_packet(header, questions, answers):
    packet = DNSRecord(header=header)
    for question in questions:
        packet.add_question(question)
    for answer in answers:
        packet.add_answer(answer)
    return packet.pack()

mp = {
    'cs.du.ac.bd' : '192.0.2.3, A'
}

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)

def make_header():
    header = b"\x00\x01\x01\x00\x00\x01\x00\x01\x00\x01\x00\x00"
    return header

def handle_client():
    connected = True
    while connected:
        msg, addr = server.recvfrom(512)
        if msg:
            print(f'yooo {mp[msg.decode()]}')
            print(f'{msg} from {addr}')
            header = DNSHeader(id=1, qr=0, opcode=0, aa=0, tc=0, rd=1, ra=0, z=0, rcode=0)

            # header = DNSHeader(id=1, qr=0, opcode='QUERY', aa=0, tc=0, rd=0, ra=0, z=0, rcode='NOERROR')
            questions = [DNSRecord.question("cs.du.ac.bd", QTYPE.A)]
            answers = [RR("cs.du.ac.bd", rdata=A(mp["cs.du.ac.bd"]), ttl=3600)]
            packet = encode_packet(header, questions, answers)
            server.sendto(packet, addr)
            # server.sendto(make_header(), addr)
            # server.sendto(f'Question {msg}'.encode(), addr)
            # server.sendto(f'Answer {mp["cse.du.ac.bd"]}'.encode(), addr)

def start():
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        #conn, addr = server.accept()
        thread = threading.Thread(target=handle_client)
        thread.start()

print("Server is starting")
start()