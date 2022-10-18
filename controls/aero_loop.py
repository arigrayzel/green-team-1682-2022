# m = 220  # Mass (kg)
# S = 2.9  # Wing Surface Area (m^2)
# rho = 1.245  # air density
# Cl_max = 1.3  # Maximum lift coefficient
import extract_geometry

design_elements = {
    'plane_mass': None,
    'S_ref': None,
    'rho': None,
    'Cl_max': None
}

extract_geometry.get_values(design_elements)
m = design_elements['plane_mass']
S = design_elements['S_ref']
rho = design_elements['rho']
Cl_max = design_elements['Cl_max']

R_min = (2*m/S) / (rho*Cl_max)  # minimum loop radius (m)
print(R_min, 'm') 
