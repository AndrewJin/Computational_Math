"""
Computational Math Module 5: Initial Value Problems
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque




def solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars):
    """
    Solves du/dt = f(t,u), u(0) = u_0 with step size dt until time t_final
    Allows for first-order systems
    
    Parameters
    f: function of t and u where f = du/dt
    u_0: initial value
    dt: time step
    t_final: final time
    method: either "euler", "midpoint", "trapezoid", "classic_rk4", "equal_rk4"
    plot_vars: list of variables to plot against time 
               (for scalar equation, leave blank)
    phase_vars: variables to plot in phase diagram (list of ordered pairs)
                (for scalar equation, leave blank)
    
    Results
    Plots the time series of chosen variables
    Plots the 2D phase space of chosen variable pairs
    
    Returns
    u_list: array of ordered tuples representing solution at each time
    """
    
    n = int(t_final / dt) #number of steps to take, total points is n + 1
    
    if isinstance(u_0, float):
        u = u_0
        u_list = np.empty( n + 1 )
    elif isinstance(u_0, np.ndarray):
        u = u_0.copy()
        u_list = np.empty( (n + 1, len(u_0)) )
    else:
        raise Exception("Initial condition must be float or np.ndarray of floats")
    
    t_list = np.linspace(0, t_final, n + 1)
    u_list[0] = u_0
    
    #==================================
    #Integration Algorithms
    if method == "euler":
        for i in range(n):
            u += f(t_list[i], u) * dt
            u_list[i + 1] = u
    
    elif method == "midpoint":
        for i in range(n):
            k1 = f(t_list[i], u) * dt #step size from initial point
            k2 = f(t_list[i] + dt/2, u + k1/2) * dt #step size from midpoint, estimate midpoint using initial point
            u += k2
            u_list[i + 1] = u
            
    elif method == "trapezoid":
        for i in range(n):
            k1 = f(t_list[i], u) * dt #step size from initial point
            k2 = f(t_list[i] + dt, u + k1) * dt #step size from endpoint, estimate endpoint using initial point
            u += k1/2 + k2/2
            u_list[i + 1] = u
            
    elif method == "ralston":
        for i in range(n):
            k1 = f(t_list[i], u) * dt
            k2 = f(t_list[i] + 2*dt/3, u + 2*k1/3) * dt
            u += k1/4 + 3*k2/4
            u_list[i + 1] = u
    
    elif method == "classic_rk4":
        for i in range(n):
            k1 = f(t_list[i], u) * dt #step size from initial point
            k2 = f(t_list[i] + dt/2, u + k1/2) * dt #step size from midpoint, estimate midpoint using initial point
            k3 = f(t_list[i] + dt/2, u + k2/2) * dt #step size from midpoint, estimate midpoint using midpoint
            k4 = f(t_list[i] + dt, u + k3) * dt #step size from endpoint, estimate endpoint using midpoint
            u += k1/6 + k2/3 + k3/3 + k4/6
            u_list[i + 1] = u
            
    elif method == "equal_rk4":
        for i in range(n):
            k1 = f(t_list[i], u) * dt
            k2 = f(t_list[i] + dt/3, u + k1/3) * dt
            k3 = f(t_list[i] + 2*dt/3, u - k1/3 + k2) * dt
            k4 = f(t_list[i] + dt, u + k1 - k2 + k3) * dt
            u += k1/8 + 3*k2/8 + 3*k3/8 + k4/8
            u_list[i + 1] = u
            
    else:
        raise Exception("Enter \"euler\", \"midpoint\", \"trapezoid\", \"ralston\", \"classic_rk4\" or \"equal_rk4\"")
    #==================================
       
    
    #==================================
    #Graphing
    fig = plt.figure( figsize = (24,12) )
    
    if isinstance(u_0, float): #can only plot solution x over time t
        if plot_vars: #list is not empty, meaning we have a variable to plot
            axes = fig.subplots(1,1)
            axes.plot(t_list, u_list)
            axes.set_title("Time series for x")
            axes.set_xlabel("t")
            axes.set_ylabel("x")
    
    elif isinstance(u_0, np.ndarray):
        axes = fig.subplots(2, max(len(plot_vars), len(phase_vars)))
        for i, var in enumerate(plot_vars):
            axes[0, i].plot(t_list, u_list[:,var])
            axes[0, i].set_title("Time series for x" + str(var))
            axes[0, i].set_xlabel("t")
            axes[0, i].set_ylabel("x" + str(var))
            
        for i, var in enumerate(phase_vars):
            axes[1, i].plot(u_list[:,var[0]], u_list[:,var[1]])
            axes[1, i].set_xlabel("x" + str(var[0]))
            axes[1, i].set_ylabel("y" + str(var[1]))
            axes[1, i].set_title("Phase diagram for x" + str(var[0]) + " and x" + str(var[1]))
    #==================================
    
    return u_list




def adaptive_ivp(f, u_0, t_final, err_target, plot_vars, phase_vars):
    """
    Solves du/dt = f(t,u), u(0) = u_0 with step size dt until time t_final
    Only allows single-variable equations
    
    Parameters
    f: function of t and u where f = du/dt
    u_0: initial value
    dt: time step
    t_final: final time
    method: either "euler" or "rk2" or "rk4"
    plot_vars: variables to plot against time
    phase_vars: variables to plot in phase diagram (list of ordered pairs)
    
    Results
    Plots the time series of chosen variables
    Plots the 2D phase space of chosen variable pairs
    
    Returns
    u_list: deque of ordered tuples representing solution at each time
    """
    
    if isinstance(u_0, float):
        u = u_0
    elif isinstance(u_0, np.ndarray):
        u = u_0.copy()
        
    t = 0
    u_list = deque()
    t_list = deque()
    u_list.append(u_0)
    t_list.append(0)
    dt_trial = 0.01
    
    while(t < t_final):
        #First, attempt a step using a dt_trial
        
        #Use midpoint method for dt^3 step error
        k1 = f(t, u) * dt_trial #step size from initial point
        k2 = f(t + dt_trial/2, u + k1/2) * dt_trial #step size from midpoint, estimate midpoint using initial point
        u_rk2 = u + k2
        
        #Use equal_rk4 method for dt^5 step error
        k1 = f(t, u) * dt_trial
        k2 = f(t + dt_trial/3, u + k1/3) * dt_trial
        k3 = f(t + 2*dt_trial/3, u - k1/3 + k2) * dt_trial
        k4 = f(t + dt_trial, u + k1 - k2 + k3) * dt_trial
        u_rk4 = u + k1/8 + 3*k2/8 + 3*k3/8 + k4/8
        
        err_current = np.linalg.norm(u_rk4 - u_rk2)
        
        #Revise dt based on error
        dt = dt_trial * (err_target / err_current) ** (1/3)
        
        #Now, make step using the adaptive dt
        k1 = f(t, u) * dt
        k2 = f(t + dt/3, u + k1/3) * dt
        k3 = f(t + 2*dt/3, u - k1/3 + k2) * dt
        k4 = f(t + dt, u + k1 - k2 + k3) * dt
        u += k1/8 + 3*k2/8 + 3*k3/8 + k4/8
        
        if isinstance(u_0, float):
            u_list.append(u)
        elif isinstance(u_0, np.ndarray):
            u_list.append(u.copy())
        
        t += dt
        t_list.append(t)
        
        dt_trial = dt

    fig = plt.figure( figsize = (24,12) )
    
    if isinstance(u_0, float):
        if plot_vars: #list is not empty, meaning we have a variable to plot
            fig = plt.figure( figsize = (24,12) )
            axes = fig.subplots(1,1)
            axes.plot(t_list, u_list)
            axes.set_title("Time series for x")
            axes.set_xlabel("t")
            axes.set_ylabel("x")
            
    elif isinstance(u_0, np.ndarray):
        axes = fig.subplots(2, max(len(plot_vars), len(phase_vars)))
        for i, var in enumerate(plot_vars):
            axes[0, i].plot(t_list, [u[var] for u in u_list])
            axes[0, i].set_title("Time series for x" + str(var))
            axes[0, i].set_xlabel("t")
            axes[0, i].set_ylabel("x" + str(var))
            
        for i, var in enumerate(phase_vars):
            axes[1, i].plot([u[var[0]] for u in u_list], [u[var[1]] for u in u_list])
            axes[1, i].set_xlabel("x" + str(var[0]))
            axes[1, i].set_ylabel("y" + str(var[1]))
            axes[1, i].set_title("Phase diagram for x" + str(var[0]) + " and x" + str(var[1]))
    
    return t_list, u_list
 

       

def compare_ivp(f, u_0_list, dt, t_final, method, plot_vars, phase_vars):
    """
    Solves du/dt = f(t,u), u(0) = u_0 with step size dt until time t_final
    for multiple different u_0, plots solution with all initial values
    
    Parameters
    f: function of t and u where f = du/dt
    u_0_list: list of initial values
    dt: time step
    t_final: final time
    method: either "euler", "midpoint", "trapezoid", "classic_rk4", "equal_rk4", "adaptive"
    plot_vars: variables to plot against time
    phase_vars: variables to plot in phase diagram (list of ordered pairs)
    
    Results
    Plots the time series of chosen variables
    Plots the 2D phase space of chosen variable pairs
    
    Returns
    u_list: array of ordered tuples representing solution for each initial condition
    """
    
    if method == "euler" or method == "midpoint" or method == "trapezoid" or method == "classic_rk4" or method == "equal_rk4":
        n = int(t_final / dt)
        fig = plt.figure( figsize = (24,12) )
        t_list = np.linspace(0, t_final, n + 1)
        
        if isinstance(u_0_list[0], float):
            u_list = np.empty( (len(u_0_list), n+1) )
            axes = fig.subplots(1, 1)
            
            for i, u_0 in enumerate(u_0_list):
                u_list[i] = solve_ivp(f, u_0, dt, t_final, method, [], [])
    
                axes.plot(t_list, u_list[i,:])
                axes.set_title("Time series for x")
                axes.set_xlabel("t")
                axes.set_ylabel("x")
        
        elif isinstance(u_0_list[0], np.ndarray):
            u_list = np.empty( (len(u_0_list), n + 1, len(u_0_list[0])) )
            axes = fig.subplots(2, max(len(plot_vars), len(phase_vars)))
            
            for i, u_0 in enumerate(u_0_list):
                u_list[i] = solve_ivp(f, u_0, dt, t_final, method, [], [])
                
                for j, var in enumerate(plot_vars):
                    axes[0, j].plot(t_list, u_list[i,:,var])
                    axes[0, j].set_title("Time series for x" + str(var))
                    axes[0, j].set_xlabel("t")
                    axes[0, j].set_ylabel("x" + str(var))
            
                for j, var in enumerate(phase_vars):
                    axes[1, j].plot(u_list[i,:,var[0]], u_list[i,:,var[1]])
                    axes[1, j].set_xlabel("x" + str(var[0]))
                    axes[1, j].set_ylabel("y" + str(var[1]))
                    axes[1, j].set_title("Phase diagram for x" + str(var[0]) + " and x" + str(var[1]))
                
        return u_list
                
    elif method == "adaptive":
        t_list = [] #2-D array, first index for initial condition, second index for time
        u_list = [] #2-D array (scalar ODE), first index for initial condition, second index for solution
                    #3-D array (system ODE), first index for initial condition, second index for solution vector, third index for solution component
        fig = plt.figure( figsize = (24,12) )
        
        if isinstance(u_0_list[0], float):
            axes = fig.subplots(1, 1)
            
            for u_0 in u_0_list:
                cur_t_list, cur_u_list = adaptive_ivp(f, u_0, t_final, 1e-6, [], [])
                u_list.append(cur_u_list)
    
                axes.plot(cur_t_list, cur_u_list)
                axes.set_title("Time series for x")
                axes.set_xlabel("t")
                axes.set_ylabel("x")
        
        elif isinstance(u_0_list[0], np.ndarray):
            axes = fig.subplots(2, max(len(plot_vars), len(phase_vars)))
            
            for u_0 in u_0_list:
                cur_t_list, cur_u_list = adaptive_ivp(f, u_0, t_final, 1e-6, [], [])
                
                for j, var in enumerate(plot_vars):
                    axes[0, j].plot(cur_t_list, [u[var] for u in cur_u_list])
                    axes[0, j].set_title("Time series for x" + str(var))
                    axes[0, j].set_xlabel("t")
                    axes[0, j].set_ylabel("x" + str(var))
            
                for j, var in enumerate(phase_vars):
                    axes[1, j].plot([u[var[0]] for u in cur_u_list], [u[var[1]] for u in cur_u_list])
                    axes[1, j].set_xlabel("x" + str(var[0]))
                    axes[1, j].set_ylabel("y" + str(var[1]))
                    axes[1, j].set_title("Phase diagram for x" + str(var[0]) + " and x" + str(var[1]))
                    
        return t_list, u_list
    