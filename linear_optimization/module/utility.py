import re
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import HTML, display
from .simplex import _find_basis
from fractions import Fraction

def plot_halfspace(xs, *cs):
    fig = plt.figure(figsize=(6, 4))
    ax = plt.subplot()

    arr = []
    
    for c in cs:
        c = c.replace(' ', '') 
        match = re.match(r'^(\-?[\d\.]+)x1\+?(\-?[\d\.]+)x2=([\d\.]+)$', c)
        if not match:
            raise ValueError("Does not match regex", c)

        arr.append(map(float, match.groups()))
    
    ys = np.zeros((len(arr), len(xs)))
    for i, eq in enumerate(arr):
        a1,a2,b = eq
        y = (b-a1*xs)/a2
        ys[i] = y
        ax.plot(xs, y)
        
    ax.fill_between(xs, 0, ys.min(axis = 0))
    return ax

def print_table(c_bar, tableau, labels=None, c = None, c_bold=[], tableau_bold=None):
    if labels is None:
        labels = [f'x_{i}' for i in range(1, len(c_bar))]
    assert len(labels) == len(c_bar) - 1
    
    if tableau_bold is None:
        tableau_bold = [[] for _ in tableau]
    else:
        y, x, h, w = tableau_bold
        tableau_bold = [[j for j in range(tableau.shape[1]) if j >= x and i >= y and j < x+w and i < y + h] for i in range(tableau.shape[0])]
        
    headers = ['', *labels, 'Solution']
    header_html = f'<tr>{"".join(f"<th>$${header}$$</th>" for header in headers)}</tr>'
    
    def format_num(num):
        try:
            # TODO: Implement this, need to change reduced_cost as it uses inverse, which messes up the Fraction object
            raise Exception('NOT IMPLEMENTED')
            numer, denom = num.as_integer_ratio()
            return r'\frac{A}{B}'.replace('A', str(numer)).replace('B', str(denom))
        except Exception:
            num = float(num)
            return re.sub(r'\.?0+$', '', f'{num:.4f}')
    
    def html_row(label, row, bold_indices):
        is_bolds = np.zeros(len(row) + 1)
        is_bolds[bold_indices] = 1
        bold_strs = [r"\bf" if b else "" for b in is_bolds]
        return f'<tr><td>{label}</td>{"".join(f"<td>$${bold_str} {format_num(item)}$$</td>" for item, bold_str in zip(row,bold_strs))}</tr>'
    
    c_bar_html = html_row(r'$$\bar {\mathbf c}$$',c_bar, c_bold)
    c_html = '' if c is None else html_row(r'$$\mathbf c$$',c, c_bold)
    
    basis = _find_basis(tableau)
    basic_vars = [labels[b] for b in basis[tableau[:, basis].argmax(axis=1)]]
    
    rows_html = (html_row(f'$${var}$$', row, t_bolds) for var, row, t_bolds in zip(basic_vars, tableau, tableau_bold))
    
    display(HTML(
       f'<table>{header_html}{c_html}{c_bar_html}{"".join(rows_html)}</table>'
    ))

def make_vars(v, n):
    return [f'{v}_{i}' for i in range(1, n + 1)]
