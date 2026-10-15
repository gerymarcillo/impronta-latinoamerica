# -*- coding: utf-8 -*-
"""
================================================================================
M08.7 — CONFIABILIDAD ESTRUCTURAL CON Y SIN DMTP - MARKOV
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.7 — Confiabilidad con y sin DMTP

OBJETIVO: Comparar la CONFIABILIDAD ESTRUCTURAL mediante Cadenas de Markov
          en dos escenarios:
          - ESCENARIO A: SIN DMTP (solo degradación)
          - ESCENARIO B: CON DMTP (con recuperación)

          Cuantificar:
          - Probabilidad de colapso a 50 años
          - MTTF (Mean Time To Failure)
          - Estado estacionario
          - Confiabilidad global

ESTADOS DE DAÑO (HAZUS):
    E0: Sin daño
    E1: Leve
    E2: Moderado
    E3: Severo
    E4: Colapso (absorbente)

DIFERENCIA CLAVE:
    SIN DMTP: E0 → E1 → E2 → E3 → E4 (solo degradación)
    CON DMTP: E0 ⇄ E1 ⇄ E2 → E3 → E4 (con recuperación)

LINK: https://gerymarcillo.github.io/impronta-latinoamerica/
================================================================================
"""

import os
import sys
from datetime import datetime
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from matplotlib.colors import LinearSegmentedColormap
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

np.random.seed(42)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "CONFIABILIDAD ESTRUCTURAL CON Y SIN DMTP - MARKOV"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La confiabilidad no es solo resistir, es recuperarse."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. DATOS DEL MODELO
# ============================================================================

n_pisos = 2
He = 3.0
b_col, h_col = 0.38, 0.38
Cm, Cv = 0.62, 0.20
Cu = 1.2 * Cm + 1.6 * Cv
fc = 210
g = 9.81

# Luces de hasta 6 m
LUCES_X = [6.00, 5.50, 6.00]
LUCES_Y = [5.00, 6.00, 5.00, 5.50]
L1, L2, L3 = LUCES_X
L4, L5, L6, L7 = LUCES_Y

n_columnas = 16
At = (L1/2 + L2/2 + L3/2) / 3 * (L4/2 + L5/2 + L6/2 + L7/2) / 4

# Periodo fundamental
E_tm2 = 15100 * np.sqrt(fc) * 10
I_col = (b_col * h_col**3) / 12
W_piso = Cu * At
m = W_piso / g
k = n_columnas * 12 * E_tm2 * I_col / He**3
omega1 = np.sqrt((3 - np.sqrt(5)) / 2 * k / m)
T1 = 2 * np.pi / omega1

# ============================================================================
# 3. ESTADOS DE DAÑO (HAZUS)
# ============================================================================

estados = [
    {'id': 0, 'nombre': 'Sin daño', 'deriva_max': 0.0033, 'color': '#2d6a4f'},
    {'id': 1, 'nombre': 'Leve', 'deriva_max': 0.0058, 'color': '#3498db'},
    {'id': 2, 'nombre': 'Moderado', 'deriva_max': 0.0156, 'color': '#f39c12'},
    {'id': 3, 'nombre': 'Severo', 'deriva_max': 0.0400, 'color': '#e67e22'},
    {'id': 4, 'nombre': 'Colapso', 'deriva_max': float('inf'), 'color': '#9d0208'},
]

print("=" * 80)
print(f"[M08.7] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n DATOS DEL MODELO:")
print(f"  T1 = {T1:.4f} s")
print(f"  k = {k:.2f} t/m")
print(f"  m = {m:.6f} t.s2/m")
print(f"  At = {At:.4f} m2")
print(f"  N columnas = {n_columnas}")

print("\n ESTADOS DE DAÑO (HAZUS):")
for e in estados:
    dmax = f"{e['deriva_max']*100:.2f}%" if e['deriva_max'] != float('inf') else "∞"
    print(f"  E{e['id']}: {e['nombre']:<12} Deriva < {dmax}")

# ============================================================================
# 4. MATRICES DE TRANSICIÓN
# ============================================================================

# ============================================
# ESCENARIO A: SIN DMTP (solo degradación)
# ============================================

P_sin = np.array([
    [0.850, 0.120, 0.025, 0.004, 0.001],  # E0
    [0.000, 0.750, 0.150, 0.080, 0.020],  # E1
    [0.000, 0.000, 0.700, 0.200, 0.100],  # E2
    [0.000, 0.000, 0.000, 0.650, 0.350],  # E3
    [0.000, 0.000, 0.000, 0.000, 1.000],  # E4
])

