import dns.message
import dns.query
import dns.resolver
import dns.rdatatype
import re

def check_dns_record_type(record):
    a_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    aaaa_regex = r"[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7}"
    ns_regex = r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    cname_regex = r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    mx_regex = r"\d+ [a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if re.match(a_regex, record):
        return "A"
    elif re.match(aaaa_regex, record):
        return "AAAA"
    elif re.match(ns_regex, record):
        return "NS"
    elif re.match(cname_regex, record):
        return "CNAME"
    elif re.match(mx_regex, record):
        return "MX"
    else:
        return None

def iterative_resolve(domain, qtype):
    authoritative_servers = []
    query = dns.message.make_query(domain, qtype)
    response = None
    server = "127.0.0.1"

    while True:
        if authoritative_servers:
            new_domain = authoritative_servers.pop()
            qtype = check_dns_record_type(new_domain)
            if new_domain == "cse.du.ac.bd.":
                qtype = dns.rdatatype.NS
            elif qtype == "NS":
                qtype = "A"
            query = dns.message.make_query(new_domain, qtype)
            print(f"DEBUG: Querying {server} for {new_domain} ({qtype})\n\n")
        else:
            print(f"DEBUG: Querying {server} for {domain} ({qtype})\n\n")
        response = dns.query.udp(query, server, port=5050)
        print(f"DEBUG: Got response: {response}\n\n")

        if response.rcode() == dns.rcode.NOERROR:
            if len(response.authority) > 0:
                for rrset in response.authority:
                    if rrset.rdtype == dns.rdatatype.NS or rrset.rdtype == dns.rdatatype.CNAME:
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

print(iterative_resolve("cse.du.ac.bd.", dns.rdatatype.NS))
