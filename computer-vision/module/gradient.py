import numpy as np
from .kernel import prewitt, Orientation
from .convolve import convolve

def compute_gradient(image, gradient_kernel=prewitt):
    sx = convolve(image, gradient_kernel(Orientation.horizontal), clip=False, pad=False)
    sy = convolve(image, gradient_kernel(Orientation.vertical), clip=False, pad=False)

    mag = np.sqrt(sx**2 + sy**2)

    with np.errstate(divide='ignore', invalid='ignore'):
        theta = np.arctan2(sy, sx)
    return mag, theta
