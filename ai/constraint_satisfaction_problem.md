---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Constraint Satisfaction Problems
A CSP is defined as a problem where the AI is tasked to find a set of values for each of the variable such that it satisfy all the constraints given.

Thus, there are the following parameters:
* Variables: $\{x_1, \dots, x_n\}$
* Domain of variables: $D_i$. This represents the range of values a given variable can take.
* Constraints: $C_i$. Constraints can be relating one or multiple variables together.

One common way to solve CSP's is with [backtrack search](#backtrack-search), which we will discuss in the case study.

## Case Study: N-queens
A classic problem is the N-queens problem.

The problem is simply define as finding a placement for n queens on a $n \times n$ chessboard such that no two queens attack each other.

For example, when n = 4, the following is one possible placement

```
+---+---+---+---+
|   |   | Q |   |
+---+---+---+---+
| Q |   |   |   |
+---+---+---+---+
|   |   |   | Q |
+---+---+---+---+
|   | Q |   |   |
+---+---+---+---+
```

### Naive Approach
A naive approach is to simply iterate through all possible locations for the 4 queens and find those that are valid.

However, even for such a small board, there are $C^{16}_4 = 1820$ combinations to consider.

A smarter approach is to notice that no two queens can be on the same column, so we can iterate all the possible rows for the queen at a particular column.

This brings our search down to $4^4 = 256$ states.

<!-- #region -->

### Backtrack Seach (without inference)
#### Intuition
Suppose we solve this problem logically.
Consider the case where we place a queen in the cell $(1,1)$, as per below.

```
+---+---+---+---+
| Q |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
```

Now suppose that we place the next queen in the cell $(1, 2)$

```
+---+---+---+---+
| Q | Q |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
|   |   |   |   |
+---+---+---+---+
```

Since the two queens attack each other, we know that whatever assignment we give to queens 3 and 4 will still result in a invalid configuration.
Thus, we can "prune" any configuration that arises from this sub-state.
Note that we still need to explore this invalid sub-state in order to determine that it and all its children are invalid.

Thus, if we calculate the number of (sub-)states needed to determine find all the valid state that arises with a $(1,1)$ queen, we would need:
* $Q_1: 1$
* $Q_2: 4$, $2$ of which are valid children
* $Q_3: 2 \times 4 = 8$, no valid children for $Q_2 = 3$, 1 for $Q_2 = 4$
* $Q_4: 1 \times 4 = 4$, none of which are valid.

Total states = $1 + 4 + 8 + 4 = 17$, which is much less than $4^3=64$ by the naive approach

#### Pseudocode
``` python
BacktrackSearch(prob, assign) # prob is the problem, assign is the current assignment of variables
    if AllVarsAreAssigned(prob, assign)
        return assign
    
    var = pick an unassigned var(prob,assign)
    
    for val in PossibleValuesOfVar(var,prob,assign)
        if (val is consistent with assignment)
            add {var=val} to assign
            
        result = BacktrackSearch(prob, assign)
        
        if(result != failure)
            return result

        remove {var=value} from assignemnt

    return failure
```


```python
PossibleValuesOfVar(var,prob,assign)
    if var is in assign
        return assignment of var in assign
    else
        return Domain of var
```
The pseudo code is written vaguely to allow for generalization to different problems.

<!-- #endregion -->

#### Implementation

