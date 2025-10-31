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
from scipy.optimize import least_squares, minimize


def thermal_conductivity_integral(k_fun, T1, T2):
    """ Returns the thermal conductivity integral (\theta) in W/m.  Compute
    heat flow by calculating \theta *(Cross sectional area)/(Length) """
    T = np.linspace(T1,T2,100000)
    dT = T[1]-T[0]
    return np.sum(k_fun(T)*dT)

def calculate_thermal_transfer(material_k_fun, area, length, T1, T2):
    if T1 == T2:
        k = material_k_fun(np.array([T1]))[0]
        thermal_conductance = k*area/length
        power_transmission = 0
    else:
        theta = thermal_conductivity_integral(material_k_fun, T1, T2)
        power_transmission = abs(theta*area/length)
        thermal_conductance = abs(power_transmission/(T1-T2))
    thermal_resistance = 1/thermal_conductance

    return power_transmission, thermal_conductance, thermal_resistance

def calculate_temperature_rise(material_k_fun, area, length, T1, heat_load):
    """ Calculate the temperature rise across a material of given thermal conductivity
    cross-sectional area, and length, given a heat load. """
    

    # Objective function: minimize the squared difference between power_transmission and heat_load
    def objective(T2_array):
        T2 = T2_array[0]
        power_transmission, _, _ = calculate_thermal_transfer(material_k_fun, area, length, T1, T2)
        return (power_transmission - heat_load)**2
    
    # Initial guess: assume some temperature rise
    T2_guess = [T1 + 0.1]  # Start with 10K rise as initial guess
    
    # Use minimize to find T2 with bounds ensuring T2 > T1
    bounds = [(T1, None)]  # T2 must be > 0
    result = minimize(objective, T2_guess, method='Nelder-Mead', bounds=bounds)
    
    T2 = result.x[0]
    power_transmission, thermal_conductance, thermal_resistance = calculate_thermal_transfer(
        material_k_fun, area, length, T1, T2
    )
    if abs(power_transmission - heat_load) > 0.1:
        print(f'Warning: Power transmission error = {abs(power_transmission - heat_load):0.3f} W')


    return T2, thermal_conductance, thermal_resistance


### Multilayer insulation

def _multilayer_insulation_balance_eqns(x, T1, T2, emissivity_first, emissivity_mylar, emissivity_last, area):
    """ Sets up equations of the form σEA(T_2^4 - T_1^4) - qdot = 0 for nonlinear solving """

    T = np.concatenate([[T1], x[:-1], [T2]])
    eps = [emissivity_first] + [emissivity_mylar]*(len(T)-2) + [emissivity_last]
    qdot = x[-1]
    eqns = []
    for n in range(len(T)-1):
        sigma = 5.67e-8 # Stefan-Boltzmann constant
        eps1 = eps[n+1]
        eps2 = eps[n]
        E = eps1*eps2/(eps1+eps2-eps1*eps2)
        A = area
        eqn = sigma*E*A*(T[n+1]**4-T[n]**4) - qdot
        eqns.append(eqn)
    return np.array(eqns)

def solve_multilayer_insulation(T1, T2, N, emissivity_first, emissivity_mylar, emissivity_last, area):

    T_guess = np.linspace(T1, T2, N+2)[1:-1]
    qdot_guess = 0.1
    x0 = np.concatenate([T_guess, [qdot_guess]])

    # Set bounds: temperatures must be positive, qdot can be any value
    lb = np.concatenate([np.full(N, 1e-6), [-np.inf]])  # Lower bound: small positive for temps, any for qdot
    ub = np.concatenate([np.full(N, np.inf), [np.inf]])  # Upper bound: any value for all variables
    
    result = least_squares(_multilayer_insulation_balance_eqns, x0, 
                          args=(T1, T2, emissivity_first, emissivity_mylar, emissivity_last, area),
                          bounds=(lb, ub))
    
    xsolve = result.x
    qdot = xsolve[-1]
    layer_temps = xsolve[:-1]

    return layer_temps, qdot