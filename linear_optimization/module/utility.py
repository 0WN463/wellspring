import re
import matplotlib.pyplot as plt
import numpy as np

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

def print_table(c_bar, tableau):
    np.set_printoptions(suppress=True, precision=3)
    print(c_bar.astype('float64'))
    print(tableau.astype('float64'))
