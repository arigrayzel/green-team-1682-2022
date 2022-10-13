import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

# Define Useful Constants
rho = 1.245
S_ref = 3.5 #m^2
b = 4.6 #m
Cl_max = 1.3 #stall occurs at about 20 deg AoA, at which point our airfoil produces this Cl
fuse_radius = 0.3 #m
av_quarter_chord = b/4 #half of half the span
g = 9.8 #m/s
maneuver_speed = 20 #m/s
plane_mass = 233 #kg
wing_mass = 10.5 #kg
fuse_mass = plane_mass - wing_mass
I_fuse = 0.5*fuse_mass*fuse_radius**2
I_wing = (1/12)*(wing_mass/2)*(b/4)**2 + (wing_mass/2)*((b/4)+fuse_radius)**2
I_plane = I_fuse + 2*I_wing

### Snap Roll Time Minimization ###
n_timesteps = 100

opti = asb.Opti()
time_final = opti.variable(init_guess=5, lower_bound=1)
time = np.linspace(0, time_final, n_timesteps)

angle = opti.variable(
    init_guess=np.linspace(0, 2*np.pi, n_timesteps)
)

angular_velocity = opti.derivative_of(
    angle,
    with_respect_to=time,
    derivative_init_guess=1
)

# model the force as half of the total lift at a certain Cl
half_span_location = fuse_radius+av_quarter_chord # fuse radius is 0.3m + location of average quarter chord (0.5*2.3)
force = 0.5*rho*maneuver_speed**2*(S_ref/2)*Cl_max
moment_max = force*half_span_location

moment = opti.variable(init_guess=np.linspace(moment_max, -moment_max, n_timesteps),n_vars = n_timesteps, lower_bound=-moment_max, upper_bound=moment_max)

opti.constrain_derivative(
    variable=angular_velocity,
    with_respect_to=time,
    derivative=moment/I_plane # TODO - is this angular acceleration?
)

opti.subject_to([
    angle[0] == 0,
    angle[-1] == 2*np.pi,
    angular_velocity[0]==0,
    angular_velocity[-1]==0,
    ])

opti.minimize(time_final)
sol = opti.solve()

fig, ax = plt.subplots(3,1)
ax[0].plot(sol.value(time), sol.value(angle))
ax[0].set_xlabel(r"Time")
ax[0].set_ylabel(r"Angle")

ax[1].plot(sol.value(time), sol.value(angular_velocity))
ax[1].set_xlabel(r"Time")
ax[1].set_ylabel(r"Anglular velocity")

ax[2].plot(sol.value(time), sol.value(moment)/half_span_location)
ax[2].set_xlabel(r"Time")
ax[2].set_ylabel(r"Aerodynamic Force")

plt.show()

