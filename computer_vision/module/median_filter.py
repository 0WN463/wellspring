import numpy as np
from .pad_image import paddable


@paddable
def median_filter(img, window_shape):
    assert len(window_shape) == 2

    wh, ww = window_shape
    height, width = img.shape
    new_image = np.zeros((height - wh + 1, width - ww + 1))

    for i in range(0, height - wh + 1):
        for j in range(0, width - ww + 1):
            new_image[i][j] = np.median(img[i:i+wh, j:j+ww])
    return new_image
