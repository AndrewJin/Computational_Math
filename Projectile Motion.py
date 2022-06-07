"""
Projectile motion with air resistance simulation
"""

import numpy as np
import matplotlib.pyplot as plt
import Initial_Value_Problems as ivp
import Integration as integrate
        
    
def main():
    #Describe ODE and initial condition
    #u[0] is x velocity, u[1] is y velocity
    f = lambda t,u: np.array([- 1/ 8 * np.sqrt(u[0] ** 2 + u[1] ** 2) * u[0], - 4 - 1/ 8 * np.sqrt(u[0] ** 2 + u[1] ** 2) * u[1] ])
    u_0 = np.array([5., 12.])
    
    #Parameters for numerical integration
    dt = 0.01
    t_final = 3.61
    plot_vars = []
    phase_vars = []
    method = "equal_rk4"
    
    #Since we solved for x velocity and y velocity
    #we must integrate to solve for x position and y position
  
    #Variables needed for integration
    t_list = np.linspace(0, t_final, t_final/dt)
    u_list = ivp.solve_ivp(f, u_0, dt, t_final, method, plot_vars, phase_vars)
    dxdt_list = u_list[:,0]
    dydt_list = u_list[:,1]
    
    #Find position using an accumulation function of velocity
    x_list = integrate.accumulate_points(t_list,dxdt_list,"simpson")
    y_list = integrate.accumulate_points(t_list,dydt_list,"simpson")
    
    #Plot the results of the projectile motion
    fig = plt.figure( figsize = (18,6) )
    ax = fig.subplots(1,3)
    ax[0].set_title("Trajectory")
    ax[0].set_xlabel("$x$")
    ax[0].set_ylabel("$y$")
    ax[0].plot(x_list, y_list)
    
    ax[1].set_title("Horizontal Distance")
    ax[1].set_xlabel("$t$")
    ax[1].set_ylabel("$x$")
    ax[1].plot(t_list, x_list)
    
    ax[2].set_title("Vertical Distance")
    ax[2].set_xlabel("$t$")
    ax[2].set_ylabel("$y$")
    ax[2].plot(t_list, y_list)
    
    
if __name__ == "__main__":
    main()