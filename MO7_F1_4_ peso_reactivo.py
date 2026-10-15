# -*- coding: utf-8 -*-
"""
================================================================================
M03 — PESO REACTIVO DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
OBJETIVO: Cálculo y visualización 3D del peso reactivo del modelo base 38×38 cm

NOTA METODOLÓGICA:
    W = Cu = 1.2Cm + 1.6Cv (criterio del Excel PROYECTO.xlsx)
    Se mantiene para coherencia con el modelo base.

MÉTODO: Shear building
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
# PALETA DE COLORES DEL PROYECTO
# ============================================================================

COLORES = {
    # Fondos
    'fondo_fig': '#f5f7fa',
    'fondo_3d': '#eaf2fb',

    # Estructura
    'col_n1': '#2c3e50',
    'col_n2': '#34495e',
    'viga_x': '#7f8c8d',
    'viga_y': '#95a5a6',
    'losa': '#aed6f1',
    'empotramiento': '#616a6b',

    # Masas
    'masa': '#e74c3c',
    'masa_borde': '#922b21',
    'masa_texto': '#922b21',

    # Textos
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',

    # Cuadros
    'box_datos_bg': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_calculo_bg': '#fef9e7',
    'box_calculo_borde': '#f39c12',
    'box_resultado_bg': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_ref_bg': '#f4ecf7',
    'box_ref_borde': '#8e44ad',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
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

Cm = 0.62
Cv = 0.20
pct_cv = 0
g = 9.81

# Cálculos
LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
Area = LX_TOTAL * LY_TOTAL
Cu = 1.2 * Cm + 1.6 * Cv
W_piso = Cu * Area
W_total = N_PISOS * W_piso
m_piso = W_piso / g
m_total = N_PISOS * m_piso

# Posiciones de ejes
x_ejes = [0.0]
for lx in LUCES_X:
    x_ejes.append(x_ejes[-1] + lx)

y_ejes = [0.0]
for ly in LUCES_Y:
    y_ejes.append(y_ejes[-1] + ly)

z_niveles = [0.0, He, 2 * He]

# ============================================================================
# 2. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M03 — PESO REACTIVO DEL PROYECTO PRINCIPAL")
print("=" * 80)
print(f"""
  GEOMETRIA:
    Lx = {LUCES_X[0]:.2f} + {LUCES_X[1]:.2f} + {LUCES_X[2]:.2f} = {LX_TOTAL:.2f} m
    Ly = {LUCES_Y[0]:.2f} + {LUCES_Y[1]:.2f} + {LUCES_Y[2]:.2f} + {LUCES_Y[3]:.2f} = {LY_TOTAL:.2f} m
    Area = {Area:.2f} m2
    He = {He:.2f} m  |  N pisos = {N_PISOS}

  CARGAS:
    Cm = {Cm} t/m2
    Cv = {Cv} t/m2
    %Cv = {pct_cv}%
    Cu = 1.2Cm + 1.6Cv = {Cu:.4f} t/m2

  PESO REACTIVO:
    W_piso = Cu x Area = {W_piso:.2f} t
    W_total = {N_PISOS} x W_piso = {W_total:.2f} t

  MASA:
    m_piso = W_piso / g = {m_piso:.4f} t.s2/m
    m_total = {N_PISOS} x m_piso = {m_total:.4f} t.s2/m
