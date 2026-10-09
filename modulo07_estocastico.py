# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 07 — ALGORITMO 5: ESTOCÁSTICO MODAL
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Monte Carlo del análisis modal del PÓRTICO DEL PROYECTO (2 pisos)

            - N = 1000 simulaciones
            - 5 variables aleatorias: E, m, I_col, He, Cu
            - Distribución de T₁, T₂, f₁, f₂, K, M
            - Confiabilidad β y P_falla
            - Sensibilidad (Spearman)
            - Comparación con valores teóricos
            - Dashboard 9 paneles

            NINGÚN SOFTWARE COMERCIAL HACE ESTO
================================================================================
"""

import os
import sys
from datetime import datetime

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.gridspec import GridSpec
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("⚠️ matplotlib no está instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "ESTOCÁSTICO MODAL — PÓRTICO 2 PISOS"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La incertidumbre no se elimina: se cuantifica."

# ============================================================================
# 2. DATOS DEL MODELO DEL PROYECTO (PÓRTICO 2 PISOS)
# ============================================================================

# --- Geometría (valores nominales) ---
n_pisos = 2
He_nom = 3.0
H_total = n_pisos * He_nom

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

b_col_nom = 0.38
h_col_nom = 0.38
b_viga = 0.30
h_viga = 0.45

# --- Materiales (valores nominales) ---
fc_nom = 210            # kg/cm²
fy = 4200               # kg/cm²
E_kgcm2_nom = 15100 * np.sqrt(fc_nom)
E_nom = E_kgcm2_nom * 10     # t/m²

# --- Carga (valor nominal) ---
Cu_nom = 1.088          # t/m²
g = 9.81                # m/s²

# --- Área tributaria ---
At = (L1/2 + L2/2) * (L3/2 + L4/2)

# --- Valores nominales derivados ---
I_col_nom = (b_col_nom * h_col_nom**3) / 12
masa_piso_nom = Cu_nom * At / g
n_columnas = 4
k_entrepiso_nom = n_columnas * 12 * E_nom * I_col_nom / He_nom**3

# --- Matrices K y M nominales ---
K_nom = np.array([
    [2 * k_entrepiso_nom, -k_entrepiso_nom],
    [-k_entrepiso_nom, k_entrepiso_nom]
])
M_nom = np.array([
    [masa_piso_nom, 0],
    [0, masa_piso_nom]
])

# --- Análisis modal nominal ---
M_inv = np.linalg.inv(M_nom)
A_nom = M_inv @ K_nom
eigenvalues_nom, eigenvectors_nom = np.linalg.eig(A_nom)
idx = np.argsort(eigenvalues_nom)
eigenvalues_nom = eigenvalues_nom[idx]
omega_nom = np.sqrt(eigenvalues_nom)
T_nom = 2 * np.pi / omega_nom
frec_nom = omega_nom / (2 * np.pi)

T1_nom = T_nom[0]
T2_nom = T_nom[1]
f1_nom = frec_nom[0]
f2_nom = frec_nom[1]

# ============================================================================
# 3. PARÁMETROS ESTOCÁSTICOS
# ============================================================================

N = 1000                # Número de simulaciones
np.random.seed(42)      # Reproducibilidad

# Coeficientes de variación
COV_E = 0.15            # Módulo elasticidad (lognormal)
COV_m = 0.10            # Masa (normal)
COV_I = 0.05            # Inercia columna (normal)
COV_He = 0.03           # Altura entrepiso (normal)
COV_Cu = 0.10           # Carga última (normal)

# ============================================================================
# 4. MONTE CARLO
# ============================================================================

print("=" * 80)
print(f"[M07 - A5] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n[EJECUTANDO MONTE CARLO] N = {N} simulaciones...")

# --- Variables aleatorias ---
# E ~ Lognormal
E_sim = np.random.lognormal(
    np.log(E_nom) - 0.5 * np.log(1 + COV_E**2),
    np.sqrt(np.log(1 + COV_E**2)),
    N
)
E_sim = np.clip(E_sim, 0.7*E_nom, 1.3*E_nom)

# m ~ Normal
m_sim = np.random.normal(masa_piso_nom, COV_m * masa_piso_nom, N)
m_sim = np.clip(m_sim, 0.7*masa_piso_nom, 1.3*masa_piso_nom)

# I_col ~ Normal
I_sim = np.random.normal(I_col_nom, COV_I * I_col_nom, N)
I_sim = np.clip(I_sim, 0.9*I_col_nom, 1.1*I_col_nom)

# He ~ Normal
He_sim = np.random.normal(He_nom, COV_He * He_nom, N)
He_sim = np.clip(He_sim, 0.95*He_nom, 1.05*He_nom)

# Cu ~ Normal
Cu_sim = np.random.normal(Cu_nom, COV_Cu * Cu_nom, N)
Cu_sim = np.clip(Cu_sim, 0.7*Cu_nom, 1.3*Cu_nom)

# --- Cálculos vectorizados ---
# Masa (depende de Cu)
masa_sim = Cu_sim * At / g

# Rigidez de entrepiso (depende de E, I, He)
k_sim = n_columnas * 12 * E_sim * I_sim / He_sim**3

# Matrices K y M (vectorizadas)
# Para cada simulación, calculamos autovalores de M^-1 K
# K = [[2k, -k],[-k, k]], M = diag(m, m)
# M^-1 K = (1/m) * [[2k, -k],[-k, k]]

# Autovalores analíticos de M^-1 K (sistema 2x2 shear building)
# ω₁² = k/m * (2 - √2) ≈ 0.586 * k/m
# ω₂² = k/m * (2 + √2) ≈ 3.414 * k/m
ratio = k_sim / masa_sim
omega1_sim = np.sqrt(ratio * (2 - np.sqrt(2)))
omega2_sim = np.sqrt(ratio * (2 + np.sqrt(2)))

T1_sim = 2 * np.pi / omega1_sim
T2_sim = 2 * np.pi / omega2_sim
f1_sim = omega1_sim / (2 * np.pi)
f2_sim = omega2_sim / (2 * np.pi)

# --- Confiabilidad ---
# P_falla = si T₁ sale del rango [0.8*T1_nom, 1.2*T1_nom]
T1_min = 0.8 * T1_nom
T1_max = 1.2 * T1_nom
P_falla = np.mean((T1_sim < T1_min) | (T1_sim > T1_max))

# β (índice de confiabilidad)
# β = (T1_nom - T1_min) / σ_T1 (aproximación)
sigma_T1 = np.std(T1_sim)
if sigma_T1 > 0:
    beta = (T1_nom - T1_min) / sigma_T1
else:
    beta = 0

# ============================================================================
# 5. ESTADÍSTICOS
# ============================================================================

def stats(arr, nombre):
    return {
        "nombre": nombre,
        "media": np.mean(arr),
        "std": np.std(arr),
        "cov": np.std(arr) / np.mean(arr) if np.mean(arr) != 0 else 0,
        "p5": np.percentile(arr, 5),
        "p50": np.percentile(arr, 50),
        "p95": np.percentile(arr, 95)
    }

stats_T1 = stats(T1_sim, "T1 (s)")
stats_T2 = stats(T2_sim, "T2 (s)")
stats_f1 = stats(f1_sim, "f1 (Hz)")
stats_f2 = stats(f2_sim, "f2 (Hz)")
stats_K = stats(k_sim, "k (t/m)")
stats_M = stats(masa_sim, "m (t·s²/m)")

# ============================================================================
# 6. SENSIBILIDAD (SPEARMAN sin scipy)
# ============================================================================

def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean()
    ry -= ry.mean()
    denom = np.sqrt((rx**2).sum() * (ry**2).sum())
    return float((rx*ry).sum() / denom) if denom > 0 else 0.0

sens = {
    'E':    abs(spearman(E_sim, T1_sim)),
    'm':    abs(spearman(m_sim, T1_sim)),
    'I_col': abs(spearman(I_sim, T1_sim)),
    'He':   abs(spearman(He_sim, T1_sim)),
    'Cu':   abs(spearman(Cu_sim, T1_sim))
}

total_sens = sum(sens.values())
contrib = {k: v/total_sens*100 for k, v in sens.items()}

# ============================================================================
# 7. IMPRESIÓN EN CONSOLA
# ============================================================================

print(f"\n[VALORES NOMINALES]")
print(f"  E_nom       = {E_nom:.2f} t/m²")
print(f"  masa_piso   = {masa_piso_nom:.4f} t·s²/m")
print(f"  I_col       = {I_col_nom:.6f} m⁴")
print(f"  He          = {He_nom:.2f} m")
print(f"  Cu          = {Cu_nom:.3f} t/m²")
print(f"  k_entrepiso = {k_entrepiso_nom:.2f} t/m")

print(f"\n[VALORES TEÓRICOS DEL M07]")
print(f"  T₁ = {T1_nom:.4f} s | f₁ = {f1_nom:.4f} Hz")
print(f"  T₂ = {T2_nom:.4f} s | f₂ = {f2_nom:.4f} Hz")

print(f"\n[MONTE CARLO (N = {N})]")
print(f"  {'Variable':<12} {'Media':<10} {'Std':<10} {'COV':<10} {'P5':<10} {'P95':<10}")
print(f"  {'-'*65}")
for s in [stats_T1, stats_T2, stats_f1, stats_f2, stats_K, stats_M]:
    print(f"  {s['nombre']:<12} {s['media']:<10.4f} {s['std']:<10.4f} {s['cov']:<10.4f} {s['p5']:<10.4f} {s['p95']:<10.4f}")

print(f"\n[CONFIABILIDAD]")
print(f"  T₁_nom       = {T1_nom:.4f} s")
print(f"  Rango acept. = [{T1_min:.4f}, {T1_max:.4f}] s")
print(f"  P_falla      = {P_falla:.5f}")
print(f"  β            = {beta:.3f}")
print(f"  {'✅ CUMPLE (β > 3.5)' if beta > 3.5 else '⚠️ REVISAR'}")

print(f"\n[SENSIBILIDAD (Spearman)]")
for k, v in sorted(contrib.items(), key=lambda x: -x[1]):
    print(f"  {k:<8}: {v:6.2f} %")

print(f"\n[FRASE DEL PROYECTO]")
print(f"  {FRASE}")

print("\n" + "=" * 80)

# ============================================================================
# 8. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M07_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M07 - A5] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"MONTE CARLO N = {N}\n\n")
    f.write(f"VALORES NOMINALES:\n")
    f.write(f"  E = {E_nom:.2f} t/m²\n")
    f.write(f"  masa_piso = {masa_piso_nom:.4f} t·s²/m\n")
    f.write(f"  I_col = {I_col_nom:.6f} m⁴\n")
    f.write(f"  He = {He_nom:.2f} m\n")
    f.write(f"  Cu = {Cu_nom:.3f} t/m²\n")
    f.write(f"  k_entrepiso = {k_entrepiso_nom:.2f} t/m\n\n")
    f.write(f"VALORES TEÓRICOS:\n")
    f.write(f"  T1 = {T1_nom:.4f} s | f1 = {f1_nom:.4f} Hz\n")
    f.write(f"  T2 = {T2_nom:.4f} s | f2 = {f2_nom:.4f} Hz\n\n")
    f.write(f"ESTADÍSTICOS:\n")
    for s in [stats_T1, stats_T2, stats_f1, stats_f2, stats_K, stats_M]:
        f.write(f"  {s['nombre']}: media={s['media']:.4f}, std={s['std']:.4f}, COV={s['cov']:.4f}\n")
    f.write(f"\nCONFIABILIDAD:\n")
    f.write(f"  P_falla = {P_falla:.5f}\n")
    f.write(f"  β = {beta:.3f}\n\n")
    f.write(f"SENSIBILIDAD:\n")
    for k, v in sorted(contrib.items(), key=lambda x: -x[1]):
        f.write(f"  {k}: {v:.2f}%\n")
    f.write("\n" + "=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 9. DASHBOARD 9 PANELES
# ============================================================================

fig = plt.figure(figsize=(20, 14))
fig.suptitle(
    f'M07 — ESTOCÁSTICO MODAL — PÓRTICO 2 PISOS (N = {N})\n'
    f'{PROYECTO} | NINGÚN SOFTWARE COMERCIAL HACE ESTO',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.30)

# ------------------------------------------------------------------
# PANEL 1: Histograma T₁
# ------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(T1_sim, bins=40, color='#3498db', alpha=0.75, edgecolor='black')
ax1.axvline(T1_nom, color='red', linestyle='--', linewidth=2, label=f'Nominal = {T1_nom:.4f}')
ax1.axvline(stats_T1['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_T1["media"]:.4f}')
ax1.axvline(T1_min, color='gray', linestyle=':', linewidth=1.5, label=f'P5 = {T1_min:.4f}')
ax1.axvline(T1_max, color='gray', linestyle=':', linewidth=1.5, label=f'P95 = {T1_max:.4f}')
ax1.set_xlabel('T₁ (s)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title(f'(a) Distribución T₁ (N={N})', fontsize=11, fontweight='bold')
ax1.legend(fontsize=7)
ax1.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 2: Histograma T₂
# ------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(T2_sim, bins=40, color='#e74c3c', alpha=0.75, edgecolor='black')
ax2.axvline(T2_nom, color='blue', linestyle='--', linewidth=2, label=f'Nominal = {T2_nom:.4f}')
ax2.axvline(stats_T2['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_T2["media"]:.4f}')
ax2.set_xlabel('T₂ (s)', fontsize=10)
ax2.set_ylabel('Frecuencia', fontsize=10)
ax2.set_title(f'(b) Distribución T₂ (N={N})', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 3: Histograma f₁
# ------------------------------------------------------------------
ax3 = fig.add_subplot(gs[0, 2])
ax3.hist(f1_sim, bins=40, color='#2ecc71', alpha=0.75, edgecolor='black')
ax3.axvline(f1_nom, color='red', linestyle='--', linewidth=2, label=f'Nominal = {f1_nom:.4f}')
ax3.axvline(stats_f1['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_f1["media"]:.4f}')
ax3.set_xlabel('f₁ (Hz)', fontsize=10)
ax3.set_ylabel('Frecuencia', fontsize=10)
ax3.set_title(f'(c) Distribución f₁', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 4: Histograma f₂
# ------------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 0])
ax4.hist(f2_sim, bins=40, color='#9b59b6', alpha=0.75, edgecolor='black')
ax4.axvline(f2_nom, color='red', linestyle='--', linewidth=2, label=f'Nominal = {f2_nom:.4f}')
ax4.axvline(stats_f2['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_f2["media"]:.4f}')
ax4.set_xlabel('f₂ (Hz)', fontsize=10)
ax4.set_ylabel('Frecuencia', fontsize=10)
ax4.set_title(f'(d) Distribución f₂', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 5: Histograma K
# ------------------------------------------------------------------
ax5 = fig.add_subplot(gs[1, 1])
ax5.hist(k_sim, bins=40, color='#f39c12', alpha=0.75, edgecolor='black')
ax5.axvline(k_entrepiso_nom, color='red', linestyle='--', linewidth=2,
            label=f'Nominal = {k_entrepiso_nom:.0f}')
ax5.axvline(stats_K['media'], color='orange', linestyle='-', linewidth=2,
            label=f'Media = {stats_K["media"]:.0f}')
ax5.set_xlabel('k_entrepiso (t/m)', fontsize=10)
ax5.set_ylabel('Frecuencia', fontsize=10)
ax5.set_title('(e) Distribución k', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 6: Histograma M
# ------------------------------------------------------------------
ax6 = fig.add_subplot(gs[1, 2])
ax6.hist(masa_sim, bins=40, color='#1abc9c', alpha=0.75, edgecolor='black')
ax6.axvline(masa_piso_nom, color='red', linestyle='--', linewidth=2,
            label=f'Nominal = {masa_piso_nom:.4f}')
ax6.axvline(stats_M['media'], color='orange', linestyle='-', linewidth=2,
            label=f'Media = {stats_M["media"]:.4f}')
ax6.set_xlabel('m (t·s²/m)', fontsize=10)
ax6.set_ylabel('Frecuencia', fontsize=10)
ax6.set_title('(f) Distribución m', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# PANEL 7: Sensibilidad (Spearman)
# ------------------------------------------------------------------
ax7 = fig.add_subplot(gs[2, 0])
keys = list(contrib.keys())
vals = list(contrib.values())
colores = plt.cm.viridis(np.linspace(0.2, 0.9, len(keys)))
bars = ax7.barh(keys, vals, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, vals):
    ax7.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
ax7.set_xlabel('Contribución a la varianza de T₁ (%)', fontsize=10)
ax7.set_title('(g) Sensibilidad (Spearman)', fontsize=11, fontweight='bold')
ax7.grid(True, alpha=0.3, axis='x')
ax7.set_xlim(0, max(vals) * 1.25)

# ------------------------------------------------------------------
# PANEL 8: Confiabilidad β / P_falla
# ------------------------------------------------------------------
ax8 = fig.add_subplot(gs[2, 1])
ax8.axis('off')

confiabilidad = (
    f"CONFIABILIDAD\n"
    f"{'─' * 35}\n"
    f"Valores nominales:\n"
    f"  T₁_nom = {T1_nom:.4f} s\n"
    f"  Rango = [{T1_min:.4f}, {T1_max:.4f}] s\n"
    f"  σ_T1 = {sigma_T1:.4f} s\n"
    f"{'─' * 35}\n"
    f"Resultados:\n"
    f"  P_falla = {P_falla:.5f}\n"
    f"  β       = {beta:.3f}\n"
    f"{'─' * 35}\n"
    f"Criterio (β > 3.5):\n"
    f"  {'✅ CUMPLE' if beta > 3.5 else '⚠️ REVISAR'}"
)

ax8.text(0.02, 0.98, confiabilidad, transform=ax8.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='#2c3e50', linewidth=2))

# ------------------------------------------------------------------
# PANEL 9: Tabla resumen
# ------------------------------------------------------------------
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

resumen = (
    f"RESUMEN ESTOCÁSTICO\n"
    f"{'─' * 35}\n"
    f"N = {N}\n"
    f"{'─' * 35}\n"
    f"T₁: media = {stats_T1['media']:.4f} s\n"
    f"    P5 = {stats_T1['p5']:.4f} | P95 = {stats_T1['p95']:.4f}\n"
    f"    COV = {stats_T1['cov']:.4f}\n"
    f"{'─' * 35}\n"
    f"T₂: media = {stats_T2['media']:.4f} s\n"
    f"    P5 = {stats_T2['p5']:.4f} | P95 = {stats_T2['p95']:.4f}\n"
    f"{'─' * 35}\n"
    f"f₁: media = {stats_f1['media']:.4f} Hz\n"
    f"f₂: media = {stats_f2['media']:.4f} Hz\n"
    f"{'─' * 35}\n"
    f"k:  media = {stats_K['media']:.0f} t/m\n"
    f"m:  media = {stats_M['media']:.4f} t·s²/m\n"
    f"{'─' * 35}\n"
    f"P_falla = {P_falla:.5f}\n"
    f"β = {beta:.3f}\n"
    f"{'─' * 35}\n"
    f"{'✅ CUMPLE' if beta > 3.5 else '⚠️ REVISAR'}"
)

ax9.text(0.02, 0.98, resumen, transform=ax9.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.96])

nombre_img = f"dashboard_M07_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120, bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando gráfica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 80)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 80)