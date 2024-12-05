from __future__ import annotations
from .state import State, Cost, GoalFunc
from .dls import make_dls

def make_ids(is_graph_search: bool):
    def iterative_deepening_search(s: State, goal_func: GoalFunc) -> Cost | None:
        d = 1
        while True:
            res = make_dls(is_graph_search)(s, goal_func, d)
            if res == "DepthExhausted":
                d += 1
                continue

            if res is None:
                return None

            return res

    return iterative_deepening_search
