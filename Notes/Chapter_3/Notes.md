## Transport Protocols

1. **TCP** $\Rightarrow$ Transmission Control Protocol
2. **UDP** $\Rightarrow$ User Datagram Protocol 

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

UDP $\Rightarrow$ needs a 2-tuple of the `Destination port` along with the `Source port` for the connectionless demuxing

TCP $\Rightarrow$ needs a 4-tuple of `Destination IP and Port` and `Source IP and Port` for the connection-oriented demuxing

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
Starting off with **rdt** short for reliable data transfer and **udt** for unreliable data transfer.

First `rdt_send()`, `udt_send()`, then `rdt_receive()` and finally `deliver_data()`.
First 2 work on host and last 2 on receiver.
**Control messages bi-directoinal but data flow only in one direction**

### rdt1.0
The finite state machine for rdt1.0 is as shown below for the sender and receiver:

![rdt1_sender](rdt1_sender.png "rdt1.0 sender fsm")
![rdt1_receiver](rdt1_receiver.png "rdt1.0 receiver fsm")

### rdt2.0
Now we try to recover from errors. To do this we introduce:
1. **ACKS** (Acknowledgements): Receiver explicitly tells the sender that the pkt has been received OK
2. **NAKS** (Negative Acknowledgements): Receiver explicitly tells the sender that the pkt had errors
3. Sender retransmits pkt in the case of a **NAK**

This is known as the **STOP AND WAIT PROTOCOL**

The Fsm for this is as below:

![rdt2_sender](rdt2_sender.png "rdt2.0 sender fsm")
![rdt2_receiver](rdt2_receiver.png "rdt2.0 receiver fsm")

BUUUUUUUUUUUUUTTTT, **ACKS** and **NAKS** too can be corrupted so this is a flaw for rdt2.0 and we can't just retransmit **ACKS** and **NAKS** since this could bring up the issue of duplicate packets being sent.

### rdt2.1
This is basically **rdt2.0** but can handle erronous **ACKS** and **NAKS** by adding a sequence number to each packet so that when retransmitting the **ACKS** or **NAKS** we don't have duplicates.

The fsm's are as below:

`Sender:`
![rdt2.1_sender](rdt2.1_sender.png "rdt2.1 sender fsm")
`Receiver:`
![rdt2.1_receiver](rdt2.1_receiver.png "rdt2.1 receiver fsm")

**ONLY ONE SEQ NO REQUIRED BECASUE STOP AND WAIT PROTOCOL SINCE ONLY 1 PACKET IS EVER IN TRANSMISSION**

### rdt2.2
Now we remove **NAKS** and thus our protocol will only have **ACKS**

Receiver will send **ACK** along with the seq no. of the packet being **ACKed**, what this changes is instead of checking for a **NAK** it will instead check for a **ACK** for the specific seq no, this basically works as a pseudo-**NAK**

### rdt3.0
Big leagues now boi, we can now handle channels with errors and loss. We achieve this by adding a reasonable timeout

1. Retransmit packet if no **ACK** received in time
2. if pkt or **ACK** is delayed
   1. Then retransmission will duplicate the pkt/**ACK** but seq no. gets rid of this issue
   2. receiver must specify seq no. being of packet being **ACKed**

The fsm for the receiver does not change, but for the sender there are new paths to follow for the timeout and new actions where we start and stop timers. 
![rdt3_sender](rdt3_sender.png "rdt3.0 sender fsm")

## Performance of Reliable Transfer Protocols
We define some terms:

$U_{sender}$ : `utilization`, i.e. the fraction of time sender is busy sending

$D_{trans}$ : `Transmission Delay`, which is nothing but $\frac{L}{R}$, where $L$ is packet size, and $R$ is the link speed.

$RTT$ : `Round Trip Time`

We have that:

$$U_{sender} = \frac{D_{trans}}{RTT + D_{trans}}$$

For a large RTT, the performance for this **STOP and WAIT** protocol is bad. But this is because we are waiting a long time for just 1 packet what we could instead do in the meanwhlie is send more packets specified in a certain window size, this is known as pipelinig.

But this requires more than 1-bit seq no. This is now implemented using the **GO-BACK-N** algorithm.

### GO-BACK-N 
What we do here is use a cumulative **ACK** where as the **cumulative** implies we check all **ACKs** for the window at once.