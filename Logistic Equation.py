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
    
    
    
if __name__ == "__main__":
    main()