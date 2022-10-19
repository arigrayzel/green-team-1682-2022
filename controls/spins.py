import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

n_timesteps = 100
I_xx = 109
I_yy = 3194
I_zz = 3293

l_rotor = 7
t_rotor = 2*250
rho = 1.245
Cd = 1.28 #flat plate
A_tail = 2.5
extra_drag_coeff = 2

opti = asb.Opti()

time_final = opti.variable(init_guess=5, lower_bound=0)

time = np.linspace(0, time_final, n_timesteps)

angle = opti.variable(init_guess=np.linspace(0, 2*np.pi, n_timesteps))

angular_velocity = opti.derivative_of(angle, with_respect_to=time, derivative_init_guess=1)
alpha = opti.derivative_of(angular_velocity, with_respect_to=time, derivative_init_guess=1)


moment_guess = 5000


moment = opti.variable(init_guess=np.linspace(moment_guess, -moment_guess, n_timesteps),n_vars = n_timesteps, lower_bound=-moment_guess, upper_bound=moment_guess)

opti.constrain_derivative(variable=angular_velocity, with_respect_to=time, derivative=(moment-Cd*A_tail*0.5*rho*(angular_velocity*l_rotor)**2)*extra_drag_coeff/I_yy)

opti.subject_to([
    angle[0] == 0,
    angle[-1] == 2*np.pi,
    angular_velocity[0]==0,
    angular_velocity[-1]==0,
    ])

opti.minimize(time_final)
sol = opti.solve()

print(f"Max angular acceleration: {max(sol.value(alpha)):.2f}")
print(f"Max negative angular acceleration: {min(sol.value(alpha)):.2f}")

fig, ax = plt.subplots(3,1)
ax[0].plot(sol.value(time), sol.value(angle))
ax[0].set_xlabel(r"Time(s)")
ax[0].set_ylabel(r"Angle(rad)")

ax[1].plot(sol.value(time), sol.value(angular_velocity))
ax[1].set_xlabel(r"Time(s)")
ax[1].set_ylabel(r"Anglular velocity(rad/s)")

ax[2].plot(sol.value(time), sol.value(moment/l_rotor))
ax[2].set_xlabel(r"Time(s)")
ax[2].set_ylabel(r"Thrust(N)")


##fig, ax = plt.subplots(1,3,2, figsize=(6.4, 4.9), dpi=200)
#plt.plot(sol.value(time), sol.value(angular_velocity))
#plt.xlabel(r"Time")
#plt.ylabel(r"Angular velocity")
#plt.title(r"Angular Velocity")
#plt.tight_layout()
#plt.show() 
#
##fig, ax = plt.subplots(1,3,3, figsize=(6.4, 4.9), dpi=200)
#plt.plot(sol.value(time), sol.value(moment))
#plt.xlabel(r"Time")
#plt.ylabel(r"Moment")
#plt.title(r"Moment")
#plt.tight_layout()
plt.show() 
