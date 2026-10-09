# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 05 - ALGORITMO 1: DISENO ANALITICO DE COLUMNA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 Cap. 18 + NEC-15
OBJETIVO: Diseno analitico de columna (replica del Excel)
          - Area tributaria At = 35.39 m2
          - Carga ultima Cu = 2.128 t/m2
          - Carga axial Pu = 90.44 t
          - Predimensionamiento Ag_req = 1190.03 cm2
          - Seccion 38 x 38 cm
          - As = 20.35 cm2 (12 varillas)
          - rho = 1.41%
          - Redistribucion SIMETRICA por EJE
          - 4 varillas eje horizontal + 4 varillas eje vertical
          - Lo = 50 cm | s_prot = 8.4 cm | s_cent = 8.4 cm
          Dashboard 2D + Modelo 3D
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
    from matplotlib.patches import Rectangle, Circle
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("matplotlib no esta instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "DISENO ANALITICO DE COLUMNA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 Cap. 18 + NEC-15"
FRASE = "Los numeros son solo el vehiculo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (del Excel)
# ============================================================================

L1 = 6.20
L2 = 5.90
L3 = 5.70
L4 = 6.00

Cm1 = 0.62
Cv1 = 0.20
Pisos = 2

fc = 210
fy = 4200

ancho_col = 38
prof_col = 38
rec = 2.5

phi_long = 14
phi_esq = 16
phi_est = 10
var_a = 4
var_p = 4

He = 3.0
H_viga = 0.30
Fm = 1.2

# ============================================================================
# 3. CALCULOS (Excel)
# ============================================================================

At = (L1/2 + L2/2) * (L3/2 + L4/2)
Cu = 1.2 * (Cm1 * Pisos) + 1.6 * (Cv1 * Pisos)
Pu = At * Cu * Fm
Ag_req = 3 * Pu * 1000 / (0.85 * fc + 0.012 * fy)

Ag_col = ancho_col * prof_col

bc = ancho_col - 2 * rec - phi_est / 10
pc = prof_col - 2 * rec - phi_est / 10

# Numero de varillas por eje (EXCEL)
num_varillas = var_a * 2 + (var_p - 2) * 2

As = 4 * 0.00785 * phi_esq**2 + (num_varillas - 4) * 0.00785 * phi_long**2

cuantia = As / Ag_col
cuantia_pct = cuantia * 100

Lo = max(45, max(ancho_col, prof_col), He * 16.6666666666667)
s_prot = min(6 * min(phi_long, phi_esq) / 10, 10)

Ash = max(
    0.3 * bc * Lo * fc / fy * (Ag_col / bc / pc - 1),
    0.09 * bc * Lo * fc / fy
)

ramas = Ash / (0.00785 * phi_est**2)

Lc = He * 100 - H_viga * 100 - 2 * phi_long

Ash_central = max(
    0.3 * bc * Lc * fc / fy * (Ag_col / bc / pc - 1),
    0.09 * bc * Lc * fc / fy
)

ramas_central = Ash_central / (0.00785 * phi_est**2)
s_cent = min(6 * min(phi_long, phi_esq) / 10, 15)

sep_a = (bc - phi_est/10 - 2*phi_esq/10 - (var_a - 2)*phi_long/10) / (var_a - 1)
sep_p = (pc - phi_est/10 - 2*phi_esq/10 - (var_p - 2)*phi_long/10) / (var_p - 1)

# ============================================================================
# 4. VERIFICACIONES
# ============================================================================

tic_seccion = Ag_col >= Ag_req
tic_cuantia_min = cuantia >= 0.012
tic_cuantia_max = cuantia <= 0.04
tic_s_prot = s_prot <= 10
tic_s_cent = s_cent <= 15
tic_sep = sep_a >= 2.5 and sep_p >= 2.5

# ============================================================================
# 5. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M05 - A1] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- AREA TRIBUTARIA ---")
print(f"  At = {At:.4f} m2")

print(f"\n--- CARGA ULTIMA ---")
print(f"  Cu = {Cu:.4f} t/m2")

print(f"\n--- CARGA AXIAL ---")
print(f"  Pu = {Pu:.4f} t")

print(f"\n--- PREDIMENSIONAMIENTO ---")
print(f"  Ag_req = {Ag_req:.2f} cm2")

print(f"\n--- SECCION ---")
print(f"  Seccion = {ancho_col} x {prof_col} cm")
print(f"  Ag = {Ag_col} cm2")
print(f"  {'CUMPLE' if tic_seccion else 'NO CUMPLE'}")

print(f"\n--- ACERO (por eje) ---")
print(f"  var_a = {var_a} (eje horizontal)")
print(f"  var_p = {var_p} (eje vertical)")
print(f"  num = {num_varillas} varillas")
print(f"  As = {As:.4f} cm2")
print(f"  rho = {cuantia_pct:.2f}%")
print(f"  {'CUMPLE (1.2% <= rho <= 4%)' if (tic_cuantia_min and tic_cuantia_max) else 'REVISAR'}")

print(f"\n--- ESTRIBOS ---")
print(f"  Lo = {Lo:.2f} cm")
print(f"  s_prot = {s_prot:.2f} cm")
print(f"  s_cent = {s_cent:.2f} cm")
print(f"  Ash = {Ash:.4f} cm2")
print(f"  ramas = {ramas:.4f} u")

print(f"\n--- VERIFICACIONES ---")
print(f"  TIC 1: Ag_col >= Ag_req    -> {'CUMPLE' if tic_seccion else 'NO'}")
print(f"  TIC 2: rho >= 1.2%         -> {'CUMPLE' if tic_cuantia_min else 'NO'}")
print(f"  TIC 3: rho <= 4%           -> {'CUMPLE' if tic_cuantia_max else 'NO'}")
print(f"  TIC 4: s_prot <= 10 cm     -> {'CUMPLE' if tic_s_prot else 'NO'}")
print(f"  TIC 5: s_cent <= 15 cm     -> {'CUMPLE' if tic_s_cent else 'NO'}")
print(f"  TIC 6: sep varillas >= 2.5 -> {'CUMPLE' if tic_sep else 'NO'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 6. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M05"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M05_algoritmo1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M05 - A1] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[NORMA] {NORMA}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"AREA TRIBUTARIA: {At:.4f} m2\n")
    f.write(f"CARGA ULTIMA: {Cu:.4f} t/m2\n")
    f.write(f"CARGA AXIAL: {Pu:.4f} t\n")
    f.write(f"PREDIMENSIONAMIENTO: {Ag_req:.2f} cm2\n")
    f.write(f"SECCION: {ancho_col} x {prof_col} cm\n")
    f.write(f"Ag: {Ag_col} cm2\n")
    f.write(f"ACERO: num={num_varillas}, As={As:.4f} cm2, rho={cuantia_pct:.2f}%\n")
    f.write(f"ESTRIBOS: Lo={Lo:.2f}, s_prot={s_prot:.2f}, s_cent={s_cent:.2f}\n")
    f.write(f"Ash: {Ash:.4f} cm2, ramas: {ramas:.4f} u\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 7. DASHBOARD 2D
# ============================================================================

fig = plt.figure(figsize=(18, 12), num='M05-A1: Dashboard Columna')
fig.suptitle(
    f"M05 - ALGORITMO 1: DISENO ANALITICO DE COLUMNA\n"
    f"{PROYECTO} | {NORMA}",
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1],
              height_ratios=[1.2, 1], hspace=0.35, wspace=0.30)

