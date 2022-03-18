import numpy as np


def downsample(img, factor=2):
    h, w = img.shape
    new_image = np.zeros((h // factor, w // factor))

    for i in range(h // factor):
        for j in range(w // factor):
            new_image[i][j] = img[i * factor][j * factor]
    return img[::factor, ::factor]


def upsample(img, factor=2):
    return img.repeat(factor, axis=1).repeat(factor, axis=0)
