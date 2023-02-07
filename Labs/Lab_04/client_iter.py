# import socket
# from dnslib import DNSRecord, DNSHeader, RR, QTYPE

# class IterativeDNSClient:
#     def __init__(self, server_ip, server_port):
#         self.server_ip = server_ip
#         self.server_port = server_port

#     def resolve(self, domain_name):
#         request = DNSRecord(DNSHeader(id=0, qr=0, aa=0, ra=0), q=RR(domain_name, qtype=QTYPE.A))
#         response = None
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.sendto(request.pack(), (self.server_ip, self.server_port))
#         data, _ = sock.recvfrom(512)
#         response = DNSRecord.parse(data)
#         if response.header.rcode == 0:
#             # The resolution was successful
#             answer = response.a
#             if answer:
#                 return answer.rdata
#             else:
#                 raise Exception("No answer found in response")
#         else:
#             raise Exception("Resolution failed with error code: {}".format(response.header.rcode))

# # Example usage
# client = IterativeDNSClient("localhost", 53)
# address = client.resolve("www.google.com")
# print("Address:", address)
import socket
from dnslib import DNSRecord, DNSHeader, QTYPE

def send_request(server, domain):
    request = DNSRecord(DNSHeader(id=0, qr=0, aa=0, rd=1, qdcount=1), q=DNSRecord.question(domain, QTYPE.A))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(request.pack(), (server, 53))
    data, _ = sock.recvfrom(512)
    response = DNSRecord.parse(data)
    return response

server = "127.0.0.1" # Change to the IP address of the DNS server you want to query
domain = "google.com" # Change to the domain name you want to query

response = send_request(server, domain)
if response.header.rcode == 0:
    for rr in response.rr:
        print("{} {} {}".format(rr.rname, rr.rtype, rr.rdata))
else:
    print("Error: {}".format(response.header.rcode))
