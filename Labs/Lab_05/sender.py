
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

recv_buffer_size = 4
window_size = 4 * recv_buffer_size
mss = 8
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

seq_num = 0
expected_ack_num = 0

data = b'This is a sample message to test the flow control algorithm, it just needs to be long enough to test the flow control algorithm.'
data_len = len(data)

timeout = 2  # in seconds
start_time = time.time()

# while expected_ack_num < data_len:

#     send_size = min(window_size, data_len - expected_ack_num)

#     client_socket.sendall(toHeader(seq_num, expected_ack_num, 1, 0, send_size) + data[seq_num:seq_num + send_size])
    
#     ack_header = client_socket.recv(12)
    
#     seqNum, ack_num, ack, sf, rwnd = fromHeader(ack_header)

#     seq_num += send_size
#     expected_ack_num = ack_num
    
#     if time.time() - start_time > timeout:
#         seq_num = expected_ack_num
#         start_time = time.time()

sent_size = 0
while sent_size < data_len:
    curr_sent_size = 0
    while curr_sent_size < window_size or sent_size < data_len:
        send_size = min(mss, data_len - mss)
        client_socket.sendall(toHeader(seq_num, seq_num, 1, 0, 0) + data[seq_num:seq_num+send_size])
        curr_sent_size += send_size 
        sent_size += send_size
        seq_num += send_size
    ack_pkt = client_socket.recv(12)
    seqNum, ack_num, ack, sf, rwnd = fromHeader(ack_pkt[:12])
    expected_ack_num = ack_num
    while rwnd == 0:
        seq_num = ack_num
        client_socket.sendall(toHeader(seq_num, ack_num, 1, 0, 0)  + data[seq_num:seq_num+send_size])
        ack_pkt = client_socket.recv(12)
        seqNum, ack_num, ack, sf, rwnd = fromHeader(ack_pkt[:12])
    if time.time() - start_time > timeout:
        seq_num = expected_ack_num
        start_time = time.time()



client_socket.close()
