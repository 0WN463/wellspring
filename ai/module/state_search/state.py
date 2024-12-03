from __future__ import annotations
from typing import Protocol, Callable
from dataclasses import dataclass, field

@dataclass
class Cost:
    value: int | float

    def __add__(self, other):
        return Cost(self.value + other.value)

@dataclass
class Transition:
    state: State
    cost: Cost = field(default_factory=lambda: Cost(1))


class State(Protocol):
    def children(self) -> list[Transition]:
        ...

GoalFunc = Callable[[State], bool]

class Vertex():
    def __init__(self, transitions: list[Transition]) -> None:
        self._transitions = transitions

    def children(self) -> list[Transition]:
        return self._transitions 

    def add_transition(self, transition: Transition) -> None:
        self._transitions.append(transition)

class InfiniteVertex():
    def children(self) -> list[Transition]:
        return [Transition(state=InfiniteVertex(), cost=Cost(1))]
