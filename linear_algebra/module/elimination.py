import numpy as np
from fractions import Fraction
from typing import Optional
import numpy.typing as npt

arr_type = npt.NDArray[np.int_]
frac_arr_type = npt.NDArray[np.object_]

def gaussian_elim(arr: arr_type, b: Optional[arr_type] = None) -> frac_arr_type|tuple[frac_arr_type, frac_arr_type]:
    _b:arr_type = np.zeros((arr.shape[0], 1)).astype('int') if b is None else b
    arr = arr + Fraction()
    _b = _b + Fraction()

    if 0 in arr.shape:
        return (arr, _b) if b is not None else arr

    r = 0
    for c in range(arr.shape[1]):
        if np.all(arr[:,c] == 0):
            continue
        if arr[r][c] == 0:
            indices = np.flatnonzero(arr[:, c])
            indices = indices[indices > r]
            if len(indices) == 0:
                continue
            i = indices[0]

            arr[i], arr[r] = arr[r].copy(), arr[i].copy()
            _b[i], _b[r] = _b[r].copy(), _b[i].copy()

        #arr[r] /= arr[r][c]
        #factors = arr[:, c].copy() 
        factors = arr[:, c].copy() / arr[r][c]
        factors[:r+1] = 0
        dx = np.tile(arr[r], (arr.shape[0], 1)) * factors[:,None]
        arr -= dx

        dx = np.tile(_b[r], (_b.shape[0], 1)) * factors[:,None]
        _b -= dx
        r += 1

    return (arr, _b) if b is not None else arr

def gauss_jordan_elim(arr: arr_type, b: Optional[arr_type] = None) -> frac_arr_type|tuple[frac_arr_type, frac_arr_type]:
    _b = np.zeros((arr.shape[0], 1)).astype('int') if b is None else b
    arr, _b = gaussian_elim(arr, _b)
    
    for i in range(arr.shape[0]):
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

