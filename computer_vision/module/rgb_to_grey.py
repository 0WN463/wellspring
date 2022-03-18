def extract_channel(img, channel):
    return img[:, :, channel]


def to_greyscale(img, weights=(0.2989, 0.587, 0.114)):
    return img[:, :, 0] * weights[0] + img[:, :, 1] * weights[1] + img[:, :, 2] * weights[2]
