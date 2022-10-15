import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u
import create_mass_props
import create_plane

#import airplane?
airplane = create_plane.create_plane()
mass_properties = create_mass_props.create_mass_props()
min_speed = 12.3 #24kt


#initialize problem
opti = asb.Opti()

#define time, unknown duration
final_time = opti.variable(init_guess=60, lower_bound=0)
time = np.linspace(0,final_time, 200)

N = np.length(time) #number of time points

#create dynamics instance, initial guesses for a roll
dyn = asb.DynamicsRigidBody3DBodyEuler(
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
    p = opti.variable(init_guess = np.concatenate((np.linspace(0,6,N//2), np.linspace(6,0,N//2)))),
    q = opti.variable(init_guess = np.zeros(N)),
    r = opti.variable(init_guess = np.zeros(N)))

#constrain initial state
opti.subject_to([
    dyn.u_b[0] == 20,
    dyn.v_b[0] == 0,
    dyn.w_b[0] == 0,
    dyn.phi[0] == 0,
    dyn.theta[0] == 0,
    dyn.psi[0] == 0,
    dyn.p[0] == 0,
    dyn.q[0] == 0,
    dyn.r[0] == 0
    ])

#constrain final state
opti.subject_to([
    dyn.u_b[-1] == 20,
    dyn.v_b[-1] == 0,
    dyn.w_b[-1] == 0,
    dyn.phi[-1] == 2*np.pi,
    dyn.theta[-1] == 0,
    dyn.psi[-1] == 0,
    dyn.p[-1] == 0,
    dyn.q[-1] == 0,
    dyn.r[-1] == 0
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
thrust = opti.variable(init_guess= 1000*np.ones(N), lower_bound=0, upper_bound=2500)
dyn.add_force(
    Fx=thrust,
    axes="body"
)

#roll moment
roll = opti.variable(init_guess=np.concatenate((np.ones(N//2), -np.ones(N//2))))
dyn.add_moment(
    Mx=roll,
    axes="body"
)

dyn.constrain_derivatives(opti, time)
opti.minimize(final_time)

sol = opti.solve()
try:
    dyn.substitute_solution(sol)
except:
    print(opti.debug.value)
print("done!")
