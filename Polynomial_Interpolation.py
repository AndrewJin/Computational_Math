"""
Computational Math Module 2: Polynomial interpolation
"""

import numpy as np
import matplotlib.pyplot as plt

def interpolate(x_list,y_list):
    """
    Given a set of points {(x,y)}, finds the interpolating polynomial through all points
    
    Parameters
    x_list: x value of all points
    y_list: y value of all points
    
    Returns
    p: function of x representing the interpolating polynomial
    """
    
    def l(k,x):
        """
        Evaluates the k-th Lagrange polynomial at x
        """
        output = 1
        for i in range( len(x_list) ):
            if i == k:
                continue
            output *= (x - x_list[i]) / (x_list[k] - x_list[i])
        return output
    
    def p(x):
        """
        Evaluate the interpolating polynomial at x, constructed using Lagrange basis
        """
        output = 0
        for i in range( len(x_list) ):
            output += y_list[i] * l(i,x)
        return output
    
    return p


def interpolate_function(f, x_min, x_max, n, method):
    """
    Given a function f, constructs a polynomial approximation from x_min to x_max using n points
    
    Parameters:
    f: function to interpolate
    x_min: lower bound
    x_max: upper bound
    n: number of points to interpolate with
    method: either "equidistant" or "chebyshev"
        
    Results:
    Plots the function f and the polynomial approximation
    
    Returns:
    p: function of x representing the polynomial
    """
    
    if method == "equidistant":
        x_list = (x_min + x_max) / 2 + (x_max - x_min) / 2 * np.linspace(-1, 1, n)
        y_list = f(x_list)
        
    elif method == "chebyshev":
        x_list = (x_min + x_max) / 2 + (x_max - x_min) / 2 * np.cos(np.linspace( (2*n - 1) * np.pi / (2*n), np.pi / (2*n), n))
        y_list = f(x_list)
        
    else:
        raise Exception("Enter \"equidistant\" or \"chebyshev\".")
    
    p = interpolate(x_list, y_list)
    
    fig = plt.figure( figsize = (8,6) )
    ax = fig.add_subplot()
    ax.set_xlabel("$x$")
    ax.set_ylabel("$f(x)$")
    ax.set_title("Interpolation of $f(x)$")
    ax.scatter(x_list,y_list)

    x_plot = np.linspace(x_min, x_max, 200)
    y_true = f(x_plot) 
    y_approx = p(x_plot)
    ax.plot(x_plot,y_true, label = 'true', color = 'blue')
    ax.plot(x_plot,y_approx, label = 'approx', color = 'red')
    ax.legend()
    
    return p