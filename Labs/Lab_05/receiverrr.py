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


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('', 8888)
server_socket.bind(server_address)

server_socket.listen(1)

client_socket, client_address = server_socket.accept()

recv_buffer_size = 4
window_size = 4 * recv_buffer_size
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, recv_buffer_size)

expected_seq_num = 0
ack_num = 0

received_data = b''
buffer = {}

while True:
    header = client_socket.recv(12)
    if not header:
        break
    seq_num, ack_numm, ack, sf, rwnd = fromHeader(header)
    print(fromHeader(header))
    # if (seq_num, ack_numm, ack, sf, rwnd) == (0, 0, 0, 0, 0): break
    
    if ack_numm in buffer:
        buffer[ack_numm] += client_socket.recv(rwnd)
    else:
        buffer[ack_numm] = client_socket.recv(rwnd)
        
    while expected_seq_num in buffer:
        data = buffer.pop(expected_seq_num)
        received_data += data

        ack_num += len(data)
        expected_seq_num += len(data)

        to_send_ack = toHeader(expected_seq_num, ack_num, 1, 0, 12)
        client_socket.sendall(to_send_ack)

    if not data:
        break

print(received_data.decode())

client_socket.close()
server_socket.close()
