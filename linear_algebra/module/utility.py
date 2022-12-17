from fractions import Fraction
import numpy as np

def _frac_to_str(frac:np.ndarray) -> str:
    if type(frac) != Fraction:
        return str(frac)
    if frac.numerator == 0:
        return "0"
    elif frac.denominator == 1:
        return str(frac.numerator)
    
    return f'{frac.numerator}/{frac.denominator}'

def print_arr(arr:np.ndarray, bs: np.ndarray=None):
    if bs is None:
        for row in arr:
            print("\t".join([f'{_frac_to_str(e)}' for e in row]))
        return
    
    for a, b in zip(arr, bs):
        a = "\t".join([f'{_frac_to_str(e)}' for e in a])
        b = "\t".join([f'{_frac_to_str(e)}' for e in b])
        print(f'{a} \t | {b}')
