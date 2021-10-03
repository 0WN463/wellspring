from .gradient import compute_one_gradient
from .kernel import Orientation
from .convolve import convolve
import numpy as np

def harris(image, window_size=5, kappa=0.05, window=None):
    Ix = compute_one_gradient(image, Orientation.horizontal)
    Iy = compute_one_gradient(image, Orientation.vertical)

    w = np.ones((window_size, window_size)) if window is None else window

    A = convolve(Ix**2, w, clip=False, pad=False)
    B = convolve(Ix*Iy, w, clip=False, pad=False)
    C = convolve(Iy**2, w, clip=False, pad=False)

    det = A * C - B ** 2
    tr = A + C

    R = det - 0.05 * tr ** 2

    return R

