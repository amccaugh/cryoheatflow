from .thermal import calculate_thermal_transfer, calculate_temperature_rise, solve_multilayer_insulation
from . import area
from . import emissivity
from . import conductivity

# Import commonly used functions at top level
from .conductivity import (
    k_ss, k_cuni, k_al6061, k_al6063, k_al1100, k_becu, k_brass, 
    k_cu_rrr50, k_cu_rrr100, k_g10, k_nylon, h_grease, h_solder_pb_sn
)
from .emissivity import (
    mylar, Al_polished, Al_oxidized, Cu_polished, Cu_oxidized,
    brass_polished, brass_oxidized, stainless
)

# Make modules available as submodules (standard approach)
import sys
sys.modules['cryoheatflow.conductivity'] = conductivity
sys.modules['cryoheatflow.emissivity'] = emissivity
sys.modules['cryoheatflow.area'] = area

# Also make them available at package level
__all__ = [
    'area', 'emissivity', 'conductivity', 'calculate_thermal_transfer', 'calculate_temperature_rise', 'solve_multilayer_insulation',
    'k_ss', 'k_cuni', 'k_al6061', 'k_al6063', 'k_al1100', 'k_becu', 'k_brass', 
    'k_cu_rrr50', 'k_cu_rrr100', 'k_g10', 'k_nylon', 'h_grease', 'h_solder_pb_sn',
    'mylar', 'Al_polished', 'Al_oxidized', 'Cu_polished', 'Cu_oxidized',
    'brass_polished', 'brass_oxidized', 'stainless'
]
