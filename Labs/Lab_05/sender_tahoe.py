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

recv_buffer_size = 12
window_size = 4 * recv_buffer_size
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

expected_ack_num = 0

data = b'This is a sample message to test the flow control algorithm, it just needs to be long enough to test the flow control algorithm.'
data_len = len(data)

timeout = 0.5  # in seconds

def TCP_Tahoe(window_size, ack_num, expected_ack_num):
    ssthresh = window_size / 2  # initial slow start threshold
    rwnd = window_size
    seq_num = 0
    start_time = time.time()

    while expected_ack_num < data_len:
        send_size = min(window_size, data_len - expected_ack_num, rwnd)

        print(fromHeader(toHeader(seq_num, expected_ack_num, 1, 0, send_size)))
        print(data[seq_num:seq_num + send_size])
        client_socket.sendall(toHeader(seq_num, expected_ack_num, 1, 0, send_size) + data[seq_num:seq_num + send_size])

        ack_header = client_socket.recv(12)

        seqNum, ack_num, ack, sf, rwnd = fromHeader(ack_header)

        seq_num += send_size

        if ack_num == expected_ack_num: 
            # packet acknowledged
            expected_ack_num = ack_num + send_size

            if window_size >= ssthresh:
                # congestion avoidance phase
                window_size += 1 / window_size
            else:
                # slow start phase
                window_size *= 2

            # update the window size based on the receiver's advertised window
            window_size = min(rwnd, window_size)

        else:
            # packet lost or delayed
            ssthresh = max(window_size / 2, 1)
            window_size = 1
            seq_num = ack_num

        # update the timeout and start time
        timeout = max(0.5, 2 * (time.time() - start_time))
        start_time = time.time()

    return expected_ack_num

expected_ack_num = TCP_Tahoe(window_size, ack_num=expected_ack_num, expected_ack_num=expected_ack_num)

client_socket.close()
