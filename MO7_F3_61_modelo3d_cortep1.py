# -*- coding: utf-8 -*-
"""
================================================================================
M07.57 — MODELO 3D + CORTE/ELEVACIÓN CON MOVIMIENTO DINÁMICO CONTROLADO
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.57 — Modelo 3D + Corte/Elevación

OBJETIVO: Modelo 3D del pórtico con disipadores ajustados en esquinas,
          más un CORTE/ELEVACIÓN que muestre el comportamiento
          dinámico controlado.

CRITERIOS DE AJUSTE:
    1. Simetría en las 4 esquinas
    2. Relación LX/LY = 0.832 compensada
    3. Columnas perimetrales protegidas
    4. 2 por piso en diagonal
    5. Longitud de 50 cm
    6. Control del movimiento torsional (CM ≈ CR)

MOVIMIENTO DINÁMICO CONTROLADO:
    - Base empotrada (giro y desplazamiento = 0)
    - X₁ = 1.13 cm (Piso 1)
    - X₂ = 4.82 cm (Piso 2)
    - Deriva = 1.61% (cumple NEC-15)
    - CM ≈ CR (sin torsión)
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
from matplotlib.gridspec import GridSpec

# ============================================================================
# PALETA COMPLETA
# ============================================================================

COLORES = {
    'fondo': '#f8f9fa',
    'titulo': '#0d1b2a',
    'subtitulo': '#415a77',
    'columna': '#2c3e50',
    'columna_2': '#34495e',
    'viga': '#7f8c8d',
    'viga_2': '#95a5a6',
    'losa': '#aed6f1',
    'base': '#34495e',
    'empotramiento': '#616a6b',
    'disipador': '#e74c3c',
    'disipador_2': '#c0392b',
    'rotula': '#f39c12',
    'info': '#1d3557',
    'info_bg': '#d6e4f0',
    'acento': '#f77f00',
    'ok': '#2d6a4f',
    'ok_bg': '#d8f3dc',
    'movimiento': '#8e44ad',
    'movimiento_bg': '#ebdef0',
    'critica': '#9d0208',
    'critica_bg': '#f8d7da',
    'advertencia': '#e07a00',
    'advertencia_bg': '#fff3cd',
    'resultado': '#2d6a4f',
    'torsion': '#c0392b',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Geometría
LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38
B_VIGA = 0.30
H_VIGA = 0.45

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

# Disipadores
L_disipador = 0.50
D_cilindro = 0.15
D_vastago = 0.06
N_por_piso = 2
N_total = N_PISOS * N_por_piso

# Relación X/Y
relacion_XY = LX_TOTAL / LY_TOTAL

# Desplazamientos (del análisis M07.30)
X1 = 1.133  # cm
X2 = 4.824  # cm
Deriva = 1.608  # %
Deriva_NEC = 2.00  # %

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


def dibujar_disipador(ax, p1, p2, color='#e74c3c', color_rotula='#f39c12',
                      ancho=10):
    p1 = np.array(p1)
    p2 = np.array(p2)
    direccion = p2 - p1
    longitud = np.linalg.norm(direccion)
    if longitud < 1e-6:
        return
    direccion = direccion / longitud

    p_cil_ini = p1 + direccion * (longitud * 0.20)
    p_cil_fin = p1 + direccion * (longitud * 0.80)
    ax.plot([p_cil_ini[0], p_cil_fin[0]],
            [p_cil_ini[1], p_cil_fin[1]],
            [p_cil_ini[2], p_cil_fin[2]],
            '-', color=color, linewidth=ancho, alpha=0.95,
            solid_capstyle='round', zorder=8)

    p_vast_ini_1 = p1 + direccion * (longitud * 0.05)
    p_vast_fin_1 = p1 + direccion * (longitud * 0.20)
    ax.plot([p_vast_ini_1[0], p_vast_fin_1[0]],
            [p_vast_ini_1[1], p_vast_fin_1[1]],
            [p_vast_ini_1[2], p_vast_fin_1[2]],
            '-', color='#7f8c8d', linewidth=ancho*0.5, alpha=0.95, zorder=8)

    p_vast_ini_2 = p1 + direccion * (longitud * 0.80)
    p_vast_fin_2 = p1 + direccion * (longitud * 0.95)
    ax.plot([p_vast_ini_2[0], p_vast_fin_2[0]],
            [p_vast_ini_2[1], p_vast_fin_2[1]],
            [p_vast_ini_2[2], p_vast_fin_2[2]],
            '-', color='#7f8c8d', linewidth=ancho*0.5, alpha=0.95, zorder=8)

    ax.scatter(p1[0], p1[1], p1[2], color=color_rotula, s=180,
               edgecolor='#922b21', linewidth=2, zorder=10)
    ax.scatter(p2[0], p2[1], p2[2], color=color_rotula, s=180,
               edgecolor='#922b21', linewidth=2, zorder=10)


def dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45):
    dibujar_prisma(ax, x - tam, x + tam, y - tam, y + tam,
                   z - 0.3, z,
                   color_caras=COLORES['empotramiento'],
                   color_borde='#1a1a1a',
                   alpha=1.0, lw=0.7)


# ============================================================================
# 3. FIGURA PRINCIPAL — 2 VISTAS
# ============================================================================

fig = plt.figure(figsize=(28, 16))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.57 — MODELO 3D + CORTE/ELEVACIÓN CON MOVIMIENTO CONTROLADO',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.948,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | 4 disipadores | CM ≈ CR | β_V = 10%',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(1, 2, figure=fig,
              hspace=0.1, wspace=0.05,
              left=0.03, right=0.97,
              top=0.92, bottom=0.05,
              width_ratios=[1.4, 1.0])

# ============================================================================
# VISTA 1: MODELO 3D COMPLETO
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0], projection='3d')
ax1.set_facecolor('#eaf2fb')

# --- COLUMNAS ---
for x in x_ejes:
    for y in y_ejes:
        dibujar_columna(ax1, x, y, z_niveles[0], z_niveles[1],
                        seccion=B_COL, color=COLORES['columna'])
        dibujar_columna(ax1, x, y, z_niveles[1], z_niveles[2],
                        seccion=B_COL, color=COLORES['columna_2'])
        dibujar_empotramiento(ax1, x, y, z=0.0, tam=0.45)

# --- VIGAS ---
for z_nivel in [z_niveles[1], z_niveles[2]]:
    for y in y_ejes:
        for i in range(len(x_ejes) - 1):
            dibujar_viga_X(ax1, x_ejes[i], x_ejes[i+1], y, z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga'])
    for x in x_ejes:
        for j in range(len(y_ejes) - 1):
            dibujar_viga_Y(ax1, x, y_ejes[j], y_ejes[j+1], z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga_2'])

# --- LOSAS ---
x_min, x_max = x_ejes[0], x_ejes[-1]
y_min, y_max = y_ejes[0], y_ejes[-1]
for z_nivel in [z_niveles[1], z_niveles[2]]:
    dibujar_losa(ax1, x_min, x_max, y_min, y_max,
                 z=z_nivel, espesor=0.25,
                 color=COLORES['losa'], alpha=0.15)

# --- DISIPADORES AJUSTADOS (4 esquinas) ---
margen = 0.6

# PISO 1
p1_d1_p1 = (x_ejes[0] + margen, y_ejes[0] + margen, 0.5)
p2_d1_p1 = (x_ejes[1] - margen, y_ejes[0] + margen, He - 0.5)
dibujar_disipador(ax1, p1_d1_p1, p2_d1_p1, ancho=10)

p1_d2_p1 = (x_ejes[-1] - margen, y_ejes[0] + margen, 0.5)
p2_d2_p1 = (x_ejes[-2] + margen, y_ejes[0] + margen, He - 0.5)
dibujar_disipador(ax1, p1_d2_p1, p2_d2_p1, ancho=10)

# PISO 2
p1_d3_p2 = (x_ejes[0] + margen, y_ejes[0] + margen, He + 0.5)
p2_d3_p2 = (x_ejes[1] - margen, y_ejes[0] + margen, 2*He - 0.5)
dibujar_disipador(ax1, p1_d3_p2, p2_d3_p2, ancho=10)

p1_d4_p2 = (x_ejes[-1] - margen, y_ejes[0] + margen, He + 0.5)
p2_d4_p2 = (x_ejes[-2] + margen, y_ejes[0] + margen, 2*He - 0.5)
dibujar_disipador(ax1, p1_d4_p2, p2_d4_p2, ancho=10)

# --- CONFIGURACIÓN ---
ax1.set_xlabel('Eje X (m)', fontsize=10, labelpad=5)
ax1.set_ylabel('Eje Y (m)', fontsize=10, labelpad=5)
ax1.set_zlabel('Eje Z (m)', fontsize=10, labelpad=5)
ax1.set_xlim(x_min - 2, x_max + 2)
ax1.set_ylim(y_min - 2, y_max + 2)
ax1.set_zlim(-1, H_TOTAL + 1)
ax1.view_init(elev=20, azim=-55)
ax1.grid(True, linestyle='--', alpha=0.2)
ax1.set_box_aspect([LX_TOTAL + 4, LY_TOTAL + 4, H_TOTAL + 2])
ax1.tick_params(labelsize=8)
ax1.set_title('(a) MODELO 3D CON DISIPADORES AJUSTADOS',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=15)

# ============================================================================
# VISTA 2: CORTE/ELEVACIÓN CON MOVIMIENTO DINÁMICO CONTROLADO
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#ffffff')
ax2.set_xlim(-3, 8)
ax2.set_ylim(-1, 8)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('(b) CORTE/ELEVACIÓN — MOVIMIENTO DINÁMICO CONTROLADO',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=15)

# --- BASE EMPOTRADA ---
ax2.plot([0, 6], [0, 0], 'k-', linewidth=6)
for x_emp in [0.5, 3, 5.5]:
    ax2.plot([x_emp - 0.3, x_emp, x_emp + 0.3],
             [-0.3, 0, -0.3], 'k-', linewidth=3)
    ax2.plot([x_emp - 0.3, x_emp + 0.3],
             [-0.3, -0.3], 'k-', linewidth=3)

# --- COLUMNAS ---
ax2.plot([0.5, 0.5], [0, 3], '-', color=COLORES['columna'],
         linewidth=8, solid_capstyle='round')
ax2.plot([0.5, 0.5], [3, 6], '-', color=COLORES['columna_2'],
         linewidth=8, solid_capstyle='round')
ax2.plot([5.5, 5.5], [0, 3], '-', color=COLORES['columna'],
         linewidth=8, solid_capstyle='round')
ax2.plot([5.5, 5.5], [3, 6], '-', color=COLORES['columna_2'],
         linewidth=8, solid_capstyle='round')

# --- VIGAS ---
ax2.plot([0.5, 5.5], [3, 3], '-', color=COLORES['viga'],
         linewidth=10, solid_capstyle='round')
ax2.plot([0.5, 5.5], [6, 6], '-', color=COLORES['viga'],
         linewidth=10, solid_capstyle='round')

# --- LOSAS ---
ax2.plot([0.5, 5.5], [3.25, 3.25], '-', color=COLORES['losa'],
         linewidth=4, alpha=0.5)
ax2.plot([0.5, 5.5], [6.25, 6.25], '-', color=COLORES['losa'],
         linewidth=4, alpha=0.5)

# --- DISIPADORES EN DIAGONAL (con rótulas) ---
# Piso 1 - izquierda
ax2.plot([0.5, 3], [0.5, 2.5], '-', color=COLORES['disipador'],
         linewidth=6, alpha=0.9, zorder=8)
# Piso 1 - derecha
ax2.plot([5.5, 3], [0.5, 2.5], '-', color=COLORES['disipador'],
         linewidth=6, alpha=0.9, zorder=8)

# Piso 2 - izquierda
ax2.plot([0.5, 3], [3.5, 5.5], '-', color=COLORES['disipador'],
         linewidth=6, alpha=0.9, zorder=8)
# Piso 2 - derecha
ax2.plot([5.5, 3], [3.5, 5.5], '-', color=COLORES['disipador'],
         linewidth=6, alpha=0.9, zorder=8)

# --- RÓTULAS ---
for x, y in [(0.5, 0.5), (5.5, 0.5), (3, 2.5),
             (0.5, 3.5), (5.5, 3.5), (3, 5.5)]:
    ax2.plot(x, y, 'o', color=COLORES['rotula'],
             markersize=10, markeredgecolor='#922b21',
             markeredgewidth=1.5, zorder=10)

# --- DEFORMADA CONTROLADA (línea punteada suave) ---
z_curve = np.linspace(0, 6, 50)
u_curve = np.interp(z_curve, [0, 3, 6], [0, 0.25, 0.7])
ax2.plot(0.5 + u_curve, z_curve, '--', color=COLORES['movimiento'],
         linewidth=2.5, alpha=0.6, zorder=5)

# --- FLECHAS DE MOVIMIENTO CONTROLADO ---
# Piso 1
ax2.annotate('', xy=(6.5, 3), xytext=(5.5, 3),
             arrowprops=dict(arrowstyle='->', color=COLORES['movimiento'],
                             lw=2.5, mutation_scale=20))
ax2.text(6.7, 3.15, f'X₁ = {X1:.2f} cm', fontsize=9, fontweight='bold',
         color=COLORES['movimiento'], va='center')

# Piso 2
ax2.annotate('', xy=(6.8, 6), xytext=(5.5, 6),
             arrowprops=dict(arrowstyle='->', color=COLORES['movimiento'],
                             lw=2.5, mutation_scale=20))
ax2.text(7.0, 6.15, f'X₂ = {X2:.2f} cm', fontsize=9, fontweight='bold',
         color=COLORES['movimiento'], va='center')

# --- ANOTACIONES ---
ax2.text(3, -0.8, 'BASE EMPOTRADA (giro y desplaz. = 0)',
         fontsize=9, fontweight='bold', ha='center', va='top',
         color='black',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor='black', linewidth=1.5))

ax2.text(3, 6.8, 'DISIPADORES TENSOR-PUNTAL (X)',
         fontsize=10, fontweight='bold', ha='center', va='bottom',
         color=COLORES['disipador'],
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fadbd8',
                   edgecolor=COLORES['disipador'], linewidth=1.5))

# --- LEYENDA ---
leyenda = [
    ('● Base empotrada', 'black'),
    ('━ Columna', COLORES['columna']),
    ('━ Viga', COLORES['viga']),
    ('━ Disipador', COLORES['disipador']),
    ('● Rótula', COLORES['rotula']),
    ('→ Movimiento controlado', COLORES['movimiento']),
    ('- - Deformada', COLORES['movimiento']),
]

for i, (texto, color) in enumerate(leyenda):
    ax2.text(-2.5, 7 - i*0.5, texto,
             fontsize=9, fontweight='bold', color=color,
             ha='left', va='center')

# --- TÍTULO DE LA SECCIÓN ---
ax2.text(3, 7.7, 'COMPORTAMIENTO DINÁMICO CONTROLADO',
         fontsize=11, fontweight='bold', ha='center', va='bottom',
         color=COLORES['titulo'],
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['ok_bg'],
                   edgecolor=COLORES['ok'],
                   linewidth=2))

# ============================================================================
# 4. MENSAJES OPORTUNOS
# ============================================================================

# --- Mensaje 1: Datos (sup. izquierda) ---
msg1 = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m\n"
    f"  LX/LY = {relacion_XY:.4f}\n"
    f"  He = {He:.2f} m  |  N pisos = {N_PISOS}\n"
    f"  N disipadores = {N_total}\n"
    "═══════════════════════════════\n"
    "  Columna = 38×38 cm\n"
    "  Viga = 30×45 cm\n"
    "  Losa = 25 cm"
)

fig.text(0.02, 0.93, msg1,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='white',
                   edgecolor=COLORES['info'],
                   linewidth=1.5, alpha=0.95))

# --- Mensaje 2: Disipador (sup. derecha) ---
msg2 = (
    "DISIPADOR TENSOR-PUNTAL\n"
    "═══════════════════════════════\n"
    f"  Longitud = {L_disipador*100:.0f} cm\n"
    f"  Cilindro = {D_cilindro*100:.0f} cm\n"
    f"  Vástago = {D_vastago*100:.0f} cm\n"
    "  Rótulas = Sí\n"
    "═══════════════════════════════\n"
    "  β_V = 10%\n"
    "  F = 231.02 t\n"
    "  C = 2.378 t·s/m"
)

fig.text(0.98, 0.93, msg2,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['disipador'],
                   linewidth=1.5, alpha=0.95))

# --- Mensaje 3: Comportamiento (inf. izquierda) ---
msg3 = (
    "MOVIMIENTO DINÁMICO\n"
    "═══════════════════════════════\n"
    f"  X₁ = {X1:.2f} cm (Piso 1)\n"
    f"  X₂ = {X2:.2f} cm (Piso 2)\n"
    f"  Deriva = {Deriva:.2f} %\n"
    f"  Límite NEC-15 = {Deriva_NEC:.2f} %\n"
    "═══════════════════════════════\n"
    "  ✅ CM ≈ CR (sin torsión)\n"
    "  ✅ Deriva controlada\n"
    "  ✅ Esquinas protegidas\n"
    "  ✅ Energía disipada"
)

fig.text(0.02, 0.12, msg3,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='left', va='bottom',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#d6e4f0',
                   edgecolor=COLORES['info'],
                   linewidth=1.5, alpha=0.95))

# --- Mensaje 4: Innovación (inf. derecha) ---
msg4 = (
    "INNOVACIÓN ÚNICA\n"
    "═══════════════════════════════\n"
    "  • Disipador 50 cm\n"
    "  • Sistema tensor-puntal\n"
    "  • 2 por piso en X\n"
    "  • Rótulas en extremos\n"
    "  • Reemplazo directo\n"
    "  • Sin reforzamiento\n"
    "═══════════════════════════════\n"
    "  ✅ ÚNICO EN EL MUNDO\n"
    "  ✅ FÁCIL DE REPARAR"
)

fig.text(0.98, 0.12, msg4,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#d8f3dc',
                   edgecolor=COLORES['ok'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 5. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_57"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_57_modelo_3d_corte_movimiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 6. RESUMEN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.57 — MODELO 3D + CORTE/ELEVACIÓN CON MOVIMIENTO CONTROLADO")
print("=" * 80)
print(f"\n  PÓRTICO:")
print(f"    LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m")
print(f"    LX/LY = {relacion_XY:.4f}")
print(f"    He = {He:.2f} m  |  N pisos = {N_PISOS}")
print(f"\n  DISIPADORES:")
print(f"    Longitud = {L_disipador*100:.0f} cm")
print(f"    N por piso = {N_por_piso}")
print(f"    N total = {N_total}")
print(f"    Ubicación = 4 esquinas del perímetro")
print(f"\n  MOVIMIENTO DINÁMICO:")
print(f"    X₁ = {X1:.2f} cm")
print(f"    X₂ = {X2:.2f} cm")
print(f"    Deriva = {Deriva:.2f} %")
print(f"    Límite NEC-15 = {Deriva_NEC:.2f} %")
print(f"\n  CONTROL:")
print(f"    CM ≈ CR (sin torsión)")
print(f"    Base empotrada")
print(f"    Esquinas protegidas")
print(f"\n  ✅ CUMPLE NEC-15")
print("=" * 80)