# ============================================
# ESCENARIO B: CON DMTP (con recuperación)
# ============================================

P_con = np.array([
    [0.880, 0.090, 0.025, 0.004, 0.001],  # E0
    [0.350, 0.480, 0.120, 0.040, 0.010],  # E1
    [0.120, 0.330, 0.380, 0.130, 0.040],  # E2
    [0.000, 0.120, 0.330, 0.400, 0.150],  # E3
    [0.000, 0.000, 0.000, 0.000, 1.000],  # E4
])

# ============================================================================
# 5. VERIFICACIÓN DE MATRICES
# ============================================================================

print("\n" + "=" * 80)
print("VERIFICACION DE MATRICES DE TRANSICION")
print("=" * 80)

print("\n  ESCENARIO A (SIN DMTP):")
for i in range(5):
    suma = P_sin[i].sum()
    print(f"    Fila E{i}: suma = {suma:.4f}  {'OK' if abs(suma-1) < 1e-6 else 'ERROR'}")

print("\n  ESCENARIO B (CON DMTP):")
for i in range(5):
    suma = P_con[i].sum()
    print(f"    Fila E{i}: suma = {suma:.4f}  {'OK' if abs(suma-1) < 1e-6 else 'ERROR'}")

# ============================================================================
# 6. EVOLUCIÓN DEL ESTADO
# ============================================================================

n_sismos = 30
pi0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

# Evolución SIN DMTP
pi_sin = np.zeros((n_sismos + 1, 5))
pi_sin[0] = pi0
for s in range(1, n_sismos + 1):
    pi_sin[s] = pi_sin[s-1] @ P_sin

# Evolución CON DMTP
pi_con = np.zeros((n_sismos + 1, 5))
pi_con[0] = pi0
for s in range(1, n_sismos + 1):
    pi_con[s] = pi_con[s-1] @ P_con

print("\n" + "=" * 80)
print("EVOLUCION DEL ESTADO A 30 SISMOS")
print("=" * 80)
print(f"\n  {'Sismo':<6} {'P(E0)':<10} {'P(E1)':<10} {'P(E2)':<10} {'P(E3)':<10} {'P(E4)':<10}")
print(f"  {'-'*66}")
print("  SIN DMTP:")
for s in [0, 5, 10, 15, 20, 30]:
    print(f"  {s:<6} " + "  ".join([f"{pi_sin[s, j]:.4f}" for j in range(5)]))
print(f"\n  CON DMTP:")
for s in [0, 5, 10, 15, 20, 30]:
    print(f"  {s:<6} " + "  ".join([f"{pi_con[s, j]:.4f}" for j in range(5)]))

# ============================================================================
# 7. ESTADO ESTACIONARIO
# ============================================================================

def estado_estacionario(P):
    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals - 1.0))
    pi = np.real(eigvecs[:, idx])
    pi = pi / pi.sum()
    return pi

pi_est_sin = estado_estacionario(P_sin)
pi_est_con = estado_estacionario(P_con)

print("\n" + "=" * 80)
print("ESTADO ESTACIONARIO")
print("=" * 80)
print(f"\n  {'Estado':<15} {'SIN DMTP':<15} {'CON DMTP':<15} {'DIFERENCIA':<15}")
print(f"  {'-'*60}")
for i, e in enumerate(estados):
    sin = pi_est_sin[i] * 100
    con = pi_est_con[i] * 100
    dif = con - sin
    print(f"  E{i} ({e['nombre']:<10}): {sin:>7.2f}%       {con:>7.2f}%       {dif:>+7.2f}%")

# Resiliencia estacionaria
res_sin = (pi_est_sin[0] + pi_est_sin[1]) * 100
res_con = (pi_est_con[0] + pi_est_con[1]) * 100
print(f"\n  RESILIENCIA ESTACIONARIA (E0+E1):")
print(f"    SIN DMTP: {res_sin:.2f}%")
print(f"    CON DMTP: {res_con:.2f}%")
print(f"    MEJORA:   {res_con - res_sin:+.2f}%")

# ============================================================================
# 8. MTTF (Mean Time To Failure)
# ============================================================================

print("\n" + "=" * 80)
print("TIEMPO MEDIO HASTA COLAPSO (MTTF)")
print("=" * 80)

# MTTF usando submatriz Q (estados transitorios)
Q_sin = P_sin[:4, :4]
Q_con = P_con[:4, :4]

