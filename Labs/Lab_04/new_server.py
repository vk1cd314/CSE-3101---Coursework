import dnslib
import socket

mp = {
    "cs.du.ac.bd." : "192.0.2.1"
}

def handle_dns_request(data, address):
    request = dnslib.DNSRecord.parse(data)
    domain_name = request.q.qname
    response = dnslib.DNSRecord(dnslib.DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)
    response.add_answer(dnslib.RR(request.q.qname, ttl=60, rdata=dnslib.A(mp[str(domain_name)])))
    return response.pack()

def run_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 5050))

    print("DNS server is listening on port 53...")

    while True:
        data, address = server_socket.recvfrom(4096)
        response = handle_dns_request(data, address)
        server_socket.sendto(response, address)

if __name__ == "__main__":
    run_dns_server()
