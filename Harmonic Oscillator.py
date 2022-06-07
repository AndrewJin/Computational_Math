"""
Real pendulum simulation
"""

import numpy as np
import Initial_Value_Problems as ivp

def main():
    f = lambda t,u: np.array([ u[1] , -10 * np.sin(u[0]) ])
    u_0 = np.array([3 * np.pi / 4, 0]) #u[0] is angular position, u[1] is angular velocity
    dt = 0.01
    t_final = 10
    method = "equal_rk4"
    plot_vars = [0, 1]
    phase_vars = [(0, 1)]
    
    ivp.solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars)
    
    
    
if __name__ == "__main__":
    main()