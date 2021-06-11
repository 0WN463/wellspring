def extract_channel(img, channel):
    return img[:, :, channel]

def to_greyscale(img, weights):
    return img[:, :, 0] * weights[0] + img[:, :, 1] * weights[1] + img[:, :, 2] * weights[2] 

