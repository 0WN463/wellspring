import numpy as np
from scipy.spatial import KDTree

def make_centers(num_clusters, features):
    feature_maxes = features.max(axis=0).max(axis=0)
    if len(features.shape) == 2:
        feature_maxes = [feature_maxes]
    centers = np.random.rand(num_clusters, len(feature_maxes))
    for i, m in enumerate(feature_maxes):
        centers[:, i] = centers[:, i] * m
        
    return centers
    
def get_labels(features, centers):
    num_features = centers.shape[1]
    tree = KDTree(centers)
    _, labels = tree.query(features.reshape((-1, num_features)))
    return labels.reshape(features.shape[:2])

def get_next_centers(curr_centers, features):
    labels = get_labels(features, curr_centers)
    new_centers = np.array([[features[labels==i].mean(axis=0)] for i in range(len(curr_centers))])
    new_centers = new_centers.reshape(curr_centers.shape)
    return new_centers

def kmeans(features: np.ndarray, num_clusters: int, initial_centers: np.ndarray=None, epsilon: float=1e-6) -> (np.ndarray, np.ndarray):
    if initial_centers is None:
        initial_centers = make_centers(num_clusters, features)
    
    assert initial_centers.shape[-1] == features.shape[-1], f"Centers dimension ({initial_centers.shape}) does not match feature space ({features.shape})"

    centers = initial_centers
    diff = float('infinity')
    while diff > epsilon:
        new_centers = get_next_centers(centers, features)
        diff = ((centers - new_centers)**2).sum()
        centers = new_centers
        
    return get_labels(features, centers), centers
