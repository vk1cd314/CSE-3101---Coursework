import socket
import dns.message

def handle_request(data, client_address):
    request = dns.message.from_wire(data)
    response = dns.message.make_response(request)

    response.answer.append(dns.rrset.from_text("cse.du.ac.bd.",
                           300, dns.rdataclass.IN, dns.rdatatype.A, "192.0.2.3"))

    return response.to_wire()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 5050))
    print("Server starting on 127.0.0.1 on port 5050")
    while True:
        data, client_address = server_socket.recvfrom(4096)
        response = handle_request(data, client_address)
        server_socket.sendto(response, client_address)

run_server()
