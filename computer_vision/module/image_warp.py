from scipy.spatial import KDTree
import numpy as np


def warp(pixels, image, n=5, eps=1e-6, max_d=3):
    grid = np.indices(image.shape).transpose(1, 2, 0)

    tree = KDTree(pixels.reshape((-1, 2)))
    dist, indices = tree.query(grid, n, workers=-1, distance_upper_bound=max_d)
    indices[dist == np.inf] = 0

    intensities = image.ravel()[indices]

    metric = (1/(dist+eps) + eps)
    avg_intensities = (intensities * metric).sum(axis=-1) / \
        (metric.sum(axis=-1))
    domain = (dist.min(axis=-1) != np.inf).reshape(image.shape)
    return avg_intensities.round().astype('uint8'), domain
