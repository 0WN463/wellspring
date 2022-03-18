import numpy as np
from functools import wraps


def pad_image(img, window, value):
    wh, ww = window.shape if hasattr(window, "shape") else window
    paddings = ((wh - 1) // 2, wh // 2), ((ww - 1) // 2, ww // 2)
    return np.pad(img, paddings, constant_values=value)


def paddable(func):
    @wraps(func)
    def inner(img, window, pad=True, value=255, **kwargs):
        if pad:
            img = pad_image(img, window, value)
        return func(img, window, **kwargs)

    return inner
