#%% Calculate thermal conductivity in W/m*K for a specific material at a specific temperature
import cryoheatflow

k_conductivity_function = cryoheatflow.conductivity.k_ss
T = 10
result = k_conductivity_function(T)
print(f'Thermal conductivity = {result} W/m*K')


#%% Calculate thermal power transfer through a copper wire (22 gauge) of medium purity (RRR = 50)
import cryoheatflow

k = cryoheatflow.conductivity.k_g10
area = 0.8e-3*5e-3*8
length = 11e-3 # 30 mm
T1 = 80 # 60 K 
T2 = 4 # 4 K

P, G, R = cryoheatflow.calculate_thermal_transfer(k, area, length, T1, T2)
print(f'Power transmission = {P*1e3:0.3f} mW')
print(f'Thermal conductance = {G:0.6f} W/K')
print(f'Thermal resistance = {R:0.3f} K/W')



#%% Calculate thermal power transfer through a copper wire (22 gauge) of medium purity (RRR = 50)
import cryoheatflow

k = cryoheatflow.conductivity.k_al6061
area = 0.8e-3*15e-3
length = 100e-3 # 30 mm
T1 = 60 # 60 K 
T2 = 60 # 4 K

P, G, R = cryoheatflow.calculate_thermal_transfer(k, area, length, T1, T2)
print(f'Power transmission = {P*1e3:0.3f} mW')
print(f'Thermal conductance = {G:0.6f} W/K')
print(f'Thermal resistance = {R:0.3f} K/W')



#%% Calculate thermal power transfer through a copper wire (22 gauge) of medium purity (RRR = 50)
import cryoheatflow

k = cryoheatflow.conductivity.k_cu_rrr50
area = 1.5e-6
length = 200e-3 # 30 mm
T1 = 60 # 60 K 
T2 = 60 # 4 K

P, G, R = cryoheatflow.calculate_thermal_transfer(k, area, length, T1, T2)
print(f'Power transmission = {P*1e3:0.3f} mW')
print(f'Thermal conductance = {G:0.6f} W/K')
print(f'Thermal resistance = {R:0.3f} K/W')


#%% Calculate thermal boundary conductance across a solder joint
import cryoheatflow

T = 15
area_m2 = 3e-3 * 10e-3 # 3 mm x 10 mm

h = cryoheatflow.conductivity.h_solder_pb_sn(T = T, area = area_m2)
print(f'Thermal conductance = {h:0.3f} W/K')
print(f'Thermal resistance = {1/h:0.3f} K/W')


#%% Calculate temperature rise across due to heat load

# Assume you have a 4mm thick x 2mm wide x 100 mm long strip of aluminum 6061-T6 that's attached to a 40K coldhead at one end.
# If the other end of the strip has 250 mW of heat load applied to it, what will the temperature be at the hot end?
import cryoheatflow

k = cryoheatflow.conductivity.k_al6061
area = 4e-3 * 2e-3 # 4 mm x 2 mm
length = 100e-3 # 100 mm
T1 = 40 # 40 K 
heat_load = .25 # 250 mW
T2, thermal_conductance, thermal_resistance = cryoheatflow.calculate_temperature_rise(k, area, length, T1, heat_load)
print(f'Temperature at cold end = {T1:0.3f} K')
print(f'Temperature at hot end = {T2:0.3f} K')
print(f'Thermal conductance = {thermal_conductance:0.3f} W/K')
print(f'Thermal resistance = {thermal_resistance:0.3f} K/W') 



#%% Plotting curves
from cryoheatflow.conductivity import k_ss, k_cuni, k_al6061, k_al6063, k_al1100, k_becu, k_brass, k_cu_rrr50, k_cu_rrr100, k_g10, k_nylon
import matplotlib.pyplot as plt
import numpy as np


for k_fun in [k_ss, k_cuni, k_al6061, k_al6063, k_al1100, k_becu, k_brass, k_cu_rrr50, k_cu_rrr100, k_g10, k_nylon]:
    T = np.linspace(4,300,1000)
    k = k_fun(T)
    plt.loglog(T,k)
plt.xlabel('Temperature (K)')
plt.ylabel('Thermal conductivity (W/m*K)')
plt.legend(['SS', 'CuNi', 'Al 6061-T6', 'Al 6063-T5', 'Al 1100', 'BeCu', 'Brass', 'Cu (RRR=50)', 'Cu (RRR=100)', 'G10', 'Nylon'], loc='lower right')




#%% Computing effectiveness of multilayer insulation
from cryoheatflow import solve_multilayer_insulation
from cryoheatflow.emissivity import Al_polished, Al_oxidized, Cu_polished, Cu_oxidized
from cryoheatflow.emissivity import brass_polished, brass_oxidized, stainless, mylar


T1 = 4
T2 = 85
N = 2 # Number of mylar layers
emissivity1 = Al_oxidized # Emissivity of the first layer (e.g. 300K walls)
emissivity_mylar = mylar # Emissivity of the multilayer mylar layers
emissivity2 =Al_polished # Emissivity of the last layer (e.g. 40K walls)
area = (20e-2)**2 # In m^2


layer_temps, qdot = solve_multilayer_insulation(T1, T2, N, emissivity1, emissivity_mylar, emissivity2, area)
print(f'Layer temperatures : {layer_temps}')
print(f'Thermal power : {abs(qdot)}')

# %%
