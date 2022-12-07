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
    'vert_tail_avchord': None,
    'fuse_length': None,
    'pilot_mass': None,
    'pilot_loc': None,
    'battery_mass': None,
    'battery_loc': None,
    'tail_motor_loc': None,
    'total_loc': None,
    'tail_motor_z_loc': None,
    'landing_gear_mass': None,
    'landing_gear_z_loc': None,
    'avionics_mass': None,
    'avionics_z_loc': None,
    'batteries_z_loc': None,
    'wing_z_loc': None,
    'tail_surfaces_z_loc': None,
    'fuse_z_loc': None,
    'pilot_z_loc': None,
    'fuse_loc': None,
    'battery_z_loc': None,
    'primary_motor_loc': None,
    'primary_motor_z_loc': None,
    'landing_gear_loc': None,
    'avionics_loc': None,
    'tail_surfaces_loc': None,
    'x_cg': None,
    'y_cg': None,
    'z_cg': None
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
    tail_surfaces_loc = design_elements['tail_surfaces_loc']
    vert_tail_avchord = design_elements['vert_tail_avchord']
    fuse_length = design_elements['fuse_length']
    fuse_loc = design_elements['fuse_loc']
    pilot_mass = design_elements['pilot_mass']
    pilot_loc = design_elements['pilot_loc']
    battery_mass = design_elements['battery_mass']
    battery_loc = design_elements['battery_loc']
    tail_motor_loc = design_elements['tail_motor_loc']
    x_cg = design_elements['x_cg']
    y_cg = design_elements['y_cg']
    z_cg = design_elements['z_cg']
    tail_motor_z_loc = design_elements['tail_motor_z_loc']
    landing_gear_mass = design_elements['landing_gear_mass']
    landing_gear_z_loc = design_elements['landing_gear_z_loc']
    avionics_mass = design_elements['avionics_mass']
    avionics_z_loc = design_elements['avionics_z_loc']
    batteries_z_loc = design_elements['batteries_z_loc']
    wing_z_loc = design_elements['wing_z_loc']
    tail_surfaces_z_loc = design_elements['tail_surfaces_z_loc']
    fuse_z_loc = design_elements['fuse_z_loc']
    pilot_z_loc = design_elements['pilot_z_loc']
    battery_z_loc = design_elements['battery_z_loc']
    primary_motor_loc = design_elements['primary_motor_loc']
    primary_motor_z_loc = design_elements['primary_motor_z_loc']
    landing_gear_loc = design_elements['landing_gear_loc']
    avionics_loc = design_elements['avionics_loc']


    # Each term will take the following form Icenter + Mass[(z_cg-z_pos)^2] Y positions haven't been added
    I_xx = ( #Roll TODO roll doesnt care about x direction offset - only y and z
        (1/12)*wing_mass*b**2 + wing_mass*(z_cg-wing_z_loc)**2 #main wing
        + (1/12)*horiz_tail_mass*b_htail**2 + horiz_tail_mass*(z_cg-tail_surfaces_z_loc)**2 #horiz T-tail
        + (1/12)*vert_tail_mass*b_vtail**2 + vert_tail_mass*(z_cg-tail_surfaces_z_loc)**2 #vert tail
        + (1/2)*fuse_mass*fuse_radius**2 + fuse_mass*(z_cg-fuse_z_loc)**2#fuse
        + 2*(motor_mass/2)*(fuse_radius+b/2)**2 #Primary motors
        + tail_motor_mass*tail_motor_z_loc**2 #tail motor
        + (2/5)*pilot_mass*0.836 + pilot_mass*(z_cg-pilot_z_loc)**2 #pilot as a sphere
        + landing_gear_mass*(z_cg-landing_gear_z_loc)**2 #landing gear
        + avionics_mass*(z_cg-avionics_z_loc)**2 #avionics
        + battery_mass*(z_cg-batteries_z_loc)**2 #bateries
    )

    # Each term will take the following form Icenter + Mass[(x_cg-x_pos)^2 + (z_cg-z_pos)^2]
    I_yy = ( #Pitch #TODO pitch doesnt care about y direction offset - only x and z
        (1/12)*wing_mass*((c_r+c_t)/2)**2 + wing_mass*((x_cg-wing_loc**2)+(z_cg-wing_z_loc)**2) #main wing
        + (1/12)*horiz_tail_mass*horiz_tail_avchord**2 + horiz_tail_mass*((x_cg-tail_surfaces_loc)**2+(z_cg-tail_surfaces_z_loc)**2) #horiz T-tail
        + (1/12)*vert_tail_mass*vert_tail_avchord**2 + vert_tail_mass*((x_cg-tail_surfaces_loc)**2+(z_cg-tail_surfaces_z_loc)**2) #vert tail
        + (1/2)*fuse_mass*fuse_length**2 + fuse_mass*((x_cg-fuse_loc)**2+(z_cg-fuse_z_loc)**2) #fuse
        + (2/5)*pilot_mass*0.836 + pilot_mass*((x_cg-pilot_loc)**2+(z_cg-pilot_z_loc)**2) #pilot
        + battery_mass*((x_cg-battery_loc)**2+(z_cg-battery_z_loc)**2) #batteries
        + tail_motor_mass*((x_cg-tail_motor_loc)**2+(z_cg-tail_motor_z_loc)**2) #tail motor
        + motor_mass*((x_cg-primary_motor_loc)**2+(z_cg-primary_motor_z_loc)**2) #primary motors
        + landing_gear_mass*((x_cg-landing_gear_loc)**2+(z_cg-landing_gear_z_loc)**2) #landing gear
    )

    # Each term will take the following form Icenter + Mass[(x_cg-x_pos)^2] Y positions haven't been added
    I_zz = ( #Yaw TODO Yaw doesn't care about z direction offset - only x and y
        (1/12)*wing_mass*b**2 + wing_mass*(x_cg-wing_loc)**2 #main wing
        + (1/12)*horiz_tail_mass*b_htail**2 + horiz_tail_mass*(x_cg-tail_surfaces_loc)**2#horiz T-tail
        + (1/12)*vert_tail_mass*vert_tail_avchord**2 + vert_tail_mass*(x_cg-tail_surfaces_loc)**2 #vert tail
        + (1/2)*fuse_mass*fuse_length**2 + fuse_mass*(x_cg-fuse_loc)**2  #fuse
        + 2*(motor_mass/2)*(x_cg-primary_motor_loc)**2 + 2*(motor_mass/2)*(fuse_radius+b/2)**2  # primary motors at half span
        + (2/5)*pilot_mass*0.836 + pilot_mass*(x_cg-pilot_loc)**2 #pilot
        + battery_mass*(battery_loc-x_cg)**2  # batteries
        + tail_motor_mass*(tail_motor_loc-x_cg)**2  # tail motor
        + avionics_mass*(x_cg-avionics_loc)**2  # avionics
    )
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
    # print(create_mass_props(design_elements))
    print(get_inertia_moments(design_elements))
