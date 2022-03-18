def is_prime(n):
    if n % 2 == 0 or n <= 1:
        return False
    
    for i in range(3, n, 2):
        if i * i > n:
            return True
        
        if n % i == 0:
            return False
