# -*- coding: utf-8 -*-
"""
================================================================================
M01 — MODELO 3D DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
OBJETIVO: Visualización 3D del pórtico principal (modelo base 38×38 cm)

NOTA: El cálculo de rigidez lateral está pendiente de análisis.
      Este módulo solo presenta la geometría y datos base.

MÉTODO: Shear building (se documenta, sin calcular todavía)
================================================================================
"""

import os
import sys
from datetime import datetime
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. DATOS BASE DEL PROYECTO
# ============================================================================

LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38
B_VIGA = 0.30
H_VIGA = 0.45

fc = 210
fy = 4200
Cm = 0.62
Cv = 0.20

# Posiciones de ejes
x_ejes = [0.0]
for lx in LUCES_X:
    x_ejes.append(x_ejes[-1] + lx)

y_ejes = [0.0]
for ly in LUCES_Y:
    y_ejes.append(y_ejes[-1] + ly)

z_niveles = [0.0, He, 2 * He]

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL
N_COL_X = len(x_ejes)
N_COL_Y = len(y_ejes)
N_COL_TOTAL = N_COL_X * N_COL_Y

# ============================================================================
# 2. FUNCIONES DE DIBUJO 3D
# ============================================================================

def dibujar_prisma(ax, x0, x1, y0, y1, z0, z1,
                   color_caras='#5c7a99', color_borde='#1a1a1a',
                   alpha=1.0, lw=0.8):
    v = np.array([
        [x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0],
        [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1],
    ])
    caras = [
        [v[0], v[1], v[2], v[3]],
        [v[4], v[5], v[6], v[7]],
        [v[0], v[1], v[5], v[4]],
        [v[2], v[3], v[7], v[6]],
        [v[1], v[2], v[6], v[5]],
        [v[0], v[3], v[7], v[4]],
    ]
    pc = Poly3DCollection(caras, facecolors=color_caras,
                          edgecolors=color_borde, linewidths=lw, alpha=alpha)
    ax.add_collection3d(pc)


def dibujar_columna(ax, x, y, z0, z1, seccion, color):
    b = seccion / 2
    dibujar_prisma(ax, x - b, x + b, y - b, y + b, z0, z1,
                   color_caras=color, color_borde='#1a1a1a',
                   alpha=0.95, lw=0.6)


def dibujar_viga_X(ax, x0, x1, y, z, b, h, color):
    dibujar_prisma(ax, x0, x1, y - b/2, y + b/2, z - h, z,
                   color_caras=color, color_borde='#2c3e50',
                   alpha=0.9, lw=0.5)


def dibujar_viga_Y(ax, x, y0, y1, z, b, h, color):
    dibujar_prisma(ax, x - b/2, x + b/2, y0, y1, z - h, z,
                   color_caras=color, color_borde='#2c3e50',
                   alpha=0.9, lw=0.5)


def dibujar_losa(ax, x0, x1, y0, y1, z, espesor=0.25,
                 color='#aed6f1', alpha=0.30):
    dibujar_prisma(ax, x0, x1, y0, y1, z, z + espesor,
                   color_caras=color, color_borde='#3498db',
                   alpha=alpha, lw=0.5)


def dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45):
    dibujar_prisma(ax, x - tam, x + tam, y - tam, y + tam,
                   z - 0.3, z,
                   color_caras='#616a6b', color_borde='#1a1a1a',
                   alpha=1.0, lw=0.7)


# ============================================================================
# 3. FIGURA PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor('#f5f7fa')

# Título principal
fig.text(0.5, 0.975,
         'MODELO 3D DEL PROYECTO UNESUM-REZ-2026-JIPIJAPA-001',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color='#1a237e')

fig.text(0.5, 0.945,
         f'Columna {B_COL*100:.0f}×{H_COL*100:.0f} cm | Viga {B_VIGA*100:.0f}×{H_VIGA*100:.0f} cm | He = {He:.2f} m | {N_PISOS} pisos',
         ha='center', va='top', fontsize=12,
         color='#5dade2', style='italic')

# Eje 3D principal
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#eaf2fb')

# ============================================================================
# 4. COLUMNAS
# ============================================================================

for x in x_ejes:
    for y in y_ejes:
        dibujar_columna(ax, x, y, z_niveles[0], z_niveles[1],
                        seccion=B_COL, color='#2c3e50')
        dibujar_columna(ax, x, y, z_niveles[1], z_niveles[2],
                        seccion=B_COL, color='#34495e')
        dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45)