""")
print("=" * 80)

# ============================================================================
# 3. FUNCIONES DE DIBUJO 3D
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
                   color_caras=COLORES['empotramiento'],
                   color_borde='#1a1a1a',
                   alpha=1.0, lw=0.7)


# ============================================================================
# 4. FIGURA PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.975,
         'M03 — PESO REACTIVO DEL PROYECTO PRINCIPAL',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo base 38×38 cm | W_total = {W_total:.2f} t',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# Eje 3D
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor(COLORES['fondo_3d'])

# ============================================================================
# 5. COLUMNAS
# ============================================================================

for x in x_ejes:
    for y in y_ejes:
        dibujar_columna(ax, x, y, z_niveles[0], z_niveles[1],
                        seccion=B_COL, color=COLORES['col_n1'])
        dibujar_columna(ax, x, y, z_niveles[1], z_niveles[2],
                        seccion=B_COL, color=COLORES['col_n2'])
        dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45)

# ============================================================================
# 6. VIGAS
# ============================================================================

for z_nivel in [z_niveles[1], z_niveles[2]]:
    for y in y_ejes:
        for i in range(len(x_ejes) - 1):
            dibujar_viga_X(ax, x_ejes[i], x_ejes[i+1], y, z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga_x'])
    for x in x_ejes:
        for j in range(len(y_ejes) - 1):
            dibujar_viga_Y(ax, x, y_ejes[j], y_ejes[j+1], z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga_y'])

# ============================================================================
# 7. LOSAS
# ============================================================================

x_min, x_max = x_ejes[0], x_ejes[-1]
y_min, y_max = y_ejes[0], y_ejes[-1]

for z_nivel in [z_niveles[1], z_niveles[2]]:
    dibujar_losa(ax, x_min, x_max, y_min, y_max,
                 z=z_nivel, espesor=0.25,
                 color=COLORES['losa'], alpha=0.30)

# ============================================================================
# 8. MASAS CONCENTRADAS (PESO REACTIVO)
# ============================================================================

cx = (x_ejes[0] + x_ejes[-1]) / 2
cy = (y_ejes[0] + y_ejes[-1]) / 2

for i, z in enumerate([He, 2 * He]):
    ax.scatter(cx, cy, z + 0.5, color=COLORES['masa'], s=450,
               edgecolor=COLORES['masa_borde'], linewidth=2.5,
               zorder=10)

    # Caja de texto con peso + masa
    ax.text(cx + 2.5, cy, z + 1.3,
            f'W{i+1} = {W_piso:.1f} t\nm{i+1} = {m_piso:.2f} t·s²/m',
            fontsize=9, fontweight='bold',
            color=COLORES['masa_texto'],
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='white', alpha=0.9,
                      edgecolor=COLORES['masa_borde'], linewidth=1.5))

# ============================================================================
# 9. CONFIGURACIÓN DE EJES
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
# 10. MENSAJES OPORTUNOS
# ============================================================================

# --- Mensaje 1: Datos del proyecto (sup. izquierda) ---
msg1 = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m\n"
    f"  Area = {Area:.2f} m2\n"
    f"  He = {He:.2f} m  |  N pisos = {N_PISOS}\n"
    f"  H_total = {H_TOTAL:.2f} m\n"
    "═══════════════════════════════\n"
    f"  Cm = {Cm} t/m2\n"
    f"  Cv = {Cv} t/m2\n"
    f"  %Cv = {pct_cv}%"
)

fig.text(0.02, 0.93, msg1,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=1.8, alpha=0.95))

# --- Mensaje 2: Peso reactivo (sup. derecha) ---
msg2 = (
    "PESO REACTIVO\n"
    "═══════════════════════════════\n"
    f"  Cu = 1.2Cm + 1.6Cv\n"
    f"  Cu = {Cu:.4f} t/m2\n"
    "───────────────────────────────\n"
    f"  W_piso  = Cu x Area\n"
    f"  W_piso  = {W_piso:.2f} t\n"
    "───────────────────────────────\n"
    f"  W_total = N x W_piso\n"
    f"  W_total = {W_total:.2f} t"
)

fig.text(0.98, 0.93, msg2,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=1.8, alpha=0.95))

# --- Mensaje 3: Masa (inf. derecha) ---
msg3 = (
    "MASA DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  m_piso = W_piso / g\n"
    f"  m_piso = {m_piso:.4f} t·s2/m\n"
    "───────────────────────────────\n"
    f"  m_total = N x m_piso\n"
    f"  m_total = {m_total:.4f} t·s2/m"
)

fig.text(0.98, 0.12, msg3,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=1.8, alpha=0.95))

# --- Mensaje 4: Referencia (inf. izquierda) ---
msg4 = (
    "REFERENCIA\n"
    "═══════════════════════════════\n"
    "  Excel PROYECTO.xlsx\n"
    "  Celda F4 = 405.30 t\n"
    "  Modelo base 38x38 cm\n"
    "  Shear building"
)

fig.text(0.02, 0.12, msg4,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=1.8, alpha=0.95))

# ============================================================================
# 11. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M03"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M03_peso_reactivo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"\nImagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M03 COMPLETADO — PESO REACTIVO DEL PROYECTO PRINCIPAL")
print("=" * 80)
print(f"  Area     = {Area:.2f} m²")
print(f"  Cu       = {Cu:.4f} t/m²")
print(f"  W_piso   = {W_piso:.2f} t")
print(f"  W_total  = {W_total:.2f} t")
print(f"  m_piso   = {m_piso:.4f} t·s²/m")
print(f"  m_total  = {m_total:.4f} t·s²/m")
print("=" * 80)