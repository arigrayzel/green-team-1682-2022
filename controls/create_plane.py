import extract_geometry
import aerosandbox as asb
import aerosandbox.numpy as np
from aerosandbox.tools import units as u

design_elements = {
    'b': None,
    'c_t': None,
    'c_r': None,
    'b_htail': None,
    'c_htail': None,
    'b_vtail': None,
    'c_vtail': None,
    'le_tail': None,
    'tip_to_le': None,
    'fuse_width': None,
}

def create_plane():
    extract_geometry.get_values(design_elements)
    b = design_elements['b']
    c_t = design_elements['c_t']
    c_r = design_elements['c_r']

    le_tail = design_elements['le_tail']
    b_htail = design_elements['b_htail']
    c_htail = design_elements['c_htail']

    b_vtail = design_elements['b_vtail']
    c_vtail = design_elements['c_vtail']

    tip_to_le = design_elements['tip_to_le']
    fuse_width = design_elements['fuse_width']


    def ft(feet, inches=0):  # Converts feet (and inches) to meters
        return feet * u.foot + inches * u.inch


    naca0015 = asb.Airfoil("naca0015")
    naca0015.generate_polars(cache_filename="assets/naca0015.json")
    # naca0015.generate_polars()

    airplane = asb.Airplane(
        name="Vortex",
        wings=[
            asb.Wing(
                name="Wing",
                xsecs=[
                    asb.WingXSec(
                        xyz_le=[0, 0, 0],
                        chord=c_r,
                        airfoil=naca0015
                    ),
                    asb.WingXSec(
                        xyz_le=[0, b/2, 0],
                        chord=c_t,
                        airfoil=naca0015
                    ),
                ],
                symmetric=True
            ),
            asb.Wing(
                name="Horizontal Stabilizer",
                xsecs=[
                    asb.WingXSec(
                        xyz_le=[le_tail, 0, 0],
                        chord=c_htail,
                        airfoil=naca0015,
                    ),
                    asb.WingXSec(
                        xyz_le=[le_tail, b_htail/2, 0],
                        chord=c_htail,
                        airfoil=naca0015,
                    )
                ],
                symmetric=True
            ),
            asb.Wing(
                name="Vertical Stabilizer",
                xsecs=[
                    asb.WingXSec(
                        xyz_le=[le_tail, 0, 0],
                        chord=c_vtail,
                        airfoil=naca0015,
                    ),
                    asb.WingXSec(
                        xyz_le=[le_tail, 0, b_vtail],
                        chord=c_vtail,
                        airfoil=naca0015,
                    ),
                ]
            )
        ],
        fuselages=[
            asb.Fuselage(
                xsecs=[
                    asb.FuselageXSec(
                        xyz_c=[-tip_to_le, 0, 0],
                        radius=0,
                    ),
                    asb.FuselageXSec(
                        xyz_c=[0, 0, 0],
                        radius=fuse_width/2,
                    ),
                    asb.FuselageXSec(
                        xyz_c=[c_r, 0, 0],
                        radius=fuse_width/2,
                    ),
                    asb.FuselageXSec(
                        xyz_c=[le_tail + c_htail, 0, 0],
                        radius=fuse_width/2,
                    ),
                ]
            )
        ]
    )
    return airplane

if __name__=="__main__":
    vlm = asb.VortexLatticeMethod(
        airplane=airplane,
        op_point=asb.OperatingPoint(
            velocity=25,  # m/s
            alpha=5,  # degree
        )
    )

    aero = vlm.run()  # Returns a dictionary
    for k, v in aero.items():
        print(f"{k.rjust(4)} : {v}")

    vlm.draw(show_kwargs=dict(jupyter_backend="static"))
