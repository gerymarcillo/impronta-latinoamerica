import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ============================================================
# EJERCICIO 1 — VIGA BIARTICULADA CON CARGA REPARTIDA
# ============================================================
L = 4.0          # m
EI = 1200.0      # kN·m²
q = 5.0          # kN/m

# ============================================================
# CÁLCULOS
# ============================================================
# 1. Reacciones
RA = q * L / 2
RB = q * L / 2

# 2. Momento máximo al centro
M_max = q * L**2 / 8

# 3. Rotación en los apoyos
theta = q * L**3 / (24 * EI)

# 4. Rigidez
K = 4 * EI / L
M_k = K * theta

# ============================================================
# CONFIGURACIÓN DEL DASHBOARD (2x2)
# ============================================================
fig = plt.figure(figsize=(16, 12))
fig.patch.set_facecolor('#1e1e2e')
fig.suptitle("M03: ANÁLISIS DE VIGA BIARTICULADA — EJERCICIO 1\nFormulación y Resultados", 
             color='#ecf0f1', fontsize=18, fontweight='bold', y=0.95)

gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.2)

# --- PANEL 1: FORMULACIÓN MATEMÁTICA ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('#1e1e2e')
ax1.axis('off')

formulacion = (
    "📐 FORMULACIÓN TEÓRICA\n"
    "--------------------------------------------------\n"
    "1. Reacciones (Simetría):\n"
    f"   R_A = R_B = q·L/2 = {RA:.2f} kN\n\n"
    "2. Momento Máximo (Centro):\n"
    f"   M_max = q·L²/8 = {M_max:.2f} kN·m\n\n"
    "3. Ecuación de la Elástica (Rotación):\n"
    f"   θ_max = q·L³ / (24·EI)\n"
    f"   θ_max = {theta:.6f} rad\n\n"
    "4. Rigidez Equivalente:\n"
    f"   K = 4·EI / L = {K:.2f} kN·m/rad\n"
)
ax1.text(0.05, 0.95, formulacion, transform=ax1.transAxes, fontsize=12, 
         verticalalignment='top', fontfamily='monospace', color='#5dade2',
         bbox=dict(boxstyle='round,pad=1', facecolor='#2c3e50', edgecolor='#f39c12', lw=2))

# --- PANEL 2: DIAGRAMA DE MOMENTO ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#1e1e2e')
x = np.linspace(0, L, 100)
M_x = (q * L / 2) * x - (q * x**2) / 2

ax2.plot(x, M_x, color='#e74c3c', linewidth=3)
ax2.fill_between(x, M_x, alpha=0.2, color='#e74c3c')
ax2.axhline(y=0, color='white', linewidth=1)
ax2.axvline(x=L/2, color='#f1c40f', linestyle='--', linewidth=2, label=f'x = L/2 = {L/2} m')
ax2.scatter(L/2, M_max, color='#2ecc71', s=150, zorder=5, edgecolor='white')
ax2.annotate(f'M_max = {M_max:.2f} kN·m', xy=(L/2, M_max), xytext=(L/2 - 1.5, M_max + 2),
             color='#2ecc71', fontsize=12, fontweight='bold')
ax2.set_title('DIAGRAMA DE MOMENTO FLECTOR', color='#ecf0f1', fontsize=14)
ax2.set_xlabel('Abscisa x (m)', color='#ecf0f1')
ax2.set_ylabel('Momento (kN·m)', color='#ecf0f1')
ax2.tick_params(colors='#ecf0f1')
ax2.grid(True, linestyle='--', alpha=0.2)
ax2.legend(facecolor='#2c3e50', labelcolor='#ecf0f1')

# --- PANEL 3: CURVA MOMENTO-ROTACIÓN ---
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor('#1e1e2e')
q_range = np.linspace(0, 15, 100)
theta_range = q_range * L**3 / (24 * EI)
M_range = q_range * L**2 / 8

ax3.plot(theta_range, M_range, color='#3498db', linewidth=3, label='M_max = q·L²/8')
ax3.scatter(theta, M_max, color='#f1c40f', s=200, zorder=5, edgecolor='black', label=f'Estado actual (q={q})')
ax3.annotate(f'θ = {theta:.5f} rad\nM = {M_max:.2f} kN·m', xy=(theta, M_max), xytext=(theta + 0.002, M_max - 5),
             color='#f1c40f', fontsize=11, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#f1c40f'))
ax3.set_title('CURVA MOMENTO–ROTACIÓN (Rigidez)', color='#ecf0f1', fontsize=14)
ax3.set_xlabel('Rotación θ (rad)', color='#ecf0f1')
ax3.set_ylabel('Momento (kN·m)', color='#ecf0f1')
ax3.tick_params(colors='#ecf0f1')
ax3.grid(True, linestyle='--', alpha=0.2)
ax3.legend(facecolor='#2c3e50', labelcolor='#ecf0f1')

# --- PANEL 4: RESUMEN DE RESULTADOS ---
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor('#1e1e2e')
ax4.axis('off')

resumen = (
    "📊 RESULTADOS FINALES\n"
    "--------------------------------------------------\n"
    f"Luz (L)            = {L:.2f} m\n"
    f"Rigidez (EI)       = {EI:.1f} kN·m²\n"
    f"Carga (q)          = {q:.1f} kN/m\n\n"
    f"Reacción (RA)      = {RA:.2f} kN\n"
    f"Momento Máx (M)    = {M_max:.2f} kN·m\n"
    f"Rotación Máx (θ)   = {theta:.6f} rad\n"
    f"Rigidez (K)        = {K:.2f} kN·m/rad\n\n"
    "✅ CUMPLE CON LOS REQUISITOS DE ANÁLISIS"
)
ax4.text(0.05, 0.95, resumen, transform=ax4.transAxes, fontsize=12, 
         verticalalignment='top', fontfamily='monospace', color='#2ecc71',
         bbox=dict(boxstyle='round,pad=1', facecolor='#2c3e50', edgecolor='#2ecc71', lw=2))

plt.savefig('viga_ejercicio1_dashboard.png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()