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

def dog(size, sigma=1, gradient_filter_func=prewitt, orientation=Orientation.horizontal):
    gradient_filter = gradient_filter_func(orientation)
    size_reduction = gradient_filter.shape[0] - 1
    return convolve(gaussian_filter(size + size_reduction, sigma), gradient_filter, pad=False, clip=False)

def laplace_filter():
    return np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

def log(size, sigma=1, orientation=Orientation.horizontal):
    return convolve(gaussian_filter(size, sigma), laplace_filter(), pad=False, clip=False)

def gabor(size, sigma=1,omega=1, lamb=1, phi=0):
    assert size % 2 == 1
    
    xs, ys = np.linspace(-5, 5, size), np.linspace(-5, 5, size)
    xs, ys = np.meshgrid(xs, ys)

    fp = 1/(2 * np.pi * sigma**2)
    sp = np.exp(- (xs ** 2 + ys**2)/ (2 * sigma**2))
    lp = np.sin(2 * np.pi * (xs * np.cos(omega) + ys * np.sin(omega))/lamb + phi)

    return fp * sp * lp
