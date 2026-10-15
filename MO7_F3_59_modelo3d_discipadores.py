# -*- coding: utf-8 -*-
"""
================================================================================
M07.53 — MODELO 3D CON DISIPADORES TENSOR-PUNTAL (RECUPERADO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.53 — Modelo 3D con Disipadores

OBJETIVO: Visualizar el pórtico en 3D con los disipadores
          tensor-puntal colocados en diagonal.

CONFIGURACIÓN:
    - Pórtico de 2 pisos
    - 2 disipadores por piso (en X)
    - Disipadores de 50 cm
    - Rótulas en extremos
    - Sistema tensor-puntal

DATOS DEL PROYECTO:
    - He = 3.00 m
    - N_pisos = 2
    - N_disipadores = 4
    - L_disipador = 50 cm
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ============================================================================
# PALETA (CORREGIDA — con todas las claves necesarias)
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
    'rotula': '#f39c12',
    'acero': '#495057',
    'info': '#1d3557',
    'acento': '#f77f00',
    'ok': '#2d6a4f',
    'ok_bg': '#d8f3dc',
    'advertencia': '#e07a00',
    'advertencia_bg': '#fff3cd',
    'critica': '#9d0208',
    'critica_bg': '#f8d7da',
    'resultado': '#2d6a4f',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_alerta': '#fadbd8',
    'box_alerta_borde': '#c0392b',
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
L_disipador = 0.50  # m (50 cm)
D_cilindro = 0.15   # m (15 cm)
D_vastago = 0.06    # m (6 cm)
N_por_piso = 2
N_total = N_PISOS * N_por_piso

# ============================================================================
# 2. FUNCIONES DE DIBUJO 3D
# ============================================================================

def dibujar_prisma(ax, x0, x1, y0, y1, z0, z1,
                   color_caras='#5c7a99', color_borde='#1a1a1a',
                   alpha=1.0, lw=0.8):
    """Dibuja un prisma rectangular 3D."""
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


def dibujar_disipador(ax, p1, p2, color='#e74c3c', color_rotula='#f39c12'):
    """Dibuja un disipador tensor-puntal entre dos puntos."""
    p1 = np.array(p1)
    p2 = np.array(p2)
    
    direccion = p2 - p1
    longitud = np.linalg.norm(direccion)
    
    if longitud < 1e-6:
        return
    
    direccion = direccion / longitud
    
    # Cilindro principal (60% del centro)
    p_cil_ini = p1 + direccion * (longitud * 0.20)
    p_cil_fin = p1 + direccion * (longitud * 0.80)
    
    ax.plot([p_cil_ini[0], p_cil_fin[0]],
            [p_cil_ini[1], p_cil_fin[1]],
            [p_cil_ini[2], p_cil_fin[2]],
            '-', color=color, linewidth=10, alpha=0.95,
            solid_capstyle='round', zorder=8)
    
    # Vástagos (20% a cada lado)
    p_vast_ini_1 = p1 + direccion * (longitud * 0.05)
    p_vast_fin_1 = p1 + direccion * (longitud * 0.20)
    ax.plot([p_vast_ini_1[0], p_vast_fin_1[0]],
            [p_vast_ini_1[1], p_vast_fin_1[1]],
            [p_vast_ini_1[2], p_vast_fin_1[2]],
            '-', color='#7f8c8d', linewidth=5, alpha=0.95, zorder=8)
    
    p_vast_ini_2 = p1 + direccion * (longitud * 0.80)
    p_vast_fin_2 = p1 + direccion * (longitud * 0.95)
    ax.plot([p_vast_ini_2[0], p_vast_fin_2[0]],
            [p_vast_ini_2[1], p_vast_fin_2[1]],
            [p_vast_ini_2[2], p_vast_fin_2[2]],
            '-', color='#7f8c8d', linewidth=5, alpha=0.95, zorder=8)
    
    # Rótulas (esferas en extremos)
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
# 3. FIGURA PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.53 — MODELO 3D CON DISIPADORES TENSOR-PUNTAL',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.948,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | 4 disipadores | L = 50 cm',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# Eje 3D
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#eaf2fb')

# ============================================================================
# 4. DIBUJAR COLUMNAS
# ============================================================================

for x in x_ejes:
    for y in y_ejes:
        dibujar_columna(ax, x, y, z_niveles[0], z_niveles[1],
                        seccion=B_COL, color=COLORES['columna'])
        dibujar_columna(ax, x, y, z_niveles[1], z_niveles[2],
                        seccion=B_COL, color=COLORES['columna_2'])
        dibujar_empotramiento(ax, x, y, z=0.0, tam=0.45)

# ============================================================================
# 5. DIBUJAR VIGAS
# ============================================================================

for z_nivel in [z_niveles[1], z_niveles[2]]:
    for y in y_ejes:
        for i in range(len(x_ejes) - 1):
            dibujar_viga_X(ax, x_ejes[i], x_ejes[i+1], y, z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga'])
    for x in x_ejes:
        for j in range(len(y_ejes) - 1):
            dibujar_viga_Y(ax, x, y_ejes[j], y_ejes[j+1], z_nivel,
                           b=B_VIGA, h=H_VIGA, color=COLORES['viga_2'])

# ============================================================================
# 6. DIBUJAR LOSAS
# ============================================================================

x_min, x_max = x_ejes[0], x_ejes[-1]
y_min, y_max = y_ejes[0], y_ejes[-1]

for z_nivel in [z_niveles[1], z_niveles[2]]:
    dibujar_losa(ax, x_min, x_max, y_min, y_max,
                 z=z_nivel, espesor=0.25,
                 color=COLORES['losa'], alpha=0.15)

# ============================================================================
# 7. DIBUJAR DISIPADORES TENSOR-PUNTAL (en diagonal)
# ============================================================================

# DISIPADORES PISO 1
# Disipador 1 - Piso 1 (frente izquierda)
p1 = (x_ejes[0] + 0.3, y_ejes[0] + 0.3, 0.5)
p2 = (x_ejes[1] - 0.3, y_ejes[0] + 0.3, He - 0.5)
dibujar_disipador(ax, p1, p2)

# Disipador 2 - Piso 1 (frente derecha)
p1 = (x_ejes[-1] - 0.3, y_ejes[0] + 0.3, 0.5)
p2 = (x_ejes[-2] + 0.3, y_ejes[0] + 0.3, He - 0.5)
dibujar_disipador(ax, p1, p2)

# DISIPADORES PISO 2
# Disipador 3 - Piso 2 (frente izquierda)
p1 = (x_ejes[0] + 0.3, y_ejes[0] + 0.3, He + 0.5)
p2 = (x_ejes[1] - 0.3, y_ejes[0] + 0.3, 2*He - 0.5)
dibujar_disipador(ax, p1, p2)

# Disipador 4 - Piso 2 (frente derecha)
p1 = (x_ejes[-1] - 0.3, y_ejes[0] + 0.3, He + 0.5)
p2 = (x_ejes[-2] + 0.3, y_ejes[0] + 0.3, 2*He - 0.5)
dibujar_disipador(ax, p1, p2)

# ============================================================================
# 8. CONFIGURACIÓN DE EJES
# ============================================================================

ax.set_xlabel('Eje X (m)', fontsize=11, labelpad=10)
ax.set_ylabel('Eje Y (m)', fontsize=11, labelpad=10)
ax.set_zlabel('Eje Z (m)', fontsize=11, labelpad=10)

ax.set_xlim(x_min - 2, x_max + 2)
ax.set_ylim(y_min - 2, y_max + 2)
ax.set_zlim(-1, H_TOTAL + 1)

ax.view_init(elev=22, azim=-55)
ax.grid(True, linestyle='--', alpha=0.2)
ax.set_box_aspect([LX_TOTAL + 4, LY_TOTAL + 4, H_TOTAL + 2])
ax.tick_params(labelsize=8)

# ============================================================================
# 9. MENSAJES OPORTUNOS
# ============================================================================

msg1 = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  LX = {LX_TOTAL:.2f} m  |  LY = {LY_TOTAL:.2f} m\n"
    f"  He = {He:.2f} m\n"
    f"  N pisos = {N_PISOS}\n"
    f"  N disipadores = {N_total}\n"
    "═══════════════════════════════\n"
    "  Columna = 38×38 cm\n"
    "  Viga = 30×45 cm\n"
    "  Losa = 25 cm"
)

fig.text(0.02, 0.93, msg1,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor=COLORES['info'],
                   linewidth=1.8, alpha=0.95))

msg2 = (
    "DISIPADOR TENSOR-PUNTAL\n"
    "═══════════════════════════════\n"
    f"  Longitud = {L_disipador*100:.0f} cm\n"
    f"  Cilindro = {D_cilindro*100:.0f} cm\n"
    f"  Vástago = {D_vastago*100:.0f} cm\n"
    "  Rótulas = Sí\n"
    "═══════════════════════════════\n"
    "  C_total = 2.378 t·s/m\n"
    "  β_V = 10%\n"
    "  F = 231.02 t"
)

fig.text(0.98, 0.93, msg2,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['disipador'],
                   linewidth=1.8, alpha=0.95))

msg3 = (
    "COLOCACIÓN\n"
    "═══════════════════════════════\n"
    "  Piso 1: 2 disipadores\n"
    "  Piso 2: 2 disipadores\n"
    "  Total: 4 disipadores\n"
    "═══════════════════════════════\n"
    "  Tipo: Tensor-puntal\n"
    "  Forma: Diagonal (X)\n"
    "  Función: Solo tracción"
)

fig.text(0.02, 0.12, msg3,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='left', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#d6e4f0',
                   edgecolor=COLORES['info'],
                   linewidth=1.8, alpha=0.95))

msg4 = (
    "OBJETIVO\n"
    "═══════════════════════════════\n"
    "  Reducir aceleración\n"
    "  Aumentar amortiguamiento\n"
    "  Proteger estructura\n"
    "═══════════════════════════════\n"
    "  β_V = 10%\n"
    "  Sa reducido = 47%\n"
    "  Deriva controlada\n"
    "  ✅ Reparación fácil"
)

fig.text(0.98, 0.12, msg4,
         transform=fig.transFigure,
         fontsize=8.5, family='monospace',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#d8f3dc',
                   edgecolor=COLORES['ok'],
                   linewidth=1.8, alpha=0.95))

# ============================================================================
# 10. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_53"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_53_modelo_3d_disipadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 11. RESUMEN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.53 — MODELO 3D CON DISIPADORES TENSOR-PUNTAL")
print("=" * 80)
print(f"\n  PÓRTICO:")
print(f"    LX = {LX_TOTAL:.2f} m")
print(f"    LY = {LY_TOTAL:.2f} m")
print(f"    He = {He:.2f} m")
print(f"    N pisos = {N_PISOS}")
print(f"\n  DISIPADORES:")
print(f"    Longitud = {L_disipador*100:.0f} cm")
print(f"    Cilindro = {D_cilindro*100:.0f} cm")
print(f"    Vástago = {D_vastago*100:.0f} cm")
print(f"    N por piso = {N_por_piso}")
print(f"    N total = {N_total}")
print(f"\n  CARACTERÍSTICAS:")
print(f"    C_total = 2.378 t·s/m")
print(f"    F = 231.02 t")
print(f"    β_V = 10%")
print(f"\n  TIPO:")
print(f"    Sistema: Tensor-puntal")
print(f"    Función: Solo tracción")
print(f"    Forma: Diagonal (X)")
print(f"\n  ✅ Reparación fácil sin reforzamiento extremo")
print("=" * 80)