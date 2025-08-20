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
k_funcs = [k_cu_rrr100, k_cu_rrr50, k_al1100, k_al6063, k_al6061,  k_brass, 
           k_becu, k_cuni, k_ss, k_g10, k_nylon]

labels = ['Cu (RRR=100)', 'Cu (RRR=50)', 'Al 1100', 'Al 6063-T5', 'Al 6061-T6', 
          'Brass', 'BeCu', 'CuNi', 'SS', 'G10', 'Nylon']

# Define unique line styles
linestyles = ['-', '--', '-.', ':', '-']*3

# # Sort k_funcs and labels by value at T=300
# k_at_300 = [k_fun(300) for k_fun in k_funcs]
# sorted_indices = np.argsort(k_at_300)
# k_funcs = [k_funcs[i] for i in sorted_indices]
# labels = [labels[i] for i in sorted_indices]
# linestyles = [linestyles[i] for i in sorted_indices]


fig, ax = plt.subplots(figsize=(10, 6))

for i, k_fun in enumerate(k_funcs):
    T = np.linspace(1, 300, 1000)
    k = k_fun(T)
    line = ax.loglog(T, k, linestyle=linestyles[i])
    
    # Add label at x=4K
    k_at_4K = k_fun(4.2)
    ax.text(4.2, k_at_4K, f'{labels[i]}  ', 
            verticalalignment='center', 
            horizontalalignment='right',
            fontsize=12,
            color=line[0].get_color())

# Customize x-axis ticks
ax.set_xscale('log')
ax.set_xticks([1, 4, 10, 30, 100, 300])
ax.set_xticklabels(['1K', '4K', '10K', '30K', '100K', '300K'])
ax.tick_params(axis='both', which='major', labelsize=14)

# Add minor grid lines
ax.grid(True, which='minor', alpha=0.3)
ax.grid(True, which='major', alpha=0.7)

ax.set_xlabel('Temperature (K)', fontsize=14)
ax.set_ylabel('Thermal conductivity (W/m·K)', fontsize=14)
ax.legend(labels, loc='center right', bbox_to_anchor=(1.25, 0.5), fontsize=11)

plt.tight_layout()
plt.show()