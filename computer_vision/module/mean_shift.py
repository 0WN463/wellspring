from scipy.spatial import KDTree
import numpy as np


def make_centers(features: np.ndarray, bandwidth: float, threshold: int) -> np.ndarray:
    compressed = np.round(features.reshape(-1, features.shape[-1]) / bandwidth)
    unique, counts = np.unique(compressed, axis=0, return_counts=True)

    centers = np.array([x for x, c in zip(unique, counts) if c >= threshold])
    return centers * bandwidth + bandwidth/2


def get_next_centers(centers, tree, bandwidth):
    indices = tree.query_ball_point(centers, bandwidth, workers=-1)
    new_centers = np.array([tree.data[ind].mean(axis=0)
                           for ind in indices if len(ind) > 0])
    return new_centers


def prune_centers(centers, prune_radius):
    center_tree = KDTree(centers)
    indices_to_remove = np.unique(
        np.array([i for i, _ in center_tree.query_pairs(prune_radius)]))
    pruned_centers = np.delete(
        centers, indices_to_remove, axis=0) if indices_to_remove.size > 0 else centers

    return pruned_centers


def mean_shift(features: np.ndarray, bandwidth: float, threshold: int, prune_radius: float,
               epsilon: float = 1e-6) -> (np.ndarray, np.ndarray):
    initial_centers = make_centers(features, bandwidth, threshold)
    tree = KDTree(features.reshape((-1, features.shape[-1])))
    assert initial_centers.shape[-1] == features.shape[-1], f"Centers dimension ({initial_centers.shape}) does not match feature space ({features.shape})"

    centers = initial_centers
    diff = float('infinity')
    while diff > epsilon * bandwidth:
        new_centers = get_next_centers(centers, tree, bandwidth)
        new_centers = prune_centers(new_centers, prune_radius)

        if centers.shape != new_centers.shape:
            centers = new_centers
            continue
        else:
            diff = ((centers - new_centers)**2).sum()
            centers = new_centers
    return get_labels(features, centers), centers


def get_labels(features, centers):
    num_features = centers.shape[1]
    tree = KDTree(centers)
    _, labels = tree.query(features.reshape((-1, num_features)), workers=-1)
    return labels.reshape(features.shape[:2])
