import numpy as np
from .pad_image import paddable

@paddable
def naive_correlate(img, window, clip=True):
    assert len(window.shape) == 2
    
    wh, ww = window.shape
    height, width = img.shape
    new_image = np.zeros((height - wh + 1, width - ww + 1))
    
    for i in range(0, height - wh + 1):
        for j in range(0, width - ww + 1):
            new_image[i][j] = (window * img[i:i+wh, j:j+ww]).sum()
    if clip:
        new_image = np.clip(new_image, 0, 255)
    return new_image

@paddable
def correlate(img, window, clip=True):
    assert len(window.shape) == 2
    wh, ww = window.shape
    height, width = img.shape
    new_height, new_width = height - wh + 1, width - ww + 1

    extracted_regions = np.zeros((new_height * new_width, wh * ww))

    for i in range(new_height):
        for j in range(new_width):
            extracted_regions[i * new_width + j] = img[i: i + wh, j: j + ww].ravel()

    products = extracted_regions * window.ravel()
    result = products.sum(axis=1).reshape((new_height, new_width))
    return result

@paddable
def normalized_correlate(img, template):
    pixel_sums = np.sqrt(correlate(img.astype("float64") ** 2, np.ones(template.shape), clip=False, pad=False))
    template_mag = np.sqrt((template**2).sum())

    return correlate(img, template, pad=False)/pixel_sums/template_mag

