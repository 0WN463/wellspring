from typing import Iterator


def crc(msg: bytes | bytearray, divisor: bytes | bytearray | str, encoding = 'little') :
    if type(divisor) is str:
        divisor = int(divisor, 2)
    else:
        divisor = int.from_bytes(divisor, encoding)

    n = int.from_bytes(msg, encoding)
    msg_len = n.bit_length()
    quotient = 0
    ones = lambda k: (1 << k) - 1
    inv = lambda k: k ^ ones(k.bit_length())

    while n:
        breakpoint()
        mask_len = msg_len - divisor.bit_length()
        mask = ones(mask_len)
        masked += (n & (mask ^ ones(msg_len))) >> mask_len
        quotient += n >> (divisor.bit_length() - 1)

    return n.to_bytes(original_len, encoding)

print(crc(bytes('Hello, World!', 'ascii'), '1011'))
