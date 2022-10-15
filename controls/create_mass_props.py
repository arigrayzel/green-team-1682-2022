import extract_geometry
import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u

design_elements = {
    'b': None,
    'plane_mass': None,
    'wing_mass': None,
    'fuse_mass': None,
    'fuse_radius': None,
    'x_cg':None,
    'y_cg': None,
    'z_cg': None,
    'c_t': None,
    'c_r': None,
    'fuse_length': None
}

def get_inertia_moments(design_elts=design_elements):
    '''
    :param design_elts: dictionary of items we want to query from master value sheet
    :return: Principal-axis moments of inertia
    '''
    b = design_elts['b']
    wing_mass = design_elts['wing_mass']
    fuse_mass = design_elts['fuse_mass']
    fuse_radius = design_elts['fuse_radius']
    c_t = design_elts['c_t']
    c_r = design_elts['c_r']
    x_cg = design_elts['x_cg']
    fuse_length = design_elts['fuse_length']

    I_xx = 0.5 * fuse_mass * fuse_radius ** 2 + (1 / 12) * wing_mass * b ** 2

    I_yy = (1/12) * wing_mass * ((c_t+c_r)/2)**2 + wing_mass * ((c_r/2)-x_cg)**2 + (fuse_mass * fuse_radius**2)/4 \
           + (fuse_mass * fuse_length**2)/12 + fuse_mass * ((fuse_length/2-1) - x_cg)**2

    I_zz = (fuse_mass * fuse_radius**2)/4 + (fuse_mass * fuse_length**2)/12 + fuse_mass * ((fuse_length/2-1) - x_cg)**2 \
           + (wing_mass * (((c_t+c_r)/2)**2 + b**2))/12 + wing_mass * ((c_r/2)-x_cg)**2

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
        Ixy= 0,
        Iyz=0,
        Ixz=0,
    )

    return mass_props


if __name__=="__main__":
    print(create_mass_props(design_elements))
