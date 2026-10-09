# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 06 - ALGORITMO 2: DEFORMADA 3D POR CARGA VIVA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 §24.2 + NEC-15
OBJETIVO: Deformada 3D de la losa alivianada POR CARGA VIVA
          - Deflexion por Cv = 0.20 t/m2
          - Limite L/360 = 15.28 mm
          - Significado fisico
          DASHBOARD MEJOR QUE REVIT
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
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("matplotlib no esta instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Losa del Colegio Alejo Lascano"
TITULO = "DEFORMADA 3D POR CARGA VIVA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 §24.2 + NEC-15"
FRASE = "La deformada no es un error. Es la estructura hablando, diciendonos como trabaja."

# ============================================================================
# 2. DATOS DE ENTRADA (de la GUIA OFICIAL M06)
# ============================================================================

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

Cm = 0.62
Cv = 0.20         # CARGA VIVA (para deflexion)
Pisos = 2

H_losa = 25.0
h_eq = 18.06
bn = 10.0
bb = 50.0
tc = 5.0
hn = H_losa - tc

fc = 210
fy = 4200
rec_losa = 2.5
phi_pos = 8

# ============================================================================
# 3. CALCULOS
# ============================================================================

Lx = max(L1, L2, L3, L4)
Ly = Lx

# Inercia equivalente
I_eq = bb * h_eq**3 / 12
I_eq_m4 = I_eq / 1e8

E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
EI = E_tm2 * I_eq_m4

# DEFLEXION POR CARGA VIVA (Cv)
delta_max = 5 * Cv * Lx**4 / (384 * EI)
delta_adm = Lx * 1000 / 360  # L/360 segun ACI 318 §24.2.2

# Factor de amplificacion visual
factor_amp = 10

# ============================================================================
# 4. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - A2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- DATOS ---")
print(f"  Lx = {Lx:.2f} m | Ly = {Ly:.2f} m")
print(f"  Cv = {Cv:.3f} t/m2 (CARGA VIVA)")
print(f"  h_eq = {h_eq:.2f} cm | H_losa = {H_losa:.2f} cm")
print(f"  I_eq = {I_eq_m4:.6f} m4")
print(f"  EI = {EI:.2f} t.m2")

print(f"\n--- DEFLEXION POR CARGA VIVA ---")
print(f"  delta_max = {delta_max*1000:.3f} mm")
print(f"  delta_adm = {delta_adm:.3f} mm (L/360)")
print(f"  {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}")

print(f"\n--- SIGNIFICADO FISICO ---")
print(f"  1. CENTRO: deflexion maxima (punto critico)")
print(f"  2. BORDES: deflexion cero (apoyos)")
print(f"  3. NERVIOS: direccion del flujo de cargas")
print(f"  4. COLUMNAS: concentracion de esfuerzos")
print(f"  5. COLORES: magnitud de deflexion")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_deformada_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - A2] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Cv = {Cv:.3f} t/m2\n")
    f.write(f"I_eq = {I_eq_m4:.6f} m4\n")
    f.write(f"delta_max = {delta_max*1000:.3f} mm\n")
    f.write(f"delta_adm = {delta_adm:.3f} mm (L/360)\n")
    f.write(f"Estado = {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD 3D
# ============================================================================

fig = plt.figure(figsize=(22, 14), facecolor='#1e1e2e')

# ------------------------------------------------------------------
# SUBPLOT IZQUIERDO: MODELO DE LA ESTRUCTURA (2 PISOS)
# ------------------------------------------------------------------
ax_izq = fig.add_subplot(1, 2, 1, projection='3d')
ax_izq.set_facecolor('#1e1e2e')

n_pisos_m = 2
n_ejes = 2
Lv_m = 3.0
He_m = 1.5

# Columnas
for i in range(n_ejes + 1):
    for j in range(n_ejes + 1):
        x_col = i * Lv_m
        y_col = j * Lv_m
        ax_izq.plot([x_col, x_col], [y_col, y_col],
                    [0, n_pisos_m * He_m],
                    color='#5dade2', linewidth=4, alpha=0.9)
        ax_izq.scatter(x_col, y_col, 0, color='cyan', s=80, marker='^', zorder=10)

# Vigas en X
for piso in range(1, n_pisos_m + 1):
    z_piso = piso * He_m
    for j in range(n_ejes + 1):
        y_viga = j * Lv_m
        ax_izq.plot([0, n_ejes * Lv_m], [y_viga, y_viga],
                    [z_piso, z_piso], color='#f39c12', linewidth=3.5, alpha=0.9)

# Vigas en Y
for piso in range(1, n_pisos_m + 1):
    z_piso = piso * He_m
    for i in range(n_ejes + 1):
        x_viga = i * Lv_m
        ax_izq.plot([x_viga, x_viga], [0, n_ejes * Lv_m],
                    [z_piso, z_piso], color='#f39c12', linewidth=3.5, alpha=0.9)

# Losa del segundo piso (amarillo)
z_losa = n_pisos_m * He_m
x_losa = np.linspace(0, n_ejes * Lv_m, 20)
y_losa = np.linspace(0, n_ejes * Lv_m, 20)
X_losa, Y_losa = np.meshgrid(x_losa, y_losa)
Z_losa = np.full_like(X_losa, z_losa)

ax_izq.plot_surface(X_losa, Y_losa, Z_losa,
                     color='yellow', alpha=0.3, edgecolor='yellow',
                     linewidth=0.5)

# Pano desarrollado (rojo)
x_pano = np.linspace(0, Lv_m, 15)
y_pano = np.linspace(0, Lv_m, 15)
X_pano, Y_pano = np.meshgrid(x_pano, y_pano)
Z_pano = np.full_like(X_pano, z_losa + 0.02)

ax_izq.plot_surface(X_pano, Y_pano, Z_pano,
                     color='red', alpha=0.6, edgecolor='darkred',
                     linewidth=1)

ax_izq.text(Lv_m/2, Lv_m/2, z_losa + 0.5,
            'PANO DESARROLLADO\n(M06 - Losa alivianada)',
            color='red', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='lightyellow',
                      edgecolor='red',
                      linewidth=2))

