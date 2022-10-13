import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt

n_timesteps = 100
I_plane = 312
rho = 1.245
CDA= 100
plane_mass =400 #kg
S_ref = 3.5 #m^2
L = 0.5*rho*S_ref*v**2

### Loop Radius Minimization ###
opti = asb.Opti()

wing_loading = plane_mass/S_ref
R_min = 2*wing_loading/Cl_max #want to minimize this

### Snap Roll Time Minimization ###
# roll rate equation: p_dot = L_p*p + L_sigmaa*sigmaa
# Lets set as requirement the roll rate of the Zivka Edge 540: 7.33 rad/sec
dyn = asb.DynamicsRigidBody3DBodyEuler(
    #mass_props=
)