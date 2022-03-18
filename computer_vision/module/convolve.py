import numpy as np
from .pad_image import paddable
from .correlate import correlate


@paddable
def convolve(img, window, clip=True):
    return correlate(img, np.flip(window), clip=clip, pad=False)
