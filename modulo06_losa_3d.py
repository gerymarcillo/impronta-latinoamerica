# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 06 - ALGORITMO 3: DEFORMADA 3D + MODELO 2 PISOS
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 + NEC-15
OBJETIVO: Deformada 3D con SIGNIFICADO FISICO
          + Modelo de 2 pisos al lado
          + Paño desarrollado señalado
          + Ubicacion del paño en la estructura
          MEJOR QUE REVIT
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
    from mpl_toolkits.mplot3d import Axes3D
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
TITULO = "DEFORMADA 3D + MODELO 2 PISOS"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 + NEC-15"
FRASE = "La deformada no es un error. Es la estructura hablando, diciendonos como trabaja."

# ============================================================================
# 2. DATOS DE ENTRADA
# ============================================================================

h_eq = 18.06
H_losa = 25.0
bn = 10.0
bb = 50.0
tc = 5.0
hn = H_losa - tc

Cu = 1.088
L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0
fc, fy = 210, 4200
rec_losa = 2.0

# Estructura de 2 pisos
He = 3.0
Pisos = 2
b_col = 0.38
b_viga = 0.30
h_viga = 0.45

# ============================================================================
# 3. CALCULOS
# ============================================================================

Lx = max(L1, L2, L3, L4)
Ly = Lx

paso_nervios = bb / 100
w_nervio = Cu * paso_nervios

h_eq_m = h_eq / 100
I_eq = (1.0 * h_eq_m**3) / 12

E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
EI = E_tm2 * I_eq

alpha = 0.00406
delta_max = alpha * Cu * Lx**4 / (E_tm2 * h_eq_m**3)
delta_adm = Lx * 1000 / 240
relacion_LH = Lx * 100 / H_losa
factor_amp = 10

# ============================================================================
# 4. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - A3] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- DATOS ---")
print(f"  Lx = {Lx:.2f} m | Ly = {Ly:.2f} m")
print(f"  h_eq = {h_eq:.2f} cm | H_losa = {H_losa:.2f} cm")
print(f"  Cu = {Cu:.3f} t/m2")
print(f"  E = {E_tm2:.2f} t/m2")
print(f"  EI = {EI:.2f} t.m2")

print(f"\n--- DEFLEXION ---")
print(f"  delta_max = {delta_max*1000:.3f} mm")
print(f"  delta_adm = {delta_adm:.3f} mm")
print(f"  {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}")

