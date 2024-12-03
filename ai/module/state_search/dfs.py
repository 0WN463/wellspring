from __future__ import annotations
from .state import State, Cost, GoalFunc
from .decorator import decorate_if, to_graph_search


def make_dfs(is_graph_search: bool):
    @decorate_if(to_graph_search, is_graph_search)
    def search(s: State, goal_func: GoalFunc) -> Cost | None:
        if goal_func(s):
            return Cost(0)

        for t in s.children():
            res = search(t.state, goal_func)

            if res is not None:
                return t.cost + res

        return None

    return search
