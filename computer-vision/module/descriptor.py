from module.gradient import compute_gradient
from module.kernel import gaussian_filter
import numpy as np


def bin_grid(mags, thetas, threshold):
    hist = np.zeros((8,))

    thetas += np.pi
    for mag, theta, in zip(mags.ravel(), thetas.ravel()):
        if mag < threshold:
            continue
        i = int(theta / (2 * np.pi / 8))
        if i == 8:
            i = 7

        hist[i] += 1

    amax = hist.argmax()

    hist = np.concatenate((hist[amax:], hist[:amax]))

    return hist


def get_patch(image, p):
    y, x = p
    # We obtain a 18x18 patch to obtain a 16x16 magnitude patch as the convolution will reduce our patch size
    if x < 9 or y < 9 or x + 9 > image.shape[1] or y + 9 > image.shape[0]:
        raise ValueError("unable to obtain 16x16 patch")

    patch = image[y - 9: y + 9, x - 9:x + 9]
    return patch


def sift(image, p, threshold=1e-12):
    patch = get_patch(image, p)
    mags, thetas = compute_gradient(patch)

    gaussian = gaussian_filter(17, sigma=10)[:16, :16]

    mags = (mags * gaussian).reshape(4, 4, -1,
                                     4).swapaxes(1, 2).reshape(-1, 4, 4)
    thetas = thetas.reshape(4, 4, -1, 4).swapaxes(1, 2).reshape(-1, 4, 4)

    descriptors = np.array([bin_grid(mag, theta, threshold)
                           for mag, theta in zip(mags, thetas)])
    sums = descriptors.sum(axis=1)[:, np.newaxis]
    descriptors /= np.where(sums > 0, sums, 1)
    return descriptors
