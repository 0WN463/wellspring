import numpy as np

def make_pos_intensity_feature(grey_image: np.ndarray, factor: float=1) -> np.ndarray:
    height, width = grey_image.shape
    result = np.zeros((height, width, 3))
    ys = np.tile(np.arange(height), (width, 1)).transpose()
    xs = np.tile(np.arange(width), (height, 1))
    result[:,:,0] = ys / (height - 1)
    result[:,:,1] = xs / (width - 1) 
    result[:,:,2] = grey_image / 255
    
    return result

def make_pos_rgb_feature(rgb_image: np.ndarray, factor:float=1) -> np.ndarray:
    height, width = rgb_image.shape[:2]
    result = np.zeros((height, width, 5))
    ys = np.tile(np.arange(height), (width, 1)).transpose()
    xs = np.tile(np.arange(width), (height, 1))
    result[:,:,0] = ys / (height - 1) * factor
    result[:,:,1] = xs / (width - 1) * factor
    result[:,:,2:5] = rgb_image / 255
    
    return result
