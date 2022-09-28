import numpy as np


class Airplane:
    def __init__(self): #add more stuff here later
        self.g = 9.8 #m/s^2
        self.rho = 1.245 #kg/m^3
        self.m = 220 #kg, total weight estimate
        self.S = 3.5 #m^2

        self.V_min = 12.9 #m/s
        self.V_max = 28.3
        self.Cl_max = 6

        self.I = [0,312,0] #placeholder diagonal of inertia tensor. Assume principal axes

        self.pitch_tail_thrust = 500
        self.tail_distance = 2.6
        
        #currently unused, might be used later when modeling drag from plane body
        self.tail_area = 1
        self.tail_Cd = 1


    def calculate_simple_pitch_roll_period(self):
        #calculate pitch roll time using just tail authority, no body drag taken into account

        net_M = self.pitch_tail_thrust*self.tail_distance #moment from tail thrust

        total_time = 2*(2*np.pi*self.I[1]/net_M)**0.5
        #Newton's second law in angular form integrated twice with 0 initial conditions. Assume we accelerate hard to pi degrees then accelerate back to come back to a full loop with zero angular velocity
        return total_time

    def calculate_loop_gs(self, v, R):
        return v**2/R/(self.g)

    def calculate_loop_R(self, v, Cl):
        return v**2/((self.rho*v**2*Cl*self.S/2)/self.m+self.g)


if __name__=="__main__":
    plane = Airplane()
    r_max_speed = plane.calculate_loop_R(plane.V_min, plane.Cl_max)
    g_max_speed = plane.calculate_loop_gs(plane.V_min, r_max_speed)
    #print(f"Flying at a speed of {plane.V_min:.2f} m/s, the airplane can fly an even loop of radius {r_max_speed:.2f}m and will experience an acceleration of {g_max_speed:.2f} gs")
    print(f"Using max tail thrust of {plane.pitch_tail_thrust:.2f}N the plane can pitch roll in approximately {plane.calculate_simple_pitch_roll_period():.2f}s (ignoring drag)")
