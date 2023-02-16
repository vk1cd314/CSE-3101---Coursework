## Transport Protocols

1. **TCP** $\rightarrow$ Transmission Control Protocol
2. **UDP** $\rightarrow$ User Datagram Protocol 

What we basically have is a form of **logical communication** between the sender and receiver to achieve lossless data transmission on a noisy channel.

## Sender
 Breaks up the message into segments and adds necessary headers and then transmits them based on some algorithm and passes it to the Network Layer.

## Receiver
 Reassembles the segments into messages and check the header for stuff and demux the message onto approriate application layer socket.

This is what happens to send and receieve messages from 2 hosts, we implement this transport using either TCP or UDP.

## TCP
1. Reliable, in-order delivery
2. Congestion Control
3. Flow Control
4. Connection Setup

## UDP
1. Unreliable, un-ordered delivery 
2. Extension of **"best-effort"** IP

### Transport Layer Muxing and Demuxing
Literally just select shit.
1. Multiplexing at sender works by taking data from multiple sockets and transport headers.
2. Demultiplexing at receiver works by using header info to send recieved packages to correct sockets.

Datagrams have Source IP and ports and Destination IP and ports, as can be seen in the TCP/UDP segment format. The host uses these information to direct segment to appropriate segment.

![seg_form](seg_format.png "TCP/UDP segment format")

UDP $\rightarrow$ needs a 2-tuple of the `Destination port` along with the `Source port` for the connectionless demuxing

TCP $\rightarrow$ needs a 4-tuple of `Destination IP and Port` and `Source IP and Port` for the connection-oriented demuxing

## Connection-Less Transport UDP
UDP is defined in **RFC 768** which you can find [here](https://www.rfc-editor.org/rfc/rfc768)
1. No handshaking
2. Each segment handled differently 
3. "Best Effort"
4. No congestion control
5. Small header size

### Use-cases for UDP
1. Streaming Multimedia
2. DNS
3. SNMP
4. HTTP/3

Reliability and congestion control can be added in application layer if needed

**UDP HEADER IS 8 BYTES** (**IMPORTANT**)
![udp_seg_format](udp_seg_format.png "UDP Segment Format")

### UDP Checksum
Literally just the checksum, used to check 1-bit errors. UDP treats whole contents as 16-bit integers and then checksums on those.

## Reliable Data Transfer