"""
Van der Pol oscillator simulation
"""

import numpy as np
import Initial_Value_Problems as ivp

def main():
    #Describe ODE and initial condition
    #u[0] is position, u[1] is velocity
    mu = 20
    f = lambda t,u: np.array([ u[1] , mu * (1 - u[0] ** 2) * u[1] - u[0] ])
    u_0 = np.array([1.05, 0.]) 
    
    #Parameters for numerical integration and graphing
    dt = 0.001
    t_final = 200
    method = "equal_rk4"
    plot_vars = [0, 1]
    phase_vars = [(0, 1)]
    
    #Run the algorithm
    ivp.solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars)
    
    #With adaptive time step
    err_target = 1e-4
    t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, plot_vars, phase_vars)
    dt_list = [t_list[i + 1] - t_list[i] for i in range(0, len(t_list) - 1)]
    
    #With different initial values, using adaptive time step
    u_0_list = [np.array([1., 0.]), np.array([1.5, 0.]), np.array([2., 0.])]
    t_list, u_list = ivp.compare_adaptive(f, u_0_list, t_final, err_target, plot_vars, phase_vars)
    dt_list = [t_list[i + 1] - t_list[i] for i in range(0, len(t_list) - 1)]

if __name__ == "__main__":
    main()