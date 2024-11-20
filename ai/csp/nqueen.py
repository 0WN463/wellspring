from typing import Hashable, Sequence
from mytypes import Variable
from collections import defaultdict
from copy import copy

class NQueensProblem:
    class Var:
        def __init__(self, c: int):
            self.value = None
            self.c = c

        def __repr__(self) -> str:
            return f"{self.c}={self.value}"

        @property
        def id(self) -> Hashable:
            return self.c

        def is_assigned(self) -> bool:
            return self.value != None

        def assign(self, n: int) -> None:
            self.value = n

        def unassign(self) -> None:
            self.value = None


    class Assignment:
        def __init__(self, n: int):
            self._vars = [NQueensProblem.Var(i + 1) for i in range(n)]

        @property
        def vars(self) -> Sequence["NQueensProblem.Var"]:
            return self._vars

        def __repr__(self) -> str:
            return str([(r+1, v.value) for r, v in enumerate(self.vars) if v.is_assigned()])

        def get_one_unassigned(self) -> "NQueensProblem.Var | None":
            for v in self.vars:
                if not v.is_assigned():
                    return v

            return None

        def will_be_consistent(self, var: Variable[int], value: int) -> bool:
            ps = [(v.value, v.c) for v in self.vars if v.is_assigned() and v.id != var.id]
            for (r,c) in ps:
                assert(c is not None)

                if r == value:
                    return False

                if value - r == c - var.c:
                    return False

                if value - r == var.c - c:
                    return False

            return True

    class Inferences:
        def __init__(self) -> None:
            self.inferences = defaultdict(set)

        def __deepcopy__(self, memo) -> "Inferences":
            new_inferences = type(self)()

            for k, v in self.inferences.items():
                new_inferences.inferences[k] = copy(v)

            return new_inferences

        def get_inference(self, var: Variable[int]) -> set[int]:
            return self.inferences[var.id]

        def add(self, var: Variable[int], invalid_value: int) -> None:
            self.inferences[var.id].add(invalid_value)

        def remove(self, var: Variable[int], invalid_values: set[int]) -> None:
            if not invalid_values:
                return

            self.inferences[var.id] -= invalid_values


    def __init__(self, n: int):
        self.n = n
        self.assignment = NQueensProblem.Assignment(n)
        self.domain = set(i for i in range(1, self.n + 1))

    def get_domain(self, v: Variable[int]) -> set[int]:
        return self.domain


def show(a: NQueensProblem.Assignment, inferences: NQueensProblem.Inferences) -> None:
    n = len(a.vars)

    arr = [['.' for _ in range(n)] for _ in range(n)]

    for c, v in enumerate(a.vars):
        if v.is_assigned():
            arr[v.value - 1][c] = 'Q'

    for v, vs in inferences.inferences.items():
        for invalid_value in vs:
            arr[invalid_value-1][v-1] = 'X'

    print('\n'.join(map( lambda x: ''.join(x), arr)))
    print('\n')
