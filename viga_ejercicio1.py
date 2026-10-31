import numpy as np
import matplotlib.pyplot as plt

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

# 2. Momento máximo
M_max = q * L**2 / 8

# 3. Rotación
theta = q * L**3 / (24 * EI)

# 4. Matriz de rigidez
K11 = 4 * EI / L
K12 = 2 * EI / L
K_mat = np.array([[K11, K12], [K12, K11]])

# 5. Inversa
K_inv = np.linalg.inv(K_mat)

# 6. Vector de fuerzas
F3 = q * L**2 / 12
F6 = -F3
F_vec = np.array([F3, F6])

# 7. Rotaciones (matricial)
theta_vec = K_inv @ F_vec

# ============================================================
# RESULTADOS
# ============================================================
print("=" * 60)
print("EJERCICIO 1 — VIGA BIARTICULADA CON CARGA REPARTIDA")
print("=" * 60)
print(f"L = {L} m")
print(f"EI = {EI} kN·m²")
print(f"q = {q} kN/m")
print("-" * 60)
print("REACCIONES:")
print(f"  RA = RB = q·L/2 = {RA:.2f} kN")
print()
print("MOMENTO:")
print(f"  M_max = q·L²/8 = {M_max:.2f} kN·m")
print(f"  MA = MB = 0 kN·m")
print()
print("ROTACIÓN (analítica):")
print(f"  θ = q·L³/(24·EI) = {theta:.6f} rad")
print()
print("MATRIZ DE RIGIDEZ:")
print(f"  [K] = [{K11:.2f}  {K12:.2f}]")
print(f"        [{K12:.2f}  {K11:.2f}]")
print()
print("INVERSA:")
print(f"  [K]⁻¹ = [{K_inv[0,0]:.6f}  {K_inv[0,1]:.6f}]")
print(f"          [{K_inv[1,0]:.6f}  {K_inv[1,1]:.6f}]")
print()
print("VECTOR DE FUERZAS:")
print(f"  F3 = q·L²/12 = {F3:.4f} kN·m")
print(f"  F6 = -q·L²/12 = {F6:.4f} kN·m")
print()
print("ROTACIONES (matricial):")
print(f"  θ1 = {theta_vec[0]:.6f} rad")
print(f"  θ2 = {theta_vec[1]:.6f} rad")
print("=" * 60)

# ============================================================
# GRÁFICA
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#F5F5F5')

# --- Subplot 1: Diagrama de Momento ---
ax1 = axes[0]
ax1.set_facecolor('#FFFFFF')
x = np.linspace(0, L, 100)
M_x = (q * L / 2) * x - (q * x**2) / 2

ax1.plot(x, M_x, color='#B71C1C', linewidth=3,
         label='M(x) = (q·L/2)·x - q·x²/2')
ax1.axhline(y=0, color='black', linewidth=1)
ax1.axvline(x=L/2, color='#0D47A1', linestyle='--',
            linewidth=2, label=f'x = L/2 = {L/2} m')
ax1.scatter(L/2, M_max, color='#F9A825', s=200,
            zorder=5, edgecolor='black', linewidth=2,
            label=f'M_max = {M_max:.2f} kN·m')
ax1.set_xlabel('x (m)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Momento M(x) (kN·m)', fontsize=12, fontweight='bold')
ax1.set_title('DIAGRAMA DE MOMENTO FLECTOR\nEjercicio 1 — Viga Biarticulada',
              fontsize=13, fontweight='bold', color='#1A1A2E')
ax1.legend(fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.4)

# --- Subplot 2: Curva Momento–Rotación ---
ax2 = axes[1]
ax2.set_facecolor('#FFFFFF')
q_range = np.linspace(0, 15, 100)
theta_range = q_range * L**3 / (24 * EI)
M_range = q_range * L**2 / 8

ax2.plot(theta_range, M_range, color='#0D47A1', linewidth=3,
         label='M_max = q·L²/8', marker='o', markevery=10, markersize=7)
ax2.scatter(theta, M_max, color='#F9A825', s=250,
            zorder=5, edgecolor='black', linewidth=2,
            label=f'Punto: q={q} kN/m')
ax2.annotate(f'q = {q} kN/m\nθ = {theta:.5f} rad\nM = {M_max:.2f} kN·m',
             xy=(theta, M_max),
             xytext=(theta+0.003, M_max+2),
             fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF9C4',
                       edgecolor='#F9A825', linewidth=2),
             arrowprops=dict(arrowstyle='->', color='#F9A825', lw=2))
ax2.set_xlabel('Rotación θ (rad)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Momento M_max (kN·m)', fontsize=12, fontweight='bold')
ax2.set_title('CURVA MOMENTO–ROTACIÓN\nEjercicio 1 — Viga Biarticulada',
              fontsize=13, fontweight='bold', color='#1A1A2E')
ax2.legend(fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('ejercicio1_completo.png', dpi=200,
            bbox_inches='tight', facecolor='#F5F5F5')
plt.show()
print("\n✅ Imagen guardada: ejercicio1_completo.png")