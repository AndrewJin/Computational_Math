"""
Lorenz Oscillator simulation
"""

import numpy as np
import Initial_Value_Problems as ivp
    
def main():
    #Describe ODE with parameters
    s = 10
    p = 28
    b = 8/3
    f = lambda t,u: np.array([s * (u[1] - u[0]), u[0] * (p - u[2]) - u[1], u[0] * u[1] - b * u[2]])
    
    #Initial conditions to compare
    u_0_list = [np.array([1., 1., 1.]), np.array([1.0002, 1.0002, 1.0002])]
    
    #Parameters for numerical integration and graphing
    dt = 0.0001
    t_final = 30
    method = "equal_rk4"
    plot_vars = [0, 1, 2]
    phase_vars = [(0,1), (0,2), (1,2)]
    
    #Run the algorithm
    ivp.compare_ivp(f, u_0_list, dt, t_final, method, plot_vars, phase_vars)    
    
    
if __name__ == "__main__":
    main()