import numpy as np


def ransac(sample_pool, N, sample_size, dist_func, delta, return_metric=False):
    best = (None, 0)
    for _ in range(N):
        indices = np.random.choice(
            np.arange(sample_pool.shape[0]), size=sample_size, replace=False)
        sample = sample_pool[indices]
        num_inliers = (dist_func(sample, sample_pool) <= delta).sum()

        if num_inliers > best[1]:
            best = (sample, num_inliers)

    return best if return_metric else best[0]
