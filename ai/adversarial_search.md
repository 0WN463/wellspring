---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
def is_pow2(n):
    return (n & (n - 1) == 0) and n != 0


from binarytree import tree, build

def build_tree(leaves):
    assert is_pow2(len(leaves))
    multiplier = 1000

    nodes = []
    level = 0

    while 2**level != len(leaves):
        nodes = nodes + [(1 if level % 2 == 0 else -1) * multiplier] * 2**level
        level += 1

    output = str(build(nodes + leaves))

    for i in range(output.count(str(-multiplier))):
        output = output.replace(
            str(-multiplier), f"P2.{i}".center(len(str(-multiplier))), 1
        )

    for i in range(output.count(str(multiplier))):
        output = output.replace(
            str(multiplier), f"P1.{i}".center(len(str(multiplier))), 1
        )

    return output
```

# Adversarial Search
Suppose we have 2 AI who are competing with each other in a **zero-sum game**. 
A zero-sum game is one that for any amount of utility achieved by a player at a terminal state, the other player suffer an equivalent amount of loss.

For the game to be well-defined, we would require there to be no recursive state in the game, because the utility of a infinite looping game cannot be defined.
We can supplement rules to the game such that this cannot be achieved, for example, the "three-fold" repetition rule in chess.

Thus, a simplification of the game would be a decision tree, where one player controls every odd-level nodes and the other controls the even-level nodes.

The player who control the node can decide which of the children node to use for the next state.

The game ends when a leave state is reached.
At that point, player 1 will achieve a utility of $x$ while player 2 will receive a utility of $-x$, where $x$ is the value of the state.
Usually, we denote some states as having positive values (where player 1 wins), and some as negative values (where player 2 wins).
However, we will stick to all positive values for discussion since it is more convenient to work with.
Note that we can shift the range of values such that each player has some states where they can win, while using the same analysis.


```
      ____P1.0____
     /            \
   P2.0           P2.1
 /     \        /     \
2       7      1       8
```

<!-- #region -->
In the above example, player 1 has choose whether the game will process to state `P2.0` or `P2.1`.

Then if `P2.0` was chosen, player 2 can choose to end the game with a value of 2 or 7.

Subsequently, if `P2.1` was chosen, player 2 can choose to end the game with a value of 1 or 8.

Note that the game tree may not be balanced; such cases are possible



```
      ____P1.0____
     /            \
   P2.0           10
 /     \      
2       7     
```

Also, note that the game tree also is not needed to be binary, a game state can allow more than 2 choices for any given player.


```
      ____P1.0____
     /     |      \
   P2.0    6      10
 /     \      
2       7     
```


## Goal of the Agents

At the leaves of the tree would be the final outcome of the game, each with a value.
One player would aim to maximise the final result while the other would aim to minimise it.

<!-- #endregion -->

```
                             ___________________________P1.0___________________________
                            /                                                          \
             ____________ P2.0___________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____P1.1____                   ____P1.2____                  ____P1.3____                   ____P1.4____
     /            \                 /            \                /            \                 /            \
   P2.2           P2.3            P2.4           P2.5           P2.6           P2.7            P2.8           P2.9
 /     \        /     \         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3
```


For the rest of the discussion, we will use the above decision tree as an example, with P1 as the maximizer and P2 as the minimizer.

<!-- #region -->
# Minimax

Suppose the game state is at P2.2, then the solution to the problem at this point is apparent.
The game state will proceed to 6 since that is the most rational option for P2.

Indeed, it is easy to determine in the most optimal action on the layers where all options are terminal states.

Notice that once we determine the values at all these states, then we can determine the value of the states above them, and so on and so forth.
This process is illustrated below


### Evaluate P2
```
                             ___________________________P1.0___________________________
                            /                                                          \
             ____________ P2.0___________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____P1.1____                   ____P1.2____                  ____P1.3____                   ____P1.4____
     /            \                 /            \                /            \                 /            \
    6              2               7              1              0              7               8              2  
 /     \        /     \         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3
```


### Evaluate P1

```
                             ___________________________P1.0___________________________
                            /                                                          \
             ____________ P2.0___________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____ 6  ____                   ____ 7  ____                  ____  7 ____                   ____ 8  ____
     /            \                 /            \                /            \                 /            \
    6              2               7              1              0              7               8              2  
 /     \        /     \         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3
