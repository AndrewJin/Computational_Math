"""
Solves, then animates solution to the real pendulum.
"""

import Initial_Value_Problems as ivp
import manim as mn
import numpy as np
import math

class HarmonicOscillatorTime(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is angular position, u[1] is angular velocity
        f = lambda t,u: np.array([ u[1] , -10 * np.sin(u[0]) ])
        u_0 = np.array([7 * np.pi / 8, 0]) 
        
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
        axes0 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                        x_length = 4,
                        y_length = 4,                     
                        tips = False)
        axes0.shift(mn.LEFT * 3)

        
        axes1 = mn.Axes(x_range = [0, t_final, t_final / 10],
                        y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                        x_length = 4,
                        y_length = 4,
                        tips = False)
        axes1.shift(mn.RIGHT * 3)
        
        #Add titles and labels
        
        labels = mn.VGroup()
        labels += axes0.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes0.get_y_axis_label(mn.Tex(r"$\theta$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        labels += axes1.get_x_axis_label(mn.Tex(r"$t$", font_size = 24), edge = mn.RIGHT, direction = mn.RIGHT)
        labels += axes1.get_y_axis_label(mn.Tex(r"$\omega$", font_size = 24), edge = mn.LEFT, direction = mn.LEFT)
        
        
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
        
        functions += axes0.plot(u0, x_range = [0, t_final], color = mn.BLUE)
        functions += axes1.plot(u1, x_range = [0, t_final], color = mn.GREEN)
        
        
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes0, axes1, labels, functions)
        
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        u0_line_anim = mn.always_redraw(lambda : axes0.plot(u0, x_range = [0, e.get_value()], color = mn.WHITE))
        u0_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes0.c2p(e.get_value(), u0(e.get_value()))))
        
        u1_line_anim = mn.always_redraw(lambda : axes1.plot(u1, x_range = [0, e.get_value()], color = mn.YELLOW))
        u1_dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes1.c2p(e.get_value(), u1(e.get_value()))))
        
        #Construct objects for animation
        self.add(u0_line_anim, u0_dot_anim, u1_line_anim, u1_dot_anim)
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 8, rate_func = mn.linear) #e.animate parameter ie end time
        self.wait(2)
        
        
class HarmonicOscillatorPhase(mn.Scene):
    def construct(self):
        #Describe and solve IVP
        #------------------------------
        #u[0] is angular position, u[1] is angular velocity
        f = lambda t,u: np.array([ u[1] , -10 * np.sin(u[0]) ])
        u_0 = np.array([7 * np.pi / 8, 0]) 
        
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
        #Position on x axis, Velocity on y axis
        axes = mn.Axes(x_range = [min(u0_list), max(u0_list), (max(u0_list) - min(u0_list)) / 10],
                       y_range = [min(u1_list), max(u1_list), (max(u1_list) - min(u1_list)) / 10],
                       x_length = 6,
                       y_length = 6,                     
                       tips = False)
                       
        
        #Add titles and labels
        
        labels = mn.VGroup()
        labels += axes.get_x_axis_label(mn.Tex(r"$\theta$", font_size = 24), edge = mn.RIGHT)
        labels += axes.get_y_axis_label(mn.Tex(r"$\omega$", font_size = 24), edge = mn.UP)
        
        
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
        
        def u0_u1(t):
            """
            Parametric function of t with u0(t) on x axis and u1(t) on y axis
            """
            return [u0(t), u1(t), 0]
        
        
        f1 = axes.plot_parametric_curve(lambda t: u0_u1(t), t_range = [0, t_final])
        
        functions += f1
        
        #Construct objects unrelated to animation (initial setup)
        self.add(axes, labels, functions)
        
        #Make objects for the animation
        e = mn.ValueTracker(0.01) #parameter is start time
        
        dot_anim = mn.always_redraw(lambda : mn.Dot(color = mn.WHITE).move_to(axes.c2p(u0(e.get_value()), u1(e.get_value()))))
        
        #Construct objects for animation
        self.add(dot_anim)
        
        #Make the animation
        self.wait(2)
        self.play(e.animate.set_value(t_final), run_time = 8)
        self.wait(2)