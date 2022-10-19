import extract_geometry
import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u

design_elements = {
    'b': None,
    'wing_mass': None,
    'horiz_tail_mass': None,
    'b_htail': None,
    'b_vtail': None,
    'vert_tail_mass': None,
    'fuse_mass': None,
    'fuse_radius': None,
    'motor_mass': None,
    'tail_motor_mass': None,
    'c_r': None,
    'c_t': None,
    'wing_loc': None,
    'horiz_tail_avchord': None,
    'tail_loc': None,
    'vert_tail_avchord': None,
    'fuse_length': None,
    'structures_loc': None,
    'pilot_mass': None,
    'pilot_loc': None,
    'battery_mass': None,
    'battery_loc': None,
    'tail_motor_loc': None,
    'total_loc': None
}


def get_inertia_moments(design_elts=design_elements):
    '''
    :param design_elts: dictionary of items we want to query from master value sheet
    :return: Principal-axis moments of inertia
    '''

    extract_geometry.get_values(design_elements)
    b = design_elements['b']
    wing_mass = design_elements['wing_mass']
    horiz_tail_mass = design_elements['horiz_tail_mass']
    b_htail = design_elements['b_htail']
    b_vtail = design_elements['b_vtail']
    vert_tail_mass = design_elements['vert_tail_mass']
    fuse_mass = design_elements['fuse_mass']
    fuse_radius = design_elements['fuse_radius']
    motor_mass = design_elements['motor_mass']
    tail_motor_mass = design_elements['tail_motor_mass']
    c_r = design_elements['c_r']
    c_t = design_elements['c_t']
    wing_loc = design_elements['wing_loc']
    horiz_tail_avchord = design_elements['horiz_tail_avchord']
    tail_loc = design_elements['tail_loc']
    vert_tail_avchord = design_elements['vert_tail_avchord']
    fuse_length = design_elements['fuse_length']
    structures_loc = design_elements['structures_loc']
    pilot_mass = design_elements['pilot_mass']
    pilot_loc = design_elements['pilot_loc']
    battery_mass = design_elements['battery_mass']
    battery_loc = design_elements['battery_loc']
    tail_motor_loc = design_elements['tail_motor_loc']
    xcg = design_elements['total_loc']
    horiz_tail_height = b_vtail

    # pilot and batteries modeled as point masses at cg - no contribution to Ixx
    I_xx = (1/12)*wing_mass*b**2 #main wing
    + (1/12)*horiz_tail_mass*b_htail**2+horiz_tail_mass*(horiz_tail_height)**2 #horiz T-tail
    + (1/12)*vert_tail_mass*b_vtail**2+vert_tail_mass*(b_vtail/2)**2 #vert tail
    + (1/2)*fuse_mass*fuse_radius**2 #fuse
    + 2*(motor_mass/2)*(fuse_radius+b/2)**2 #primary motors at wing tips
    + tail_motor_mass*horiz_tail_height**2 #tail motor

    I_yy = (1/12)*wing_mass*((c_r+c_t)/2)**2 + wing_mass*(wing_loc-xcg)**2 #main wing
    + (1/12)*horiz_tail_mass*horiz_tail_avchord**2 + horiz_tail_mass*(tail_loc-xcg)**2 #horiz T-tail
    + (1/12)*vert_tail_mass*vert_tail_avchord**2 + vert_tail_mass*(tail_loc-xcg)**2 #vert tail
    + (1/2)*fuse_mass*fuse_length**2 + fuse_mass(structures_loc-xcg)**2 #fuse
    + pilot_mass*(pilot_loc-xcg)**2 #pilot
    + battery_mass*(battery_loc-xcg)**2 #batteries
    + tail_motor_mass*(tail_motor_loc-xcg)**2 #tail motor

    I_zz = (1/12)*wing_mass*b**2 #main wing
    + (1/12)*horiz_tail_mass*b_htail**2 #horiz T-tail
    + (1/12)*vert_tail_mass*vert_tail_avchord**2 + vert_tail_mass*(tail_loc-xcg)**2 #vert tail
    + (1/2) * fuse_mass * fuse_length ** 2 + fuse_mass(structures_loc - xcg) ** 2  # fuse
    + 2*(motor_mass/2)*(fuse_radius+b/2)**2  # primary motors at wing tips
    + pilot_mass * (pilot_loc - xcg) ** 2  # pilot
    + battery_mass * (battery_loc - xcg) ** 2  # batteries
    + tail_motor_mass * (tail_motor_loc - xcg) ** 2  # tail motor

    return I_xx, I_yy, I_zz


def create_mass_props(design_elts=design_elements):
    '''
    :param design_elts: dictionary of items we want to query from master value sheet
    :return: AeroSandbox MassProperties object
    '''
    extract_geometry.get_values(design_elts)
    plane_mass = design_elts['plane_mass']
    x_cg = design_elts['x_cg']
    y_cg = design_elts['y_cg']
    z_cg = design_elts['z_cg']
    I_xx, I_yy, I_zz = get_inertia_moments(design_elts)

    mass_props = asb.MassProperties(
        mass=plane_mass,
        x_cg=x_cg,
        y_cg=y_cg,
        z_cg=z_cg,
        Ixx=I_xx,
        Iyy=I_yy,
        Izz=I_zz,
        Ixy=0,
        Iyz=0,
        Ixz=0,
    )

    return mass_props


if __name__=="__main__":
    print(create_mass_props(design_elements))
