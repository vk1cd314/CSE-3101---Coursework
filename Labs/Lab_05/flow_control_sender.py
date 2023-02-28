
import socket
import time

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


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 8888)
client_socket.connect(server_address)

header_length = 12
recv_buffer_size = 4
mss = 8
window_size = mss
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

seq_num = 0
expected_ack_num = 0

data = b'This is a sample message to test the flow control algorithm, it just needs to be long enough to test the flow control algorithm.'
data_len = len(data)

timeout = 2  
start_time = time.time()
rwnd = 50
sent_size = 0
dup_ack = 0
last_ack = 0

while seq_num < data_len:
    curr_sent_size = 0
    while curr_sent_size < window_size and seq_num < data_len:
        send_size = min(mss, data_len - seq_num)
        client_socket.sendall(toHeader(seq_num, seq_num, 0, 0, 0) + data[seq_num:seq_num+send_size])
        curr_sent_size += send_size 
        sent_size += send_size
        seq_num += send_size

    expected_ack_num = seq_num
    ack_pkt = client_socket.recv(header_length)
    seqNum, ack_num, ack, sf, rwnd = fromHeader(ack_pkt)

    window_size = min(2 * recv_buffer_size, rwnd)

    if ack_num == last_ack:
        dup_ack += 1
    else:
        dup_ack = 0
    if dup_ack == 3:
        print("Received Triple Duplicate Acknowledgement go back to last_ack")
        dup_ack = 0
        seq_num = last_ack

    last_ack = ack_num

client_socket.close()