```



### Evaluate P1
```
                             ___________________________ 7  ___________________________
                            /                                                          \
             ____________  6  ___________                                 ____________   7 ___________
            /                            \                               /                            \
      ____ 6  ____                   ____ 7  ____                  ____  7 ____                   ____ 8  ____
     /            \                 /            \                /            \                 /            \
    6              2               7              1              0              7               8              2  
 /     \        /     \         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3
```

Therefore, we know that for this game, player 1 will always achieve at least a score of 7, while player 2 achieve a loss of at least -7.

Thus, we have introduced Minimax, a way to determine the end result of the game (assuming both players play optimally) as well as the optimal move to make at each state of the game.

Minimax assumes that the opponent will play optimally, thus each agent is trying to minimize the value of the best possible move for the opponent.
<!-- #endregion -->

## Implementation
The below is the implementation of Minimax.
Notice that the main driver of the code is really short, simply 

```python
def minimax(node):
    if node.is_terminal:
        return node.value
    
    if node.nodetype == 'max':
        return max(minimax(child) for child in node.children)
    else:
        return min(minimax(child) for child in node.children)
```

```python
class Node:
    def __init__(self, value, children, nodetype):
        assert nodetype in ["max", "min", "terminal"]

        self.value = value
        self.children = children
        self.is_terminal = nodetype == "terminal"
        self.nodetype = nodetype


class GameTree:
    def __init__(self, leaves):
        assert is_pow2(len(leaves))

        leave_nodes = [Node(value, [], "terminal") for value in leaves]

        layers = [leave_nodes]

        while len(layers[0]) > 1:
            new_layer = []

            for a, b in zip(layers[0][0::2], layers[0][1::2]):
                new_node = Node(None, [a, b], "min" if len(layers) % 2 == 1 else "max")
                new_layer.append(new_node)

            layers.insert(0, new_layer)

        self.layers = layers
        self.leave_nodes = leave_nodes
        self.root = self.layers[0][0]


leaves = [7, 6, 2, 8, 8, 7, 1, 3, 0, 7, 7, 8, 8, 8, 2, 3]

tree = GameTree(leaves)

print("Value of root is:", minimax(tree.root))
```

## Time Complexity
Suppose that at each level, the game branches by $b$, and the game have a depth of $d$.

Using the above algorithm, the complexity is clearly $O(b^d)$

Even for simple games, this complexity may be too large to compute in time.

We can see that we explored 31 states for our previous problem.

```python
def count_state_explored(func):
    def wrapper(*args, **kwargs):
        wrapper.state_explored += 1
        return func(*args)

    wrapper.state_explored = 0
    return wrapper

minimax = count_state_explored(minimax)

print("Value of root is:", minimax(tree.root))
print("States Explored:", minimax.state_explored)
```

<!-- #region -->
# Alpha-beta Pruning

Consider the following tree that is mid evaluation, where X is the maximizer and Y is the minimizer, and the `?` represents any value:

```
      ____ Y  ____          
     /            \          
    6              X   ____________ ....
                /     \     \      \ 
               2       ?     ?      ? 
```

Since we saw a `2` as an option for X, we know that the value of the X node is at most 2.

Now, taking the perspective of Y, since it knows that the right path has a value of at most 2, Y will choose the left path with a value of `6` instead.

Notice that we did not need to evaluate any of the `?` to reach this conclusion.
In fact, they can be any possible value, since the `2` has already bounded the maximum possible value for the X node.
This means we can potentially skip a lot of evaluation of nodes by simply not exploring them, since we know they won't contribute to the solution.

This is the basis of alpha-beta pruning.


Let us consider the situation on the previous game tree after we evaluated the P2.2, and are beginning to evaluate P2.3

```
                             ___________________________P1.0___________________________
                            /                                                          \
             ____________ P2.0___________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____P1.1____                   ____P1.2____                  ____P1.3____                   ____P1.4____
     /            \                 /            \                /            \                 /            \
    6             P2.3            P2.4           P2.5           P2.6           P2.7            P2.8           P2.9
 /     \        /     \         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

