import numpy as np
from scipy.spatial import KDTree


def simple_area(image, window_size=11):
    mask = np.full(image.shape, True)

    LEFT = window_size // 2
    RIGHT = window_size - LEFT
    sorted_response_inds = np.flip(image.argsort(axis=None))
    indices = np.unravel_index(sorted_response_inds, image.shape)

    for ind in zip(indices[0], indices[1]):
        if not mask[ind]:
            continue
        left = max(ind[0] - LEFT, 0)
        top = max(ind[1] - LEFT, 0)

        mask[left: ind[0] + RIGHT,
             top: ind[1] + RIGHT] = False
        mask[ind] = True

    return np.argwhere(mask)


def top_k(image, points, k):
    intensities = image[points[:, 0], points[:, 1]]
    return points[np.flip(np.argsort(intensities, axis=0))][:k]


def adaptive_area(image, r):
    ps = simple_area(image)

    tree = KDTree(ps)

    neighbours = tree.query_ball_point(ps, r, workers=-1)

    for i, n in enumerate(neighbours):
        n.remove(i)

    result = []

    for p, n in zip(ps, neighbours):
        if len(n) == 0:
            result.append(p)
            continue

        indices = ps[n]
        largest_n = image[ps[n][:, 0], ps[n][:, 1]].max()

        self = image[p[0], p[1]]
        if self > largest_n:
            result.append(p)

    return np.array(result)
