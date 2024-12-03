from __future__ import annotations
from typing import Literal
from .state import State, Cost, GoalFunc
from .decorator import decorate_if, to_graph_search


def make_dls(is_graph_search: bool):
    @decorate_if(to_graph_search, is_graph_search)
    def depth_limited_search(s: State, goal_func: GoalFunc, depth: int) -> Cost | None | Literal["DepthExhausted"]:
        if goal_func(s):
            return Cost(0)

        if depth == 0:
            return "DepthExhausted"

        has_exhausted = False
        for t in s.children():
            res = depth_limited_search(t.state, goal_func, depth-1)

            if res is None:
                continue

            # DepthExhausted occurs when dls fails to visit the whole graph before using all its depth
            if res == "DepthExhausted":
                has_exhausted = True
                continue

            return t.cost + res

        return "DepthExhausted" if has_exhausted else None

    return depth_limited_search
