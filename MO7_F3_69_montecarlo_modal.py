# -*- coding: utf-8 -*-
"""
================================================================================
M08.2 — METODO DE MONTE CARLO + COMPARATIVA CON ANALISIS MODAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.2 — Monte Carlo vs Análisis Modal

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
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# Semilla para reproducibilidad
np.random.seed(42)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "MONTE CARLO vs ANALISIS MODAL - LUCES HASTA 6 m"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La incertidumbre no se elimina: se cuantifica."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. VALORES NOMINALES (NUEVAS LUCES HASTA 6 m)
# ============================================================================

n_pisos = 2
He_nom = 3.0
b_col_nom, h_col_nom = 0.38, 0.38
Cm_nom, Cv_nom = 0.62, 0.20
fc_nom = 210
g = 9.81
n_columnas = 16

LUCES_X = [6.00, 5.50, 6.00]
LUCES_Y = [5.00, 6.00, 5.00, 5.50]

L1, L2, L3 = LUCES_X
L4, L5, L6, L7 = LUCES_Y

At = (L1/2 + L2/2 + L3/2) / 3 * (L4/2 + L5/2 + L6/2 + L7/2) / 4

# ============================================================================
# 3. COEFICIENTES DE VARIACION (CoV)
# ============================================================================

CoV = {
    'fc': 0.15,
    'b_col': 0.03,
    'h_col': 0.03,
    'Cm': 0.08,
    'Cv': 0.25,
    'He': 0.02,
    'L': 0.02,
}

# ============================================================================
# 4. ANALISIS DETERMINISTA (nominal)
# ============================================================================

def calcular_T(fc, b_col, h_col, Cm, Cv, He, factor_L=1.0):
    E_tm2 = 15100 * np.sqrt(fc) * 10
    I_col = (b_col * h_col**3) / 12
    Cu = 1.2 * Cm + 1.6 * Cv
    At_local = At * factor_L**2
    W_piso = Cu * At_local
    m = W_piso / g
    k = n_columnas * 12 * E_tm2 * I_col / He**3

    K = np.array([[2*k, -k], [-k, k]])
    M = np.array([[m, 0], [0, m]])

    M_inv = np.linalg.inv(M)
    A = M_inv @ K
    eigenvalues = np.linalg.eigvals(A)
    eigenvalues = np.sort(eigenvalues)

    omega1 = np.sqrt(eigenvalues[0])
    omega2 = np.sqrt(eigenvalues[1])
    T1 = 2 * np.pi / omega1
    T2 = 2 * np.pi / omega2

    phi1 = np.array([1.0, (3 - np.sqrt(5)) / 2 * k / (m * eigenvalues[0])])
    phi1 = phi1 / np.max(np.abs(phi1))
    phi2 = np.array([1.0, (3 + np.sqrt(5)) / 2 * k / (m * eigenvalues[1])])
    phi2 = phi2 / np.max(np.abs(phi2))

    return T1, T2, k, m, eigenvalues, phi1, phi2

T1_nom, T2_nom, k_nom, m_nom, eig_nom, phi1_nom, phi2_nom = calcular_T(
    fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom
)

print("=" * 80)
print(f"[M08.2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n ANALISIS MODAL DETERMINISTA (nominal):")
print(f"  k = {k_nom:.2f} t/m")
print(f"  m = {m_nom:.6f} t.s2/m")
print(f"  T1_nom = {T1_nom:.4f} s")
print(f"  T2_nom = {T2_nom:.4f} s")

# ============================================================================
# 5. SIMULACION MONTE CARLO
# ============================================================================

N_SIM = 10000

def norm_var(nom, cov):
    return np.random.normal(nom, nom * cov, N_SIM)

def gumbel_var(nom, cov):
    beta = nom * cov * np.sqrt(6) / np.pi
    mu = nom - 0.5772 * beta
    return np.random.gumbel(mu, beta, N_SIM)

fc_s = np.abs(norm_var(fc_nom, CoV['fc']))
b_col_s = np.abs(norm_var(b_col_nom, CoV['b_col']))
h_col_s = np.abs(norm_var(h_col_nom, CoV['h_col']))
Cm_s = np.abs(norm_var(Cm_nom, CoV['Cm']))
Cv_s = np.abs(gumbel_var(Cv_nom, CoV['Cv']))
He_s = np.abs(norm_var(He_nom, CoV['He']))
L_factor_s = np.abs(norm_var(1.0, CoV['L']))

E_s = 15100 * np.sqrt(fc_s) * 10
I_s = (b_col_s * h_col_s**3) / 12
Cu_s = 1.2 * Cm_s + 1.6 * Cv_s
At_s = At * L_factor_s**2
W_s = Cu_s * At_s
m_s = W_s / g
k_s = n_columnas * 12 * E_s * I_s / He_s**3

omega2_1_s = (3 - np.sqrt(5)) / 2 * k_s / m_s
omega2_2_s = (3 + np.sqrt(5)) / 2 * k_s / m_s

omega1_s = np.sqrt(omega2_1_s)
omega2_s = np.sqrt(omega2_2_s)
T1_s = 2 * np.pi / omega1_s
T2_s = 2 * np.pi / omega2_s

# ============================================================================
# 6. ESTADISTICAS
# ============================================================================

def stats(x, nombre):
    media = np.mean(x)
    std = np.std(x, ddof=1)
    cv = std / media
    p5 = np.percentile(x, 5)
    p50 = np.percentile(x, 50)
    p95 = np.percentile(x, 95)
    return {
        'nombre': nombre,
        'media': media, 'std': std, 'cv': cv,
        'p5': p5, 'p50': p50, 'p95': p95,
        'min': np.min(x), 'max': np.max(x)
    }

stats_T1 = stats(T1_s, 'T1')
stats_T2 = stats(T2_s, 'T2')
stats_k = stats(k_s, 'k')
stats_m = stats(m_s, 'm')

IC95_T1 = (stats_T1['p5'], stats_T1['p95'])
prob_T1_alto = np.mean(T1_s > T1_nom * 1.2) * 100

# ============================================================================
# 7. DIFERENCIAS (NECESARIAS PARA EL PRINT FINAL)
# ============================================================================

dif_T1 = abs(stats_T1['media'] - T1_nom) / T1_nom * 100
dif_T2 = abs(stats_T2['media'] - T2_nom) / T2_nom * 100
dif_k = abs(stats_k['media'] - k_nom) / k_nom * 100
dif_m = abs(stats_m['media'] - m_nom) / m_nom * 100

# ============================================================================
# 8. RESUMEN EN CONSOLA (CORREGIDO)
# ============================================================================

print("\n" + "=" * 80)
print("M08.2 — MONTE CARLO vs ANALISIS MODAL (LUCES 6 m)")
print("=" * 80)
print(f"\n  COMPARATIVA:")
print(f"  {'PARAMETRO':<15} {'MODAL':<15} {'MONTE CARLO':<15} {'DIF %':<10}")
print(f"  {'-'*60}")
print(f"  {'T1 (s)':<15} {T1_nom:<15.4f} {stats_T1['media']:<15.4f} {dif_T1:<10.4f}")
print(f"  {'T2 (s)':<15} {T2_nom:<15.4f} {stats_T2['media']:<15.4f} {dif_T2:<10.4f}")
print(f"  {'k (t/m)':<15} {k_nom:<15.2f} {stats_k['media']:<15.2f} {dif_k:<10.4f}")
print(f"  {'m (t.s2/m)':<15} {m_nom:<15.6f} {stats_m['media']:<15.6f} {dif_m:<10.4f}")

print(f"\n  INCERTIDUMBRE DE T1:")
print(f"    CoV      = {stats_T1['cv']*100:.2f} %")
print(f"    IC 95%   = [{stats_T1['p5']:.4f}, {stats_T1['p95']:.4f}] s")
print(f"    P(T1 > 1.2*T1_nom) = {prob_T1_alto:.2f} %")

print(f"\n  LINK: {LINK}")
print("=" * 80)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 80)

# ============================================================================
# 9. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(22, 15))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.975,
         'M08.2 - MONTE CARLO vs ANALISIS MODAL - LUCES HASTA 6 m',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.948, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.91, bottom=0.10)

# Panel 1: Histograma T1
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(T1_s, bins=50, color='#3498db', edgecolor='black', alpha=0.7)
ax1.axvline(T1_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Modal = {T1_nom:.4f}')
ax1.axvline(stats_T1['media'], color='green', linestyle='-', linewidth=2.5,
            label=f'MC Media = {stats_T1["media"]:.4f}')
ax1.axvspan(stats_T1['p5'], stats_T1['p95'], alpha=0.2, color='orange',
            label='IC 95%')
ax1.set_xlabel('T1 (s)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title('Distribucion T1', fontsize=11, fontweight='bold')
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

# Panel 2: Histograma T2
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(T2_s, bins=50, color='#e74c3c', edgecolor='black', alpha=0.7)
ax2.axvline(T2_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Modal = {T2_nom:.4f}')
ax2.axvline(stats_T2['media'], color='green', linestyle='-', linewidth=2.5,
            label=f'MC Media = {stats_T2["media"]:.4f}')
ax2.set_xlabel('T2 (s)', fontsize=10)
ax2.set_ylabel('Frecuencia', fontsize=10)
ax2.set_title('Distribucion T2', fontsize=11, fontweight='bold')
ax2.legend(fontsize=7)
ax2.grid(True, alpha=0.3)

# Panel 3: Tabla resumen
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
txt3 = (
    f"RESUMEN ESTADISTICO\n"
    f"{'-' * 34}\n"
    f"  Simulaciones: {N_SIM}\n"
    f"  Luces max: 6.00 m\n"
    f"{'-' * 34}\n"
    f"  T1 MODAL    = {T1_nom:.4f} s\n"
    f"  T1 MEDIA MC = {stats_T1['media']:.4f} s\n"
    f"  T1 STD      = {stats_T1['std']:.4f} s\n"
    f"  T1 CoV      = {stats_T1['cv']*100:.2f} %\n"
    f"  T1 P5       = {stats_T1['p5']:.4f} s\n"
    f"  T1 P95      = {stats_T1['p95']:.4f} s\n"
    f"{'-' * 34}\n"
    f"  T2 MODAL    = {T2_nom:.4f} s\n"
    f"  T2 MEDIA MC = {stats_T2['media']:.4f} s\n"
    f"  T2 CoV      = {stats_T2['cv']*100:.2f} %\n"
    f"{'-' * 34}\n"
    f"  P(T1 > 1.2*T1_nom)\n"
    f"      = {prob_T1_alto:.2f} %"
)
ax3.text(0.5, 0.5, txt3, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# Panel 4: Convergencia
ax4 = fig.add_subplot(gs[1, 0])
medias_acum = np.cumsum(T1_s) / np.arange(1, N_SIM + 1)
ax4.plot(np.arange(1, N_SIM + 1), medias_acum, 'b-', linewidth=1.5)
ax4.axhline(T1_nom, color='red', linestyle='--', linewidth=2,
            label=f'Modal = {T1_nom:.4f}')
ax4.axhline(stats_T1['media'], color='green', linestyle=':',
            linewidth=2, label=f'MC Media = {stats_T1["media"]:.4f}')
ax4.set_xlabel('Numero de simulaciones', fontsize=10)
ax4.set_ylabel('Media acumulada de T1 (s)', fontsize=10)
ax4.set_title('Convergencia de la media', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# Panel 5: Sensibilidad
ax5 = fig.add_subplot(gs[1, 1])
vars_names = ['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L']
sens_values = []

for var in vars_names:
    params_nom = [fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom]
    if var == 'L':
        T1_hi = calcular_T(*params_nom, factor_L=1.10)[0]
        T1_lo = calcular_T(*params_nom, factor_L=0.90)[0]
    else:
        idx = vars_names.index(var)
        params_hi = params_nom.copy()
        params_hi[idx] *= 1.10
        params_lo = params_nom.copy()
        params_lo[idx] *= 0.90
        T1_hi = calcular_T(*params_hi)[0]
        T1_lo = calcular_T(*params_lo)[0]
    sens = (T1_hi - T1_lo) / (2 * T1_nom) * 100
    sens_values.append(sens)

order = np.argsort(np.abs(sens_values))
vars_sorted = [vars_names[i] for i in order]
sens_sorted = [sens_values[i] for i in order]

colores_sens = ['#2ecc71' if v > 0 else '#e74c3c' for v in sens_sorted]
ax5.barh(vars_sorted, sens_sorted, color=colores_sens,
         edgecolor='black', linewidth=1.5)
ax5.axvline(0, color='black', linestyle='-', linewidth=1)
ax5.set_xlabel('Cambio en T1 (%) para +-10% variable', fontsize=9)
ax5.set_title('Sensibilidad de T1', fontsize=11, fontweight='bold')
ax5.grid(axis='x', linestyle='--', alpha=0.3)

# Panel 6: Boxplot
ax6 = fig.add_subplot(gs[1, 2])
bp = ax6.boxplot([T1_s, T2_s], labels=['T1', 'T2'],
                 patch_artist=True, widths=0.5)
for patch, color in zip(bp['boxes'], ['#3498db', '#e74c3c']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax6.axhline(T1_nom, color='blue', linestyle='--', linewidth=1.5,
            label=f'T1 modal = {T1_nom:.3f}')
ax6.axhline(T2_nom, color='red', linestyle='--', linewidth=1.5,
            label=f'T2 modal = {T2_nom:.3f}')
ax6.set_ylabel('Periodo (s)', fontsize=10)
ax6.set_title('Boxplot T1 y T2', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# Panel 7: Histograma k
ax7 = fig.add_subplot(gs[2, 0])
ax7.hist(k_s, bins=50, color='#9b59b6', edgecolor='black', alpha=0.7)
ax7.axvline(k_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Modal = {k_nom:.0f}')
ax7.axvline(stats_k['media'], color='green', linestyle='-',
            linewidth=2.5, label=f'MC Media = {stats_k["media"]:.0f}')
ax7.set_xlabel('k (t/m)', fontsize=10)
ax7.set_ylabel('Frecuencia', fontsize=10)
ax7.set_title('Distribucion de rigidez k', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)

# Panel 8: Histograma m
ax8 = fig.add_subplot(gs[2, 1])
ax8.hist(m_s, bins=50, color='#e67e22', edgecolor='black', alpha=0.7)
ax8.axvline(m_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Modal = {m_nom:.3f}')
ax8.axvline(stats_m['media'], color='green', linestyle='-',
            linewidth=2.5, label=f'MC Media = {stats_m["media"]:.3f}')
ax8.set_xlabel('m (t.s2/m)', fontsize=10)
ax8.set_ylabel('Frecuencia', fontsize=10)
ax8.set_title('Distribucion de masa m', fontsize=11, fontweight='bold')
ax8.legend(fontsize=8)
ax8.grid(True, alpha=0.3)

# Panel 9: Formas modales
ax9 = fig.add_subplot(gs[2, 2])
alturas = [0, He_nom, 2*He_nom]

phi1_mc = np.array([0, 1.0, np.mean((3 - np.sqrt(5)) / 2 * k_s / (m_s * omega2_1_s))])
phi1_mc = phi1_mc / np.max(np.abs(phi1_mc))
ax9.plot(phi1_mc, alturas, 'bo-', linewidth=2.5, markersize=10,
         label=f'Modo 1 MC')

phi1_mod = np.array([0, 1.0, phi1_nom[1]])
phi1_mod = phi1_mod / np.max(np.abs(phi1_mod))
ax9.plot(phi1_mod, alturas, 'b--', linewidth=2, markersize=8,
         alpha=0.5, label=f'Modo 1 Modal')

phi2_mc = np.array([0, 1.0, np.mean((3 + np.sqrt(5)) / 2 * k_s / (m_s * omega2_2_s))])
phi2_mc = phi2_mc / np.max(np.abs(phi2_mc))
ax9.plot(phi2_mc, alturas, 'ro-', linewidth=2.5, markersize=10,
         label=f'Modo 2 MC')

phi2_mod = np.array([0, 1.0, phi2_nom[1]])
phi2_mod = phi2_mod / np.max(np.abs(phi2_mod))
ax9.plot(phi2_mod, alturas, 'r--', linewidth=2, markersize=8,
         alpha=0.5, label=f'Modo 2 Modal')

ax9.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax9.set_xlabel('Desplaz. normalizado', fontsize=10)
ax9.set_ylabel('Altura (m)', fontsize=10)
ax9.set_title('Formas modales: MC vs Modal',
              fontsize=11, fontweight='bold')
ax9.legend(fontsize=7, loc='best')
ax9.grid(True, alpha=0.3)

# ============================================================================
# LINK DEL PROYECTO
# ============================================================================

fig.text(0.5, 0.02,
         f'🌐 Más información: {LINK}',
         ha='center', va='bottom', fontsize=11, fontweight='bold',
         color='#2980b9',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor='#2980b9',
                   linewidth=2))

# ============================================================================
# GUARDAR
# ============================================================================

carpeta = "Resultados_M08_2"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_2_montecarlo_comparativa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\n[OK] Dashboard guardado: {ruta_img}")

plt.show()