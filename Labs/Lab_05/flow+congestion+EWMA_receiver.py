 
import socket
import time 
import random

def toHeader(seqNum=0, ackNum=0, ack=0, sf=0, rwnd=0):
    return seqNum.to_bytes(
        4, byteorder="little") + ackNum.to_bytes(
            4, byteorder="little") + ack.to_bytes(
                1, byteorder="little") + sf.to_bytes(
                    1, byteorder="little") + rwnd.to_bytes(
                        2, byteorder="little")

def fromHeader(segment):
    return int.from_bytes(
        segment[:4], byteorder="little"), int.from_bytes(
            segment[4:8], byteorder="little"), int.from_bytes(
                segment[8:9], byteorder="little"), int.from_bytes(
                    segment[9:10], byteorder="little"), int.from_bytes(
                        segment[10:12], byteorder="little")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8888)
server_socket.bind(server_address)

server_socket.listen(1)

client_socket, client_address = server_socket.accept()

recv_buffer_size = 16
window_size = 4 * recv_buffer_size
mss = 8
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

expected_seq_num = 0
ack_num = 0
start_time = time.time()
client_socket.settimeout(1)
timeout = 1
received_data = b''
buffer_data = b''
while True:
    try:
        header = client_socket.recv(12)
        seq_num, ack_num, ack, sf, rwnd = fromHeader(header)
    
        data = client_socket.recv(mss)
    except:
        rwind = recv_buffer_size - (len(buffer_data)+mss - 1)//mss
        to_send_ack = toHeader(expected_seq_num, ack_num, 1, 0, rwind)
        client_socket.sendall(to_send_ack)
        start_time = time.time()
        continue

    if not data:
        print("no data")
        break
    
    seq_num = ack_num
    
    if seq_num == expected_seq_num and random.randint(0, 2) != 0:
        buffer_data += data
        ack_num += len(data)
        expected_seq_num += len(data)
        to_send_ack = toHeader(seq_num, ack_num, 1, 0, 8)
        if(len(buffer_data)>=recv_buffer_size):
            received_data += buffer_data
            buffer_data = b''
            try:
                print("full buffer")
                client_socket.sendall(to_send_ack)
            except:
                print("client closed")
    else:
        to_send_ack = toHeader(expected_seq_num, expected_seq_num, 1, 0, 0)
        client_socket.sendall(to_send_ack)
        client_socket.sendall(to_send_ack)
        client_socket.sendall(to_send_ack)

print(received_data.decode())

client_socket.close()
server_socket.close()