"""
Solves, then animates solution to the Lorenz oscillator.
"""

import Initial_Value_Problems as ivp
import manim as mn
import numpy as np
import math

class LorenzOscillatorAdaptiveTime(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is angular position, u[1] is angular velocity
        s = 10
        p = 28
        b = 8/3
        f = lambda t,u: np.array([s * (u[1] - u[0]), u[0] * (p - u[2]) - u[1], u[0] * u[1] - b * u[2]])
        u_0 = np.array([1., 1., 1.])
        
        #Parameters for the solution algorithm
        t_final = 30
        err_target = 1e-6

        
        #Run the algorithm, but don't plot, just return solution
        t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, [], [])
        u0_list = [u[0] for u in u_list]
        u1_list = [u[1] for u in u_list]
        u2_list = [u[2] for u in u_list]
        #------------------------------
        
        
        #Setup animation and animate solution
        #------------------------------
        #Construct the coordinate axes
        axes0 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)
        axes0.shift(mn.LEFT * 4.5)

        
        axes1 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        x_length = 4,
                        y_length = 4,
                        tips = False)
                        
                        
        axes2 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,
                    tips = False)              
        axes2.shift(mn.RIGHT * 4.5)
        
        
        
        #Add titles and labels
        
        labels = mn.VGroup()
        labels += axes0.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes0.get_y_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        labels += axes1.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes1.get_y_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        labels += axes2.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes2.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        
        
        #Add functions to plot
        functions = mn.VGroup()  #Stores functions to plot
        
        
        #ADAPTIVE dt SOLUTION (Implement binary search for index of element less than input
        #Or possibly how to animate without creating function, just iterating through the list once
        def largest_leq_than(t):
            """
            Finds the largest time value in t_list less than or equal to input t,
            which allows us to determine which interval t is in
            """
            n = len(t_list)
            
            lower_index = 0 
            #lower bound is t_list[0] which is t = 0
            upper_index = n - 1 
            #upper bound is t_list[n - 1] which is t = t_final
            
            #This should never occur in normal use
            if t < t_list[0] or t > t_list[n - 1]:
                raise Exception("t not within bounds")
            
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
            Solution to x interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u0_list[i + 1] - u0_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u0_list[i]
            #linear interpolating function, in point-slope form
        
        
        def u1(t):
            """
            Solution to y interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u1_list[i + 1] - u1_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u1_list[i]
            #linear interpolating function, in point-slope form


        def u2(t):
            """
            Solution to z interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u2_list[i + 1] - u2_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u2_list[i]
            #linear interpolating function, in point-slope form
        
        functions += axes0.plot(u0, x_range = [0, t_final], color = mn.BLUE)
        functions += axes1.plot(u1, x_range = [0, t_final], color = mn.GREEN)
        functions += axes2.plot(u2, x_range = [0, t_final], color = mn.RED)
        
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes0, axes1, axes2, labels, functions)
        
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        u0_line_anim = mn.always_redraw(lambda : axes0.plot(u0, x_range = [0, e.get_value()], color = mn.WHITE))
        u0_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes0.c2p(e.get_value(), u0(e.get_value()))))
        
        u1_line_anim = mn.always_redraw(lambda : axes1.plot(u1, x_range = [0, e.get_value()], color = mn.WHITE))
        u1_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes1.c2p(e.get_value(), u1(e.get_value()))))
        
        u2_line_anim = mn.always_redraw(lambda : axes2.plot(u2, x_range = [0, e.get_value()], color = mn.WHITE))
        u2_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes2.c2p(e.get_value(), u2(e.get_value()))))
        
        #Construct objects for animation
        self.add(u0_line_anim, u0_dot_anim, u1_line_anim, u1_dot_anim, u2_line_anim, u2_dot_anim)
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 30, rate_func = mn.linear) #e.animate parameter ie end time
        self.wait(2)
        
        
