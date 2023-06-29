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

# Framing


Now that we've sorted out how to transit our binary data across the medium, we need to perform **framing**.

This means to group the bits in some logical manner, so that we can treat them "as a block" to perform things like error checking.


## Approaches



### Sentinel

We use a special sequence (`01111110`) to determine when a frame starts/stops.

A typical frame would look like:

```
Starting sequence - Headers - Body - CRC - Ending sequence
```


However, the frame would be wrong if the special sequence appears in the payload.

We combat this by performing bit-stuffing or byte-stuffing.



#### Bit stuffing

When sending, we simply insert a 0 after 5 consecutive 1's, thus we would never encounter the 6 1's pattern (which is required in the sentinel) in our message.

When receiving, we remove the 0 after 5 consecutive 1's.

Usage: HLDC (high level datalink protocol)


#### Byte stuffing

`01111110` is `7E` as bytes.

We use `7D` as an escape sequence.

When sending, we replace `7E` with `7D 5E`, and `7D` with `7D 5D`.

When receiving, we just undo the operation.

Usage: PPP (Point to Point protocol)


### Counter



We include the frame length in the header.

Usage: DDMP (Digital data messaging protocol)


### Clock


Each frame is a specified time period long (_eg_ $125 \mu s$).

Usage: (SONET) Synchronous optical network


## Error detecting


We need to be mindful that our transmission medium is not 100% reliable.
So we need a way for the receiver to detect errors in the message.

### Cyclic redundancy check (CRC)

We add $k$ bits of data which is used to check for errors.

Ideally, $k$ should be as small as possible, while being informative enough to detect different levels of errors.

We represent the $n$ bit message as a $n-1$ degree polynomial.
So if the message is `1001101`, the polynomial is $x^6 + x^3 + x^2 + 1$.



We then have some pre-agreed divisor polynomial with degree $k+1$, _eg_ `1101` = $x^3 + x^2 + 1$.


To compute the CRC:
1. shift the message by $k$ bits
2. divide the message by the divisor
3. the $k$ bit remainder is the CRC

When we subtract the remainder from the shifted message, notice that the result can be evenly divided by the divisor.

Note that division is done in a finite field, so there is no "carrying". _eg_ `101` / `11` = `11`.


If the message received is evenly divisible by the divisor, then **no error is detected**.

If there is a non-zero remainder, then **some error is detected** in the message.

Note that it is possible for some errors to be undetected, _ie_ if $M$ is the original message, and $M + E$ is the corrupted message; if $E$ is divisible by the divisor, then the error is undetected.


#### Choice of divisors

Choosing different divisors gives us the ability to catch different levels of errors:
* $x^k$ and $x^0$ are non-zero allows us to catch any single bit error
    * $E = 1 << m$ will never be divisible by $x^k + \dots + 1$
* when the divisor is a factor of $(x + 1)$, we can catch any odd bit errors
    * any $E$ with odd number of 1's will never be divisible by $x + 1$, since each step of the division changes the number of bits in the partial quotient by an even amount, but no number of steps can turn all odd bits off
* any "burst" errors (consecutive bit errors) of length $\leq k$ is detectable
* **most** burst errors of length $> k$ are detectable


Standard CRC's includes:
* CRC-8
* CRC-10
* CRC-12
* CRC-16
* CRC-32
    * Used by Ethernet
    
where each number is the degree of the polynomial.
