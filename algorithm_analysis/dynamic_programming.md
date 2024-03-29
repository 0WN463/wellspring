---
jupyter:
  jupytext:
    formats: ipynb,md
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

# Dynamic Programming
Dynamic programming is a way to solve a problem by solving the smaller subproblems, where to solution to the overall problem depends on the solution of the smaller subproblems.

A simple way to view this is that this is simply, in some sense, a recursive way to approach the problem.

## Recursive (Top-down)
Suppose we wish to compute the n-th triangle number, where triangle number follows the series of `0, 1, 3, 6, 10, 15, 21, 28, 36, 45, ...`. 
Each number if `n` more than the previous number, using 0-indexing.

One way to approach this recursively is simply.

```python
def triangle(n):
    if n == 0:
        return 0
    return n + triangle(n - 1)


[triangle(n) for n in range(10)]
```

Let us analyse the complexity of this recursive algorithm.
`triangle` is called a total of n times, and each time, $O(1)$ amount of work is done, thus the total complexity is $O(n)$.

Suppose instead, we were to compute the $n$-th Tribonacci number, where the series is `0, 1, 1, 2, 4, 7, 13, 24, 44, ...`.

Each number is the sum of the previous 3 numbers in the series.

The recursive way to approach this would be:


```python
def tribonacci(n):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return sum([tribonacci(i) for i in range(n - 3, n)])


[tribonacci(n) for n in range(10)]
```

Now suppose that we wish to compute a large Tribonnaci number.

```python
%%timeit -n 10
tribonacci(20)
```

As we can see, it takes a long time even just to compute the 20-th Tribonacci number.

```python
from common.count import count

with count(tribonacci, globals()) as c:
    tribonacci(20)
    print("Total calls:", c)
```

Consider the time complexity of the algorithm.

```
          ________n______
         /        |      \
     _n-1__      n-2     n-3 
    /   |  \     /|\          
  n-2  n-3  n-4                   
 / |\ /|\  / |\                  
...  ... ... .. ..  .. .. .. . .. .
```

If we only consider the largest branch of the recursion, we can see that it grows by 3 every layer.
Thus, the complexity is bounded by $O(3^n)$.
Since the complexity is exponential, it becomes slow for large numbers.


### Memoization
However, notice that we are recomputing the same value multiple times.
In the tree, we computed `tribonacci(n-2)` in the left branch as well as in the center branch from the root.
If we were to "cache" these results, we can obtain the result of the subproblem right away rather than having to recompute it each time.

The modification to the algorithm is simple, just have a table that stores the computed results for us:

```python
def tribonacci_helper(n):
    table = [None for i in range(n + 1)]
    return tribonacci_dp(n, table)


def tribonacci_dp(n, table):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1

    if table[n] != None:
        return table[n]
    table[n] = sum([tribonacci_dp(i, table) for i in range(n - 3, n)])
    return table[n]
```

```python
%%timeit -n 10
tribonacci_helper(20)
```

Notice this pattern of searching if we have ran the function with some arguments; if we did, then return the previous results, otherwise we compute it and store the result.
Because of this repeating pattern, we can simply implement a decorator which takes care of this repeat logic for all dynamic programming problems.

```python
from common.cache import cache
show_implementation(cache)
```

```python
%%timeit -n 10
with cache(tribonacci, globals(), lambda *args: args[0]):
    tribonacci(20)
```

```python
with count(tribonacci, globals()) as c:
    with cache(tribonacci, globals(), lambda *args: args[0]):
        tribonacci(20)
        print("Total calls:", c)
```

Notice that we called the function a total of 21 times, once each for $n = 0$ to $n = 20$.

## Bottom-up
Another way to solve this problem by DP is to try to unwind the problem and solve the smaller subproblem first.

This would lead to better space usage because we may need to store less results from the previous subproblems.
However, trying to come up with a bottom-up approach may not always be straight forward.

Going back to the Tribonacci example, we know that to solve `tribonacci(n)`, we only need `tribonacci(n-1)`, `tribonacci(n-2)` and `tribonacci(n-2)`.
Thus, we can start from the bottom, starting from `tribonacci(0)`, `tribonacci(1)` and `tribonacci(2)`; then proceeding to solve `tribonacci(3)` then `tribonacci(4)`...


