import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor('#F5F5F5')
ax.set_facecolor('#FFFFFF')

# Diferentes EI
EI_vals = [800, 1000, 1200, 1500, 2000]
colors = ['#B71C1C', '#E65100', '#F9A825', '#0D47A1', '#00695C']

L = 4.0
q_range = np.linspace(0, 20, 100)

for EI, color in zip(EI_vals, colors):
    theta = q_range * L**3 / (24 * EI)
    M = q_range * L**2 / 8
    ax.plot(theta, M, color=color, linewidth=3,
            label=f'EI = {EI} kN·m²')

ax.set_xlabel('Rotación θ (rad)', fontsize=14, fontweight='bold')
ax.set_ylabel('Momento M_max (kN·m)', fontsize=14, fontweight='bold')
ax.set_title('CURVA MOMENTO–ROTACIÓN\n'
             'Efecto de la rigidez EI (L=4 m)',
             fontsize=15, fontweight='bold', color='#1A1A2E', pad=20)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('curva_momento_rotacion_EI.png', dpi=200,
            bbox_inches='tight', facecolor='#F5F5F5')
plt.show()
print("\n✅ Imagen guardada: curva_momento_rotacion_EI.png")