from __future__ import annotations
import unittest
from state_search import state, dfs, dls, ids, bfs
from dataclasses import dataclass
from typing import Callable, Literal, TypeAlias
import sys
import signal


class timeout:
    def __init__(self, seconds=0.001, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.setitimer(signal.ITIMER_VIRTUAL, self.seconds)
        signal.signal(signal.SIGVTALRM, self.handle_timeout)

    def __exit__(self, type, value, traceback):
        signal.setitimer(signal.ITIMER_VIRTUAL, 0)


@dataclass
class Input:
    name: str
    start: state.State
    goal: state.State | None
    actual_cost: int | None


Expectation: TypeAlias = int | Literal['correct'] | Literal["nonterminate"] | Literal["DepthExhausted"]
FuncUnderTest: TypeAlias = Callable[[
    state.State, dfs.GoalFunc], state.Cost | None | Literal["DepthExhausted"]]


@dataclass
class TestCase:
    input: Input
    func_under_test: FuncUnderTest
    expected: Expectation


def line_graph() -> Input:
    extra = state.Vertex(transitions=[])
    goal = state.Vertex(transitions=[state.Transition(state=extra)])

    v = goal

    for _ in range(3):
        v = state.Vertex(transitions=[state.Transition(state=v)])

    return Input("line graph", v, goal, 3)


def line_graph_no_goal() -> Input:
    extra = state.Vertex(transitions=[])
    v = state.Vertex(transitions=[state.Transition(state=extra)])

    for _ in range(3):
        v = state.Vertex(transitions=[state.Transition(state=v)])

    return Input("line graph no goal", v, None, None)


def diamond_graph_goal_first() -> Input:
    goal = state.Vertex(transitions=[])

    a = state.Vertex(transitions=[state.Transition(state=goal)])
    b = state.Vertex(transitions=[state.Transition(
        state=goal), state.Transition(state=a)])
    c = state.Vertex(transitions=[state.Transition(state=b)])

    return Input("diamond graph goal first", c, goal, 2)


def diamond_graph_goal_second() -> Input:
    goal = state.Vertex(transitions=[])

    a = state.Vertex(transitions=[state.Transition(state=goal)])
    b = state.Vertex(transitions=[state.Transition(
        state=a), state.Transition(state=goal)])
    c = state.Vertex(transitions=[state.Transition(state=b)])

    return Input("diamond graph goal second", c, goal, 2)


def infinite_graph_goal_first() -> Input:
    goal = state.Vertex(transitions=[])

    v = state.Vertex(transitions=[state.Transition(
        state=goal), state.Transition(state=state.InfiniteVertex())])

    return Input("infinite graph goal first", v, goal, 1)


def infinite_graph_goal_second() -> Input:
    goal = state.Vertex(transitions=[])

    v = state.Vertex(transitions=[state.Transition(
        state=state.InfiniteVertex()), state.Transition(state=goal)])

    return Input("infinite graph goal second", v, goal, 1)


def cyclic_graph_no_goal() -> Input:
    v1 = state.Vertex(transitions=[])

    v2 = state.Vertex(transitions=[state.Transition(state=v1)])
    v1.add_transition(state.Transition(state=v2))

    return Input("cyclic graph no goal", v2, None, None)


def cyclic_graph_goal_second() -> Input:
    goal = state.Vertex(transitions=[])

    v1 = state.Vertex(transitions=[])
    v2 = state.Vertex(transitions=[state.Transition(state=v1)])
    v1.add_transition(state.Transition(state=v2))
    v1.add_transition(state.Transition(state=goal))

    return Input("cyclic graph goal second", v2, goal, 2)


def cyclic_graph_goal_first() -> Input:
    goal = state.Vertex(transitions=[])

    v1 = state.Vertex(transitions=[])
    v2 = state.Vertex(transitions=[state.Transition(state=v1)])
    v1.add_transition(state.Transition(state=goal))
    v1.add_transition(state.Transition(state=v2))

    return Input("cyclic graph goal first", v2, goal, 2)


table_inputs = [
    line_graph(),
    line_graph_no_goal(),
    diamond_graph_goal_first(),
    diamond_graph_goal_second(),
    infinite_graph_goal_first(),
    infinite_graph_goal_second(),
    cyclic_graph_goal_first(),
    cyclic_graph_goal_second(),
    cyclic_graph_no_goal(),
]


class TestTable(unittest.TestCase):
    def test_dfs_tree(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            3,
            "correct",
            "nonterminate",
            "correct",
            "nonterminate",
            "nonterminate",
        ]

        self._table(expecteds, lambda s,
                    goal_func: dfs.make_dfs(False)(s, goal_func))

    def test_dfs_graph(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            3,
            "correct",
            "nonterminate",
            "correct",
            "correct",
            "correct",
        ]

        self._table(expecteds, lambda s,
                    goal_func: dfs.make_dfs(True)(s, goal_func))

    def test_dls_tree(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            3,
            "correct",
            "correct",
            "correct",
            4,
            "DepthExhausted",
        ]

        self._table(expecteds, lambda s, goal_func: dls.make_dls(
            False)(s, goal_func, depth=5))

    def test_dls_graph(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            3,
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
        ]

        self._table(expecteds, lambda s, goal_func: dls.make_dls(
            True)(s, goal_func, depth=5))

    def test_ids_tree(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "nonterminate",
        ]

        self._table(expecteds, lambda s,
                    goal_func: ids.make_ids(False)(s, goal_func))

    def test_ids_graph(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
        ]

        self._table(expecteds, lambda s,
                    goal_func: ids.make_ids(True)(s, goal_func))

    def test_bfs_tree(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "nonterminate",
        ]

        self._table(expecteds, lambda s,
                    goal_func: bfs.make_bfs(False)(s, goal_func))

    def test_bfs_graph(self) -> None:
        expecteds: list[Expectation] = [
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
            "correct",
        ]

        self._table(expecteds, lambda s,
                    goal_func: bfs.make_bfs(True)(s, goal_func))

    def _table(self, expecteds: list[Expectation], func: FuncUnderTest) -> None:
        test_cases = [TestCase(
            input=i,
            expected=o,
            func_under_test=func)
            for i, o in zip(table_inputs, expecteds, strict=True)
        ]

        sys.setrecursionlimit(100)
        for t in test_cases:
            def goal_func(v): return v == t.input.goal

            with self.subTest(t.input.name):
                if t.expected == "nonterminate":

                    with self.assertRaises((TimeoutError, RecursionError), msg="should not terminate"):
                        with timeout():
                            t.func_under_test(t.input.start, goal_func)

                    continue

                with timeout():
                    res = t.func_under_test(t.input.start, goal_func)

                if t.expected == "correct":
                    self.assertEqual(res, state.Cost(
                        t.input.actual_cost) if t.input.actual_cost is not None else None, msg=f"distance should be {t.input.actual_cost}")
                elif t.expected == "DepthExhausted":
                    self.assertEqual(
                        res, t.expected, msg=f"should exhaust all depth")
                else:
                    self.assertEqual(res, state.Cost(
                        t.expected), msg=f"should get wrong distance of {t.expected}")


class TestDFSDepthLimited(unittest.TestCase):
    def test_line_graph_exact_depth_correct(self):
        case = line_graph()
        assert (case.actual_cost == 3)

        def goal_func(v): return v == case.goal

        res = dls.make_dls(False)(case.start, goal_func=goal_func, depth=3)
        self.assertEqual(res, state.Cost(case.actual_cost),
                         f"dfs should obtain distance of {case.actual_cost}")

    def test_line_graph_insufficient_depth_wrong(self):
        case = line_graph()
        assert (case.actual_cost == 3)

        def goal_func(v): return v == case.goal

        res = dls.make_dls(False)(case.start, goal_func=goal_func, depth=2)
        self.assertEqual(res, "DepthExhausted", "dls should exhaust its depth")

    def test_diamond_graph_correct(self):
        case = diamond_graph_goal_second()
        assert (case.actual_cost == 2)

        def goal_func(v): return v == case.goal

        res = dls.make_dls(False)(case.start, goal_func=goal_func, depth=2)
        self.assertEqual(res, state.Cost(
            case.actual_cost), f"dfs should obtain distance of {case.actual_cost} when actual cost == depth")


if __name__ == '__main__':
    unittest.main()