ax_izq.plot([Lv_m/2, Lv_m/2], [Lv_m/2, Lv_m/2],
            [z_losa + 0.4, z_losa + 0.05],
            color='red', linewidth=3)
ax_izq.scatter(Lv_m/2, Lv_m/2, z_losa + 0.05, color='red',
               s=150, marker='v', zorder=20)

ax_izq.text(-0.5, -0.5, He_m, 'PISO 1',
            color='#5dade2', fontsize=9, fontweight='bold')
ax_izq.text(-0.5, -0.5, 2 * He_m, 'PISO 2',
            color='#5dade2', fontsize=9, fontweight='bold')

ax_izq.set_xlabel('X (m)', color='white', fontsize=10)
ax_izq.set_ylabel('Y (m)', color='white', fontsize=10)
ax_izq.set_zlabel('Z (m)', color='white', fontsize=10)
ax_izq.tick_params(axis='x', colors='white')
ax_izq.tick_params(axis='y', colors='white')
ax_izq.tick_params(axis='z', colors='white')
ax_izq.set_title('MODELO DE LA ESTRUCTURA (2 PISOS)\nPano desarrollado senalado en rojo',
                 color='#5dade2', fontsize=13, fontweight='bold', pad=15)
ax_izq.view_init(elev=20, azim=-55)

# ------------------------------------------------------------------
# SUBPLOT DERECHO: DEFORMADA 3D POR CARGA VIVA
# ------------------------------------------------------------------
ax_der = fig.add_subplot(1, 2, 2, projection='3d')
ax_der.set_facecolor('#1e1e2e')

nx, ny = 50, 50
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Deformada por carga viva
delta = delta_max * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)
Z_plot = -delta * factor_amp

surf = ax_der.plot_surface(X, Y, Z_plot,
                            cmap='jet',
                            edgecolor='none',
                            alpha=0.95,
                            rstride=1, cstride=1,
                            linewidth=0)

cbar = fig.colorbar(surf, ax=ax_der, shrink=0.5, aspect=10, pad=0.08)
cbar.set_label(f'Deflexion por Cv (mm x {factor_amp})', color='white', fontsize=10)
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Nervios
for i in range(0, nx, 5):
    ax_der.plot(X[i, :], Y[i, :], Z_plot[i, :],
                color='white', alpha=0.25, linewidth=0.6)
for j in range(0, ny, 5):
    ax_der.plot(X[:, j], Y[:, j], Z_plot[:, j],
                color='white', alpha=0.25, linewidth=0.6)

# Bordes
ax_der.plot([0, Lx], [0, 0], [0, 0], color='cyan', linewidth=4)
ax_der.plot([0, Lx], [Ly, Ly], [0, 0], color='cyan', linewidth=4)
ax_der.plot([0, 0], [0, Ly], [0, 0], color='cyan', linewidth=4)
ax_der.plot([Lx, Lx], [0, Ly], [0, 0], color='cyan', linewidth=4)