# --------------------------------------------------------
# (a) Seccion transversal - REDISTRIBUCION SIMETRICA POR EJE
# --------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-5, ancho_col + 15)
ax1.set_ylim(-15, prof_col + 5)
ax1.set_aspect('equal')
ax1.add_patch(Rectangle((0, 0), ancho_col, prof_col,
                         linewidth=3, edgecolor='black', facecolor='#e8e8e8'))
ax1.add_patch(Rectangle((rec, rec), ancho_col - 2*rec, prof_col - 2*rec,
                         linewidth=2, edgecolor='blue', facecolor='none'))

# Coordenadas base
x_ini = rec + phi_est/10 + phi_esq/20
x_fin = ancho_col - rec - phi_est/10 - phi_esq/20
y_ini = rec + phi_est/10 + phi_esq/20
y_fin = prof_col - rec - phi_est/10 - phi_esq/20

# --- 4 ESQUINAS (φ16, rojas) ---
ax1.add_patch(Circle((x_ini, y_fin), phi_esq/20, color='red', zorder=10))
ax1.add_patch(Circle((x_fin, y_fin), phi_esq/20, color='red', zorder=10))
ax1.add_patch(Circle((x_ini, y_ini), phi_esq/20, color='red', zorder=10))
ax1.add_patch(Circle((x_fin, y_ini), phi_esq/20, color='red', zorder=10))

# --- 2 varillas ARRIBA (φ14, entre esquinas) ---
# var_a = 4 → 4 varillas por eje horizontal, 2 son esquinas, 2 intermedias
espacio_horiz = (x_fin - x_ini) / (var_a - 1)
for i in range(1, var_a - 1):
    x_pos = x_ini + i * espacio_horiz
    ax1.add_patch(Circle((x_pos, y_fin), phi_long/20, color='orange', zorder=10))

# --- 2 varillas ABAJO (φ14, entre esquinas) ---
for i in range(1, var_a - 1):
    x_pos = x_ini + i * espacio_horiz
    ax1.add_patch(Circle((x_pos, y_ini), phi_long/20, color='orange', zorder=10))

