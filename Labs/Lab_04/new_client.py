import dnslib
import socket

def send_dns_query(domain_name):
    query = dnslib.DNSRecord(q=dnslib.DNSQuestion(domain_name, qtype=1))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 5050)
    client_socket.sendto(query.pack(), server_address)
    data, _ = client_socket.recvfrom(4096)
    response = dnslib.DNSRecord.parse(data)
    return response

if __name__ == "__main__":
    domain_name = "cs.du.ac.bd"
    response = send_dns_query(domain_name)
    print(response)
