import numpy as np
import enum
from .convolve import convolve

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

class Orientation(enum.Enum):
    horizontal = 0
    vertical_reversed = 1
    horizontal_reversed = 2
    vertical = 3

def prewitt(orientation=Orientation.horizontal):
    horizontal_matrix = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    
    return np.rot90(horizontal_matrix, orientation.value)

def sobel(orientation=Orientation.horizontal):
    horizontal_matrix = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    
    return np.rot90(horizontal_matrix, orientation.value)

def dog(size, sigma=1, gradient_filter=prewitt, orientation=Orientation.horizontal):
    return convolve(gaussian_filter(size, sigma), gradient_filter(orientation), pad=False, clip=False)

def laplace_filter():
    return np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

def log(size, sigma=1, orientation=Orientation.horizontal):
    return convolve(gaussian_filter(size, sigma), laplace_filter(), pad=False, clip=False)
