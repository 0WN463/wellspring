from __future__ import annotations
from typing import Literal
from .state import State, Cost, GoalFunc
from .decorator import decorate_if, to_graph_search


def make_dls(is_graph_search: bool, use_stack=True):
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

    def explicit(s: State, goal_func: GoalFunc, depth: int) -> Cost | None | Literal["DepthExhausted"]:
        if is_graph_search:
            visited: set[State] = set()

        if goal_func(s):
            return Cost(0)

        stack = [(s, iter(s.children()), Cost(0), depth)]

        depth_exhausted = False
        while stack:
            v, it, cost, depth = stack[-1]

            if goal_func(v):
                return cost

            if is_graph_search:
                visited.add(v)

            if depth == 0:
                depth_exhausted = True
                stack.pop()
                continue

            for c in it:
                if is_graph_search and c.state in visited:
                        continue

                stack.append((c.state, iter(c.state.children()), c.cost + cost, depth-1))
                break
            else:
                stack.pop()

        return "DepthExhausted" if depth_exhausted else None

    return explicit if use_stack else depth_limited_search
