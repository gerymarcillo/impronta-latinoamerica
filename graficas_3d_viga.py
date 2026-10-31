# ============================================================
# GRÁFICAS 3D: MOMENTO–ROTACIÓN–CARGA E INDICADORES DEL MODELO
# Proyecto UNESUM-REZ-2026-JIPIJAPA-001
# Caso: Viga del Colegio Alejo Lascano (Jipijapa, Manabí)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# ============================================================
# FASE 1 — DATOS DE ENTRADA
# ============================================================
L1, EI1, q1 = 4.0, 1200.0, 5.0
L2, EI2, q2 = 5.0, 1500.0, 8.0

# ============================================================
# FASE 2 — CÁLCULO ESTRUCTURAL
# ============================================================
def calculo_estructural(L, EI, q):
    RA = q * L / 2
    M_max = q * L**2 / 8
    theta = q * L**3 / (24 * EI)
    K = 4 * EI / L
    M_k = K * theta
    IP = M_k / M_max
    IR = max(0, min(1, 1 - (theta / 0.1)))
    return {
        'RA': RA, 'M_max': M_max, 'theta': theta,
        'K': K, 'M_k': M_k, 'IP': IP, 'IR': IR
    }

res1 = calculo_estructural(L1, EI1, q1)
res2 = calculo_estructural(L2, EI2, q2)

# ============================================================
# FASE 3 — GRÁFICAS 3D
# ============================================================
fig = plt.figure(figsize=(18, 14))
fig.patch.set_facecolor('#F5F5F5')

# --- Subplot 3D 1 ---
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.set_facecolor('#FFFFFF')
q_range = np.linspace(0, 15, 40)
L_range = np.linspace(3, 7, 40)
Q, Lg = np.meshgrid(q_range, L_range)
Theta = Q * Lg**3 / (24 * 1200.0)
M = Q * Lg**2 / 8
surf1 = ax1.plot_surface(Theta, Lg, M, cmap='viridis',
                         edgecolor='none', alpha=0.9)
ax1.set_xlabel('θ (rad)', fontsize=9, fontweight='bold')
ax1.set_ylabel('L (m)', fontsize=9, fontweight='bold')
ax1.set_zlabel('M (kN·m)', fontsize=9, fontweight='bold')
ax1.set_title('Ejercicio 1: M–θ–L (EI=1200)',
              fontsize=11, fontweight='bold', color='#1A1A2E')
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=10, label='M (kN·m)')

# --- Subplot 3D 2 ---
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
ax2.set_facecolor('#FFFFFF')
Q2, Lg2 = np.meshgrid(q_range, L_range)
Theta2 = Q2 * Lg2**3 / (24 * 1500.0)
M2 = Q2 * Lg2**2 / 8
surf2 = ax2.plot_surface(Theta2, Lg2, M2, cmap='plasma',
                         edgecolor='none', alpha=0.9)
ax2.set_xlabel('θ (rad)', fontsize=9, fontweight='bold')
ax2.set_ylabel('L (m)', fontsize=9, fontweight='bold')
ax2.set_zlabel('M (kN·m)', fontsize=9, fontweight='bold')
ax2.set_title('Ejercicio 2: M–θ–L (EI=1500)',
              fontsize=11, fontweight='bold', color='#1A1A2E')
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=10, label='M (kN·m)')

# --- Subplot 3D 3 ---
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
ax3.set_facecolor('#FFFFFF')
indicadores = ['IP', 'IR', 'AT/100', 'ITT']
valores1 = [res1['IP'], res1['IR'], 1.0, 1.0]
valores2 = [res2['IP'], res2['IR'], 1.0, 1.0]
xpos = np.arange(len(indicadores))
ax3.bar3d(xpos - 0.2, np.zeros(len(indicadores)), 0,
          0.35, 0.35, valores1, color='#B71C1C', alpha=0.9, label='E1')
ax3.bar3d(xpos + 0.2, np.ones(len(indicadores))*1.5, 0,
          0.35, 0.35, valores2, color='#0D47A1', alpha=0.9, label='E2')
ax3.set_xticks(xpos + 0.1)
ax3.set_xticklabels(indicadores, fontsize=9)
ax3.set_ylabel('Ejercicio', fontsize=9, fontweight='bold')
ax3.set_zlabel('Valor', fontsize=9, fontweight='bold')
ax3.set_title('Indicadores del modelo (3D)',
              fontsize=11, fontweight='bold', color='#1A1A2E')
ax3.legend(fontsize=8)
ax3.set_yticks([0, 1.5])
ax3.set_yticklabels(['E1', 'E2'], fontsize=8)

# --- Subplot 3D 4 ---
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
ax4.set_facecolor('#FFFFFF')
L_freq = np.linspace(3, 7, 30)
EI_freq = np.linspace(800, 2000, 30)
Lf, EIf = np.meshgrid(L_freq, EI_freq)
m_sup = 0.36
F = (1.57 / Lf**2) * np.sqrt(EIf / m_sup)
surf4 = ax4.plot_surface(Lf, EIf, F, cmap='coolwarm',
                         edgecolor='none', alpha=0.9)
ax4.set_xlabel('L (m)', fontsize=9, fontweight='bold')
ax4.set_ylabel('EI (kN·m²)', fontsize=9, fontweight='bold')
ax4.set_zlabel('f (Hz)', fontsize=9, fontweight='bold')
ax4.set_title('Frecuencia natural f(L, EI)',
              fontsize=11, fontweight='bold', color='#1A1A2E')
fig.colorbar(surf4, ax=ax4, shrink=0.5, aspect=10, label='f (Hz)')

# ============================================================
# AJUSTE MANUAL (reemplaza tight_layout)
# ============================================================
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05,
                    wspace=0.25, hspace=0.30)

plt.savefig('graficas_3d_viga_unesum.png', dpi=200,
            bbox_inches='tight', facecolor='#F5F5F5')
plt.show()
print("\n✅ Imagen guardada: graficas_3d_viga_unesum.png")

# ============================================================
# REPORTE
# ============================================================
print("\n" + "=" * 70)
print("REPORTE 3D — VIGA COLEGIO ALEJO LASCANO")
print("Proyecto UNESUM-REZ-2026-JIPIJAPA-001")
print("=" * 70)

for nombre, res in [("Ejercicio 1", res1), ("Ejercicio 2", res2)]:
    print(f"\n--- {nombre} ---")
    print(f"  M_max     = {res['M_max']:.2f} kN·m")
    print(f"  M_k       = {res['M_k']:.4f} kN·m")
    print(f"  θ         = {res['theta']:.6f} rad")
    print(f"  IP        = {res['IP']:.4f}")
    print(f"  IR        = {res['IR']:.4f}")

print("\n" + "=" * 70)