# ============================================================================
# 5. VIGAS
# ============================================================================

for z_nivel in [z_niveles[1], z_niveles[2]]:
    for y in y_ejes:
        for i in range(len(x_ejes) - 1):
            dibujar_viga_X(ax, x_ejes[i], x_ejes[i+1], y, z_nivel,
                           b=B_VIGA, h=H_VIGA, color='#7f8c8d')
    for x in x_ejes:
        for j in range(len(y_ejes) - 1):
            dibujar_viga_Y(ax, x, y_ejes[j], y_ejes[j+1], z_nivel,
                           b=B_VIGA, h=H_VIGA, color='#95a5a6')

# ============================================================================
# 6. LOSAS
# ============================================================================

x_min, x_max = x_ejes[0], x_ejes[-1]
y_min, y_max = y_ejes[0], y_ejes[-1]

for z_nivel in [z_niveles[1], z_niveles[2]]:
    dibujar_losa(ax, x_min, x_max, y_min, y_max,
                 z=z_nivel, espesor=0.25,
                 color='#aed6f1', alpha=0.30)

# ============================================================================
# 7. CONFIGURACIÓN DE EJES
# ============================================================================

ax.set_xlabel('Eje X (m)', fontsize=11, labelpad=10)
ax.set_ylabel('Eje Y (m)', fontsize=11, labelpad=10)
ax.set_zlabel('Eje Z (m)', fontsize=11, labelpad=10)

ax.set_xlim(x_min - 2, x_max + 2)
ax.set_ylim(y_min - 2, y_max + 2)
ax.set_zlim(-1, H_TOTAL + 1)

ax.view_init(elev=20, azim=-60)
ax.grid(True, linestyle='--', alpha=0.3)
ax.set_box_aspect([LX_TOTAL + 4, LY_TOTAL + 4, H_TOTAL + 2])

# ============================================================================
# 8. MENSAJES OPORTUNOS (3 CUADROS)
# ============================================================================

# --- Mensaje 1: Datos del proyecto (sup. izquierda) ---
msg1 = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m\n"
    f"  Area = {AREA:.2f} m2\n"
    f"  Columnas: {N_COL_X} x {N_COL_Y} = {N_COL_TOTAL} u\n"
    f"  He = {He:.2f} m  |  N pisos = {N_PISOS}\n"
    f"  H_total = {H_TOTAL:.2f} m\n"
    "═══════════════════════════════\n"
    f"  fc = {fc} kg/cm2\n"
    f"  fy = {fy} kg/cm2\n"
    f"  E = 12600*raiz(fc)"
)

fig.text(0.02, 0.93, msg1,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor='#1a237e',
                   linewidth=1.8))

# --- Mensaje 2: Método de análisis (sup. derecha) ---
msg2 = (
    "METODO DE ANALISIS\n"
    "═══════════════════════════════\n"
    "  Shear building\n"
    "  (metodo de cortante)\n"
    "  - Rigidez lateral: solo columnas\n"
    "  - Vigas: solo aportan masa\n"
    "  - Losa: diafragma rigido"
)

fig.text(0.98, 0.93, msg2,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#fef9e7',
                   edgecolor='#f39c12',
                   linewidth=1.8))

# --- Mensaje 3: Referencia (inf. izquierda) ---
msg3 = (
    "REFERENCIA\n"
    "═══════════════════════════════\n"
    "  Modelo base extraido del\n"
    "  Excel PROYECTO.xlsx\n"
    "  Columna 38x38 cm"
)

fig.text(0.02, 0.12, msg3,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#f4ecf7',
                   edgecolor='#8e44ad',
                   linewidth=1.8))

# ============================================================================
# 9. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M01"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M01_modelo_3d_principal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M01 COMPLETADO — MODELO 3D PRINCIPAL")
print("=" * 80)
print(f"  Columna: {B_COL*100:.0f}×{H_COL*100:.0f} cm")
print(f"  Viga:    {B_VIGA*100:.0f}×{H_VIGA*100:.0f} cm")
print(f"  He:      {He:.2f} m  |  N pisos: {N_PISOS}")
print(f"  N° columnas: {N_COL_TOTAL}")
print("=" * 80)
print("  NOTA: Rigidez lateral pendiente de análisis.")
print("=" * 80)