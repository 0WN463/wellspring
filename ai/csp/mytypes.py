from typing import Protocol, Hashable, Sequence

class Variable[T](Protocol):
    # Used to uniquely identify a variable
    @property
    def id(self) -> Hashable:
        ...

    def is_assigned(self) -> bool:
        ...

    def assign(self, n: T) -> None:
        ...

    def unassign(self) -> None:
        ...
    

class Assignment[T](Protocol):
    def get_one_unassigned(self) -> Variable[T] | None:
        ...

    @property
    def vars(self) -> Sequence[Variable[T]]:
        ...

    def will_be_consistent(self, var: Variable[T], value: T) -> bool:
        ...


class Inferences[T]:
    def __deepcopy__(self, memo) -> "Inferences[T]":
        ...
    # Returns a set of invalid values for the variable
    def get_inference(self, var: Variable[T]) -> set[T]:
        ...

    def add(self, var: Variable[T], invalid_value: T) -> None:
        ...

    def remove(self, var: Variable[T], invalid_values: set[T]) -> None:
        ...


class CSP[T](Protocol):
    @property
    def assignment(self) -> Assignment[T]:
        ...

    def get_domain(self, v: Variable[T]) -> set[T]:
        ...