Suppose that when we evaluate the first leaf in P2.3, we chose 2.

Notice that since 2 is smaller than the value that we got in the other branch (P2.1), we can immediately say that this branch is more optimal for P2, the minimizer.
Thus, P1 will never choose the branch on the right since it is always worse for him.
This means that we do not need to evaluate the other leaf (9), which means we can potentially save the computation of some states by ignoring them.

We will use a `*` to denotes paths that we do not have to evaluate fully.

```
                             ___________________________P1.0___________________________
                            /                                                          \
             ____________ P2.0___________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____P1.1____                   ____P1.2____                  ____P1.3____                   ____P1.4____
     /            *                 /            \                /            \                 /            \
    6             ≤2             P2.4           P2.5           P2.6           P2.7            P2.8           P2.9
 /     \        /     *         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```
Note that we do not know the exact value of the state in 2, since it is possible that the other branch have some value smaller than 2, _eg_ the other branch is actually a 1 instead of an 8, then the value of this node is actually 1 instead of 2; but we know that the value is **at most** 2, and thus we know that the maximizer at P1.1 will not want this path.

Equivalently, we perform the same logic to obtain bounds on the higher layers at this point.


```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________ P2.0 __________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____  6 ____                   ____P1.2____                  ____P1.3____                   ____P1.4____
     /            *                 /            \                /            \                 /            \
    6              ≤2             P2.4           P2.5           P2.6           P2.7            P2.8           P2.9
 /     \        /     *         /     \        /     \        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

Proceeding to evaluate other leaves, we will get the follow sequence of evaluations.


```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________ P2.0 __________                                 ____________ P2.1___________
            /                            \                               /                            \
      ____  6 ____                   _____ 7_____                  ____P1.3____                   ____P1.4____
     /            *                 /            *                /            \                 /            \
    6              ≤2              7             ≤1             P2.6           P2.7            P2.8           P2.9
 /     \        /     *         /     \        /    *         /     \        /     \         /     \        /     \
7       6      2       8       8       7      1      3       0       7      7       8       8       8      2       3

```

Again, at this point, notice that P2.0 will never go to the right path, thus we can also prune it.


```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________  6 ____________                                 ____________ P2.1___________
            /                            *                               /                            \
      ____  6 ____                   _____ 7_____                  ____P1.3____                   ____P1.4____
     /            *                 /            *                /            \                 /            \
    6              ≤2              7             ≤1             P2.6           P2.7            P2.8           P2.9
 /     \        /     *         /     \        /     *        /     \        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

<!-- #endregion -->

Continuing on
```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________ 6 ____________                                 ____________ P2.1___________
            /                            *                               /                            \
      ____ 6 ____                   _____ 7 _____                  ____P1.3____                   ____P1.4____
     /            *                 /            *                *            \                 /            \
    6              ≤2              7             ≤1             ≤0            P2.7             P2.8           P2.9
 /     \        /     *         /     \        /     *        /     *        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

Notice that once we see the 0 in the leaf, we can immediately prune that branch since P1 can always obtain a better reward of 6 from going to P2.0 from the root instead.
This is called **deep cutoff**, where we prune the tree using information that is further up the tree.

Continuing on, evaluating the other branch
```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________  6 ____________                                 ___________ P2.1 __________
            /                            *                               /                            \
      ____  6 ____                   _____ 7_____                  ____ 7  ____                   ____P1.4____
     /            *                 /            *                *            \                 /            \
    6              ≤2              7             ≤1             ≤0              7              P2.8           P2.9
 /     \        /     *         /     \        /     *        /     *        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

```
                             _________________________ P1.0 ___________________________
                            /                                                          \
             ____________ ≤6 ____________                                 ____________ P2.1 __________
            /                            *                               /                            \
      ____ ≥6 ____                   _____≥7_____                  ____ 7 ____                    ____P1.4____
     /            *                 /            *                *            \                 /            \
    6              ≤2              7              1             ≤0              7               8             P2.9
 /     \        /     *         /     \        /     *        /     *        /     \         /     \        /     \
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

Once again, since the value of P1.4 is at least 8, the P2 would rather go to P1.3 with a value of 7.

```
                             ___________________________ ≥7 ___________________________
                            /                                                          \
             ____________ ≤6 ____________                                 ____________ ≤7  ___________
            /                            *                               /                            *
      ____ ≥6 ____                   _____≥7_____                  ____ ≥7 ____                   ____≥9______
     /            *                 /            *                *            \                 /            *
    6              ≤2              7              1             ≤0              7               8             P2.9
 /     \        /     *         /     \        /     *        /     *        /     \         /     \        *     *
