def extended_euclid(n, m):
    quotients, modulos = [], []
    
    while n % m > 0:
        quotients.append(n // m)
        modulos.append(m)
        n, m = m, n % m
        
    small_factor, big_factor = -quotients[-1], 1
    
    for q in reversed(quotients[:-1]):
        small_factor, big_factor = small_factor * -q + big_factor, small_factor
    
    # gcd(n,m) = pn + qm
    gcd, p, q = m, big_factor, small_factor
    return gcd, p, q
        
