import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb

def show_images(*img_label_tuples, grey=True):
    if len(img_label_tuples) == 1 and type(img_label_tuples[0]) == list:
        img_label_tuples = img_label_tuples[0]

    n = len(list(img_label_tuples))
    f = plt.figure(figsize=(12.8, 9.6))
    
    axes = [f.add_subplot(100 + 10 * n + i) for i in range(1, n+1)]
    
    imgs_max = 1 if all([image.max() <= 1 for image, *_ in img_label_tuples]) else 255

    for ax, (image, label, *others) in zip(axes, img_label_tuples):
        ax.title.set_text(label)
        autoscale = others[0] if len(others) > 0 else False
        vmin, vmax = (0, imgs_max) if not autoscale else (image.min(), image.max())
        if grey:
            ax.imshow(image, cmap='gray', vmin=vmin, vmax=vmax)
        else:
            ax.imshow(image)
            
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

def show_pyramids(pyramid, label_format, grey=True, autoscale=False, format_func=None):
    n = len(pyramid)
    f = plt.figure(figsize=(20, 15))

    axes = [f.add_subplot(100 + 10 * n + i) for i in range(1, n+1)]
    vmax = 1 if all([image.max() <= 1 for image in pyramid]) else 255

    for i, (ax, image) in enumerate(zip(axes, pyramid)):
        level = i + 1
        placeholder = level if format_func is None else format_func(level)
        ax.title.set_text(label_format.format(placeholder))
        if autoscale:
            vmax = image.max()
        if grey:
            ax.imshow(image, cmap='gray', vmin=0, vmax=vmax)
        else:
            ax.imshow(image)

        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    for ax in axes[1:]:
        ax.sharex(axes[0])
        ax.sharey(axes[0])

def array_is_equal(arr1, arr2, epsilon=1e-10):
    return np.abs((arr1 - arr2)).max() < epsilon

def make_segments(image):
    perm = np.random.permutation(image.max() + 1)
    image = np.vectorize(lambda x: perm[x])(image)    
    hsv_image = np.zeros((image.shape[0], image.shape[1], 3))
    hsv_image[:,:,0] = image / (image.max() + 1)
    hsv_image[:,:,1] = 1
    hsv_image[:,:,2] = 1
    return hsv_to_rgb(hsv_image)

