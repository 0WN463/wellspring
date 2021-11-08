import numpy as np
from scipy.spatial import KDTree

def simple_area(image, window_size=11):
    result = np.copy(image)

    LEFT = window_size // 2
    RIGHT = window_size - LEFT
    sorted_response_inds = np.flip(image.argsort(axis=None))
    indices = np.unravel_index(sorted_response_inds, image.shape)

    for ind in zip(indices[0], indices[1]):
        if result[ind] <= 0:
            result[ind] = 0
            continue

        result[ind[0] - LEFT: ind[0] + RIGHT,
               ind[1] - LEFT: ind[1] + RIGHT] = 0
        result[ind] = image[ind]

    return result

def adaptive_area(image, r):
    local_maxima = simple_area(image)
    ps = np.argwhere(local_maxima > 0)

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
        largest_n = local_maxima[ps[n][:, 0], ps[n][:, 1]].max()

        self = local_maxima[p[0], p[1]]
        if self > largest_n * 1:
            result.append(p)

    new = np.zeros(image.shape)

    for y, x in result:
        new[y, x] = 255

    return new

def top_k(image, k):
    indices = np.argsort(image, axis=None)
    indices = np.unravel_index(indices, image.shape)
    indices = zip(reversed(indices[0]), reversed(indices[1]))

    result = np.zeros(image.shape)

    for i, ind in enumerate(indices):
        if i == k:
            break

        result[ind] = 255

    return result