```python
from itertools import combinations
from common.count import count

def backtrack_search(prob, assign):
    if all([val != None for val in assign]):
        return assign

    var = assign.index(None)
    assign = assign.copy()

    for val in prob.get_values(var, assign):
        if prob.is_consistent(var, val, assign):
            assign[var] = val
            result = backtrack_search(prob, assign)

            if result != None:
                return result

            assign[var] = None

    return None


class NQueenProblem:
    def __init__(self, n):
        self.n = n

    def get_initial_domain(self):
        return set([i for i in range(self.n)])

    def get_values(self, var, assign):
        domain = self.get_initial_domain()

        return domain

    def is_consistent(self, var, val, assign):
        cells = []
        for col, row in enumerate(assign):
            if row != None:
                cells.append((row, col))
        cells.append((val, var))
        for (x1, y1), (x2, y2) in combinations(cells, r=2):
            if x1 == x2:
                return False
            if y1 == y2:
                return False
            if x1 - x2 == y1 - y2:
                return False
            if x1 - x2 == y2 - y1:
                return False
        return True


prob = NQueenProblem(n=4)

with count(backtrack_search, globals()) as num_function_calls:
    print(backtrack_search(prob, [None for i in range(4)]))
    print("Number of function calls:", num_function_calls)
```

```python
prob = NQueenProblem(n=8)
with count(backtrack_search, globals()) as num_function_calls:
    print(backtrack_search(prob, [None for i in range(8)]))
    print("Number of function calls:", num_function_calls)
```

Note that the number of function calls is slightly different from the number of state explored, because we did not count the number of invalid states that the AI considered for a given assignment.


### Backtrack Seach (with inference) <a id="backtrack-search"></a>
We can model the problem as a CSP with the following parameters:
* Variables: $\{x_1, \dots, x_4\}$, where $x_i$ is the row number of the queen in the $i^{ith}$ column
* Domain of variables: $D_i = \{1, 2, 3, 4\}$ for $1 \leq i \leq 4$, since each queen can take any row.
* Constraints: $C_{i,j} = \text{NoAttack}(x_i, x_j)$ for $1 \leq i,j \leq 4$. NoAttack returns true if a queen in the $i^{th}$ column, $x_i^{th}$ row will not attack a queen in the $j^{th}$, $x_j^{th}$, false otherwise.

#### Intuition
Suppose we solve this problem logically.
Consider the case where we place a queen in the cell $(1,1)$, as per below.
We can indicate the cells that are no longer available (marked with an `x`) for the queens in the other columns.
This is called an **inference**.

```
+---+---+---+---+
| Q | x | x | x |
+---+---+---+---+
|   | x |   |   |
+---+---+---+---+
|   |   | x |   |
+---+---+---+---+
|   |   |   | x |
+---+---+---+---+
```

Now suppose that there is a queen in the cell $(3, 2)$ and perform inference as per below.

```
+---+---+---+---+
| Q | x | x | x |
+---+---+---+---+
|   | x | x |   |
+---+---+---+---+
|   | Q | x | x |
+---+---+---+---+
|   |   | x | x |
+---+---+---+---+
```

Notice that we do not have a valid value for column 3, thus the current configuration must be invalid.

Now suppose that there is a queen in the cell $(4, 2)$ and perform inference as per below.

```
+---+---+---+---+
| Q | x | x | x |
+---+---+---+---+
|   | x |   | x |
+---+---+---+---+
|   |   | x | x |
+---+---+---+---+
|   | Q | x | x |
+---+---+---+---+
```
Notice that we do not have a valid value for column 4, thus the current configuration must also be invalid.
Hence, it must be the case that there cannot be a queen in $(1,1)$.

Our previous approach searched 17 states to reach this conclusion, while we only searched 3 states!
(To be fair, the "amount of work" needed per state is different for the 2 algorithms, so it is not exactly a fair comparison).

Thus, we derive the following algorithm.

<!-- #region -->
#### Pseudocode

```python 
BacktrackSearch(prob, assign, inferences)
    if AllVarsAreAssigned(prob, assign)
        return assign
    
    var = pick an unassigned var(prob,assign)
    
    for val in PossibleValuesOfVar(var,prob,assign)
        if (val is consistent with assignment)
            add {var=val} to assign

        inference = Infer(prob, var, assign)

        add inference to inferences

        if (inference != failure)
            result = BackTrackSearch(prob, assign, inferences)

        if(result != failure)
            return result

        remove {var=value} and inference from inferences

    return failure
```

