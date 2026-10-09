# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 05 - ALGORITMO 2: MODELO ESTOCASTICO DEL AS DE COLUMNA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 Cap. 18 + NEC-15
OBJETIVO: Modelo estocastico Monte Carlo del As de columna
          - Distribucion de As (N=1000)
          - Confiabilidad beta
          - Probabilidad de falla P_falla
          - Sensibilidad (Spearman)
          - Comparacion con Algoritmo 1 (determinista)
          NINGUN SOFTWARE COMERCIAL HACE ESTO
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
    print("matplotlib no esta instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "MODELO ESTOCASTICO DEL AS DE COLUMNA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 Cap. 18 + NEC-15"
FRASE = "La incertidumbre no se elimina: se cuantifica."

# ============================================================================
# 2. DATOS BASE (del Excel)
# ============================================================================

L1 = 6.20
L2 = 5.90
L3 = 5.70
L4 = 6.00

Cm1_nom = 0.62
Cv1_nom = 0.20
Pisos = 2

fc_nom = 210
fy_nom = 4200
Es = 2.1e6

ancho_nom = 38
prof_nom = 38
rec = 2.5
phi_long = 14
phi_esq = 16
phi_est = 10
var_a = 4
var_p = 4

He = 3.0
H_viga = 0.30
Fm = 1.2

# Valores nominales
At = (L1/2 + L2/2) * (L3/2 + L4/2)
Cu_nom = 1.2 * (Cm1_nom * Pisos) + 1.6 * (Cv1_nom * Pisos)
Pu_nom = At * Cu_nom * Fm

Ag_col = ancho_nom * prof_nom
num_varillas = var_a * 2 + (var_p - 2) * 2
As_nom = 4 * 0.00785 * phi_esq**2 + (num_varillas - 4) * 0.00785 * phi_long**2
rho_nom = As_nom / Ag_col * 100

# Coeficientes de variacion
COV_Cu = 0.10
COV_fc = 0.15
COV_fy = 0.05
COV_b = 0.03
COV_h = 0.03

N = 1000

# ============================================================================
# 3. MODELO ESTOCASTICO - MONTE CARLO
# ============================================================================

np.random.seed(42)

print(f"\n[EJECUTANDO MONTE CARLO] N = {N} simulaciones...")

# Variables aleatorias
Cu_sim = np.random.normal(Cu_nom, COV_Cu * Cu_nom, N)
fc_sim = np.random.lognormal(
    np.log(fc_nom) - 0.5 * np.log(1 + COV_fc**2),
    np.sqrt(np.log(1 + COV_fc**2)), N
)
fy_sim = np.random.normal(fy_nom, COV_fy * fy_nom, N)
b_sim = np.random.normal(ancho_nom, COV_b * ancho_nom, N)
h_sim = np.random.normal(prof_nom, COV_h * prof_nom, N)

# Asegurar valores fisicos
Cu_sim = np.clip(Cu_sim, 0.8 * Cu_nom, 1.2 * Cu_nom)
fc_sim = np.clip(fc_sim, 150, 280)
fy_sim = np.clip(fy_sim, 3800, 4600)
b_sim = np.clip(b_sim, 0.95 * ancho_nom, 1.05 * ancho_nom)
h_sim = np.clip(h_sim, 0.95 * prof_nom, 1.05 * prof_nom)

# Calculos vectorizados
Pu_sim = At * Cu_sim * Fm
Ag_sim = b_sim * h_sim
Ag_req_sim = 3 * Pu_sim * 1000 / (0.85 * fc_sim + 0.012 * fy_sim)

# As requerido (por cuantia minima 1.2% del Ag real)
As_min_sim = 0.012 * Ag_sim

# As requerido si Ag < Ag_req (aumentar cuantia)
As_req_sim = np.where(Ag_sim >= Ag_req_sim, As_min_sim, 0.012 * Ag_req_sim)

# Cuantia
rho_sim = As_req_sim / Ag_sim * 100

# P_falla (si Ag < Ag_req)
P_falla = np.mean(Ag_sim < Ag_req_sim)

# Confiabilidad beta
ratio = Ag_sim / Ag_req_sim
if np.std(np.log(ratio)) > 0:
    beta = np.mean(np.log(ratio)) / np.std(np.log(ratio))
else:
    beta = 0

# ============================================================================
# 4. ESTADISTICOS
# ============================================================================

def stats(arr, nombre):
    media = np.mean(arr)
    std = np.std(arr)
    cov = std / media if media != 0 else 0
    p5 = np.percentile(arr, 5)
    p50 = np.percentile(arr, 50)
    p95 = np.percentile(arr, 95)
    return {"nombre": nombre, "media": media, "std": std, "cov": cov, "p5": p5, "p50": p50, "p95": p95}

stats_As = stats(As_req_sim, "As")
stats_Pu = stats(Pu_sim, "Pu")
stats_Ag = stats(Ag_sim, "Ag")
stats_rho = stats(rho_sim, "rho")

# ============================================================================
# 5. SENSIBILIDAD (SPEARMAN sin scipy)
# ============================================================================

def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean()
    ry -= ry.mean()
    denom = np.sqrt((rx**2).sum() * (ry**2).sum())
    return float((rx*ry).sum()/denom) if denom > 0 else 0.0

sens = {
    'Cu': abs(spearman(Cu_sim, As_req_sim)),
    'fc': abs(spearman(fc_sim, As_req_sim)),
    'fy': abs(spearman(fy_sim, As_req_sim)),
    'b':  abs(spearman(b_sim, As_req_sim)),
    'h':  abs(spearman(h_sim, As_req_sim))
}

total_sens = sum(sens.values())
contrib = {k: v/total_sens*100 for k, v in sens.items()}

# ============================================================================
# 6. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M05 - A2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- VALORES NOMINALES ---")
print(f"  At = {At:.2f} m2")
print(f"  Cu = {Cu_nom:.4f} t/m2")
print(f"  Pu = {Pu_nom:.2f} t")
print(f"  Ag = {Ag_col} cm2")
print(f"  As = {As_nom:.2f} cm2")
print(f"  rho = {rho_nom:.2f}%")

print(f"\n--- MONTE CARLO (N = {N}) ---")
print(f"  {'Variable':<10} {'Media':<10} {'Std':<10} {'COV':<10} {'P5':<10} {'P95':<10}")
print(f"  {'-'*65}")
for s in [stats_As, stats_Pu, stats_Ag, stats_rho]:
    print(f"  {s['nombre']:<10} {s['media']:<10.3f} {s['std']:<10.3f} {s['cov']:<10.4f} {s['p5']:<10.3f} {s['p95']:<10.3f}")

print(f"\n--- CONFIABILIDAD ---")
print(f"  P_falla = {P_falla:.5f}")
print(f"  beta = {beta:.3f}")
print(f"  {'CUMPLE (beta > 3.5)' if beta > 3.5 else 'REVISAR'}")

print(f"\n--- SENSIBILIDAD (Spearman) ---")
for k, v in sorted(contrib.items(), key=lambda x: -x[1]):
    print(f"  {k:<6}: {v:6.2f} %")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M05"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M05_algoritmo2_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M05 - A2] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[NORMA] {NORMA}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"MONTE CARLO N = {N}\n\n")
    f.write(f"ESTADISTICOS:\n")
    for s in [stats_As, stats_Pu, stats_Ag, stats_rho]:
        f.write(f"  {s['nombre']}: media={s['media']:.3f}, std={s['std']:.3f}, COV={s['cov']:.4f}\n")
    f.write(f"\nCONFIABILIDAD:\n")
    f.write(f"  P_falla = {P_falla:.5f}\n")
    f.write(f"  beta = {beta:.3f}\n\n")
    f.write(f"SENSIBILIDAD:\n")
    for k, v in sorted(contrib.items(), key=lambda x: -x[1]):
        f.write(f"  {k}: {v:.2f}%\n")
    f.write("\n" + "=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 8. DASHBOARD 2D (6 PANELES)
# ============================================================================

fig1 = plt.figure(figsize=(20, 14), num='M05-A2: Modelo Estocastico Columna')
fig1.suptitle(
    f"M05 - ALGORITMO 2: MODELO ESTOCASTICO DEL AS DE COLUMNA (N={N})\n"
    f"{PROYECTO} | {NORMA} | NINGUN SOFTWARE COMERCIAL HACE ESTO",
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs1 = GridSpec(3, 2, figure=fig1, hspace=0.45, wspace=0.30)

# (a) Distribucion de As
ax1 = fig1.add_subplot(gs1[0, 0])
ax1.hist(As_req_sim, bins=40, color='#3498db', alpha=0.75, edgecolor='black')
ax1.axvline(As_nom, color='red', linestyle='--', linewidth=2, label=f'Nominal = {As_nom:.2f}')
ax1.axvline(stats_As['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_As["media"]:.2f}')
ax1.axvline(stats_As['p95'], color='darkred', linestyle=':', linewidth=2, label=f'P95 = {stats_As["p95"]:.2f}')
ax1.set_xlabel('As (cm2)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title(f'(a) Distribucion de As (N={N})', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# (b) Distribucion de Pu
ax2 = fig1.add_subplot(gs1[0, 1])
ax2.hist(Pu_sim, bins=40, color='#e74c3c', alpha=0.75, edgecolor='black')
ax2.axvline(Pu_nom, color='blue', linestyle='--', linewidth=2, label=f'Nominal = {Pu_nom:.2f}')
ax2.axvline(stats_Pu['media'], color='orange', linestyle='-', linewidth=2, label=f'Media = {stats_Pu["media"]:.2f}')
ax2.set_xlabel('Pu (t)', fontsize=10)
ax2.set_ylabel('Frecuencia', fontsize=10)
ax2.set_title('(b) Distribucion de Pu', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# (c) Confiabilidad - Ag vs Ag_req
ax3 = fig1.add_subplot(gs1[1, 0])
ax3.hist(Ag_sim, bins=40, color='#2ecc71', alpha=0.6, edgecolor='black', label='Ag (col)')
ax3.hist(Ag_req_sim, bins=40, color='#e74c3c', alpha=0.6, edgecolor='black', label='Ag_req')
ax3.axvline(np.percentile(Ag_sim, 5), color='darkgreen', linestyle='--', linewidth=2, label=f'Ag P5 = {np.percentile(Ag_sim, 5):.0f}')
ax3.axvline(np.percentile(Ag_req_sim, 95), color='darkred', linestyle='--', linewidth=2, label=f'Ag_req P95 = {np.percentile(Ag_req_sim, 95):.0f}')
ax3.set_xlabel('Area (cm2)', fontsize=10)
ax3.set_ylabel('Frecuencia', fontsize=10)
ax3.set_title(f'(c) Ag vs Ag_req\nP_falla = {P_falla:.5f} | beta = {beta:.3f}', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# (d) Distribucion de rho
ax4 = fig1.add_subplot(gs1[1, 1])
ax4.hist(rho_sim, bins=40, color='#9b59b6', alpha=0.75, edgecolor='black')
ax4.axvline(rho_nom, color='red', linestyle='--', linewidth=2, label=f'Nominal = {rho_nom:.2f}%')
ax4.axvline(1.2, color='orange', linestyle=':', linewidth=2, label='Min = 1.2%')
ax4.axvline(4.0, color='darkred', linestyle=':', linewidth=2, label='Max = 4%')
ax4.set_xlabel('rho (%)', fontsize=10)
ax4.set_ylabel('Frecuencia', fontsize=10)
ax4.set_title('(d) Distribucion de rho', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# (e) Sensibilidad (Spearman)
ax5 = fig1.add_subplot(gs1[2, 0])
keys = list(contrib.keys())
vals = list(contrib.values())
colores = plt.cm.viridis(np.linspace(0.2, 0.9, len(keys)))
bars = ax5.barh(keys, vals, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, vals):
    ax5.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
ax5.set_xlabel('Contribucion a la varianza de As (%)', fontsize=10)
ax5.set_title('(e) Sensibilidad (Spearman)', fontsize=11, fontweight='bold')
ax5.grid(True, alpha=0.3, axis='x')
ax5.set_xlim(0, max(vals)*1.25)

# (f) Ficha tecnica
ax6 = fig1.add_subplot(gs1[2, 1])
ax6.axis('off')

ficha = (
    f"FICHA TECNICA ESTOCASTICA\n"
    f"{'=' * 45}\n"
    f"MONTE CARLO N = {N}\n"
    f"{'=' * 45}\n"
    f"VARIABLES ALEATORIAS:\n"
    f"  Cu ~ Normal (COV = 10%)\n"
    f"  fc ~ Lognormal (COV = 15%)\n"
    f"  fy ~ Normal (COV = 5%)\n"
    f"  b  ~ Normal (COV = 3%)\n"
    f"  h  ~ Normal (COV = 3%)\n"
    f"{'=' * 45}\n"
    f"RESULTADOS:\n"
    f"  As medio = {stats_As['media']:.2f} cm2\n"
    f"  As P5    = {stats_As['p5']:.2f} cm2\n"
    f"  As P95   = {stats_As['p95']:.2f} cm2\n"
    f"  rho medio = {stats_rho['media']:.2f}%\n"
    f"{'=' * 45}\n"
    f"CONFIABILIDAD:\n"
    f"  P_falla = {P_falla:.5f}\n"
    f"  beta = {beta:.3f}\n"
    f"{'=' * 45}\n"
    f"SENSIBILIDAD:\n"
    f"  Cu : {contrib['Cu']:.1f}%\n"
    f"  fc : {contrib['fc']:.1f}%\n"
    f"  fy : {contrib['fy']:.1f}%\n"
    f"  b  : {contrib['b']:.1f}%\n"
    f"  h  : {contrib['h']:.1f}%\n"
    f"{'=' * 45}\n"
    f"{'CUMPLE (beta > 3.5)' if beta > 3.5 else 'REVISAR'}"
)

ax6.text(0.02, 0.98, ficha, transform=ax6.transAxes,
         fontsize=8.5, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout()
plt.savefig('M05_A2_dashboard_estocastico.png', dpi=150, bbox_inches='tight')
print(f"\nDashboard 2D guardado: M05_A2_dashboard_estocastico.png")
plt.show(block=False)

# ============================================================================
# 9. MODELO 3D DE COLUMNA CON DISTRIBUCION
# ============================================================================

fig2 = plt.figure(figsize=(18, 12), num='M05-A2: Modelo 3D Estocastico')
ax = fig2.add_subplot(111, projection='3d')

fig2.suptitle(
    f"M05 - ALGORITMO 2: MODELO 3D CON DISTRIBUCION ESTOCASTICA\n"
    f"As medio = {stats_As['media']:.2f} cm2 | P_falla = {P_falla:.5f} | beta = {beta:.3f}",
    fontsize=14, fontweight='bold', color='#2c3e50'
)

b_3d = ancho_nom / 100
h_3d = prof_nom / 100
L_3d = He

# Columna
x = np.array([0, b_3d, b_3d, 0, 0])
y = np.array([0, 0, h_3d, h_3d, 0])

for z in [0, L_3d]:
    ax.plot(x, y, zs=z, color='black', linewidth=2)
for i in range(4):
    ax.plot([x[i], x[i]], [y[i], y[i]], [0, L_3d], color='black', linewidth=2)

# 12 varillas simetricas
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
x_ini = rec/100 + phi_est/1000 + phi_esq/2000
x_fin = b_3d - rec/100 - phi_est/1000 - phi_esq/2000
y_ini = rec/100 + phi_est/1000 + phi_esq/2000
y_fin = h_3d - rec/100 - phi_est/1000 - phi_esq/2000

# 4 esquinas
for xv, yv in [(x_ini, y_fin), (x_fin, y_fin), (x_ini, y_ini), (x_fin, y_ini)]:
    ax.plot([xv, xv], [yv, yv], [0, L_3d], color='red', linewidth=4, zorder=10)

# 2 arriba + 2 abajo
espacio_h = (x_fin - x_ini) / 3
for i in range(1, 3):
    x_pos = x_ini + i * espacio_h
    ax.plot([x_pos, x_pos], [y_fin, y_fin], [0, L_3d], color='orange', linewidth=3, zorder=10)
    ax.plot([x_pos, x_pos], [y_ini, y_ini], [0, L_3d], color='orange', linewidth=3, zorder=10)

# 2 izq + 2 der
espacio_v = (y_fin - y_ini) / 3
for i in range(1, 3):
    y_pos = y_ini + i * espacio_v
    ax.plot([x_ini, x_ini], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)
    ax.plot([x_fin, x_fin], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)

# Estribos
for z in np.linspace(0, L_3d, 15):
    ax.plot(x, y, zs=z, color='gray', linewidth=1, alpha=0.5)

# Etiquetas
tic_3d = (
    f"MODELO ESTOCASTICO\n"
    f"As medio = {stats_As['media']:.2f} cm2\n"
    f"As P5 = {stats_As['p5']:.2f} cm2\n"
    f"As P95 = {stats_As['p95']:.2f} cm2\n"
    f"P_falla = {P_falla:.5f}\n"
    f"beta = {beta:.3f}"
)
ax.text(b_3d/2, h_3d/2, L_3d + 0.3, tic_3d, color='darkgreen', fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='green', linewidth=2))

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.set_title('Modelo 3D - Columna con Distribucion Estocastica', fontsize=13, fontweight='bold')
ax.view_init(elev=20, azim=-55)

plt.tight_layout()
plt.savefig('M05_A2_modelo_3D_estocastico.png', dpi=150, bbox_inches='tight')
print(f"Modelo 3D guardado: M05_A2_modelo_3D_estocastico.png")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)