class LorenzOscillatorAdaptivePhase(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is angular position, u[1] is angular velocity
        s = 10
        p = 28
        b = 8/3
        f = lambda t,u: np.array([s * (u[1] - u[0]), u[0] * (p - u[2]) - u[1], u[0] * u[1] - b * u[2]])
        u_0 = np.array([1., 1., 1.])
        
        #Parameters for the solution algorithm
        t_final = 30
        err_target = 1e-6

        
        #Run the algorithm, but don't plot, just return solution
        t_list, u_list = ivp.adaptive_ivp(f, u_0, t_final, err_target, [], [])
        u0_list = [u[0] for u in u_list]
        u1_list = [u[1] for u in u_list]
        u2_list = [u[2] for u in u_list]
        #------------------------------
        
        
        #Setup animation and animate solution
        #------------------------------
        #x-y projection
        axes0 = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)
        axes0.shift(mn.LEFT * 4.5)
                        
        #x-z projection               
        axes1 = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)  
                        
        #y-z projection              
        axes2 = mn.Axes(x_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        y_range = [min(u2_list), max(u2_list), (max(u2_list) - min(u2_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)   
        axes2.shift(mn.RIGHT * 4.5)
        
        #Add titles and labels
        
        labels = mn.VGroup()
        labels += axes0.get_x_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.RIGHT)
        labels += axes0.get_y_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.UP)
        labels += axes1.get_x_axis_label(mn.Tex(r"$x$", font_size = 24), edge = mn.RIGHT)
        labels += axes1.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.UP)
        labels += axes2.get_x_axis_label(mn.Tex(r"$y$", font_size = 24), edge = mn.RIGHT)
        labels += axes2.get_y_axis_label(mn.Tex(r"$z$", font_size = 24), edge = mn.UP)
        
        
        #Add functions to plot
        functions = mn.VGroup()  #Stores functions to plot
        
        def largest_leq_than(t):
            """
            Finds the largest time value in t_list less than or equal to input t,
            which allows us to determine which interval t is in
            """
            n = len(t_list)
            
            lower_index = 0 
            #lower bound is t_list[0] which is t = 0
            upper_index = n - 1 
            #upper bound is t_list[n - 1] which is t = t_final
            
            #This should never occur in normal use
            if t < t_list[0] or t > t_list[n - 1]:
                raise Exception("t not within bounds")
            
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
            
        def x(t):
            """
            Solution to x interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u0_list[i + 1] - u0_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u0_list[i]
            #linear interpolating function, in point-slope form
        
        
        def y(t):
            """
            Solution to y interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u1_list[i + 1] - u1_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u1_list[i]
            #linear interpolating function, in point-slope form


        def z(t):
            """
            Solution to z interpolated from list of points.
            """
            i = largest_leq_than(t)
            #t is between t_list[i] and t_list[i + 1]
            
            return (u2_list[i + 1] - u2_list[i]) / (t_list[i + 1] - t_list[i]) * (t - t_list[i]) + u2_list[i]
            #linear interpolating function, in point-slope form
        
        def xy(t):
            """
            Paramemtric function for (x,y)
            """
            return [x(t), y(t), 0]
            
        def xz(t):
            """
            Parametric function for (x,z)
            """
            return [x(t), z(t), 0]
            
        def yz(t):
            """
            Parametric function for (y,z)
            """
            return [y(t), z(t), 0]
        
        
        f_xy = axes0.plot_parametric_curve(lambda t: xy(t), t_range = [0, t_final], color = mn.BLUE)
        f_xz = axes1.plot_parametric_curve(lambda t: xz(t), t_range = [0, t_final], color = mn.BLUE)
        f_yz = axes2.plot_parametric_curve(lambda t: yz(t), t_range = [0, t_final], color = mn.BLUE)
        
        functions += f_xy
        functions += f_xz
        functions += f_yz
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes0, axes1, axes2, labels, functions)
        
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        lines = mn.VGroup()
        dots = mn.VGroup()
        
        xy_line_anim = mn.always_redraw(lambda : axes0.plot_parametric_curve(lambda t: xy(t), t_range = [0, e.get_value()], color = mn.WHITE))
        xz_line_anim = mn.always_redraw(lambda : axes1.plot_parametric_curve(lambda t: xz(t), t_range = [0, e.get_value()], color = mn.WHITE))
        yz_line_anim = mn.always_redraw(lambda : axes2.plot_parametric_curve(lambda t: yz(t), t_range = [0, e.get_value()], color = mn.WHITE))
        
        xy_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes0.c2p(x(e.get_value()), y(e.get_value()))))
        xz_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes1.c2p(x(e.get_value()), z(e.get_value()))))
        yz_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.RED).move_to(axes2.c2p(y(e.get_value()), z(e.get_value()))))
        
        lines += xy_line_anim 
        lines += xz_line_anim
        lines += yz_line_anim
        
        dots += xy_dot_anim
        dots += xz_dot_anim
        dots += yz_dot_anim
        
        #Construct objects for animation
        self.add(lines, dots)
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 30)
        self.wait(2)