7       6      2       8       8       7      1       3      0       7      7       8       8       8      2       3

```

Notice at for levels belonging to the maximiser, we are using the upper bound of the lower level, while for levels belonging to the minimizer, we are using the lower bound.

This is exactly what we call alpha and beta.

α: best value from POV of max player

β: best value from POV of min player


## Implementation


```python
def max_val(node, alpha, beta):
    if node.is_terminal:
        return node.value

    v = -float("infinity")

    for child in node.children:
        v = max(v, min_val(child, alpha, beta))

        if v >= beta:
            return v

        alpha = max(alpha, v)

    return v


def min_val(node, alpha, beta):
    if node.is_terminal:
        return node.value

    v = float("infinity")

    for child in node.children:
        v = min(v, max_val(child, alpha, beta))

        if v <= alpha:
            return v

        beta = min(beta, v)

    return v


print("Value of root is:", max_val(tree.root, -float("infinity"), float("infinity")))
```

## Time Complexity
Now, we can see how many state we explored using alpha-beta pruning

```python
max_val = count_state_explored(max_val)
min_val = count_state_explored(min_val)

state_explored = 0

print("Value of root is:", max_val(tree.root, -float("infinity"), float("infinity")))
print("States Explored:", max_val.state_explored + min_val.state_explored)
```

As we can see, the number of states have been cut by some sizeable amount.

Since the number of states pruned is heavily dependant on how the leaves are arranged, we will only consider the best case complexity.

In the best case, we will prune every other branch in the game tree, thus we can effectively half the branching factor.

Thus, our complexity is $O(b^{d/2})$ in the best case.

However, this is still insufficient to solve slightly complex problems like checkers.

## Maximum/minimum state

Another small optimization we can make is to perform the alpha-beta pruning once we find a child which has the value of maximum possible value for the maximizer, or minimum possible value for the minimizer.
Once we find such child, we don't need to consider further children since we know that child will be the best option for the player.
For example, in chess, a player wouldn't need to consider other moves if he found a move that forces checkmate.


# Heuristic
Suppose that we do not evaluate the exact value of each state, but rather have some heuristic that can approximate the value of each state.

For example, for those familiar with chess, usually people assign pawns a value of 1, bishop/knights a value of 3, rooks a value of 5 and queen a value of 8.

Then for each possible chess board state, we evaluate the sum of our pieces - sum of the opponents pieces.
For boards where the king is checkmated, we assign it the value of $-\infty$ or $\infty$.

With this, we can quickly evaluate the values of the next state of the board without determining the values of the children.

This allows us to decide the best action at each state.

However, this doesn't always give the best move, unless the heuristic used perfectly matches the value of each game state.
Thus, we perform normal alpha-beta pruning as per usual, only switching to the heuristic evaluation of the node when we reach a certain depth in the game tree.

```python
class Hexapawn():
    def __init__(self, n:int=3, points=[1]*3, curr_player='W', board=None):
        assert(len(points) == n)
        self.board = ['B' * n, *['.' * n for _ in range(n-2)], 'W' * n] if board == None else board
        self.points = points
        self.curr_player = curr_player

    def is_terminal():
        return 'W' in self.board[0] or 'B' in self.board[-1]

    def value(self):
        if 'W' in self.board[0]:
            return self.points[self.board[0].index('W')]

        if 'B' in self.board[-1]:
            return self.points[self.board[-1].index('B')]

    def children(self):
        piece = self.curr_player
        delta = 1 if self.player == 'W' else -1

        res = []
        for i in range(n):
            for j in range(n):
                if self.board[i][j] != piece:
                    continue

                if self.board[i+delta][j] == '.':
                    res.append(Hexapawn(n=self.n, points=self.points, curr_player='B' if self.curr_player=='W' else 'W'))
```
