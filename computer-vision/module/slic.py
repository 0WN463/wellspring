import numpy as np
from module.rgb_to_grey import to_greyscale
from module.gradient import compute_gradient
from module.feature import make_pos_rgb_feature
from scipy.spatial import KDTree


def _calc_distance(image: np.ndarray, num_super_pixels: int):
    height, width = image.shape[:2]
    return int(np.ceil(np.sqrt(height * width / num_super_pixels)))


def _make_initial_centers(image: np.ndarray, s: int):
    height, width = image.shape[:2]
    return np.array([(i + s//2, j + s//2) for j in range(0, width, s) for i in range(0, height, s)])


def _shift_centers(centers: np.ndarray, image_magnitude: np.ndarray):
    new_centers = np.zeros((centers.shape), dtype=np.int32)
    for i, center in enumerate(centers):
        y, x = center
        window = image_magnitude[max(y - 1, 0): y + 2, max(x - 1, 0): x + 2]
        offset = np.argwhere(window == window.min())[0]
        new_centers[i] = (offset - 1) + center
    return new_centers


def make_slic_centers(image: np.ndarray, num_super_pixels: int):
    s = _calc_distance(image, num_super_pixels)
    initial_centers = _make_initial_centers(image, s)
    gradient_magnitude, _ = compute_gradient(to_greyscale(image))
    centers = _shift_centers(initial_centers, gradient_magnitude)
    assert centers.shape[0] == num_super_pixels, "Number of super pixel is not evenly divided across the image"
    return centers, s


def _get_labels(features: np.ndarray, centers: np.ndarray,
                prev_distances: np.ndarray,
                prev_labels: np.ndarray, s: int) -> (np.ndarray, np.ndarray):
    _, num_features = centers.shape
    tree = KDTree(centers)
    queried_dist, queried_labels = tree.query(
        features.reshape((-1, num_features)), k=centers.shape[0])

    filtered_dist, filtered_labels = _filter_outside(features, s, queried_dist, queried_labels, centers)

    prev_distances = prev_distances.reshape(filtered_dist.shape)
    prev_labels = prev_labels.reshape(filtered_labels.shape)

    labels = np.where(filtered_dist < prev_distances,
                      filtered_labels, prev_labels)
    distances = np.minimum(filtered_dist, prev_distances)

    return labels.reshape(features.shape[:2]), distances

def _filter_outside(features: np.ndarray, s: int,
                    distances: np.ndarray,
                    labels: np.ndarray,
                    centers: np.ndarray) -> (np.ndarray, np.ndarray):
    yx = features[:,:,:2]
    yxs = np.repeat(yx[:, : , np.newaxis], labels.shape[-1], axis=2)
    
    center_yx = centers[:,:2][labels]
    yxs = yxs.reshape(center_yx.shape)
    
    is_inside = np.all(np.abs(yxs - center_yx) <= s, axis=2)
    
    assert np.all(np.any(is_inside, axis=1)), f"No candidate found among top-{labels.shape[-1]} candidates"
    
    indices = np.apply_along_axis(np.argmax, 1, is_inside)
    return distances[range(len(indices)),indices], labels[range(len(indices)),indices]


def _get_next_centers(curr_centers: np.ndarray, features: np.ndarray, labels: np.ndarray):
    new_centers = np.array([[features[labels == i].mean(axis=0)]
                           for i in range(len(curr_centers))])
    new_centers = new_centers.reshape(curr_centers.shape)
    return new_centers


def slic(image: np.ndarray, num_super_pixels: int, factor: float = 1.0, epsilon: float = 1e-6) -> (np.ndarray, np.ndarray):
    centers, s = make_slic_centers(image, num_super_pixels)

    features = make_pos_rgb_feature(image, factor)
    feature_centers = features[centers[:, 0], centers[:, 1]]

    distances = np.ones((features.shape[:2])) * float('infinity')
    labels = np.ones((features.shape[:2]), dtype=np.int32) * -1

    centers = feature_centers
    diff = float('infinity')
    while diff > epsilon:
        labels, distances = _get_labels(features, centers, distances, labels, s)
        new_centers = _get_next_centers(centers, features, labels)
        diff = ((centers - new_centers)**2).sum()
        centers = new_centers

    return _get_labels(features, centers, distances, labels, s)[0], centers


