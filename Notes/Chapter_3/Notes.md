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
    Literally just select shit

