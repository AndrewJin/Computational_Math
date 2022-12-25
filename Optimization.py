"""
Contains nonlinear optimization algorithms.
"""

import numpy as np

def gradient_method(f, x0, t, tol):
    """
    Solves unconstrained optimization problem: min f(x)
    using gradient descent 

    Parameters:
    f - function of vector x
    x0 - initial point
    t - guess for initial step size
    tol - tolerance, terminates when | grad(f) | < tol 

    Returns: 
    x_min - the minimum x
    f_min - the value of f at the minimum x
    """
    x = x0
    while np.linalg.norm(grad(f, x, 0.01)) > tol:
        x_next = x + t * grad(f, x, 0.01)
        #need to do: determine value of t to satisfy sufficient decrease
        


def grad(f, x, step):
    """
    Computes gradient of a function f(x) at point x
    using fourth-order center difference.

    Parameters:
    f - function of vector x
    x - the point at which to evaluate the gradient
    dx - step length

    Returns:
    grad_f - the gradient of f at x
    """
    n = len(x)
    grad_f = np.empty(n)

    for i in range(n):
        dx = np.zeros(n)
        dx[i] += step
        grad_f[i] = (-f(x + 2*dx) + 8*f(x + dx) - 8*f(x - dx) + f(x - 2*dx)) / (12 * step)

    return grad_f