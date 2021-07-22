import numpy as np
from .kernel import dog
from .gradient import compute_gradient

def canny_edge(image, high_threshold, low_threshold, kernel_size=5):    
    make_dog = lambda orientation: dog(kernel_size, orientation=orientation)

    mag, theta = compute_gradient(image, gradient_kernel=make_dog)
    
    high_pixels = nonmaximum_suppression(np.where(mag >= high_threshold, mag, 0), theta)
    low_pixels = nonmaximum_suppression(np.where(mag >= low_threshold, mag, 0), theta)

    result = hysteresis_threshold(high_pixels, low_pixels)
    return result


def nonmaximum_suppression(mag, theta, interpolate=True):
    octant = np.floor((theta + np.pi * 2) / (np.pi / 4)) % 8
    excess = (theta + np.pi * 2) - octant * (np.pi/4)
    excess = np.where(excess >= np.pi * 2, excess - np.pi * 2, excess)
    excess_ratio = excess / (np.pi / 4)

    octant_map = {0: (0,  1), 1: ( 1, 1),  2: ( 1, 0), 3: (1, -1), 
                  4: (0, -1), 5: (-1, -1), 6: (-1, 0), 7: (-1, 1)}
    
    result = np.zeros(mag.shape, dtype=np.uint8)
    
    height, width = mag.shape
    
    for i in range(1, height - 1):
        for j in range(1, width -1):
            pixel_val = mag[i][j]
            
            main_dir = octant_map[octant[i][j]]
            next_dir = octant_map[(octant[i][j] + 1) % 8]
            main_mag = mag[i + main_dir[0]][j + main_dir[1]]
            next_mag = mag[i + next_dir[0]][j + next_dir[1]]
            
            if interpolate:
                target_mag = excess_ratio[i][j] * next_mag + (1-excess_ratio[i][j]) * main_mag
            else:
                target_mag = next_mag if excess_ratio[i][j] >= 0.5 else main_mag
            
            if pixel_val > target_mag:
                result[i][j] = 1
            
    
    return result


def hysteresis_threshold(high_pixels, low_pixels):
    assert high_pixels.shape == low_pixels.shape
    
    result = np.zeros(high_pixels.shape)
    
    height, width = high_pixels.shape
    
    def neighbours(i, j):
        arr = [(i-1, j-1), (i-1, j), (i-1, j+1),
               (i, j-1), (i, j), (i, j+1),
               (i+1, j-1), (i+1, j), (i+1, j+1),
              ]
        
        arr = tuple(filter(lambda e: e[0] >= 0 and e[0] < height and e[1] >= 0 and e[1] < width, arr))
        
        return arr
    
    start_indices = tuple(zip(*high_pixels.nonzero()))
    
    def dfs(i, j):
        result[i][j] = 1
        
        for i_p, j_p in neighbours(i, j):
            if not result[i_p][j_p] and low_pixels[i_p][j_p]:
                dfs(i_p, j_p)
    
    for index in start_indices:
        dfs(*index)
    
    return result
