---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Wireless networks

Since wireless network operates over "less concrete" medium, it is rather difficult for hosts to detect collisions as with [Ethernet](./ethernet.ipynb).

Thus, wireless networks adopt **carrier sense multiple access collision avoidance** (CSMA/CA) instead.

## Collision avoidance

### Hidden node problem

Consider three nodes: A, B and C.

B is in the range of A and C, but A and C are not in the range of each other.

Suppose that both A and C wants to transfer to B.

But since A and C are not within each other range, they won't know that the other is transmitting.

Thus, the frames would collide at B.

A and C are **hidden nodes** to each other, where they don't see each other, but can interfere with each other's transmission.

### Exposed node problem

Similarly, consider a situation with 4 nodes: A, B, C and D.

A and C are in the range of B, B and D are in the range of C, but A and C are not in the range of each other, and so are B and D.

Now suppose B wants to transmit to A, and C wants to transmit to D.

When B begins sending to A, C would also hear it as it is in range.
C may think that it is unsafe for it to begin transmitting to D as it is in the range of the B -> A transmission.

However, it is actually safe since A is outside the range of C, so it can actually safely transmit to D without causing any issue.

### Multiple access with collision avoidance

Thusly, our proposed solution accounted for the above situations in mind, and is as follows:

Sender and receiver exchanges control frames to each other before actual data transfer:
1. Sender sends _Request to Send_ (RTS) which includes how long the sender wants to use the medium for
2. Receiver replies with _Clear to Send_ (CTS) which echoes back the duration that was indicated


Nearby nodes will notice this control frames and act accordingly:
* If they see the CTS, they are too close to the receiver and thus will refrain from sending
* If they see the RTS but not the CTS, it means they are close to the sender, but far enough from the receiver, thus is clear to send

Senders do not detect RTS frame collision.
They only know a collision happened when they failed to receive the CTS frame.
They then retransmit using the [exponential backoff policy](./ethernet.ipynb#Transmit-algorithm).

## Distributed system

Since wireless is designed for mobility of the nodes, the standard defines some additional structure to accommodate for this.

Some nodes are free to move, while others are designated as **access points**, of which are connected to each other via the **distribution system**.

For wireless LAN, mobile nodes communicate to each other via the access points, and the access points are connected to each other via Ethernet or IP routers.

Even if two mobile nodes are in range of each other, the protocol dictates that they associate themselves with a certain access point.
Then communication between the nodes are forwarded to their access points who then forward it to the respective node via the distribution system.

### Scanning

A node selects an access point via **(active) scanning**:
1. node sends the _Probe_ frame
2. all access points in range replies with _Probe Response_
3. node selects one of the access point and sends it n _Association Request_
4. the access point replies with _Association Response_

This protocol occurs when a node initially joins a network, or if a node wants to change its access point, _ie_ when the connection with the current access point becomes weak.

Once a node changes its designated access point, the new access point will inform the old access point via the distribution system.

Each access point also periodically sends _Beacon_ frame, which advertizes its capabilities.
Any node can then send its _Association Request_ to designate it.
This is called **passive scanning**.


## Frame format

```
| Control | Duration | Addr1 | Addr2 | Addr3 | SeqCtrl | Add4 | Payload | CRC |
```

The control field consist of:
* type field which indicates if it is a RTS/CTS frame
* ToDS field to indicate if the request needs to go into the distribution system
* FromDS field to indicate if the request needs to comes out from the distribution system

The meaning of _Addr_ field will change depending on the setting of _ToDS_ and _FromDS_

The addresses are of the form:

```
ultimate destination - [intermediate sender] - [intermediate receiver] - original source
```

Both intermediate nodes are optional, _ie_ when two nodes communicate directly with each other without using access points.

_Addr1_ refers to the ultimate destination.
Then each subsequent address refers to the each existing host in the chain.