I_Q = np.eye(4)
MTTF_sin = np.linalg.solve(I_Q - Q_sin, np.ones(4))
MTTF_con = np.linalg.solve(I_Q - Q_con, np.ones(4))

print(f"\n  {'Desde estado':<18} {'SIN DMTP':<15} {'CON DMTP':<15} {'MEJORA':<15}")
print(f"  {'-'*60}")
for i, e in enumerate(estados[:4]):
    print(f"  E{i} ({e['nombre']:<10}): {MTTF_sin[i]:>8.2f}        {MTTF_con[i]:>8.2f}        {MTTF_con[i]-MTTF_sin[i]:>+8.2f}")

# Confiabilidad desde E0
print(f"\n  CONFIABILIDAD DESDE E0:")
print(f"    MTTF SIN DMTP: {MTTF_sin[0]:.2f} sismos")
print(f"    MTTF CON DMTP: {MTTF_con[0]:.2f} sismos")
print(f"    MEJORA: {(MTTF_con[0]/MTTF_sin[0]-1)*100:+.2f}%")

# ============================================================================
# 9. PROBABILIDAD DE COLAPSO A 50 AÑOS
# ============================================================================

print("\n" + "=" * 80)
print("PROBABILIDAD DE COLAPSO A 50 AÑOS")
print("=" * 80)

T_vida_util = 50
Tasa_sismos = 1.0
n_sismos_vida = int(T_vida_util * Tasa_sismos)

pi_vida_sin = np.linalg.matrix_power(P_sin, n_sismos_vida)[0]
pi_vida_con = np.linalg.matrix_power(P_con, n_sismos_vida)[0]

print(f"\n  Vida util: {T_vida_util} años")
print(f"  Tasa sismos: {Tasa_sismos} sismo/año")
print(f"  N sismos: {n_sismos_vida}")

print(f"\n  P(colapso a 50 años):")
print(f"    SIN DMTP: {pi_vida_sin[4]*100:.4f}%")
print(f"    CON DMTP: {pi_vida_con[4]*100:.4f}%")
print(f"    MEJORA:   {(1 - pi_vida_con[4]/max(pi_vida_sin[4], 1e-10))*100:.2f}%")

print(f"\n  P(daño severo o colapso):")
P_sev_sin = pi_vida_sin[3] + pi_vida_sin[4]
P_sev_con = pi_vida_con[3] + pi_vida_con[4]
print(f"    SIN DMTP: {P_sev_sin*100:.4f}%")
print(f"    CON DMTP: {P_sev_con*100:.4f}%")

# Evaluación normativa
print(f"\n  EVALUACION NORMATIVA (NEC-15):")
print(f"    Criterio: P(colapso) < 1% en 50 años")
if pi_vida_sin[4] < 0.01:
    print(f"    SIN DMTP: ✅ CUMPLE ({pi_vida_sin[4]*100:.4f}%)")
else:
    print(f"    SIN DMTP: ❌ NO CUMPLE ({pi_vida_sin[4]*100:.4f}%)")
if pi_vida_con[4] < 0.01:
    print(f"    CON DMTP: ✅ CUMPLE ({pi_vida_con[4]*100:.4f}%)")
else:
    print(f"    CON DMTP: ❌ NO CUMPLE ({pi_vida_con[4]*100:.4f}%)")

# ============================================================================
# 10. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M08.7 — CONFIABILIDAD ESTRUCTURAL CON Y SIN DMTP',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.92, bottom=0.08)

# ============================================================================
# FILA 1: MATRICES DE TRANSICIÓN
# ============================================================================

cmap = LinearSegmentedColormap.from_list('custom', ['#ffffff', '#3498db', '#1a237e'])

