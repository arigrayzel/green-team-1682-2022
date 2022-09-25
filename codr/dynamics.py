import numpy as np


class Airplane:
    def __init__(self): #add more stuff here later
        self.g = -9.8 #m/s^2, keeping this negative
        self.rho = 1.225 #kg/m^3
        self.m = 220 #kg, total weight estimate
        self.S = 3.5 #m^2

        self.V_min = 12.9 #m/s
        self.V_max = 28.3
        self.Cl_max = 6

    def calculate_loop_gs(self, v, R):
        return v**2/R

    def calculate_loop_R(self, v, Cl):
        return v**2/((self.rho*v**2*Cl*self.S)/self.m-self.g)


if __name__=="__main__":
    plane = Airplane()
    r_max_speed = plane.calculate_loop_R(plane.V_max, plane.Cl_max)
    g_max_speed = plane.calculate_loop_gs(plane.V_max, r_max_speed)
    print(f"Flying at max speed {plane.V_max:.2f} m/s, the airplane can fly an even loop of radius {r_max_speed:.2f}m and will experience an acceleration of {g_max_speed:.2f} gs")
