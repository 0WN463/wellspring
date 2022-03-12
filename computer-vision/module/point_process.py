import numpy as np


def normalize(img):
    return img / np.repeat(np.sum(img, axis=2)[:, :, np.newaxis], 3, axis=2)


def adjust_brightness(img, amount):
    img = img.astype(np.uint16)
    return np.clip(img + amount, 0, 255)


def adjust_contrast(img, amount):
    img = np.array(img).astype(np.float32)
    return np.clip(img * amount, 0, 255).astype(np.uint16)


def adjust_gamma(img, gamma):
    img = np.array(img).astype(np.float32)
    return np.clip(255 * (img / 255) ** gamma, 0, 255).astype(np.uint16)


def whiten(img):
    mu = np.array(img).mean()
    sigma = np.array(img).std()
    return np.clip((img-mu)/sigma * 255, 0, 255)


def hist_stretch(img):
    lo = img.min()
    hi = img.max()
    img = img.astype(np.float32)
    return np.clip((img - lo) * 255/(hi-lo), 0, 255)


def hist_eq(img):
    freqs, bins = np.histogram(img.ravel(), bins=range(
        257), range=(0, 256), density=True)

    intensity_map = {}
    pdf = 0
    for f, b in zip(freqs, bins):
        pdf += f
        intensity_map[b] = 255 * pdf

    def map_pixels(x): return round(intensity_map[x])
    map_pixels = np.vectorize(map_pixels)
    return map_pixels(img)
