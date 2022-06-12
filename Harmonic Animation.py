"""
Solves, then animates solution to the harmonic oscillator. WORK IN PROGRESS
"""

import Initial_Value_Problems as ivp
import manim as mn
import numpy as np
import math

class AnimHarmonicOscillator(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is angular position, u[1] is angular velocity
        f = lambda t,u: np.array([ u[1] , -10 * np.sin(u[0]) ])
        u_0 = np.array([31 * np.pi / 32, 0]) 
        
        #Parameters for numerical integration and graphing
        dt = 0.01
        t_final = 10
        method = "equal_rk4"
        
        #Run the algorithm, but don't plot, just return solution
        u_list = ivp.solve_ivp(f, u_0, dt, t_final, method, [], [])
        u0_list = [u[0] for u in u_list] #Solution for angular position 
        u1_list = [u[1] for u in u_list] #Solution for angular velocity
        #------------------------------
        
        #Setup animation and animate solution
        #------------------------------
        #Construct the coordinate axes
        #TO DO: Add labels to axes
        axes = mn.Axes(x_range = [0, t_final, t_final / 10],
                    y_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                    x_length = 6,
                    y_length = 6,
                    tips = False)
        
        """
        #Add lines to the coordinate axes
        #TO DO: Restore this function
        lines = mn.VGroup() #Stores all the individual lines as a group
        for i in np.arange(0, 1 + 0.1, 0.1):
            lines += axes.get_vertical_line(axes.c2p(i, 1), color = mn.WHITE)
            lines += axes.get_horizontal_line(axes.c2p(1, i), color = mn.WHITE)
        """
        
        #Add functions to plot
        functions = mn.VGroup()  #Stores functions to plot
        
        def u0(t):
            """
            Solution to angular position interpolated from list of points.
            """
            i = t / dt
            if i <= len(u0_list) - 1:
                if i == int(i): #i is integer
                    return u0_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u0_list[math.ceil(i)] * math.modf(i)[0] + u0_list[math.floor(i)] * (1 - math.modf(i)[0])   
        
        def u1(t):
            """
            Solution to angular velocity interpolated from list of points.
            """
            i = t / dt
            if i <= len(u1_list) - 1:
                if i == int(i): #i is integer
                    return u1_list[int(i)]
                else: #i isn't integer, interpolate between nearest points
                    return u1_list[math.ceil(i)] * math.modf(i)[0] + u1_list[math.floor(i)] * (1 - math.modf(i)[0])   
        
        functions += axes.plot(u0, x_range = [0, t_final], color = mn.BLUE)
        
        #Construct objects unrelated to animation
        self.add(axes, functions)
        
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        line_anim = mn.always_redraw(lambda : axes.plot(u0, x_range = [0, e.get_value()], color = mn.WHITE))
        dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes.c2p(e.get_value(), u0(e.get_value()))))
        
        #Construct objects for animation
        self.add(line_anim, dot_anim)
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 8, rate_func = mn.linear) #e.animate parameter ie end time
        self.wait(2)