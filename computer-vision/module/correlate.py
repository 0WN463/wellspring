import numpy as np

def correlate(img, window):
    height, width = img.shape
    
    assert window.shape[0] == window.shape[1]
    
    window_size = window.shape[0]
    
    new_image = np.zeros((height-window_size, width-window_size))
    
    for i in range(0, height - window_size):
        for j in range(0, width - window_size):
            new_image[i][j] = (window * img[i:i+window_size, j:j+window_size]).sum()
    return np.clip(new_image, 0, 255)
