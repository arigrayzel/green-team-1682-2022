import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u
import create_mass_props
import create_plane
import matplotlib.pyplot as plt
import extract_geometry

# design_elements = {
#     'b': None,
#     'c_t': None,
#     'c_r': None,
#     'b_htail': None,
#     'c_htail': None,
#     'b_vtail': None,
#     'c_vtail': None,
#     'le_tail': None,
#     'tip_to_le': None,
#     'fuse_width': None,
#     'Cl_max': None
# }
# extract_geometry.get_values(design_elements)

#import airplane?
airplane = create_plane.create_plane()
# define airplane op point?
mass_properties = create_mass_props.create_mass_props()
min_speed = 12.3 #24kt


#initialize problem
opti = asb.Opti()

#define time, unknown duration
final_time = opti.variable(init_guess=12.0, lower_bound=0.0)
time = np.linspace(0,final_time, 200)

N = np.length(time) #number of time points

#create dynamics instance, initial guesses for a roll
dyn = asb.DynamicsRigidBody3DBodyEuler(
    mass_props=mass_properties,
    x_e = opti.variable(init_guess=np.zeros(N), n_vars=N), #x-pos
    y_e = opti.variable(init_guess=np.zeros(N), n_vars=N),             #y-pos
    z_e = opti.variable(init_guess=-1000*np.ones(N), n_vars=N),        #z-pos
    u_b = opti.variable(init_guess= 25*np.ones(N), n_vars=N),          #x-vel
    v_b = opti.variable(init_guess= np.zeros(N), n_vars=N),            #y-vel
    w_b = opti.variable(init_guess= np.zeros(N), n_vars=N),            #z-vel
    phi = opti.variable(init_guess= np.zeros(N), n_vars=N),            #roll angle
    theta = opti.variable(init_guess= np.zeros(N), n_vars=N),          #pitch angle
    psi = opti.variable(init_guess = np.zeros(N), n_vars=N),           #yaw angle
    p = opti.variable(init_guess = np.zeros(N), n_vars=N),             #roll angular vel
    q = opti.variable(init_guess = np.zeros(N), n_vars=N),             #pitch angular vel
    r = opti.variable(init_guess = np.zeros(N), n_vars=N))             #yaw angular vel

#constrain initial state
opti.subject_to([
    dyn.x_e[0] == 0,
    dyn.y_e[0] == 0,
    dyn.z_e[0] == -1000,
    dyn.u_b[0] == 25,
    dyn.v_b[0] == 0,
    dyn.w_b[0] == 0,
    dyn.phi[0] == 0,
    dyn.theta[0] == 0,
    dyn.psi[0] == 0,
    dyn.p[0] == 0,
    dyn.q[0] == 0,
    dyn.r[0] == 0
    ])

eps = 1e-1
#constrain final state
opti.subject_to([
    dyn.z_e[-1] < -1010,
    # dyn.y_e[-1] == 0,
    # dyn.y_e[-1] > 0-eps,
    # dyn.w_b[-1] < 0+eps,
    dyn.w_b[-1] == 0,
    #dyn.u_b[-1] == 20,
    #dyn.v_b[-1] == 0,
    #dyn.w_b[-1] == 0,
    # dyn.phi[-1] < 2*np.pi+eps,
    # dyn.phi[-1] > 2*np.pi-eps,
    # dyn.theta[-1] == 0,
    #dyn.psi[-1] == 0,
    dyn.p[-1] == 0,
    dyn.q[-1] == 0,
    #dyn.r[-1] == 0
    ])

#add in forces
dyn.add_gravity_force(g=9.81)

aero = asb.AeroBuildup(
    airplane=airplane,
    op_point = dyn.op_point
).run()

dyn.add_force(
    *aero["F_w"],
    axes="wind"
)

#thrust variables
thrust = opti.variable(init_guess= 1000*np.ones(N), lower_bound=0, upper_bound=2500, n_vars=N)
dyn.add_force(
    Fx=thrust,
    axes="body"
)

#roll moment
# roll = opti.variable(init_guess=np.concatenate((1000*np.ones(N//2), -1000*np.ones(N//2))), n_vars=N, lower_bound=-1000, upper_bound=1000)
roll = opti.variable(init_guess=np.zeros(N), n_vars=N, lower_bound=-1000, upper_bound=1000)
#
#pitch moment
# max_pitching_moment = 0.5*1.225*dyn.u_b**2*1.5*1.54 * (8-0.75)
pitch = opti.variable(init_guess=500*np.ones(N), n_vars=N, lower_bound=-1000, upper_bound=1000)
#yaw moment
#yaw = opti.variable(init_guess=np.zeros(N), n_vars=N, lower_bound=-1000, upper_bound=1000)
dyn.add_moment(
    Mx=roll,
    My=pitch,
    #Mz=yaw,
    axes="body"
)


dyn.constrain_derivatives(opti, time)
opti.minimize(final_time)
# opti.minimize(dyn.x_e**2 + dyn.y_e**2)
sol = opti.solve()
dyn.substitute_solution(sol)

# fig, ax = plt.subplots(3,1)
# ax[0].plot(sol.value(time), sol.value(dyn.phi))
# ax[0].set_xlabel(r"Time(s)")
# ax[0].set_ylabel(r"Angle(rad)")
#
# ax[1].plot(sol.value(time), sol.value(dyn.p))
# ax[1].set_xlabel(r"Time(s)")
# ax[1].set_ylabel(r"Angular velocity(rad/s)")
#
# ax[2].plot(sol.value(time), sol.value(roll))
# ax[2].set_xlabel(r"Time(s)")
# ax[2].set_ylabel(r"Roll moment")

plt.show()

plotter = dyn.draw(
        vehicle_model=airplane,
        scale_vehicle_model=0.25,
        show=False
        )
plotter.show()
