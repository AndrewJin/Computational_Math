"""
Logistic differential equation simulation
"""

import Initial_Value_Problems as ivp

def main():
    #Describe ODE and initial condition
    f = lambda t,u: u * (1 - u)
    u_0 = 0.5
    
    #Parameters for numerical integration and graphing
    dt = 0.01
    t_final = 10
    method = "equal_rk4"
    plot_vars = [0]
    phase_vars = []
    
    #Run the algorithm
    ivp.solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars)
    
    #with different initial values
    u_0_list = [0.1, 0.2, 0.3, 0.4, 0.5]
    ivp.compare_ivp(f, u_0_list, dt, t_final, method, plot_vars, phase_vars)
    
    #Using adaptive solver
    err_target = 1e-6
    t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, plot_vars, phase_vars)
    dt_list = [t_list[i + 1] - t_list[i] for i in range(0, len(t_list) - 1)]
    
    
    
if __name__ == "__main__":
    main()