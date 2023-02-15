import dns.message
import dns.query
import dns.resolver
import dns.rdatatype

def recursive_resolve(domain, qtype):
    query = dns.message.make_query(domain, qtype)
    response = None

    server = "127.0.0.1"

    print(f"DEBUG: Querying {server} for {domain} ({qtype})\n\n")
    response = dns.query.udp(query, server, port=5050)
    print(f"DEBUG: Got response: {response}\n\n")

    return response

print(recursive_resolve("cse.du.ac.bd.", dns.rdatatype.NS))
