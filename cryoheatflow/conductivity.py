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


def _valid_temperatures(T, T_min, T_max):
    if np.isscalar(T):
        if T < T_min or T > T_max:
            return np.nan
        else:
            return T
    else:
        return np.where((T >= T_min) & (T <= T_max), T, np.nan)


def k_ss(T):
    """ Stainless steel (316/314/304L) cryogenic thermal conductivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 1, T_max = 300)
    a,b,c,d,e,f,g,h,i = [-1.4087,1.3982,0.2543,-0.626,0.2334,0.4256,-0.4658,0.165,-0.0199]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_cuni(T):
    """ 70-30 CuNi cupronickel -- approximated as 2x more conductive than SS from
     Kushino, A., Ohkubo, M., & Fujioka, K. (2005).  Cryogenics, 45(9), 637–640.
    https://doi.org/10.1016/j.cryogenics.2005.07.002 """
    return k_ss(T)*2

def k_al6061(T):
    """ Aluminum 6061-T6 cryogenic thermal conductivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 1, T_max = 300)
    a,b,c,d,e,f,g,h,i = [0.07918,1.0957,-0.07277,0.08084,0.02803,-0.09464,0.04179,-0.00571,0]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_al6063(T):
    """ Aluminum 6063-T5 cryogenic thermal conductivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [22.401433,-141.13433,394.95461,-601.15377,547.83202,-305.99691,102.38656,-18.810237,1.4576882,]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_al1100(T):
    """ Aluminum 1100 cryogenic thermal conductivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [23.39172, -148.5733, 422.1917, -653.6664, 607.0402, -346.152, 118.4276, -22.2781, 1.770187]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_brass(T):
    """ Brass (UNS C26000) cryogenic thermal conductivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 5, T_max = 110)
    a,b,c,d,e,f,g,h,i = [0.021035,-1.01835,4.54083,-5.03374,3.20536,-1.12933,0.174057,-0.0038151,0]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_becu(T):
    """ Beryllium copper cryogenic thermal conducitivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 120)
    a,b,c,d,e,f,g,h,i = [-0.50015,1.9319,-1.6954,0.71218,1.2788,-1.6145,0.68722,-0.10501,0]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_cu_rrr50(T):
    """ Copper (RRR=50, typically ETP or OFHC) thermal conducitivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [1.8743,-0.41538,-0.6018,0.13294,0.26426,-0.0219,-0.051276,0.0014871,0.003723]
    k = 10**((a+c*T**0.5+e*T+g*T**1.5+i*T**2)/(1+b*T**0.5+d*T+f*T**1.5+h*T**2))
    return k

def k_cu_rrr100(T):
    """ Copper (RRR=100) thermal conducitivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [2.2154,-0.47461,-0.88068,0.13871,0.29505,-0.02043,-0.04831,0.001281,0.003207]
    k = 10**((a+c*T**0.5+e*T+g*T**1.5+i*T**2)/(1+b*T**0.5+d*T+f*T**1.5+h*T**2))
    return k

def k_g10(T):
    """ Fiberglass-epoxy (G-10) thermal conducitivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [-4.1236,13.788,-26.068,26.272,-14.663,4.4954,-0.6905,0.0397,0]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k

def k_nylon(T):
    """ Nylon (polyamide) thermal conducitivity reference data
    from https://trc.nist.gov/cryogenics/materials/materialproperties.htm """
    T = _valid_temperatures(T, T_min = 4, T_max = 300)
    a,b,c,d,e,f,g,h,i = [-2.6135, 2.3239 , -4.7586, 7.1602 , -4.9155, 1.6324 , -0.2507, 0.0131, 0]
    k = 10**(a+b*np.log10(T)**1+c*np.log10(T)**2+d*np.log10(T)**3+e*np.log10(T)**4 + 
                  f*np.log10(T)**5+g*np.log10(T)**6+h*np.log10(T)**7+i*np.log10(T)**8)
    return k




### Thermal boundary conductance
def h_grease(T, area):
    """ The thermal conductance `h` (W/K) of grease for a given area of contact (in cm^2). Ekin p63 """
    T_pts = [3.65E-01, 8.52E-01, 2.70E+00, 5.73E+00, 1.06E+01, 1.93E+01, 3.53E+01, 1.38E+02, 2.96E+02]
    h_pts = [1.42E-03, 7.39E-03, 4.84E-02, 1.38E-01, 2.67E-01, 4.33E-01, 6.50E-01, 1.33E+00, 1.89E+00]
    h = np.interp(T,T_pts,h_pts)*area/1e-4 # Convert to m^2 from cm^2
    return h

def h_solder_pb_sn(T, area):
    """ The thermal conductance `h` (W/K) of PbSn solder for a given area of contact (in m^2). Ekin p63 """
    T_pts = [2.75E+00, 4.37E+00, 1.13E+01, 2.17E+01, 3.41E+01, 5.52E+01, 1.05E+02, 2.10E+02, 2.88E+02]
    h_pts = [7.03E-01, 1.36E+00, 4.98E+00, 8.90E+00, 1.12E+01, 1.34E+01, 1.47E+01, 1.50E+01, 1.47E+01]
    h = np.interp(T,T_pts,h_pts)*area/1e-4 # Convert to m^2 from cm^2
    return h