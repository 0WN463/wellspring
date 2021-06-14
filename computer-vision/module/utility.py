import matplotlib.pyplot as plt
import numpy as np

def show_images(img_label_tuples, grey=True):
    n = len(img_label_tuples)
    f = plt.figure(figsize=(12.8, 9.6))
    
    axes = [f.add_subplot(100 + 10 * n + i) for i in range(1, n+1)]
    
    vmax = 1 if all([image.max() <= 1 for image, *_ in img_label_tuples]) else 255

    for ax, (image, label, *others) in zip(axes, img_label_tuples):
        ax.title.set_text(label)
        autoscale = others[0] if len(others) > 0 else False
        if grey:
            ax.imshow(image, cmap='gray', vmin=0, vmax=vmax if not autoscale else image.max())
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
