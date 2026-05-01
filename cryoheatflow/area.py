# This file is part of cryoheatflow
# Copyright (C) 2025 by Adam McCaughan

# cryoheatflow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

# SWG diameters in mm (gauges 1–50) per BS 3737
_SWG_DIAMETER_MM = {
     1: 7.620,  2: 7.010,  3: 6.401,  4: 5.893,  5: 5.385,
     6: 4.877,  7: 4.470,  8: 4.064,  9: 3.658, 10: 3.251,
    11: 2.946, 12: 2.642, 13: 2.337, 14: 2.032, 15: 1.829,
    16: 1.626, 17: 1.422, 18: 1.219, 19: 1.016, 20: 0.914,
    21: 0.813, 22: 0.711, 23: 0.610, 24: 0.559, 25: 0.508,
    26: 0.457, 27: 0.4166,28: 0.3759,29: 0.3454,30: 0.3150,
    31: 0.2946,32: 0.2743,33: 0.2540,34: 0.2337,35: 0.2134,
    36: 0.1930,37: 0.1727,38: 0.1524,39: 0.1321,40: 0.1219,
    41: 0.1118,42: 0.1016,43: 0.0914,44: 0.0813,45: 0.0711,
    46: 0.0610,47: 0.0508,48: 0.0406,49: 0.0305,50: 0.0254,
}

def wire_swg_area(swg):
    """ Cross-sectional area (m²) of a solid wire by Standard Wire Gauge (SWG / Imperial).
    Valid for SWG 1–50 per BS 3737. """
    if swg not in _SWG_DIAMETER_MM:
        raise ValueError(f'SWG {swg} is not valid; must be an integer between 1 and 50.')
    d = _SWG_DIAMETER_MM[swg] * 1e-3  # mm → m
    return np.pi * (d / 2) ** 2

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
