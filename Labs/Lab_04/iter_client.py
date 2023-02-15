import dns.message
import dns.query
import dns.resolver
import dns.rdatatype

def iterative_resolve(domain, qtype):
    authoritative_servers = []
    query = dns.message.make_query(domain, qtype)
    response = None

    while True:
        if authoritative_servers:
            server = "127.0.0.1"
            query = dns.message.make_query(authoritative_servers.pop(), "A")
            # break
        else:
            server = "127.0.0.1"

        print(f"DEBUG: Querying {server} for {domain} ({qtype})\n\n")
        response = dns.query.udp(query, server, port=5050)
        print(f"DEBUG: Got response: {response}\n\n")

        if response.rcode() == dns.rcode.NOERROR:
            if len(response.authority) > 0:
                for rrset in response.authority:
                    if rrset.rdtype == dns.rdatatype.NS:
                        for rdata in rrset:
                            authoritative_servers.append(str(rdata))
                print(f"DEBUG: Adding authoritative servers: {authoritative_servers}\n\n")
            else:
                break
        else:
            print(f"Error: {response.rcode()}\n\n")

        if not authoritative_servers:
            break

    return response

print(iterative_resolve("www.cse.du.ac.bd.", dns.rdatatype.CNAME))
