import extract_geometry
design_element_values = {
    'rho': None,
    'S_ref': None, #m^2
    'b': None, #m
    'Cl_max': None, #stall occurs at about 20 deg AoA, at which point our airfoil produces this Cl
    'fuse_radius': None, #m
    'av_quarter_chord': None, #half of half the span
    'g': None, #m/s
    'plane_mass': None,#kg
    'wing_mass': None, #kg
    'fuse_mass': None,
    'I_fuse': None,
    'I_wing': None,
    'I_plane': None,
    'Cd_tail_roll': None
}
data = extract_geometry.get_values(design_element_values)
b = design_element_values['b']
rho = design_element_values['rho']
print(data)
print('b is', b, 'rho is', rho)