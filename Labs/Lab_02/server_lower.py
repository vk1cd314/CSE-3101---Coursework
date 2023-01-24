import socket

def server_program():
    host = ""
    port = 5000

    server_socket = socket.socket() 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        conn.send(data.lower().encode())
    conn.close()

if __name__ == '__main__':
    server_program()
