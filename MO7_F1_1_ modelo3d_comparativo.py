# -*- coding: utf-8 -*-
"""
================================================================================
M01 — MODELO 3D COMPARATIVO (3 MODELOS DE SECCIÓN)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001

NOTA DIDÁCTICA:
    - Modelo base: 38×38 cm (extraído del Excel PROYECTO.xlsx)
    - Modelos A (25×25) y B (30×30): variaciones didácticas
    - Los 3 modelos comparten LAS MISMAS LUCES y geometría en planta

MÉTODO: Shear building (rigidez lateral = solo columnas)
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
# 2. DEFINICIÓN DE LOS 3 MODELOS
# ============================================================================

MODELOS = {
    'A': {
        'B_COL': 0.25, 'H_COL': 0.25,
        'nombre': 'MODELO A',
        'subtitulo': '25x25 cm (didactico)',
        'etiqueta': 'Variacion didactica',
        'color_col': '#e74c3c',
        'color_viga': '#ec7063',
        'color_bg': '#fadbd8'
    },
    'B': {
        'B_COL': 0.30, 'H_COL': 0.30,
        'nombre': 'MODELO B',
        'subtitulo': '30x30 cm (didactico)',
        'etiqueta': 'Variacion didactica',
        'color_col': '#f39c12',
        'color_viga': '#f8c471',
        'color_bg': '#fdebd0'
    },
    'C': {
        'B_COL': 0.38, 'H_COL': 0.38,
        'nombre': 'MODELO C',
        'subtitulo': '38x38 cm (base)',
        'etiqueta': 'Modelo base (Excel)',
        'color_col': '#27ae60',
        'color_viga': '#52be80',
        'color_bg': '#d5f5e3'
    }
}

# ============================================================================
# 3. CÁLCULO DE RIGIDEZ (SHEAR BUILDING)
# ============================================================================

E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

def calcular_rigidez(B_COL, H_COL):
    I_col_m4 = (B_COL * H_COL**3) / 12
    I_col_cm4 = I_col_m4 * 100**4
    k_col_tm = 12 * E_tm2 * I_col_m4 / He**3
    k_piso_tm = N_COL_TOTAL * k_col_tm
    return {
        'I_col_cm4': I_col_cm4,
        'k_col_tm': k_col_tm,
        'k_piso_tm': k_piso_tm,
    }

RIGIDECES = {k: calcular_rigidez(m['B_COL'], m['H_COL'])
             for k, m in MODELOS.items()}

# ============================================================================
# 4. FUNCIONES DE DIBUJO 3D
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
                   alpha=0.95, lw=0.5)


def dibujar_viga_X(ax, x0, x1, y, z, b, h, color):
    dibujar_prisma(ax, x0, x1, y - b/2, y + b/2, z - h, z,
                   color_caras=color, color_borde='#2c3e50',
                   alpha=0.9, lw=0.4)


def dibujar_viga_Y(ax, x, y0, y1, z, b, h, color):
    dibujar_prisma(ax, x - b/2, x + b/2, y0, y1, z - h, z,
                   color_caras=color, color_borde='#2c3e50',
                   alpha=0.9, lw=0.4)


def dibujar_losa(ax, x0, x1, y0, y1, z, espesor=0.25,
                 color='#aed6f1', alpha=0.15):
    dibujar_prisma(ax, x0, x1, y0, y1, z, z + espesor,
                   color_caras=color, color_borde='#3498db',
                   alpha=alpha, lw=0.3)


def dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45):
    dibujar_prisma(ax, x - tam, x + tam, y - tam, y + tam,
                   z - 0.3, z,
                   color_caras='#616a6b', color_borde='#1a1a1a',
                   alpha=1.0, lw=0.5)


def dibujar_portico(ax, modelo):
    B_COL = modelo['B_COL']
    color_col = modelo['color_col']
    color_viga = modelo['color_viga']

    for x in x_ejes:
        for y in y_ejes:
            dibujar_columna(ax, x, y, z_niveles[0], z_niveles[1],
                            seccion=B_COL, color=color_col)
            dibujar_columna(ax, x, y, z_niveles[1], z_niveles[2],
                            seccion=B_COL, color=color_col)
            dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45)

    for z_nivel in [z_niveles[1], z_niveles[2]]:
        for y in y_ejes:
            for i in range(len(x_ejes) - 1):
                dibujar_viga_X(ax, x_ejes[i], x_ejes[i+1], y, z_nivel,
                               b=B_VIGA, h=H_VIGA, color=color_viga)
        for x in x_ejes:
            for j in range(len(y_ejes) - 1):
                dibujar_viga_Y(ax, x, y_ejes[j], y_ejes[j+1], z_nivel,
                               b=B_VIGA, h=H_VIGA, color=color_viga)

    x_min, x_max = x_ejes[0], x_ejes[-1]
    y_min, y_max = y_ejes[0], y_ejes[-1]
    for z_nivel in [z_niveles[1], z_niveles[2]]:
        dibujar_losa(ax, x_min, x_max, y_min, y_max,
                     z=z_nivel, espesor=0.25,
                     color='#aed6f1', alpha=0.15)

    ax.set_xlabel('X (m)', fontsize=8, labelpad=3)
    ax.set_ylabel('Y (m)', fontsize=8, labelpad=3)
    ax.set_zlabel('Z (m)', fontsize=8, labelpad=3)

    ax.set_xlim(x_min - 2, x_max + 2)
    ax.set_ylim(y_min - 2, y_max + 2)
    ax.set_zlim(-1, H_TOTAL + 1)

    ax.view_init(elev=18, azim=-60)
    ax.grid(True, linestyle='--', alpha=0.15)
    ax.set_box_aspect([LX_TOTAL + 4, LY_TOTAL + 4, H_TOTAL + 2])
    ax.tick_params(labelsize=6)


# ============================================================================
# 5. FIGURA PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(28, 14))
fig.patch.set_facecolor('#f5f7fa')

# Título
fig.text(0.5, 0.980,
         'M01 — MODELO 3D COMPARATIVO DE 3 SECCIONES ESTRUCTURALES',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color='#1a237e')

fig.text(0.5, 0.952,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo base 38x38 cm | Variaciones didacticas: 25x25 y 30x30 cm',
         ha='center', va='top', fontsize=12,
         color='#5dade2', style='italic')

# Subtítulo destacado
fig.text(0.5, 0.925,
         'METODO SHEAR BUILDING: rigidez lateral = solo columnas | Las MISMAS LUCES para los 3 modelos',
         ha='center', va='top', fontsize=11, fontweight='bold',
         color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fadbd8',
                   edgecolor='#c0392b',
                   linewidth=1.5))

# GridSpec: 3D en la parte inferior
gs = GridSpec(1, 3, figure=fig,
              left=0.02, right=0.98,
              top=0.80, bottom=0.04,
              wspace=0.10)

# Modelo A
ax_a = fig.add_subplot(gs[0, 0], projection='3d')
ax_a.set_facecolor(MODELOS['A']['color_bg'])
dibujar_portico(ax_a, MODELOS['A'])
rig_a = RIGIDECES['A']
ax_a.set_title(
    f"{MODELOS['A']['nombre']} — {MODELOS['A']['subtitulo']}\n"
    f"I_col = {rig_a['I_col_cm4']:.0f} cm4 | k_piso = {rig_a['k_piso_tm']:.0f} t/m",
    fontsize=13, fontweight='bold',
    color=MODELOS['A']['color_col'], pad=15)

# Modelo B
ax_b = fig.add_subplot(gs[0, 1], projection='3d')
ax_b.set_facecolor(MODELOS['B']['color_bg'])
dibujar_portico(ax_b, MODELOS['B'])
rig_b = RIGIDECES['B']
ax_b.set_title(
    f"{MODELOS['B']['nombre']} — {MODELOS['B']['subtitulo']}\n"
    f"I_col = {rig_b['I_col_cm4']:.0f} cm4 | k_piso = {rig_b['k_piso_tm']:.0f} t/m",
    fontsize=13, fontweight='bold',
    color=MODELOS['B']['color_col'], pad=15)

# Modelo C
ax_c = fig.add_subplot(gs[0, 2], projection='3d')
ax_c.set_facecolor(MODELOS['C']['color_bg'])
dibujar_portico(ax_c, MODELOS['C'])
rig_c = RIGIDECES['C']
ax_c.set_title(
    f"{MODELOS['C']['nombre']} — {MODELOS['C']['subtitulo']}\n"
    f"I_col = {rig_c['I_col_cm4']:.0f} cm4 | k_piso = {rig_c['k_piso_tm']:.0f} t/m",
    fontsize=13, fontweight='bold',
    color=MODELOS['C']['color_col'], pad=15)

# ============================================================================
# 6. CUADROS DE MENSAJES (ZONA SUPERIOR LIBRE)
# ============================================================================

# --- Cuadro 1: Resumen del proyecto ---
resumen_txt = (
    "[RESUMEN] DEL PROYECTO\n"
    "═══════════════════════════════════\n"
    f"  LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m\n"
    f"  Area = {AREA:.2f} m2\n"
    f"  Columnas: {N_COL_X} x {N_COL_Y} = {N_COL_TOTAL} u\n"
    f"  He = {He:.2f} m  |  N pisos = {N_PISOS}\n"
    f"  H_total = {H_TOTAL:.2f} m\n"
    f"  Vigas: {B_VIGA*100:.0f} x {H_VIGA*100:.0f} cm\n"
    "═══════════════════════════════════\n"
    f"  fc = {fc} kg/cm2  |  fy = {fy} kg/cm2\n"
    f"  Cm = {Cm} t/m2  |  Cv = {Cv} t/m2\n"
    f"  E = 12600*raiz(fc)"
)

fig.text(0.015, 0.905, resumen_txt,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor='#1a237e',
                   linewidth=1.8))

# --- Cuadro 2: Comparativo 1 ---
comp1_txt = (
    "[COMPARATIVO 1] SECCION DE COLUMNA\n"
    "═══════════════════════════════════════\n"
    f"  A: 25x25 cm  ->  k_piso = {RIGIDECES['A']['k_piso_tm']:>8.0f} t/m\n"
    f"  B: 30x30 cm  ->  k_piso = {RIGIDECES['B']['k_piso_tm']:>8.0f} t/m\n"
    f"  C: 38x38 cm  ->  k_piso = {RIGIDECES['C']['k_piso_tm']:>8.0f} t/m\n"
    "═══════════════════════════════════════\n"
    "  I_col = b x h^3 / 12"
)

fig.text(0.50, 0.905, comp1_txt,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='center', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#fef9e7',
                   edgecolor='#f39c12',
                   linewidth=1.8))

# --- Cuadro 3: Comparativo 2 ---
comp2_txt = (
    "[COMPARATIVO 2] RIGIDEZ AL CORTE\n"
    "═══════════════════════════════════════\n"
    f"  A: I_col = {RIGIDECES['A']['I_col_cm4']:>8.0f} cm4\n"
    f"  B: I_col = {RIGIDECES['B']['I_col_cm4']:>8.0f} cm4\n"
    f"  C: I_col = {RIGIDECES['C']['I_col_cm4']:>8.0f} cm4\n"
    "═══════════════════════════════════════\n"
    "  k_piso = N x k_col\n"
    "  k_col  = 12EIc / He^3"
)

fig.text(0.985, 0.905, comp2_txt,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#eafaf1',
                   edgecolor='#27ae60',
                   linewidth=1.8))

# ============================================================================
# 7. NOTA DIDÁCTICA AL PIE
# ============================================================================

fig.text(0.5, 0.012,
         'NOTA DIDACTICA: El MODELO C (38x38 cm) es el modelo base extraido del Excel PROYECTO.xlsx. '
         'Los MODELOS A y B son variaciones didacticas para comparar el efecto de la seccion de columna. '
         'Los 3 modelos comparten LAS MISMAS LUCES y geometria en planta.',
         ha='center', va='bottom', fontsize=9, style='italic',
         color='#7f8c8d',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#f8f9fa',
                   edgecolor='#bdc3c7',
                   linewidth=1))

# ============================================================================
# 8. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M01"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M01_modelo_3d_comparativo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M01 COMPLETADO")
print("=" * 80)
for key, modelo in MODELOS.items():
    rig = RIGIDECES[key]
    print(f"  Modelo {key} ({modelo['B_COL']*100:.0f}x{modelo['H_COL']*100:.0f} cm) [{modelo['etiqueta']}]:")
    print(f"    I_col  = {rig['I_col_cm4']:.2f} cm4")
    print(f"    k_piso = {rig['k_piso_tm']:.2f} t/m")
print("=" * 80)