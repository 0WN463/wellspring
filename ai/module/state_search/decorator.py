from .state import State
from typing import Callable, Concatenate

def decorate_if[T](dec: Callable[[T], T], cond: bool) -> Callable[[T], T]:
    def wrapper(f: T) -> T:
        if not cond:
            return f
        return dec(f)

    return wrapper

def to_graph_search[T, **P](f: Callable[Concatenate[State, P], T | None]) -> Callable[Concatenate[State, P], T | None]:
    visited:set[State] = set()
    def wrapper(s: State, *args: P.args, **kwargs: P.kwargs) -> T | None:
        if s in visited:
            return None

        visited.add(s)

        return f(s, *args, **kwargs)

    return wrapper
