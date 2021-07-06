from .euclids_algorithm import extended_euclid 
from .is_prime import is_prime

def modulo_inverse(e, n):
    gcd, p, _ = extended_euclid(e, n)
    if gcd != 1:
        raise ValueError(f"e ({e}) is not relatively prime to n ({n})")
    return (p + n) % n
        
def make_keys(p, q, e):
    assert is_prime(p), "p is not prime"
    assert is_prime(q), "q is not prime"
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modulo_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(m, public_key):
    e, n = public_key
    return pow(m, e, n)

def decrypt(m, private_key):
    d, n = private_key
    return pow(m, d, n)
