import numpy as np
from scipy.optimize import least_squares


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