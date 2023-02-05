import socket
import struct

def get_name(data, offset):
    name = ""
    while True:
        length, = struct.unpack("!B", data[offset:offset + 1])
        if (length & 0xc0) == 0xc0:
            pointer, = struct.unpack("!H", data[offset:offset + 2])
            offset = pointer & 0x3fff
            return name + get_name(data, offset), offset + 2
        if (length & 0xc0) != 0:
            raise Exception("Not a valid DNS name")
        if length == 0:
            return name, offset + 1
        name += data[offset + 1:offset + 1 + length].decode() + "."
        offset += 1 + length

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = socket.gethostname()
port = 5050

msg = "cs.du.ac.bd"
msg = bytes(msg, 'utf-8')

sock.sendto(msg,(host, port))
data, addr = sock.recvfrom(512)
# Unpack the DNS response using struct format
query_id, flags, questions, answer_rrs, authority_rrs, additional_rrs = struct.unpack("!HHHHHH", data[:12])

# Parse the question section
offset = 12
question_name, question_type, question_class = "", 0, 0
for i in range(questions):
    qname, offset = get_name(data, offset)
    question_name = qname
    question_type, question_class = struct.unpack("!HH", data[offset:offset + 4])
    offset += 4

# Parse the answer section
answer_name, answer_type, answer_class, answer_ttl, answer_rdlength, answer_rdata = "", 0, 0, 0, 0, ""
for i in range(answer_rrs):
    aname, offset = get_name(data, offset)
    answer_name = aname
    answer_type, answer_class, answer_ttl, answer_rdlength = struct.unpack("!HHIH", data[offset:offset + 10])
    offset += 10
    if answer_type == 1:
        answer_rdata = socket.inet_ntoa(data[offset:offset + answer_rdlength])
    offset += answer_rdlength

# Print the parsed information
print("Query ID:", query_id)
print("Flags:", flags)
print("Questions:", questions)
print("Question Name:", question_name)
print("Question Type:", question_type)
print("Question Class:", question_class)
print("Answer RRS:", answer_rrs)
print("Answer Name:", answer_name)
print("Answer Type:", answer_type)
print("Answer Class:", answer_class)
print("Answer TTL:", answer_ttl)
print("Answer RD Length:", answer_rdlength)
print("Answer RDATA:", answer_rdata)
# print(header)
# questions_count = int.from_bytes(header[4:6], "big")
# print(questions_count)
# answer_count = int.from_bytes(header[6:8], "big")
# print(answer_count)
# for i in range(questions_count):
#     msg_question, addr = sock.recvfrom(512)
#     print(msg_question)

# for i in range(answer_count):
#     msg_answer, addr = sock.recvfrom(512)
#     print(msg_answer)
