import numpy as np


def discretize_color(img, levels):
    img = np.array(img)
    bucket_size = 256 // levels
    return img // bucket_size * bucket_size


def discretize_space(img, factor):
    resized_img = img.resize((img.size[0]//factor, img.size[1]//factor))
    return np.array(resized_img)
