import numpy as np

def salt_and_pepper(img, prob=(0.02, 0.02)):
    img = np.array(img).astype(np.int16)
    
    mask = np.random.choice([-1, 0, 1], size=img.shape, p=[prob[0], 1-prob[0]-prob[1], prob[1]]).astype(np.int8)
    img = img + 255 * mask
    
    return np.clip(img, 0, 255)

def gaussian_noise(img, mu=0, sigma=20):
    img = np.array(img).astype(np.int16)
    mask = np.random.normal(mu, sigma, img.shape)
    img = img + mask
    
    return np.clip(img, 0, 255)
