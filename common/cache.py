from functools import wraps
import contextlib
from typing import Callable

@contextlib.contextmanager
def cache(f, original_global, hash_func: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        h = hash_func(*args, **kwargs)
        if (res := f.table.get(h)) is not None:
            return res

        res = f(*args, **kwargs)
        f.table[h] = res
        return res
    f.table = {}

    original_global[f.__name__] = wrapper
    yield
    original_global[f.__name__] = f
