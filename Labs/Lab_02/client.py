import socket

def client_program():
    host = '10.33.2.77'  
    port = 5000 

    client_socket = socket.socket() 
    client_socket.connect((host, port))  

    message = input(" -> ")  
    while message.lower().strip() != 'end':
        client_socket.send(message.encode()) 
        data = client_socket.recv(1024).decode()  

        if not data:
            break

        print(data)  

        message = input(" -> ")  

    client_socket.close()

if __name__ == '__main__':
    client_program()