import numpy as np


def spectrum_line(fs, values, buffer=(1, 1)):
    fs, values = np.array(fs), np.array(values)

    freqs = np.arange(min(0, fs.min()) - buffer[0], fs.max() + buffer[1], 1e-2)

    indices = np.array([np.argwhere(np.isclose(freqs, f))
                       for f in fs]).reshape(fs.shape)

    result = np.zeros(freqs.shape)
    result[indices] = values
    return freqs, result
