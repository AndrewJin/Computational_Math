"""
Real pendulum simulation
"""

import numpy as np
import Initial_Value_Problems as ivp

def main():
    #Describe ODE and initial condition
    #u[0] is angular position, u[1] is angular velocity
    f = lambda t,u: np.array([ u[1] , -10 * np.sin(u[0]) ])
    u_0 = np.array([3 * np.pi / 4, 0]) 
    
    #Parameters for numerical integration and graphing
    dt = 0.01
    t_final = 10
    method = "equal_rk4"
    plot_vars = [0, 1]
    phase_vars = [(0, 1)]
    
    #Run the algorithm
    ivp.solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars)
    
    #With adaptive time step
    err_target = 1e-6
    t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, plot_vars, phase_vars)
    dt_list = [t_list[i + 1] - t_list[i] for i in range(0, len(t_list) - 1)]
    
    #With different initial values
    u_0_list = [np.array([np.pi / 4, 0]), np.array([np.pi / 2, 0]), np.array([3 * np.pi / 4, 0])]
    ivp.compare_ivp(f, u_0_list, dt, t_final, method, plot_vars, phase_vars)
    
    #With adaptive time step
    ivp.compare_adaptive(f, u_0_list, t_final, err_target, plot_vars, phase_vars)
    
    
    
if __name__ == "__main__":
    main()