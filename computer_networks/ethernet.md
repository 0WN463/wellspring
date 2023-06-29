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

# Ethernet

Ethernet adapter receives all the frames in the network, and accepts frames that are addressed to:
* itself
* broadcast address
* multicast address

(or all frames if operating in promiscuous mode)

Since many hosts shares the same Ethernet wire, collision can happen and corrupt both senders messages.

Thus, Ethernet adopts **carrier sense multiple access - collision detection** (CSMA-CD).

Carrier sense: host can detects if the link is in use

Collision detection: host can detect if the frames its transmitting collides with another hosts frames


## CSMA persistence

When the host is ready to send, it will keep monitoring the wire.
Once it notices that the wire is idle, in a $p$-persistent CSMA, it will transmit its frame with a probability of $p$.

Ethernet uses a 1-persistent CSMA.

## Transmit algorithm

If the link is busy, wait for it to be idle.
If the line is idle, immediately transmit, with an upper bound on message size of 1500bytes

If collision is detected, transmit a 64 bit preamble followed by a 32 bit jamming sequence, then stop transmitting.

If it is the i-th consecutive collision, it selects a random integer in $[0, 2^i - 1]$, and wait that number of slots before transmitting.
Usually each slot is $51.2\micro s$

This repeats up until a certain limit (usually 16) before giving up.


## Minimum frame size

A frame must be at least 64 bytes long:
* 14 byte header
* 46 byte data
* 4 byte CRC

A host needs to transmit for at least RTT for CSMA-CD to work
If the host transmit for shorter, it is unable to react to the jamming sequence that is sent from another host, which makes it fail to act on the collision in time.

Since RTT is bounded by $51.2\micro s$ for Ethernet, the message needs to be of size 512 bits if we are using a 10Mbps network.

We need the jamming sequence for the case where host A transmit and a collision happens far away from it.
Host B needs to send the jamming sequence so that host A receives sufficient energy to detect the collision

## Bridges

Since LANs have a physical limitation of 2500 metres, 
we can extend its range by connecting LANs together using bridges.

(we are focused on transparent bridges, where hosts do not need to know of their existence)

### Learning

Bridges need to keep track if which host is on which port.
Thus it maintains a **dynamic** forwarding table.

Initially it is empty.
When it receives a frame from host A to B which arrives from port A,
it notes down that host A is on port A.
Since it doesn't know the port of host B, it will forward the frame to all its ports.
If it had known host B's port, then it will forward the frame if needed.

### Loops

It is possible for our LANs to be connected with a loop,
for reliability concerns.
Howler, consider the case that both bridges in the loop doesn't know the location of a receiver when it receive a frame.
Both bridges will indefinitely forward the frame to each other between the LANs.

To prevent this, we create a **spanning tree network** of the actual network.

See also: [Spanning trees](../graph_theory/trees_and_bipartite_graphs.ipynb#Spanning-Tree-)

It spans all the LANs, and turns off some of the ports of bridges to remove loops,
_ie_ the LANs are the vertices and the bridges are the "edges" (not exactly edges because a bridge can connect > 2 LANs).

We assign an ID to each of the bridge, and the bridge with the smallest ID is the root.
The spanning tree is generated such that the distance of each LAN to the root is minimized.

### Spanning tree algorithm


Initially bridge assumes it is the root.

Bridges exchanges the following information periodically:
* id of self
* id of assumed root
* distance to assumed root

When a bridge knows that it is not a root, it stops advertizing its information.
At steady state, only the root initiates this information while the others propagates it.

When a bridge receives a message which has a root that has lower id than its own assumed root,
it takes that id as the root instead.

If any bridge doesn't receive any information in a while, it assumes it is the root and begins to advertize its information.
