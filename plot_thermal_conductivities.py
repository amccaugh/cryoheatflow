#%%
from cryoheatflow.conductivity import ( k_ss, k_cuni, k_al6061, k_al6063, k_brass,
     k_cu_rrr50, k_al1100, k_becu, k_cu_rrr100, k_g10, k_nylon)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("husl")

# Plot thermal conductivity vs temperature for all materials
k_funcs = [k_cu_rrr100, k_cu_rrr50, k_al1100, k_brass, k_becu, k_cuni, k_ss, k_g10, k_nylon]

labels = ['Cu (RRR=100)', 'Cu (RRR=50)', 'Al 1100', 'Brass', 'BeCu', 'CuNi', 'SS', 'G10', 'Nylon']

# Define unique line styles
linestyles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-']

fig, ax = plt.subplots(figsize=(10, 6))

for i, k_fun in enumerate(k_funcs):
    T = np.linspace(1, 300, 1000)
    k = k_fun(T)
    ax.loglog(T, k, linestyle=linestyles[i])

# Customize x-axis ticks
ax.set_xscale('log')
ax.set_xticks([1, 4, 10, 30, 100, 300])
ax.set_xticklabels(['1K', '4K', '10K', '30K', '100K', '300K'])

# Add minor grid lines
ax.grid(True, which='minor', alpha=0.3)
ax.grid(True, which='major', alpha=0.7)

ax.set_xlabel('Temperature (K)')
ax.set_ylabel('Thermal conductivity (W/m·K)')
ax.legend(labels, loc='center right', bbox_to_anchor=(1.15, 0.5))

plt.tight_layout()
plt.show()