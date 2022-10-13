m = 220  # Mass (kg)
S = 2.9  # Wing Surface Area (m^2)
rho = 1.245  # air density
Cl_max = 1.3  # Maximum lift coefficient

R_min = (2*m/S) / (rho*Cl_max)  # minimum loop radius (m)
print(R_min, 'meters')
