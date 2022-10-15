import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u

#import airplane?
#mass_properties = ?
min_speed = 12.3 #24kt


#initialize problem
opti = asb.Opti()

#define time, unknown duration
time = np.linspace(0,opti.variable(init_guess=60, lower_bound=0, 200)

N = np.length(time) #number of time points

#create dynamics instance, initial guesses for a roll
dyn = asb.DynamicsRigidBody3DEuler(
    mass_props=mass_properties,
    x_e = opti.variable(init_guess=1000*np.linspace(0,1,N)),
    y_e = opti.variable(init_guess=0*np.linspace(0,1,N)),
    z_e = opti.variable(init_guess=-1000*np.ones(N)),
    u_b = opti.variable(init_guess= 30*np.ones(N), upper_bound=0),
    v_b = opti.variable(init_guess= 0*np.ones(N)),
    w_b = opti.variable(init_guess= 0*np.ones(N)),
    phi = opti.variable(init_guess= np.zeros(N)),
    theta = opti.variable(init_guess= np.zeros(N)),
    psi = opti.variable(init_guess = np.zeros(N)),
    p = opti.variable(init_guess = np.concatenate((np.linspace(0,6,N/2, np.linspace(6,0,N/2))))),
    q = opti.variable(init_guess = np.zeros(N)),
    r = opti.variable(init_guess = np.zeros(N)))

#constrain initial state
opti.subject_to([
    u_b[0] == 20,
    v_b[0] == 0,
    w_b[0] == 0,
    phi[0] == 0,
    theta[0] == 0,
    psi[0] == 0,
    p[0] == 0,
    q[0] == 0,
    r[0] == 0
    ])

#constrain final state
opti.subject_to([
    u_b[-1] == 20,
    v_b[-1] == 0,
    w_b[-1] == 0,
    phi[-1] == 2*np.pi,
    theta[-1] == 0,
    psi[-1] == 0,
    p[-1] == 0,
    q[-1] == 0,
    r[-1] == 0
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
thrust = opti.variable(init
dyn.add_force(
    Fx=thrust,
    axes="body"
)

