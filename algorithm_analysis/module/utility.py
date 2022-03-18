import sys

class _SetTrace(object):
    def __init__(self, func):
        self.func = func

    def __enter__(self):
        sys.settrace(self.func)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

_count = 0
_func_name = None

def monitor(frame, event, arg):
    if event == "line" and frame.f_code.co_name == _func_name:
        global _count
        _count += 1
    return monitor


def count_lines(func, func_name=None):
    global _count, _func_name
    _count = 0
    _func_name = func.__name__ if func_name is None else func_name

    with _SetTrace(monitor):
        func()
        print(f"{func_name} executed {_count} lines of code")