# Columnas
for cx, cy in [(0, 0), (Lx, 0), (0, Ly), (Lx, Ly)]:
    ax_der.plot([cx, cx], [cy, cy], [0, -0.6], color='red',
                linewidth=6, alpha=0.9)
    ax_der.scatter(cx, cy, 0, color='red', s=100, zorder=20)

# Punto critico
cx_centro = Lx / 2
cy_centro = Ly / 2
z_centro = -delta_max * factor_amp

ax_der.scatter(cx_centro, cy_centro, z_centro, color='yellow', s=300,
               edgecolor='red', linewidth=3, zorder=30)
ax_der.plot([cx_centro, cx_centro], [cy_centro, cy_centro],
            [0, z_centro], color='yellow', linewidth=2,
            linestyle='--', alpha=0.8)

ax_der.text(cx_centro + 0.3, cy_centro + 0.3, z_centro - 0.3,
            f'PUNTO CRITICO\nDelta_max = {delta_max*1000:.2f} mm',
            color='yellow', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='#1e1e2e',
                      edgecolor='yellow',
                      linewidth=2))

ax_der.text(0, -0.5, 0, 'APOYO\n(Delta = 0)',
            color='cyan', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='#1e1e2e',
                      edgecolor='cyan',
                      linewidth=1.5))

ax_der.text(Lx/2, -0.7, 0.5, 'NERVIOS\n(flujo de cargas)',
            color='white', fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='#1e1e2e',
                      edgecolor='white',
                      linewidth=1.5))

ax_der.set_xlabel('X (m)', color='white', fontsize=10)
ax_der.set_ylabel('Y (m)', color='white', fontsize=10)
ax_der.set_zlabel(f'Z (mm x {factor_amp})', color='white', fontsize=10)
ax_der.tick_params(axis='x', colors='white')
ax_der.tick_params(axis='y', colors='white')
ax_der.tick_params(axis='z', colors='white')
ax_der.set_title(f'DEFORMADA 3D POR CARGA VIVA (Cv = {Cv} t/m2)\n'
                 f'Delta_max = {delta_max*1000:.2f} mm | L/360 = {delta_adm:.2f} mm | '
                 f'{"CUMPLE" if delta_max*1000 < delta_adm else "NO CUMPLE"}',
                 color='#5dade2', fontsize=12, fontweight='bold', pad=15)
ax_der.view_init(elev=25, azim=-50)

# ------------------------------------------------------------------
# PANEL DE SIGNIFICADO FISICO
# ------------------------------------------------------------------
fig.text(0.02, 0.02,
    "SIGNIFICADO FISICO:\n"
    "1. CENTRO: deflexion maxima (punto critico)\n"
    "2. BORDES: deflexion cero (apoyos)\n"
    "3. NERVIOS: direccion del flujo de cargas\n"
    "4. COLUMNAS: concentracion de esfuerzos\n"
    "5. COLORES: magnitud de deflexion",
    ha='left', va='bottom',
    fontsize=9, color='#f39c12', fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.5',
              facecolor='#1e1e2e',
              edgecolor='#f39c12',
              linewidth=2,
              alpha=0.95))

# ------------------------------------------------------------------
# TIC
# ------------------------------------------------------------------
tic_box = (
    f"VERIFICACION NEC-15 / ACI 318:\n"
    f"  Cv = {Cv:.3f} t/m2 (carga viva)\n"
    f"  Delta_max = {delta_max*1000:.2f} mm\n"
    f"  L/360 = {delta_adm:.2f} mm\n"
    f"  L/H = {Lx*100/H_losa:.2f} <= 28\n"
    f"  {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}"
)
fig.text(0.98, 0.85,
    tic_box,
    ha='right', va='top',
    fontsize=9, color='darkgreen', fontweight='bold',
    bbox=dict(boxstyle='round,pad=0.5',
              facecolor='lightyellow',
              edgecolor='green',
              linewidth=2,
              alpha=0.95))

# ------------------------------------------------------------------
# FRASE
# ------------------------------------------------------------------
fig.text(0.98, 0.02,
    f'"{FRASE}"\n- Proyecto UNESUM-REZ-2026-JIPIJAPA-001',
    ha='right', va='bottom',
    fontsize=8, style='italic', color='#f39c12',
    bbox=dict(boxstyle='round,pad=0.5',
              facecolor='#1e1e2e',
              edgecolor='#f39c12',
              linewidth=1.5,
              alpha=0.95))

fig.suptitle(
    f"M06 - ALGORITMO 2: DEFORMADA 3D POR CARGA VIVA\n"
    f"{PROYECTO} | {NORMA}",
    fontsize=14, fontweight='bold', color='#5dade2', y=0.98
)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])

nombre_img = f"M06_A2_deformada_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, facecolor='#1e1e2e', bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)