``` python
Infer(prob, var, assign)
    inference = []
    varQueue = [var]
    while (varQueue is not empty)
        Y = varQueue.pop()
        
        for constraint where Y in (constraints with variable Y)
            for all X in variables of constraint that is not Y
                S = ComputeDomain(x, assign, inference)
                
                for each v in S
                    if {x = v} is not consistent
                        inference.add({x != v})
    
            T = ComputeDomain(x, assign, inference)

            if T is empty
                return Failure

            if S != T
                varQueue.add(x)
                
    return inference
```

Notice that the pseudocode is exactly the same, only with the addition of an inference step.
Also note that we are storing all the previous inferences in `assign`.
<!-- #endregion -->

```python
def backtrack_search(
    prob, assign, inferences
):  # Inferences[i] stores all the values that variable i cannot take
    if all([val != None for val in assign]):
        return assign

    var = assign.index(None)
    assign = assign.copy()

    for val in prob.get_values(var, assign, inferences):
        if prob.is_consistent(var, val, assign):
            assign[var] = val

            inference = infer(prob, var, assign)

            if inference is not None:
                for arr1, arr2 in zip(inferences, inference):
                    arr1.extend(arr2)

                result = backtrack_search(prob, assign, inferences)

                if result is not None:
                    return result

                for arr1, arr2 in zip(inference, inferences):
                    for i in arr1:
                        arr2.remove(i)

            assign[var] = None

    return None

    return failure


def infer(prob, var, assign):
    inference = [[] for _ in range(8)]
    varQueue = [var]
    while len(varQueue) > 0:
        Y = varQueue.pop(0)

        for x in [i for i in prob.get_initial_domain() if i != Y and assign[i] == None]:
            S = prob.get_values(x, assign, inference)

            for v in S:
                if not prob.is_consistent(x, v, assign):
                    inference[x].append(v)

            T = prob.get_values(x, assign, inference)

            if len(T) == 0:
                return None

            if S != T:
                varQueue.append(x)

    return inference


class NQueenProblem:
    def __init__(self, n):
        self.n = n

    def get_initial_domain(self):
        return set([i for i in range(self.n)])

    def get_values(self, var, assign, inferences):
        domain = self.get_initial_domain()

        return domain - set(inferences[var])

    def is_consistent(self, var, val, assign):
        cells = []
        for col, row in enumerate(assign):
            if row != None:
                cells.append((row, col))
        cells.append((val, var))
        for (x1, y1), (x2, y2) in combinations(cells, r=2):
            if x1 == x2:
                return False
            if y1 == y2:
                return False
            if x1 - x2 == y1 - y2:
                return False
            if x1 - x2 == y2 - y1:
                return False
        return True


prob = NQueenProblem(n=4)
with count(backtrack_search, globals()) as num_function_calls:
    print(backtrack_search(prob, [None for i in range(4)], [[] for i in range(4)]))
    print("Number of function calls:", num_function_calls)
```

```python
prob = NQueenProblem(n=8)
with count(backtrack_search, globals()) as num_function_calls:
    print(backtrack_search(prob, [None for i in range(8)], [[] for i in range(8)]))
    print("Number of function calls:", num_function_calls)
```

#### Variants
For faster, but shallower inferences, we can:
* Avoid adding anything to `varQueue`. Also known as "Forward check"
* Instead of adding to `varQueue` when `S != T`, we only add when `|T| = 1`


#### Ordering
Notice that if within our unassigned variable, if there exists one that can only take one value, it is sensible try to assign this variable first instead of the others, so that we consider less states down the line.
Hence, the heuristics to choose variables are:
* Minimum remaining value: Select the variable with the least possible values
* Degree heuristic: Select the variable that is in the largest number of constraints on unassigned variables

And for choosing values for variables:
* Least constraining value: Pick value that gives the largest domain for the unassigned variables
