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

<!-- #region deletable=false run_control={"frozen": true} -->
$$
\newcommand{theorem}{\textbf{Theorem: }}
\newcommand{proof}{\textbf{Proof: }}
\newcommand{example}{\textbf{Example: }}
\newcommand{lemma}{\textbf{Lemma: }}
\newcommand{corollary}{\textbf{Corollary: }}
\newcommand{prop}{\textbf{Proposition: }}
$$
<!-- #endregion -->

$$
\newcommand{v}{\mathbf}
\newcommand{inv}{^{-1}}
\newcommand\mat[1]{\begin{pmatrix}#1\end{pmatrix}} 
\newcommand\det[1]{\left| #1\right|} 
\newcommand\norm[1]{\lVert #1\rVert} 
\newcommand\set[1]{\left\{#1\right\}} 
\newcommand\dels[2]{\frac{\partial #1}{\partial #2}} 
$$

# Partial differential equation 

A **partial differential equation** (PDE) is an equation with a known function $u$ of two or more **independent** variables, $x, y, \dots$ and partial derivatives of $u$ with respect to them.

The solution to ODE contains arbitrary constants, and thus by extension, we would arrive at the fact the **solutions of PDE** have arbitrary functions.


<details>
<summary style=\color: blue\>$\example$ (Click to expand)</summary>
<div style=\background: aliceblue\>
For $u_{xx} + u_{yy} = 0$, all these are valid solutions:
$$
\displaylines{
u = x^2 - y^2 \\
u = e^{x} \sin y \\
u = \ln(x^2 + y^2)
}
$$
</div>
</details>

## Separation of variables

We assume that the solution is of the form:
$$
u = X(x) Y(y)
$$

Then notice that:
$$
\displaylines{
u_x = X' Y \\
u_y = X Y'\\
u_{xx} = X'' Y\\
u_{xy} = X'Y' \\
u_{yy} = XY''
}
$$

Now suppose that we are given an equation of the form:
$$
u_x = f(x) g(y) u_y
$$

Then we can do our above substitution and get:
$$
\begin{align}
X' Y &= f(x) g(y) XY'\\
\frac{1}{f(x)} \frac{X'}{X} &= g(y) \frac{Y'}{Y}
\end{align}
$$

Since the $x,y$ are independent, and we have a function of $x$ on the left and a function of $y$ on the right,
the only way they can be equal is if they are some constant.

$$
\begin{align}
\frac{1}{f(x)} \frac{X'}{X} &= g(y) \frac{Y'}{Y}\\
\Rightarrow
\frac{1}{f(x)} \frac{X'}{X} = k & \quad g(y) \frac{Y'}{Y} = k \\
\Rightarrow
X' = kX f(x) & \quad Y' = \frac{kY}{g(y)}
\end{align}
$$

From here, we can solve them separately as per a normal ODE and get the solution.

## Applications

### Wave equation

Suppose that we have the following:
* a string that is stretch tightly across the $x$-axis.
* each of its endpoints are tied to $y=0$, spanning from $x=0$ to $x = \pi$.
* the initial shape of the string is $y = f(x)$.
* the string is initially stationary, 

We want to model the shape of the string over time.
Thus, we need $y$ to be a function of $x$ and $t$.

Using the above assumptions, we arrive at the following constraints:
$$
f(t, 0) = 0
f(t, \pi) = 0
f(0, x) = f(x)
$\dels{y}{x} = 0$
$$

Using some physics, we would arrive at the following:
$$
c^2 \dels{ ^2 y }{x^2} = \dels{^2y}{t^2}
$$

where $c$ is an arbitrary constant.


We notice that one possible solution to it is:
$$
y = \frac{1}{2}\left( f(x + ct) + f(x - ct) \right)
$$

We can verify that our constraints hold for this equation.
(We need to extend $f$ to be an odd periodic function with a period of $2\pi$ to allow $f$ to be defined outside of $[0, \pi]$).

Suppose we consider that $f = \sin 2x$.

```python
%matplotlib notebook

from IPython.display import HTML
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np

c = 0.5
f = np.vectorize(lambda x: np.sin(2 * x))
func = lambda x, t: 0.5 * (f(x + c * t) + f(x - c * t))

def plot(func, x_max, t_max=10):
    fig, ax = plt.subplots()
    ax.axis([0, x_max,-3,3])
    l, = ax.plot([],[])

    t = np.linspace(0, t_max)
    xs = np.linspace(0, x_max, num=1000)

    def animate(i):
        l.set_data(xs, func(xs, t[i]))

    return matplotlib.animation.FuncAnimation(fig, animate, frames=len(t))


ani = plot(func, np.pi)
HTML(ani.to_jshtml())
```

When we look at the change of the string over time, it looks natural and intuitive, albeit a bit too theoretical.



```python
f = np.vectorize(lambda x: np.sin(x) * np.cos(3 *x))

ani = plot(func, np.pi)
HTML(ani.to_jshtml())
```

When we look at $f = \sin x \cos 3x$, this looks surprisingly natural.

### Heat equation

Suppose that we have:
* a thin bar made of homogeneous material
* oriented along the $x$-axis
* is perfectly insulated laterally, so heat only flows in the $x$-direction

This means that the temperature $u$ only depends on $x$ and $t$, and is governed by the following heat equation:
$$
u_t = c^2 u_{xx}
$$
where $c^2$ is the thermal diffusivity ($length^2/time$) of the material.

We now further constrain our system:
* the ends of the bar ($x = 0, x = L$) are always at temperature $0$
* the initial temperature of the bar is modelled by $u(x, 0) = f(x)$

---

Suppose that we are given the following system:
$$
u_t = 2 u_{xx}
$$
with $L = 3$ and $f(x) = 5 \sin 4 \pi x$.

When we solve the equation, we will arrive at:
$$
u = 5e^{-32\pi^2t} \sin 4 \pi x
$$

<details>
<summary style=\color: blue\>$\textbf{Derivation}$ (Click to expand)</summary>
<div style=\background: aliceblue\>
Let $u = X(x) T(t)$.

Then
$$
XT' = 2X'' T \Rightarrow \frac{X''}{X} = {T'}{2T}
$$

Thus:
$$
X'' = k X \quad T' = 2kT
$$

Now we focus on $X'' - kX = 0$.
We [know](introduction.ipynb#Constant-coefficients) that this either have solutions that are exponential or trigonometrical, based on the value of $k$.

But since we want $X(0) = 0$ and $X(L) = 0$, it rules out the exponential solution, leaving us with the trigonometric one (and the fact that $k < 0$ to satisfy this).

Thus we get:
$$
X = a \cos \sqrt{-kx} + b \sin \sqrt{-kx}
$$

We then solve for $T$ to get:
$$
T = de^{2kt}
$$

Thus, our solution is of the form:
$$
u = XT = \left(a \cos \sqrt{-kx} + b \sin \sqrt{-kx} \right) de^{2kt}
$$

Since $T \neq 0$ for all $t$, we must have $X(0) = 0$ and $X(L) = 0$.
Substituting, we would arrive at $a = 0, b\sin (3\sqrt{-k}) = 0$.

We wouldn't want $a$ and $b$ to both be $0$ (else $X = 0$ which isn't interesting), thus 
we would get $\sin (3 \sqrt{-k}) = 0$

Hence $\sqrt{-k} = \frac{n \pi}{3}$.
And our equation becomes:
$$
u =   b \sin \frac{n \pi x}{3} de^{2kt}
=  B \sin \frac{n \pi x}{3} e^{-2n^2 \pi^2 t / 9}
$$

Lastly, since $u(x, 0) = f(x) = 5 \sin 4 \pi x$, we can compare this with our equation and get:
$$
u(x, 0) =  B \sin \frac{n \pi x}{3} = 5 \sin 4 \pi x
$$
Thus, $B = 5, n = 12$.
Hence, our solution is:
$$
u = 5e^{-32\pi^2t} \sin 4 \pi x
$$

$QED$
</div>
</details>



```python
func = lambda x, t: 5 * np.exp(-32 * np.pi**2 * t) * np.sin(4 * np.pi * x)

ani = plot(func, np.pi, 0.02)
HTML(ani.to_jshtml())
```

From here, we can see that initially there are regions of high temperature and low temperature.
Then the system quickly dissipates the energy across the $x$-axis, and over time, the temperature becomes homogeneous across the bar, which fits our intuition.
