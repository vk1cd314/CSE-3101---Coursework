import socket

def is_prime(n):
    for i in range(2,n):
        if (n%i) == 0:
            return False
    return True

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
        res = 'Not a prime'
        try: 
            x = int(data)
            if is_prime(x): res = 'Is a Prime'
        except:
            res = 'Not an integer number'
            pass
        print("from connected user: " + str(data))
        conn.send(res.encode())

    conn.close()


if __name__ == '__main__':
    server_program()
