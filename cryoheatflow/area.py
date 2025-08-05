import numpy as np

### Cross-section-area measurements in meters, returns m^2
def tube_area(diameter, wall_thickness):
    area= np.pi*(diameter/2)**2 - np.pi*(diameter/2-wall_thickness)**2
    return area

def cylinder_area(diameter):
    area= np.pi*(diameter/2)**2
    return area

def wire_gauge_area(awg):
    d = 0.127e-3*92**((36-awg)/39)
    area = np.pi*(d/2)**2
    return area

def _coax_area(d_inner_conductor, d_insulation, d_outer_conductor):
    area_outer_conductor = np.pi*(d_outer_conductor/2)**2 - np.pi*(d_insulation/2)**2
    area_inner_conductor = np.pi*(d_inner_conductor/2)**2
    area = area_outer_conductor + area_inner_conductor
    return area


in2m = 1/39.37 # Convert inches to meters
coax_141 = _coax_area(.036*in2m, 0.118*in2m, .141*in2m) # 7.5x .047"
coax_085 = _coax_area(.02*in2m,  0.066*in2m, .085*in2m)  # 3.4x .047"
coax_047 = _coax_area(.011*in2m, 0.037*in2m, .047*in2m)
coax_034 = _coax_area(.008*in2m, 0.026*in2m, .034*in2m)
