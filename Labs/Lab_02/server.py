import socket
import random

users = {
    1:"password",
    2:"password2"
}
taka = {
    1: 1000,
    2: 2000
}

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
    st = False
    logged_in = False
    while True:
        print("Shuru")
        if not st:
            print("here rn")
            data = conn.recv(1024).decode()
            print(data)
            if not data:
                break
            if str(data) == "start": st = True
        if not st: continue 
        prompt = "Give User ID:"
        conn.send(prompt.encode())
        data = conn.recv(1024).decode()
        try:
            x = int(data)
            if x in users.keys():
                prompt = "what is your password?"
                conn.send(prompt.encode())
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(data)
                if users[x] == str(data):
                    
                    prompt1 = "Logged In, please type continue to continue"
                    
                    print("userID "+str(x)+" logged in")
                    
                    conn.send(prompt1.encode())
                    data = conn.recv(1024).decode()
                    if data != "continue":
                        conn.close()
                        break

                    logged_in = True

                    print("userID "+str(x)+" logged in")
                    prompt  = "account info" + "you have "+str(taka[x])+" taka " + "what do you want to do?\n 1: Withdraw\n 2: Deposit" 
                    conn.send(prompt.encode())
                    data = conn.recv(1024).decode()
                    if data == '1':
                        prompt = "How much?"
                        conn.send(prompt.encode())
                        data = conn.recv(1024).decode()

                        try:
                            xx = int(data)
                            taka[x] -= xx
                            if taka[x] < 0:
                                taka[x] += xx
                                prompt = "You dont have enough money to withdraw"
                                conn.send(prompt.encode())
                                conn.close()
                                break
                            prompt = str(xx) + " has been withdrawn, Current Balance " + str(taka[x])
                            conn.send(prompt.encode())
                        except:
                            conn.close()
                            break
                    elif data == '2':
                        prompt = "How much?"
                        conn.send(prompt.encode())
                        data = conn.recv(1024).decode()
                        try:
                            xx = int(data)
                            taka[x] += xx
                            prompt = str(xx) + " has been deposited, Current Balance " + str(taka[x])
                            conn.send(prompt.encode())
                        except:
                            conn.close()
                            break
                    else:
                        conn.close()
                        break
                else:
                    prompt = "Wrong Pass. Please type retry to retry"
                    conn.send(prompt.encode())
                    data = conn.recv(1024).decode()
                    if data == "retry": 
                        continue
                    else:
                        conn.close() 
                        break 
                    print("userID "+x+" attempted to log in")
            else:
                prompt = "No such user ID exists. Please type retry to retry"
                conn.send(prompt.encode())
                data = conn.recv(1024).decode()
                if data == "retry": 
                    continue
                else:
                    conn.close() 
                    break    
        except:
            prompt = "Not a correct user ID. Please type retry to retry"
            conn.send(prompt.encode())
            data = conn.recv(1024).decode()
            if data == "retry": 
                continue
            else:
                conn.close() 
                break 
    conn.close()


if __name__ == '__main__':
    server_program()
