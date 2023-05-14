from functools import wraps
import contextlib

class Counter:
    def __init__(self):
        self.count = 0

    def __str__(self):
        return str(self.count)

    def inc(self):
        self.count += 1

@contextlib.contextmanager
def count(f, original_global, counter=None):
    @wraps(f)
    def wrapper(*args, **kwargs):
        counter.inc()
        return f(*args, **kwargs)
    counter = counter if counter else Counter()

    original_global[f.__name__] = wrapper
    yield counter
    original_global[f.__name__] = f
