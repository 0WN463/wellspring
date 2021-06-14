import numpy as np
from .convolve import convolve
from .resize import downsample, upsample
from .kernel import gaussian_filter

default_kernel = gaussian_filter(7, sigma=1)

def make_gaussian_pyramid(image, levels, kernel=default_kernel):
    blur_downsample = lambda x: downsample(convolve(x, kernel))

    arr = [image]

    for _ in range(levels - 1):
        arr.append(blur_downsample(arr[-1]))

    return arr

def make_laplacian_pyramid(image, levels, kernel=default_kernel):
    gaussian_pyramid = make_gaussian_pyramid(image, levels, kernel)
    flipped_pyramid = list(reversed(gaussian_pyramid))
    arr = [flipped_pyramid[0]]

    for image, next_image in zip(flipped_pyramid, flipped_pyramid[1:]):
        upsampled = upsample(image)
        blurred = convolve(upsampled, kernel)
        diff = next_image - blurred
        arr.append(diff)
        
    return arr[::-1]

def combine(img, residual, kernel=default_kernel):
    upsampled = upsample(img)
    blurred = convolve(upsampled, kernel)
    return blurred + residual

def recover(laplacian_pyramid, kernel=default_kernel):
    recovered_images = [laplacian_pyramid[-1]]

    for residual in reversed(laplacian_pyramid[:-1]):
        recovered_images.append(combine(recovered_images[-1], residual, kernel))
    return recovered_images