# --- Panel 1: Matriz P_sin ---
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(P_sin, cmap=cmap, vmin=0, vmax=1, aspect='auto')
ax1.set_xticks(range(5))
ax1.set_yticks(range(5))
ax1.set_xticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax1.set_yticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax1.set_xlabel('Estado destino', fontsize=10)
ax1.set_ylabel('Estado origen', fontsize=10)
ax1.set_title('(a) MATRIZ P — SIN DMTP', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_sin[i, j]
        color = 'white' if val > 0.5 else 'black'
        ax1.text(j, i, f'{val:.3f}', ha='center', va='center',
                 fontsize=8, fontweight='bold', color=color)

plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

# --- Panel 2: Matriz P_con ---
ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(P_con, cmap=cmap, vmin=0, vmax=1, aspect='auto')
ax2.set_xticks(range(5))
ax2.set_yticks(range(5))
ax2.set_xticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax2.set_yticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax2.set_xlabel('Estado destino', fontsize=10)
ax2.set_ylabel('Estado origen', fontsize=10)
ax2.set_title('(b) MATRIZ P — CON DMTP', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_con[i, j]
        color = 'white' if val > 0.5 else 'black'
        ax2.text(j, i, f'{val:.3f}', ha='center', va='center',
                 fontsize=8, fontweight='bold', color=color)

plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

# --- Panel 3: Diferencia ---
ax3 = fig.add_subplot(gs[0, 2])
P_diff = P_con - P_sin
cmap_diff = LinearSegmentedColormap.from_list('diff', ['#e74c3c', '#ffffff', '#2ecc71'])
im3 = ax3.imshow(P_diff, cmap=cmap_diff, vmin=-0.35, vmax=0.35, aspect='auto')
ax3.set_xticks(range(5))
ax3.set_yticks(range(5))
ax3.set_xticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax3.set_yticklabels([f'E{i}' for i in range(5)], fontsize=9)
ax3.set_xlabel('Estado destino', fontsize=10)
ax3.set_ylabel('Estado origen', fontsize=10)
ax3.set_title('(c) DIFERENCIA P_con - P_sin', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_diff[i, j]
        if abs(val) > 0.001:
            color = 'white' if abs(val) > 0.2 else 'black'
            ax3.text(j, i, f'{val:+.3f}', ha='center', va='center',
                     fontsize=7, fontweight='bold', color=color)

plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

# ============================================================================
# FILA 2: EVOLUCIÓN Y MTTF
# ============================================================================

# --- Panel 4: Evolución SIN DMTP ---
ax4 = fig.add_subplot(gs[1, 0])
sismos = np.arange(n_sismos + 1)
for j in range(5):
    ax4.plot(sismos, pi_sin[:, j], 'o-', linewidth=2, markersize=4,
             label=f'E{j}', color=estados[j]['color'])
ax4.set_xlabel('Número de sismos', fontsize=10)
ax4.set_ylabel('Probabilidad', fontsize=10)
ax4.set_title('(d) EVOLUCIÓN SIN DMTP', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8, loc='center right')
ax4.grid(True, alpha=0.3)
ax4.set_ylim(0, 1.05)

# --- Panel 5: Evolución CON DMTP ---
ax5 = fig.add_subplot(gs[1, 1])
for j in range(5):
    ax5.plot(sismos, pi_con[:, j], 'o-', linewidth=2, markersize=4,
             label=f'E{j}', color=estados[j]['color'])
ax5.set_xlabel('Número de sismos', fontsize=10)
ax5.set_ylabel('Probabilidad', fontsize=10)
ax5.set_title('(e) EVOLUCIÓN CON DMTP', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8, loc='center right')
ax5.grid(True, alpha=0.3)
ax5.set_ylim(0, 1.05)

# --- Panel 6: MTTF ---
ax6 = fig.add_subplot(gs[1, 2])
x_pos = np.arange(4)
width = 0.35

bars1 = ax6.bar(x_pos - width/2, MTTF_sin, width, color='#e74c3c',
                edgecolor='black', linewidth=1.5, label='Sin DMTP', alpha=0.85)
bars2 = ax6.bar(x_pos + width/2, MTTF_con, width, color='#2ecc71',
                edgecolor='black', linewidth=1.5, label='Con DMTP', alpha=0.85)

for bar, val in zip(bars1, MTTF_sin):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.1f}', ha='center', fontsize=8, fontweight='bold')
for bar, val in zip(bars2, MTTF_con):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.1f}', ha='center', fontsize=8, fontweight='bold')

ax6.set_xticks(x_pos)
ax6.set_xticklabels([f'E{i}' for i in range(4)], fontsize=10)
ax6.set_ylabel('MTTF (número de sismos)', fontsize=10)
ax6.set_title('(f) TIEMPO MEDIO HASTA COLAPSO', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, axis='y', linestyle='--', alpha=0.3)

# ============================================================================
# FILA 3: ESTADO ESTACIONARIO Y PROBABILIDAD DE COLAPSO
# ============================================================================

# --- Panel 7: Estado estacionario ---
ax7 = fig.add_subplot(gs[2, 0])
x_pos = np.arange(5)
width = 0.35

bars1 = ax7.bar(x_pos - width/2, pi_est_sin * 100, width, color='#e74c3c',
                edgecolor='black', linewidth=1.5, label='Sin DMTP', alpha=0.85)
bars2 = ax7.bar(x_pos + width/2, pi_est_con * 100, width, color='#2ecc71',
                edgecolor='black', linewidth=1.5, label='Con DMTP', alpha=0.85)

for i, (s, c) in enumerate(zip(pi_est_sin*100, pi_est_con*100)):
    ax7.text(i - width/2, s + 1, f'{s:.1f}%', ha='center', fontsize=7, fontweight='bold')
    ax7.text(i + width/2, c + 1, f'{c:.1f}%', ha='center', fontsize=7, fontweight='bold')

ax7.set_xticks(x_pos)
ax7.set_xticklabels([f'E{i}' for i in range(5)], fontsize=10)
ax7.set_ylabel('Probabilidad estacionaria (%)', fontsize=10)
ax7.set_title('(g) ESTADO ESTACIONARIO', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 8: Probabilidad de colapso a 50 años ---
ax8 = fig.add_subplot(gs[2, 1])

categorias = ['Sin DMTP', 'Con DMTP']
colapso_vals = [pi_vida_sin[4] * 100, pi_vida_con[4] * 100]
colores = ['#e74c3c', '#2ecc71']

bars = ax8.bar(categorias, colapso_vals, color=colores,
               edgecolor='black', linewidth=2, alpha=0.85)
for bar, val in zip(bars, colapso_vals):
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{val:.4f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax8.axhline(1.0, color='red', linestyle='--', linewidth=2.5,
            label='Límite NEC-15 = 1%')
ax8.set_ylabel('P(colapso a 50 años) (%)', fontsize=10)
ax8.set_title('(h) PROBABILIDAD DE COLAPSO', fontsize=11, fontweight='bold')
ax8.legend(fontsize=8)
ax8.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 9: Conclusión ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.set_title('(i) CONCLUSIÓN', fontsize=12, fontweight='bold', pad=10)

txt9 = (
    f"CONFIABILIDAD ESTRUCTURAL\n"
    f"─────────────────────────────\n\n"
    f"  MTTF desde E0:\n"
    f"    Sin DMTP: {MTTF_sin[0]:.1f} sismos\n"
    f"    Con DMTP: {MTTF_con[0]:.1f} sismos\n"
    f"    Mejora:   {(MTTF_con[0]/MTTF_sin[0]-1)*100:+.1f}%\n\n"
    f"  P(colapso a 50 años):\n"
    f"    Sin DMTP: {pi_vida_sin[4]*100:.4f}%\n"
    f"    Con DMTP: {pi_vida_con[4]*100:.4f}%\n\n"
    f"  RESILIENCIA ESTACIONARIA:\n"
    f"    Sin DMTP: {res_sin:.1f}%\n"
    f"    Con DMTP: {res_con:.1f}%\n"
    f"    Mejora:   {res_con-res_sin:+.1f}%\n\n"
    f"─────────────────────────────\n"
    f"  CLAVE:\n"
    f"    El DMTP permite la\n"
    f"    RECUPERACIÓN desde\n"
    f"    E1, E2 y E3, aumentando\n"
    f"    la confiabilidad global.\n"
    f"─────────────────────────────\n"
    f"  {FRASE}"
)

ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=7.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# ============================================================================
# LINK DEL PROYECTO
# ============================================================================

fig.text(0.5, 0.015,
         f'🌐 Más información: {LINK}',
         ha='center', va='bottom', fontsize=11, fontweight='bold',
         color='#2980b9',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor='#2980b9',
                   linewidth=2))

# ============================================================================
# 11. GUARDAR
# ============================================================================

carpeta = "Resultados_M08_7"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_7_confiabilidad_DMTP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\n[OK] Dashboard guardado: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M08.7 COMPLETADO — CONFIABILIDAD CON Y SIN DMTP")
print("=" * 80)
print(f"\n  MTTF desde E0:")
print(f"    Sin DMTP: {MTTF_sin[0]:.2f} sismos")
print(f"    Con DMTP: {MTTF_con[0]:.2f} sismos")
print(f"\n  P(colapso a 50 años):")
print(f"    Sin DMTP: {pi_vida_sin[4]*100:.4f}%")
print(f"    Con DMTP: {pi_vida_con[4]*100:.4f}%")
print(f"\n  RESILIENCIA ESTACIONARIA:")
print(f"    Sin DMTP: {res_sin:.2f}%")
print(f"    Con DMTP: {res_con:.2f}%")
print(f"    Mejora:   {res_con-res_sin:+.2f}%")
print("=" * 80)