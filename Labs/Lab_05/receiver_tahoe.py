import socket

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

def update_cwnd(cwnd, ssthresh, acked, cwnd_max):
    if cwnd < ssthresh:
        # slow start
        cwnd += acked
    else:
        # congestion avoidance
        cwnd += (acked / cwnd)
    if cwnd > cwnd_max:
        cwnd = cwnd_max
    return cwnd

def slow_start(cwnd):
    cwnd //= 2
    if cwnd < 1:
        cwnd = 1
    return cwnd

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8888)
server_socket.bind(server_address)

server_socket.listen(1)

client_socket, client_address = server_socket.accept()

recv_buffer_size = 12
window_size = 4 * recv_buffer_size
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

expected_seq_num = 0
ack_num = 0
cwnd = 1
ssthresh = window_size
cwnd_max = 64

received_data = b''
buffer = {}

while True:
    header = client_socket.recv(12)
    if not header:
        break
    seq_num, ack_numm, ack, sf, rwnd = fromHeader(header)
    print(fromHeader(header))
    
    if ack_numm in buffer:
        buffer[ack_numm] += client_socket.recv(rwnd)
    else:
        buffer[ack_numm] = client_socket.recv(rwnd)
        
    while expected_seq_num in buffer:
        data = buffer.pop(expected_seq_num)
        received_data += data

        acked = len(data)
        cwnd = update_cwnd(cwnd, ssthresh, acked, cwnd_max)

        ack_num += len(data)
        expected_seq_num += len(data)

        to_send_ack = toHeader(0, ack_num, 1, 0, 12)
        client_socket.sendall(to_send_ack)

        if cwnd >= ssthresh:
            # congestion avoidance
            to_send_rwnd = min(window_size, int(cwnd))
            to_send_sf = 0
        else:
            # slow start
            to_send_rwnd = rwnd
            to_send_sf = 1

        to_send_header = toHeader(expected_seq_num, ack_num, 0, to_send_sf, to_send_rwnd)
        print('yo what')
        print(fromHeader(to_send_header))
        client_socket.sendall(to_send_header)

    if not data:
        break

print(received_data.decode())

client_socket.close()
server_socket.close()
