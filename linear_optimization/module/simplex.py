import numpy as np
from fractions import Fraction

def reduced_cost(costs, tableau, basis=None):
    assert costs.shape[0] == tableau.shape[1]

    if not basis:
        basis = _find_basis(tableau)

    B = tableau[:, basis]
    return costs.T - costs[basis].T @ np.linalg.inv(B) @ tableau

def simplex(c_bar, tableau, maxit=100):
    assert c_bar.shape[0] == tableau.shape[1]

    c_bar = c_bar + Fraction()
    tableau = tableau + Fraction()
    counter = 0
    while np.any(c_bar[:-1] < 0) and counter < maxit:
        col = c_bar[:-1].argmin()
        pivot_col = tableau[:, col]
        if np.all(pivot_col <= 0):
            raise ValueError("Unbounded objective")

        value = tableau[:, -1]
        metric = np.where(pivot_col > 0, value /
                          (pivot_col + (pivot_col == 0)), np.inf)
        row = metric.argmin()

        c_bar, tableau = pivot(c_bar, tableau, row,  col)
        counter += 1
    if counter == maxit:
        raise RuntimeError("Iterations exceeded")
    return c_bar, tableau


def pivot(c_bar, tableau, row, col):
    c_bar, tableau = c_bar.copy(), tableau.copy()

    tableau[row] /= tableau[row][col]

    rows = np.tile(tableau[row], (tableau.shape[0], 1))
    mult = np.tile(tableau[:,col], (tableau.shape[1], 1)).T
    sub = rows * mult
    sub[row] = 0
    tableau -= sub

    c_bar -= tableau[row] * c_bar[col]

    return c_bar, tableau

def dual_simplex(c_bar, tableau):
    while True:
        assert (c_bar[:-1] >= 0).all()

        c_bar, tableau = c_bar.copy(), tableau.copy()
        c_bar, tableau = c_bar + Fraction(), tableau + Fraction()
        b = tableau[:, -1]
        if (b >= 0).all():
            return c_bar, tableau

        row = b.argmin()
        pivot_row = tableau[row, :-1]
        i_s = np.argwhere(pivot_row < 0).ravel()

        if i_s.size == 0:
            raise ValueError("Problem is infeasible")

        c_s = c_bar[i_s]
        v_i = pivot_row[i_s]
        metric = c_s / np.abs(v_i)
        col = i_s[metric.argmin()]
        
        c_bar, tableau = pivot(c_bar, tableau, row, col)

def _find_basis(tableau):
    h = tableau.shape[0]
    is_elem = ((tableau == 1).sum(axis=0) == 1) & (
        (tableau == 0).sum(axis=0) == h - 1)
    cols = np.argwhere(is_elem)

    mask = np.full(h, False)

    indices = []
    for c in cols:
        c = c[0]
        col = tableau[:, c] == 1
        if not (col & mask).any():
            mask |= col
            indices.append(c)

    return indices