```python
def tribonacci_bottom_up(n):
    a, b, c = 0, 1, 1

    for _ in range(n):
        a, b, c = b, c, a + b + c

    return a
```

```python
%%timeit -n 10
tribonacci_bottom_up(20)
```

As we can see, the bottom-up approach is equally as fast (if not faster due to not having to keep track of the function stack due to the lack of recursive calls).


## Comparison

| Memoization | Bottom up |
| --- | --- |
| Order of computing sub-problems does not matter | Order of computing sub-problems is important, need to ensure that smaller sub-problems are filled before larger ones |
| Solves only the subproblems required | Might solve subproblems that are not needed to get the answer |
| Complexity derivation may be difficult | Once the imperative loop is written, complexity derivation is straightforwards |


(The two DP solutions are $O(n)$.
However, there is an $O(\log n)$ method which uses [matrix exponentiation](../linear_algebra/diagonalization.ipynb#Application-to-algorithms))


## Other problems

### Edit Distance  <a id="edit_distance"></a>

Problem: Given two strings, $A[1:n]$ and $B[1:m]$, compute the minimum number of edits to get from A to B.

Edits can be
* Insertion of 1 character
* Deletion of 1 character
* Substitution of 1 character

Example: `lumen` to `almond` has an edit distance of 4.

`lumen` $\rightarrow$ `alumen` $\rightarrow$ `almun` $\rightarrow$ `almon` $\rightarrow$ `almond`

Solution: 

**Base Case**

Suppose we are comparing the edit distance of `lumen` to an empty string, then the edit distance is simply 5, the length of `lumen`.

Similarly, if we are comparing the edit distance of an empty string to `lumen`, then the edit distance is also 5, the length of `lumen`.


**Further Cases**

Consider the case where the last character of both strings are the same, then total edits required, dist(A[1:n], B[1:m]), can be dist(A[1:n-1], B[1:m-1]), because we do not need to modify the last character.

Suppose the character is different, then in the case of insertion, we need to insert B[m] at the back of A, thus we need a total of dist(A[1:n], B[1:m-1]) + 1 edits, because the last character in B is matched by the new insertion, and the +1 is the cost of the insertion.

* Insertion will compare `lumend` to `almond`, where the `d` is added and we now solve the subproblem of `lumen` to `almon`

Similarly for deletion, we need to delete A[n] from the back of A, thus we need a total of dist(A[1:n-1], B[1:m]) + 1 edits, since the last character is removed and no longer a concern.

* Deletion will compare `lume` to `almond`, where the `n` is deleted and we now solve the subproblem of `lume` to `almond`

Lastly, for substitution, we would need to swap out the last character of A with the last character of B, which means we need a total of dist(A[1:n-1], B[1:m-1]) + 1 edits, since both A and B will have one last character to match.

* Substitution will compare `lumed` to `almond`, where the `n` is changed with a `d` and we now solve the subproblem of `lume` to `almon`

And thus, the minimum edit distance is simply the smallest value out of all the possible operations.

```python
def dist(A, B, n, m):
    if n == 0:
        return m

    if m == 0:
        return n

    return min(
        dist(A, B, n - 1, m) + 1,
        dist(A, B, n, m - 1) + 1,
        dist(A, B, n - 1, m - 1) + (0 if A[n - 1] == B[m - 1] else 1),
    )


def dist_helper(func, A, B):
    return func(A, B, len(A), len(B))


with cache(dist, globals(), lambda *args: tuple(args)):
    print("The distance is", dist_helper(dist, "lumen", "almond"))
```

Similarly, we can do it with a bottom-up approach

```python
def dist_bottom_up(A, B, n, m):
    for i in range(n + 1):
        new_row = [i for i in range(m + 1)]

        if i > 0:
            for j in range(m + 1):
                if j == 0:
                    new_row[j] = row[j] + 1
                else:
                    new_row[j] = min(
                        row[j] + 1,
                        new_row[j - 1] + 1,
                        row[j - 1] + (0 if A[i - 1] == B[j - 1] else 1),
                    )
        row = new_row
    return row[m]


print(f"The distance is", dist_helper(dist_bottom_up, "lumen", "almond"))
```

#### Variations
Notice that we can set the cost of each operation to be different.
If we wish to view substitution as an insertion followed by deletion, we can set the cost of substitution to 2.
However, the algorithm would be similar.
