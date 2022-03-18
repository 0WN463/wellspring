import numpy as np
from .kernel import prewitt, Orientation
from .convolve import convolve


def compute_gradient(image, gradient_kernel=prewitt):
    sx = compute_one_gradient(image, Orientation.horizontal, gradient_kernel)
    sy = compute_one_gradient(image, Orientation.vertical, gradient_kernel)

    mag = np.sqrt(sx**2 + sy**2)

    with np.errstate(divide='ignore', invalid='ignore'):
        theta = np.arctan2(sy, sx)
    return mag, theta


def compute_one_gradient(image, orientation, gradient_kernel=prewitt):
    return convolve(image, gradient_kernel(orientation), clip=False, pad=False)
