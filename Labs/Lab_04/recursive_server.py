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

def handle_request(data, client_address):
    request = dns.message.from_wire(data)

    response = dns.message.make_response(request)
    for item in request.question:
        domain_name, qtype = item.to_text().split(" IN ")
        if qtype == "NS":
            rrset = dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpNS[domain_name]);
            response.answer.append(rrset)
            rrset = dns.rrset.from_text(mpNS[domain_name], 86400, dns.rdataclass.IN, "A", mpA[mpNS[domain_name]]);
            response.answer.append(rrset)
            rrset = dns.rrset.from_text(mpNS[domain_name], 86400, dns.rdataclass.IN, "AAAA", mpAAAA[mpNS[domain_name]]);
            response.answer.append(rrset)
        elif qtype == "AAAA":
            rrset = dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpAAAA[domain_name]);
            response.answer.append(rrset)
        elif qtype == "CNAME":
            rrset = dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpCNAME[domain_name]);
            response.answer.append(rrset)
        elif qtype == "MX":
            rrset = dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpMX[domain_name]);
            response.answer.append(rrset)
        else:
            rrset = dns.rrset.from_text(domain_name, 86400, dns.rdataclass.IN, qtype, mpA[domain_name]);
            response.answer.append(rrset)
        print(f"DEBUG: Query for {domain_name} with type {qtype}")

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