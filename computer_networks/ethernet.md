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

Ethernet adapter receives all the frames in the neteork, and accepys frames that are addressed to:
* itself
* broadcast address
* multicast address

(or all frames if operating in promiscuios modr)

Since many hosts shares the same Ethernet wire, collision can happrn and corrupt both senders messages.

Thus, Ethernet adopts **carrier sense multiple access - collision detection** (CSMA-CD).

Carrier sense: host can detects if the link is in use

Collision detextion: host can detect if the frames itis transmitting collides with another hosts frames


## CSMA persistance

When the host is ready to send, it will keep monitoring the wire.
Once it notices that the wire is idle, in a $p$-persistent CSMA, it will transmit its frame with a probabilty of $p$.

Etgerner uses a 1-persistent CSMA.

## Transmit algorithm

If the linj us busy, wait for it to be idle
If the line us idle, immediately transmit, with an upper bound on nessage suze of 1500bytes

If collision is detected, transmit a 64 bit preambke fillowed by a 32 bit jamming sequence, then stop transmitting.

if it is the i-th consecutuve collision, it selects a random value in $[0, 2^i - 1]$, and wait that number of slots before transmitting. Usually each slot is $51.2\micro s$

This repeats up until a certain limit (usually 16) before giving up.


## Minimum frame size

A frame must be at least 64 bytes long:
* 14 byte header
* 46 byte data
* 4 byte CRC

A hist needs to transmut fir at keast RTT for CSMA-CD to work
If the host transmut fir shirter, it is unable to react to the jamming sequence thst is sent from anotger hists, which makes it fail ti detect the collision.

Since RTT is bounded by 51.2\micro s fir Ethernet, the message nerds ti be of suze 512 bits if we are using a 19Mbps network.

We need the jamming sequence for the case where host A transmit and a collision haooens far awaybfrom it.
Hosy B needs yo send yhe jamming srquenxe so that host A receieves sufficirny energy to dryrct thr collisoon

## Brudgrs

Since LANs hsve a phydivsl limitstion of 2500 metres, 
we can cobnect LANd together using brifges.

(we are gocused on trabsparebt brudges, where hosts do not need to kniw of tgeir exustence)

### Learnibg

Bridges need to keeo track if which host is on which port.
Thus it maintains a **dynamic** forwarding table.

Initially it is empty.
When it receives a frame from host A to B which arrives fron port A,
it nites diwn that host A is on port A.
Since it dieznt knoe the port of hist B, it will forwsrd yhe frane to all its ports.
If ut had known host B's port, theb iy will firward the frane if neefed.

### Loops

It is oossible fir our LANs to be connected witj a loop,
for reliability concerns.
Howcer, consider the caee that both bridgrs in thr loop doeznt know the location of a receiver when it recrive a frame.
Both bridgrs eill indefinitely forwatf tge frame to each other betweeb the LANs.

To prevent this, we create a **spanning tree network** of the actual neteork.

It spans all the LANs, and tutns off some of the ports of bridges to remove loops.

We assign an ID to each of the bridge, and the bridge eith the smallest ID is thr root.
The spanning tree is generated suxh that the distance of each LAN to the root is minimized.