# --- 2 varillas LATERALES IZQUIERDA (φ14, entre esquinas) ---
espacio_vert = (y_fin - y_ini) / (var_p - 1)
for i in range(1, var_p - 1):
    y_pos = y_ini + i * espacio_vert
    ax1.add_patch(Circle((x_ini, y_pos), phi_long/20, color='orange', zorder=10))

# --- 2 varillas LATERALES DERECHA (φ14, entre esquinas) ---
for i in range(1, var_p - 1):
    y_pos = y_ini + i * espacio_vert
    ax1.add_patch(Circle((x_fin, y_pos), phi_long/20, color='orange', zorder=10))

# Cotas
ax1.annotate('', xy=(0, -6), xytext=(ancho_col, -6), arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(ancho_col/2, -12, f'b = {ancho_col} cm', ha='center', fontsize=10, fontweight='bold')
ax1.annotate('', xy=(ancho_col + 6, 0), xytext=(ancho_col + 6, prof_col), arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(ancho_col + 12, prof_col/2, f'h = {prof_col} cm', va='center', fontsize=10, fontweight='bold', rotation=90)

ax1.set_title(f'(a) Seccion 38x38 cm - {num_varillas} varillas (simetria por eje)', fontsize=11, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.axis('off')

# --------------------------------------------------------
# (b) Distribucion de estribos
# --------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, He * 100)
ax2.set_ylim(-5, 15)
ax2.add_patch(Rectangle((0, 0), He * 100, 10, facecolor='#e8e8e8', edgecolor='black'))
ax2.axvspan(0, Lo, alpha=0.3, color='red')
ax2.axvspan(He * 100 - Lo, He * 100, alpha=0.3, color='red')
ax2.axvspan(Lo, He * 100 - Lo, alpha=0.2, color='blue')

n_est_prot = int(Lo / s_prot) + 1
for i in range(n_est_prot):
    x = i * s_prot
    ax2.plot([x, x], [0, 10], color='red', linewidth=2)
for i in range(n_est_prot):
    x = He * 100 - i * s_prot
    ax2.plot([x, x], [0, 10], color='red', linewidth=2)

n_est_cent = int((He * 100 - 2 * Lo) / s_cent)
for i in range(n_est_cent):
    x = Lo + i * s_cent
    ax2.plot([x, x], [0, 10], color='blue', linewidth=1.5)

ax2.text(Lo/2, 12, f'Lo={Lo:.0f}\ns={s_prot:.1f}', ha='center', fontsize=9, color='red', fontweight='bold')
ax2.text(He*100/2, 12, f's={s_cent:.1f}', ha='center', fontsize=9, color='blue', fontweight='bold')
ax2.text(He*100 - Lo/2, 12, f'Lo={Lo:.0f}\ns={s_prot:.1f}', ha='center', fontsize=9, color='red', fontweight='bold')

ax2.set_title('(b) Distribucion de estribos', fontsize=12, fontweight='bold')
ax2.set_xlabel('Altura (cm)', fontsize=10)
ax2.set_yticks([])
ax2.grid(True, alpha=0.3)

# --------------------------------------------------------
# (c) Barras comparativas
# --------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 0])
categorias = ['Ag_req', 'Ag_col']
valores = [Ag_req, Ag_col]
colores = ['#e74c3c', '#2ecc71']
bars = ax3.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5, width=0.5)
for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax3.set_ylabel('Area (cm2)', fontsize=10)
ax3.set_title(f'(c) Verificacion de Seccion', fontsize=12, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.set_ylim(0, max(valores) * 1.2)

# --------------------------------------------------------
# (d) Ficha tecnica
# --------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

ficha = (
    f"FICHA TECNICA - COLUMNA\n"
    f"{'-' * 40}\n"
    f"Proyecto: UNESUM-REZ-2026\n"
    f"Norma: {NORMA}\n"
    f"{'-' * 40}\n"
    f"GEOMETRIA:\n"
    f"  At = {At:.2f} m2\n"
    f"  Cu = {Cu:.3f} t/m2\n"
    f"  Pu = {Pu:.2f} t\n"
    f"{'-' * 40}\n"
    f"SECCION:\n"
    f"  Ag_req = {Ag_req:.0f} cm2\n"
    f"  Seccion = {ancho_col} x {prof_col} cm\n"
    f"  Ag = {Ag_col} cm2\n"
    f"{'-' * 40}\n"
    f"ACERO (por eje):\n"
    f"  var_a = {var_a} (horizontal)\n"
    f"  var_p = {var_p} (vertical)\n"
    f"  num = {num_varillas} varillas\n"
    f"  As = {As:.2f} cm2\n"
    f"  rho = {cuantia_pct:.2f}%\n"
    f"{'-' * 40}\n"
    f"ESTRIBOS:\n"
    f"  Lo = {Lo:.0f} cm\n"
    f"  s_prot = {s_prot:.1f} cm\n"
    f"  s_cent = {s_cent:.1f} cm\n"
    f"  Ash = {Ash:.2f} cm2\n"
    f"  ramas = {ramas:.2f} u\n"
    f"{'-' * 40}\n"
    f"{'CUMPLE' if (tic_seccion and tic_cuantia_min and tic_s_prot and tic_s_cent) else 'REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout()
plt.savefig('M05_A1_dashboard_2D.png', dpi=150, bbox_inches='tight')
print(f"\nDashboard 2D guardado: M05_A1_dashboard_2D.png")
plt.show(block=False)

# ============================================================================
# 8. MODELO 3D
# ============================================================================

fig2 = plt.figure(figsize=(16, 12), num='M05-A1: Modelo 3D Columna')
ax = fig2.add_subplot(111, projection='3d')

fig2.suptitle(
    f"M05 - ALGORITMO 1: MODELO 3D DE COLUMNA (SIMETRIA POR EJE)\n"
    f"Seccion {ancho_col}x{prof_col} cm | {num_varillas} varillas | Lo = {Lo:.0f} cm",
    fontsize=14, fontweight='bold', color='#2c3e50'
)

b_3d = ancho_col / 100
h_3d = prof_col / 100
L_3d = He

x = np.array([0, b_3d, b_3d, 0, 0])
y = np.array([0, 0, h_3d, h_3d, 0])

for z in [0, L_3d]:
    ax.plot(x, y, zs=z, color='black', linewidth=2)

for i in range(4):
    ax.plot([x[i], x[i]], [y[i], y[i]], [0, L_3d], color='black', linewidth=2)

# 4 esquinas (φ16)
esquinas_3d = [
    (x_ini/100, y_fin/100),
    (x_fin/100, y_fin/100),
    (x_ini/100, y_ini/100),
    (x_fin/100, y_ini/100)
]
for xv, yv in esquinas_3d:
    ax.plot([xv, xv], [yv, yv], [0, L_3d], color='red', linewidth=4, zorder=10)

# 2 varillas arriba (φ14)
for i in range(1, var_a - 1):
    x_pos = (x_ini + i * espacio_horiz) / 100
    y_pos = y_fin / 100
    ax.plot([x_pos, x_pos], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)

# 2 varillas abajo (φ14)
for i in range(1, var_a - 1):
    x_pos = (x_ini + i * espacio_horiz) / 100
    y_pos = y_ini / 100
    ax.plot([x_pos, x_pos], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)

# 2 laterales izquierda (φ14)
for i in range(1, var_p - 1):
    y_pos = (y_ini + i * espacio_vert) / 100
    x_pos = x_ini / 100
    ax.plot([x_pos, x_pos], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)

# 2 laterales derecha (φ14)
for i in range(1, var_p - 1):
    y_pos = (y_ini + i * espacio_vert) / 100
    x_pos = x_fin / 100
    ax.plot([x_pos, x_pos], [y_pos, y_pos], [0, L_3d], color='orange', linewidth=3, zorder=10)

# Estribos
for z in np.linspace(0, L_3d, 15):
    ax.plot(x, y, zs=z, color='gray', linewidth=1, alpha=0.5)

# Zona protegida
ax.plot([0, b_3d, b_3d, 0, 0], [0, 0, h_3d, h_3d, 0], zs=0, color='red', linewidth=3)
ax.plot([0, b_3d, b_3d, 0, 0], [0, 0, h_3d, h_3d, 0], zs=L_3d, color='red', linewidth=3)
ax.plot([0, b_3d, b_3d, 0, 0], [0, 0, h_3d, h_3d, 0], zs=Lo/100, color='orange', linewidth=2, linestyle='--')

tic_3d = (
    f"COLUMNA {ancho_col}x{prof_col} cm\n"
    f"At = {At:.2f} m2\n"
    f"Pu = {Pu:.2f} t\n"
    f"As = {As:.2f} cm2\n"
    f"rho = {cuantia_pct:.2f}%\n"
    f"Lo = {Lo:.0f} cm"
)
ax.text(b_3d/2, h_3d/2, L_3d + 0.3, tic_3d, color='darkgreen', fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='green', linewidth=2))

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.set_title('Modelo 3D - Columna (simetria por eje)', fontsize=13, fontweight='bold')
ax.view_init(elev=20, azim=-55)

plt.tight_layout()
plt.savefig('M05_A1_modelo_3D.png', dpi=150, bbox_inches='tight')
print(f"Modelo 3D guardado: M05_A1_modelo_3D.png")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)