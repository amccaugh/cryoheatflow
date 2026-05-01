#%%
from cryoheatflow.conductivity import ( k_ss, k_cuni, k_al6061, k_al6063, k_brass,
     k_cu_rrr50, k_al1100, k_becu, k_cu_rrr100, k_g10, k_nylon,
     k_phosphor_bronze, k_nichrome, k_manganin)
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set seaborn style
sns.set_style("whitegrid")
sns.set_palette("husl")

# All materials with their label text
k_funcs = [k_cu_rrr100, k_cu_rrr50, k_al1100, k_al6063, k_al6061, k_brass,
           k_becu, k_phosphor_bronze, k_cuni, k_manganin, k_ss, k_nichrome, k_g10, k_nylon]

labels = ['Cu (RRR=100)', 'Cu (RRR=50)', 'Al 1100', 'Al 6063-T5', 'Al 6061-T6',
          'Brass', 'BeCu', 'Phosphor bronze', 'CuNi', 'Manganin', 'SS', 'Nichrome', 'G10', 'Nylon']

# Sort by value at 4 K so seaborn colors spread naturally across the palette;
# use the first valid temperature for materials that don't reach 4 K (e.g. Brass starts at 5 K)
def k_at_4K_safe(k_fun):
    v = k_fun(4.0)
    return v if np.isfinite(v) else k_fun(10.0)

order = np.argsort([k_at_4K_safe(f) for f in k_funcs])
k_funcs = [k_funcs[i] for i in order]
labels  = [labels[i]  for i in order]

linestyles = ['-', '--', '-.', ':', '-'] * 3


fig, ax = plt.subplots(figsize=(10, 6))

for i, (k_fun, label) in enumerate(zip(k_funcs, labels)):
    T = np.linspace(1, 300, 1000)
    k = k_fun(T)
    line, = ax.loglog(T, k, linestyle=linestyles[i])

    # Place the label at the first valid temperature on the left side of the plot
    label_T_overrides = {'Brass': 30, 'BeCu': 10, 'Manganin': 4, 'Nichrome': 10, 'CuNi': 2, 'SS': 2}
    for T_label in [label_T_overrides.get(label, 4.2), 10, 20]:
        k_label = k_fun(T_label)
        if np.isfinite(k_label):
            break
    ax.text(T_label, k_label, f'{label}  ',
            verticalalignment='center',
            horizontalalignment='right',
            fontsize=12,
            color=line.get_color())

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