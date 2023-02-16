# import re
import socket
import dns.message

mpA = {
    "cse.du.ac.bd." : "192.0.2.3",
    "ns1.cse.du.ac.bd." : "192.0.2.1",
    "ns2.cse.du.ac.bd." : "192.0.2.2",
    "mail.cse.du.ac.bd." : "192.0.2.4"
}

mpNS = {
    "cse.du.ac.bd." : "ns1.cse.du.ac.bd."
}

mpAAAA = {
    "cse.du.ac.bd." : "2001:db8::3",
    "ns1.cse.du.ac.bd." : "2001:db8::1",
    "ns2.cse.du.ac.bd." : "2001:db8::2",
    "mail.cse.du.ac.bd." : "2001:db8::4"
}

mpCNAME = {
    "www.cse.du.ac.bd." : "cse.du.ac.bd."    
}

mpMX = {
    "cse.du.ac.bd." : "10 mail.cse.du.ac.bd."
}

def recurse(domain_name, qtype):
    ret = []
    if qtype == "A":
        ret.append(dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpA[domain_name]));
        return ret
    if qtype == "AAAA":
        ret.append(dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpAAAA[domain_name]));
        return ret
    if qtype == "MX":
        ret.append(dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpMX[domain_name]));
        return ret
    if qtype == "NS":
        ret.append(dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpNS[domain_name]));
        retrec = recurse(mpNS[domain_name], "A")
        for item in retrec:
            ret.append(item)
        return ret
    if qtype == "CNAME":
        ret.append(dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpCNAME[domain_name]));
        retrec = recurse(mpCNAME[domain_name], "NS")
        for item in retrec:
            ret.append(item)
        return ret
    return None

def handle_request(data, client_address):
    request = dns.message.from_wire(data)

    response = dns.message.make_response(request)
    for item in request.question:
        domain_name, qtype = item.to_text().split(" IN ")
        print(domain_name + " " + qtype)
        ret = recurse(domain_name, qtype)
        for item in ret:
            print(item)
            response.answer.append(item)

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