print(f"\n--- ESTRUCTURA 2 PISOS ---")
print(f"  He = {He} m | Pisos = {Pisos}")
print(f"  b_col = {b_col} m | b_viga = {b_viga} m | h_viga = {h_viga} m")
print(f"  Luces: L1={L1}, L2={L2}, L3={L3}, L4={L4}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_deformada_2pisos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - A3] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DEFORMADA:\n")
    f.write(f"  delta_max = {delta_max*1000:.3f} mm\n")
    f.write(f"  delta_adm = {delta_adm:.3f} mm\n")
    f.write(f"  Estado = {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. FIGURA CON 2 SUBPLOTS: IZQUIERDA MODELO 2 PISOS | DERECHA DEFORMADA 3D
# ============================================================================

fig = plt.figure(figsize=(22, 14), facecolor='#1e1e2e')

# ------------------------------------------------------------------
# SUBPLOT IZQUIERDO: MODELO DE 2 PISOS (Pórtico 3D)
# ------------------------------------------------------------------
ax_izq = fig.add_subplot(1, 2, 1, projection='3d')
ax_izq.set_facecolor('#1e1e2e')

# Dimensiones del pórtico
n_pisos_modelo = 2
n_ejes_x = 2  # 2 vanos
n_ejes_y = 2
Lv_x = 3.0  # Luz en X (simplificada para visualizacion)
Lv_y = 3.0
He_modelo = 1.5  # Altura de entrepiso

# Columnas (esquinas del grid)
for i in range(n_ejes_x + 1):
    for j in range(n_ejes_y + 1):
        x_col = i * Lv_x
        y_col = j * Lv_y
        ax_izq.plot([x_col, x_col], [y_col, y_col],
                    [0, n_pisos_modelo * He_modelo],
                    color='#5dade2', linewidth=4, alpha=0.9)
        # Apoyo en la base
        ax_izq.scatter(x_col, y_col, 0, color='cyan', s=80, marker='^', zorder=10)

# Vigas en X (cada piso)
for piso in range(1, n_pisos_modelo + 1):
    z_piso = piso * He_modelo
    for j in range(n_ejes_y + 1):
        y_viga = j * Lv_y
        ax_izq.plot([0, n_ejes_x * Lv_x], [y_viga, y_viga],
                    [z_piso, z_piso], color='#f39c12', linewidth=3.5, alpha=0.9)

# Vigas en Y (cada piso)
for piso in range(1, n_pisos_modelo + 1):
    z_piso = piso * He_modelo
    for i in range(n_ejes_x + 1):
        x_viga = i * Lv_x
        ax_izq.plot([x_viga, x_viga], [0, n_ejes_y * Lv_y],
                    [z_piso, z_piso], color='#f39c12', linewidth=3.5, alpha=0.9)

# LOSA DEL SEGUNDO PISO (paño desarrollado) - resaltada en amarillo
z_losa = n_pisos_modelo * He_modelo  # Segundo piso

# Dibujar losa como superficie
x_losa = np.linspace(0, n_ejes_x * Lv_x, 20)
y_losa = np.linspace(0, n_ejes_y * Lv_y, 20)
X_losa, Y_losa = np.meshgrid(x_losa, y_losa)
Z_losa = np.full_like(X_losa, z_losa)

ax_izq.plot_surface(X_losa, Y_losa, Z_losa,
                     color='yellow', alpha=0.3, edgecolor='yellow',
                     linewidth=0.5)

# PAÑO DESARROLLADO (el que estamos analizando) - resaltado en rojo
# Es el primer paño del segundo piso
x_pano = np.linspace(0, Lv_x, 15)
y_pano = np.linspace(0, Lv_y, 15)
X_pano, Y_pano = np.meshgrid(x_pano, y_pano)
Z_pano = np.full_like(X_pano, z_losa + 0.02)

ax_izq.plot_surface(X_pano, Y_pano, Z_pano,
                     color='red', alpha=0.6, edgecolor='darkred',
                     linewidth=1)

# Flecha señalando el paño desarrollado
ax_izq.text(Lv_x/2, Lv_y/2, z_losa + 0.5,
            'PAÑO DESARROLLADO\n(M06 - Losa alivianada)',
            color='red', fontsize=10, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='lightyellow',
                      edgecolor='red',
                      linewidth=2))

# Flecha vertical
ax_izq.plot([Lv_x/2, Lv_x/2], [Lv_y/2, Lv_y/2],
            [z_losa + 0.4, z_losa + 0.05],
            color='red', linewidth=3)
ax_izq.scatter(Lv_x/2, Lv_y/2, z_losa + 0.05, color='red',
               s=150, marker='v', zorder=20)

# Etiquetas de pisos
ax_izq.text(-0.5, -0.5, He_modelo, 'PISO 1',
            color='#5dade2', fontsize=9, fontweight='bold')
ax_izq.text(-0.5, -0.5, 2 * He_modelo, 'PISO 2',
            color='#5dade2', fontsize=9, fontweight='bold')

# Etiquetas de elementos
ax_izq.text(n_ejes_x * Lv_x + 0.3, 0, He_modelo, 'Columna\n38x38',
            color='#5dade2', fontsize=8, fontweight='bold')
ax_izq.text(n_ejes_x * Lv_x / 2, n_ejes_y * Lv_y + 0.3, He_modelo,
            'Viga 30x45', color='#f39c12', fontsize=8, fontweight='bold')

