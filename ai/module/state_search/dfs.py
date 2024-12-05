from __future__ import annotations
from .state import State, Cost, GoalFunc
from .decorator import decorate_if, to_graph_search


def make_dfs(is_graph_search: bool, use_stack=True):
    @decorate_if(to_graph_search, is_graph_search)
    def implicit(s: State, goal_func: GoalFunc) -> Cost | None:
        if goal_func(s):
            return Cost(0)

        for t in s.children():
            res = implicit(t.state, goal_func)

            if res is not None:
                return t.cost + res

        return None

    def explicit(s: State, goal_func: GoalFunc) -> Cost | None:
        if is_graph_search:
            visited: set[State] = set()

        if goal_func(s):
            return Cost(0)

        stack = [(s, iter(s.children()), Cost(0))]

        while stack:
            v, it, cost = stack[-1]

            if goal_func(v):
                return cost

            if is_graph_search:
                visited.add(v)

            for c in it:
                if is_graph_search and c.state in visited:
                        continue

                stack.append((c.state, iter(c.state.children()), c.cost + cost))
                break
            else:
                stack.pop()

        return None

    return explicit if use_stack else implicit
