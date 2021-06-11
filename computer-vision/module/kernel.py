import numpy as np

def box_filter(size):
    return np.ones((size, size))/size**2

def gaussian_filter(size, sigma=1):
    assert size % 2 == 1
    
    kernel = np.ones((size, size), np.float64)
    k = size // 2
    for i in range(size):
        for j in range(size):
            exponent = -((i - k)**2 + (j-k)**2) / (2 * sigma**2) 
            kernel[i][j] = np.exp(exponent)/ (2 * np.pi*sigma**2)
    return kernel
