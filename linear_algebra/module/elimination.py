import numpy as np


def gaussian_elim(arr: np.ndarray, b: np.ndarray = None) -> np.ndarray:
    _b = np.zeros((arr.shape[0], 1)) if b is None else b

    if 1 in arr.shape:
        return (arr, _b) if b is not None else arr

    arr = arr.astype('float')
    _b = _b.astype('float')

    try:
        col = np.argwhere(np.any(arr != 0, axis=0)).ravel()[0]
    except IndexError:
        return (arr, _b) if b is not None else arr
    if arr[0][col] == 0:
        i = np.argwhere(arr[:, col] != 0).ravel()[0]
        arr[i], arr[0] = arr[0].copy(), arr[i].copy()
        _b[i], _b[0] = _b[0].copy(), _b[i].copy()
    for i in range(1, arr.shape[0]):
        factor = arr[i][col] / arr[0][col]
        arr[i] -= arr[0] * factor
        _b[i] -= _b[0] * factor

    arr[1:, 1:], _b[1:, :] = gaussian_elim(arr[1:, 1:], _b[1:, :])

    return (arr, _b) if b is not None else arr


def gauss_jordan_elim(arr: np.ndarray, b: np.ndarray = None) -> np.ndarray:
    arr, _b = gaussian_elim(arr, b)
    for i in range(1, arr.shape[0]):
        cols = np.argwhere(arr[i] != 0).ravel()
        if not cols.size:
            break

        col = cols[0]
        _b[i] /= arr[i][col]
        arr[i] /= arr[i][col]

        for j in range(i):
            factor = arr[j][col]
            arr[j] -= arr[i] * factor
            _b[j] -= _b[i] * factor

    return (arr, _b) if b is not None else arr
