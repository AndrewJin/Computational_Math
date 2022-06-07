"""
Computational Math Module 4: Numerical Integration
"""

import numpy as np

def left_endpoint(x_list, y_list):
    "integrate points using the left endpoint method"
    n = len(x_list) 
    total = 0
    for i in range(n - 1):
        dt = x_list[i + 1] - x_list[i]
        total += y_list[i] * dt
    return total
        
def right_endpoint(x_list, y_list):
    "integrate points using the right endpoint method"
    n = len(x_list)
    total = 0
    for i in range(n - 1):
        dt = x_list[i + 1] - x_list[i]
        total += y_list[i + 1] * dt
    return total
    
def trapezoid(x_list, y_list):
    "integrate points using the trapezoid method"
    n = len(x_list)
    total = 0
    for i in range(n - 1):
        dt = x_list[i + 1] - x_list[i]
        total += (y_list[i] / 2 + y_list[i + 1] / 2) * dt
    return total
    
def simpson(x_list, y_list):
    "integrate points using simpson's method"
    "note: odd number of points required (even number of intervals), equal distance intervals"
    n = len(x_list)
    dt = x_list[1] - x_list[0]
    total = 0
    for i in range(0, n - 1, 2):
        total += ( y_list[i] / 6 + 2 * y_list[i + 1] / 3 + y_list[i + 2]/6 ) * 2 * dt
    return total

def integrate_points(x_list, y_list, method):
    """
    Given a set of points {(x,y)}, integrates using those points
    
    Parameters
    x_list: set of x values
    y_list: set of y values
    method: method of integration, either "left", "right", "trapezoid", "simpson"
    """
    if method == "left":
        return left_endpoint(x_list, y_list)
    
    elif method == "right":
        return right_endpoint(x_list, y_list)
        
    elif method == "trapezoid":
        return trapezoid(x_list, y_list)
    
    elif method == "simpson":
        return simpson(x_list, y_list)
    
    else:
        raise Exception("Enter valid method")
        
def accumulate_points(x_list, y_list, method, y_0 = 0):
    """
    Given a set of points {(x,y)}, returns the accumulation function as list.
    
    Parameters:
    x_list: set of x values
    y_list: set of y values
    y_0: value of accumulation function at the start
    method: method for integration    
        
    Returns:
    y_out: set of y values for the accumulation function
    """
    n = len(x_list)
    y_out = np.empty(n)
    y_out[0] = 0
    total = 0
    
    if method == "left":
        for i in range(n - 1):
            dt = x_list[i + 1] - x_list[i]
            total += y_list[i] * dt
            y_out[i + 1] = total
            
    if method == "right":
        for i in range(n - 1):
            dt = x_list[i + 1] - x_list[i]
            total += y_list[i + 1] * dt
            y_out[i + 1] = total
            
    if method == "trapezoid":
        for i in range(n - 1):
            dt = x_list[i + 1] - x_list[i]
            total += (y_list[i] / 2 + y_list[i + 1] / 2) * dt
            y_out[i + 1] = total
            
    if method == "simpson":
        "note: odd number of points required (even number of intervals), equal distance intervals"
        dt = x_list[1] - x_list[0]
        for i in range(0, n - 1, 2):
            half_step = ( 5 * y_list[i] / 24 + y_list[i + 1] / 3 - y_list[i + 2] / 24 ) * 2 * dt
            whole_step = ( y_list[i] / 6 + 2 * y_list[i + 1] / 3 + y_list[i + 2] / 6 ) * 2 * dt
            y_out[i + 1] = total + half_step
            y_out[i + 2] = total + whole_step
            total += whole_step
                    
    return y_out
            
    
def integrate_function(f, x_min, x_max, n, method):
    """
    Given a function f with lower and upper bound, numerically integrates the function
    
    Parameters
    f: function to integrate
    x_min: lower bound
    x_max: upper bound
    n: number of points to integrate with
    method: method of integration, either "left", "right", "trapezoid", "simpson"
    
    Returns:
    integral: value of the definite integral
    """
    x_list = np.linspace(x_min, x_max, n)
    y_list = f(x_list)
    
    return integrate_points(x_list, y_list, method)


def accumulate_function(f, x_min, x_max, n, method = "simpson"):
    x_list = np.linspace(x_min, x_max, n)
    y_list = f(x_list)
    
    return accumulate_points(x_list, y_list, 0, method)