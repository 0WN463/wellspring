from dataclasses import dataclass
from enum import Enum
from typing import Protocol, Callable
from functools import wraps
import contextlib

@contextlib.contextmanager
def memoize(f, hash_func: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        h = hash_func(*args, **kwargs)
        if (res := f.table.get(h)) is not None:
            return res

        res = f(*args, **kwargs)
        f.table[h] = res
        return res
    f.table = {}

    globals()[f.__name__] = wrapper
    yield
    globals()[f.__name__] = f

class Counter:
    def __init__(self):
        self.count = 0

    def __str__(self):
        return str(self.count)

    def inc(self):
        self.count += 1

@contextlib.contextmanager
def count(f, counter=None):
    @wraps(f)
    def wrapper(*args, **kwargs):
        counter.inc()
        return f(*args, **kwargs)
    counter = counter if counter else Counter()

    globals()[f.__name__] = wrapper
    yield counter
    globals()[f.__name__] = f

class NodeType(Enum):
    MIN = 0
    MAX = 1

    @property
    def comp(self):
        return min if self == NodeType.MIN else max


class Game(Protocol):
    def is_terminal(self) -> tuple[bool, float]:
        pass

    @property
    def nodetype(self) -> NodeType:
        pass

    def children(self) -> list['Game']:
        pass

def minimax(node:Game) -> float:
    is_terminal, value = node.is_terminal()
    if is_terminal:
        return value
    value = node.nodetype.comp(minimax(child) for child in node.children())
    return value



def alphabeta(node:Game) -> float:
    func = max_val if node.nodetype == NodeType.MAX else min_val

    return func(node, float('-infinity'), float('infinity'))

def max_val(node:Game, alpha:float, beta:float):
    is_terminal, value = node.is_terminal()
    if is_terminal:
        return value

    v = -float("infinity")

    for child in node.children():
        v = max(v, min_val(child, alpha, beta))

        if v >= beta:
            return v

        alpha = max(alpha, v)

    return v


def min_val(node:Game, alpha:float, beta:float):
    is_terminal, value = node.is_terminal()
    if is_terminal:
        return value
    
    v = float("infinity")

    for child in node.children():
        v = min(v, max_val(child, alpha, beta))

        if v <= alpha:
            return v

        beta = min(beta, v)

    return v



class Player(Enum):
    WHITE = 'W'
    BLACK = 'B'

    @property
    def opponent(self):
        return Player.WHITE if self == Player.BLACK else Player.BLACK

@dataclass
class Action:
    pawn: tuple[int, int]
    to: tuple[int, int]

    

@dataclass
class State:
    def __init__(self, grid, curr_player=Player.WHITE):
        assert all(len(r) == len(grid[0]) for r in grid)
        self.grid = grid
        self.curr_player = curr_player

    def __repr__(self):
        return '\n'.join(''.join(r) for r in self.grid)

    @staticmethod
    def new_square(n): 
        return State(['W'*n, *['.'*n], 'B' * n])

    def is_terminal(self):
        if 'B' in self.grid[0]:
            return True, 'B'

        if 'W' in self.grid[-1]:
            return True, 'W'

        if all('W' not in r for r in self.grid):
            return True, 'B'

        if all('B' not in r for r in self.grid):
            return True, 'W'

        if not self.moves():
            return True, None

        return False, None

    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0])

    def moves(self):
        pawns = [(i, j) for i in range(self.rows) for j in range(self.cols) if self.grid[i][j] == self.curr_player.value]

        dy = 1 if self.curr_player == Player.WHITE else -1

        advances = [Action((i, j), (dy + i, j)) for i, j in pawns if 0 <= dy+i < self.rows and self.grid[dy+i][j] == '.']
        captures= [Action((i, j), (dy + i, j + dx)) for i, j in pawns for dx in [-1, 1] if 0 <= dy+i < self.rows and 0 <= dx + j < self.cols and self.grid[dy+i][j+dx] == self.curr_player.opponent.value]
        return [*advances, *captures]

    def next(self, action: Action):
        arr = [[c for c in r] for r in self.grid]

        arr[action.to[0]][action.to[1]] = arr[action.pawn[0]][action.pawn[1]]
        arr[action.pawn[0]][action.pawn[1]] = '.'
        new = State([''.join(row) for row in arr], curr_player=self.curr_player.opponent)


        return new

class Tree():
    def __init__(self, game):
        self.game = game
    def is_terminal(self):
        boo, winner = self.game.is_terminal()
        if winner is None:
            return boo, 0
        return boo, 1 if winner == Player.WHITE.value else -1
    def children(self):
        return (Tree(self.game.next(m)) for m in self.game.moves())
    
    @property
    def nodetype(self):
        return NodeType.MAX if self.game.curr_player == Player.WHITE else NodeType.MIN

    @property
    def hash(self):
        return tuple([*self.game.grid, self.game.curr_player])

#s = Tree(State(['WW', '..', '..', 'BB']))

s = Tree(State.new_square(5))
with count(minimax) as c:
    print(minimax(s))
    print(c.count)

hash_func = lambda *args: args[0].hash
with memoize(minimax, hash_func):
    with count(minimax) as c:
        print(minimax(s))
        print(c)

with count(min_val) as c:
    with count(max_val, c) as c:
        print(alphabeta(s))
        print(c)

with memoize(min_val, hash_func):
    with memoize(max_val, hash_func):
        with count(min_val) as c:
            with count(max_val, c) as c:
                print(alphabeta(s))
                print(c)