# Configuracion de ejes
ax_izq.set_xlabel('X (m)', color='white', fontsize=10)
ax_izq.set_ylabel('Y (m)', color='white', fontsize=10)
ax_izq.set_zlabel('Z (m)', color='white', fontsize=10)
ax_izq.tick_params(axis='x', colors='white')
ax_izq.tick_params(axis='y', colors='white')
ax_izq.tick_params(axis='z', colors='white')
ax_izq.set_title('MODELO DE LA ESTRUCTURA (2 PISOS)\nPaño desarrollado señalado en rojo',
                 color='#5dade2', fontsize=13, fontweight='bold', pad=15)
ax_izq.view_init(elev=20, azim=-55)

# ------------------------------------------------------------------
# SUBPLOT DERECHO: DEFORMADA 3D (paño desarrollado)
# ------------------------------------------------------------------
ax_der = fig.add_subplot(1, 2, 2, projection='3d')
ax_der.set_facecolor('#1e1e2e')

# Malla de la deformada
nx, ny = 50, 50
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

delta = delta_max * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)
Z_plot = -delta * factor_amp

surf = ax_der.plot_surface(X, Y, Z_plot,
                            cmap='jet',
                            edgecolor='none',
                            alpha=0.95,
                            rstride=1, cstride=1,
                            linewidth=0)

# Colorbar
cbar = fig.colorbar(surf, ax=ax_der, shrink=0.5, aspect=10, pad=0.08)
cbar.set_label(f'Deflexion (mm x {factor_amp})', color='white', fontsize=10)
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Nervios
for i in range(0, nx, 5):
    ax_der.plot(X[i, :], Y[i, :], Z_plot[i, :],
                color='white', alpha=0.25, linewidth=0.6)
for j in range(0, ny, 5):
    ax_der.plot(X[:, j], Y[:, j], Z_plot[:, j],
                color='white', alpha=0.25, linewidth=0.6)

# Bordes (apoyos)
ax_der.plot([0, Lx], [0, 0], [0, 0], color='cyan', linewidth=4)
ax_der.plot([0, Lx], [Ly, Ly], [0, 0], color='cyan', linewidth=4)
ax_der.plot([0, 0], [0, Ly], [0, 0], color='cyan', linewidth=4)
ax_der.plot([Lx, Lx], [0, Ly], [0, 0], color='cyan', linewidth=4)

# Columnas en esquinas
for cx, cy in [(0, 0), (Lx, 0), (0, Ly), (Lx, Ly)]:
    ax_der.plot([cx, cx], [cy, cy], [0, -0.6], color='red',
                linewidth=6, alpha=0.9)
    ax_der.scatter(cx, cy, 0, color='red', s=100, zorder=20)

# Punto critico (centro)
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

# Anotaciones
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
ax_der.set_title(f'DEFORMADA 3D DEL PAÑO DESARROLLADO\n'
                 f'Delta_max = {delta_max*1000:.2f} mm | L/240 = {delta_adm:.2f} mm | '
                 f'{"CUMPLE" if delta_max*1000 < delta_adm else "NO CUMPLE"}',
                 color='#5dade2', fontsize=12, fontweight='bold', pad=15)
ax_der.view_init(elev=25, azim=-50)

# ------------------------------------------------------------------
# PANEL DE SIGNIFICADO FISICO (pie de figura)
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
    f"VERIFICACION NEC-15:\n"
    f"  Delta_max = {delta_max*1000:.2f} mm\n"
    f"  L/240 = {delta_adm:.2f} mm\n"
    f"  L/H = {relacion_LH:.2f} <= 28\n"
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

# Titulo general
fig.suptitle(
    f"M06 - ALGORITMO 3: DEFORMADA 3D CON SIGNIFICADO FISICO\n"
    f"{PROYECTO} | {NORMA}",
    fontsize=14, fontweight='bold', color='#5dade2', y=0.98
)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])

nombre_img = f"M06_A3_deformada_2pisos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, facecolor='#1e1e2e', bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)