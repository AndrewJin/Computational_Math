"""
Solves, then animates solution to the Van der Pol oscillator
"""

import Initial_Value_Problems as ivp
import manim as mn
import numpy as np
import math

class VanDerPolAnim(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is position, u[1] is velocity
        mu = 20
        f = lambda t,u: np.array([ u[1] , mu * (1 - u[0] ** 2) * u[1] - u[0] ])
        u_0 = np.array([1.05, 0.]) 
        
        #Parameters for numerical integration and graphing
        t_final = 50
        err_target = 1e-4
        
        #Run the algorithm, but don't plot
        t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, [], [])
        u0_list = [u[0] for u in u_list] #position over time
        u1_list = [u[1] for u in u_list] #velocity over time
        
        #Setup animation
        #------------------------------
        #Construct the coordinate axes
        u0_axes = mn.Axes(x_range = [0, t_final, t_final / 10],
                          y_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                          x_length = 4,
                          y_length = 4,                     
                          tips = False)
        u0_axes.shift(mn.LEFT * 4.5)
        
        
        u1_axes = mn.Axes(x_range = [0, t_final, t_final / 10],
                          y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                          x_length = 4,
                          y_length = 4,
                          tips = False)              
        u1_axes.shift(mn.RIGHT * 4.5)

        
        u0u1_axes = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                            y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                            x_length = 4,
                            y_length = 4,
                            tips = False)


        axes = mn.VGroup()
        axes += u0_axes
        axes += u1_axes
        axes += u0u1_axes
        
        
        #Add labels
        labels = mn.VGroup()
        labels += u0_axes.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += u0_axes.get_y_axis_label(mn.Tex(r"$u_0$", font_size = 24), edge = mn.UL)
        labels += u1_axes.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += u1_axes.get_y_axis_label(mn.Tex(r"$u_1$", font_size = 24), edge = mn.UL)
        labels += u0u1_axes.get_x_axis_label(mn.Tex(r"$u_0$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += u0u1_axes.get_y_axis_label(mn.Tex(r"$u_1$", font_size = 24), edge = mn.UP)
        
        #Add functions
        def largest_leq_than(t):
            """
            Finds the largest time value in t_list less than or equal to input t,
            which allows us to determine which interval t is in
            """
            n = len(t_list)
            
            lower_index = 0 
            #lower bound starts at t_list[0] which is t = 0
            upper_index = n - 1 
            #upper bound starts at t_list[n - 1] which is t = t_final
            
            #Catch t not within time range, should not happen in normal use
            if t < t_list[0] or t > t_list[n - 1]:
                raise Exception("t not within time range")
            
            #Binary search for the interval that t is in
            while upper_index - lower_index > 1:
                mid_index = math.floor( (lower_index + upper_index) / 2 )
                if t == t_list[mid_index]:
                    lower_index = mid_index
                    upper_index = mid_index + 1
                elif t < t_list[mid_index]:
                    upper_index = mid_index
                elif t > t_list[mid_index]:
                    lower_index = mid_index
                    
            return lower_index 
            #t is between t_list[lower_index] (inclusive) and t_list[lower_index + 1] exclusive
            #except for input t = t_final
            
        
        def u0(t):
            """
            Solution to u_0 (position) interpolated from a list of points
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u0_list[i + 1] - u0_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u0_list[i]
            #linear interpolating function, in point-slope form
            
            
        def u1(t):
            """
            Solution to u_1 (velocity) interpolated from a list of points
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u1_list[i + 1] - u1_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u1_list[i]
            #linear interpolating function, in point-slope form
            
        
        def u0_u1(t):
            """
            Parametric function of t with u_0 (position) on x axis and u_1 (velocity) on y axis
            """
            return [u0(t), u1(t), 0]
            
            
        functions = mn.VGroup()  #Stores functions to plot
        functions += u0_axes.plot(u0, x_range = [0, t_final], color = mn.BLUE)
        functions += u1_axes.plot(u1, x_range = [0, t_final], color = mn.BLUE)
        functions += u0u1_axes.plot_parametric_curve(lambda t: u0_u1(t), t_range = [0, t_final], color = mn.RED)
        
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes, labels, functions)
        #------------------------------
        
        
        
        #Make the animation
        #------------------------------
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        u0_line_anim = mn.always_redraw(lambda : u0_axes.plot(u0, x_range = [0, e.get_value()], color = mn.WHITE))
        u0_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(u0_axes.c2p(e.get_value(), u0(e.get_value()))))
        
        u1_line_anim = mn.always_redraw(lambda : u1_axes.plot(u1, x_range = [0, e.get_value()], color = mn.YELLOW))
        u1_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(u1_axes.c2p(e.get_value(), u1(e.get_value()))))
        
        u0u1_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(u0u1_axes.c2p(u0(e.get_value()), u1(e.get_value()))))
        
        
        #Construct objects for animation
        self.add(u0_line_anim, u0_dot_anim, u1_line_anim, u1_dot_anim, u0u1_dot_anim)
        
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 24, rate_func = mn.linear)
        self.wait(2)
        #------------------------------