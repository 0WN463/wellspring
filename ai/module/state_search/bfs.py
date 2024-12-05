from __future__ import annotations
from .state import State, Cost, GoalFunc
from collections import deque


def make_bfs(is_graph_search: bool):
    def search(s: State, goal_func: GoalFunc) -> Cost | None:
        if is_graph_search:
            visited: set[State] = set()

        frontier: deque[tuple[State, Cost]] = deque()
        frontier.append((s, Cost(0)))

        while frontier:
            s, cost = frontier.popleft()

            if is_graph_search:
                if s in visited:
                    continue
                visited.add(s)

            if goal_func(s):
                return cost

            for c in s.children():
                frontier.append((c.state, c.cost + cost))

        return None

    return search
