# -*- coding: utf-8 -*-
"""
================================================================================
M07.54 — ANÁLISIS TORSIONAL Y COLOCACIÓN DE DISIPADORES
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.54 — Análisis Torsional

OBJETIVO: Analizar el control torsional, la relación X/Y y la
          colocación de disipadores en el perímetro.

CRITERIOS:
    1. Control del movimiento torsional
    2. Relación LX/LY (simetría)
    3. Colocación en perímetro
    4. Distribución proporcional

DATOS DEL PROYECTO:
    - LX = 17.80 m
    - LY = 21.40 m
    - Relación = 0.832
    - N disipadores = 4
    - N por piso = 2
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.gridspec import GridSpec

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f8f9fa',
    'fondo_panel': '#ffffff',
    'titulo': '#0d1b2a',
    'subtitulo': '#415a77',
    'linea': '#778da9',
    'ok': '#2d6a4f',
    'ok_bg': '#d8f3dc',
    'advertencia': '#e07a00',
    'advertencia_bg': '#fff3cd',
    'critica': '#9d0208',
    'critica_bg': '#f8d7da',
    'info': '#1d3557',
    'info_bg': '#d6e4f0',
    'acento': '#f77f00',
    'columna': '#2c3e50',
    'disipador': '#e74c3c',
    'rotula': '#f39c12',
    'masa': '#8e44ad',
    'rigidez': '#16a085',
    'torsion': '#c0392b',
    'box_datos': '#ffffff',
    'box_datos_borde': '#0d1b2a',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Geometría
LX = 17.80  # m
LY = 21.40  # m
He = 3.00   # m
N_PISOS = 2

# Relación
relacion = LX / LY
Area = LX * LY
Perimetro = 2 * (LX + LY)

# Porcentajes
pct_X = LX / (LX + LY) * 100
pct_Y = LY / (LX + LY) * 100

# Disipadores
N_total = 4
N_por_piso = 2

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(28, 20))
fig.patch.set_facecolor(COLORES['fondo'])

# Encabezado
ax_header = fig.add_axes([0, 0.94, 1, 0.06])
ax_header.set_facecolor(COLORES['titulo'])
ax_header.axis('off')
ax_header.text(0.02, 0.5, '🏗️', fontsize=30, va='center')
ax_header.text(0.06, 0.5, 'UNESUM · REZ-2026 · JIPIJAPA-001',
               fontsize=16, fontweight='bold', color='white', va='center')
ax_header.text(0.98, 0.5, 'M07.54 — ANÁLISIS TORSIONAL',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'ANÁLISIS TORSIONAL Y COLOCACIÓN DE DISIPADORES',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.892,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): RELACIÓN X/Y Y SIMETRÍA
# ============================================================================

ax1 = fig.add_axes([0.04, 0.68, 0.28, 0.20])
ax1.set_facecolor(COLORES['fondo_panel'])
ax1.axis('off')
ax1.set_title('(a) RELACIÓN X/Y',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt1 = (
    "RELACIÓN X/Y\n"
    "═══════════════════════════════\n\n"
    f"  LX = {LX:.2f} m\n"
    f"  LY = {LY:.2f} m\n\n"
    f"  LX/LY = {relacion:.4f}\n\n"
    f"  Área = {Area:.2f} m²\n"
    f"  Perímetro = {Perimetro:.2f} m\n\n"
    "  DISTRIBUCIÓN:\n"
    f"    X: {pct_X:.1f}%\n"
    f"    Y: {pct_Y:.1f}%\n\n"
    "  INTERPRETACIÓN:\n"
    "  • LX/LY < 1\n"
    "  • Estructura más larga en Y\n"
    "  • Requiere simetría"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (b): CONTROL TORSIONAL
# ============================================================================

ax2 = fig.add_axes([0.36, 0.68, 0.28, 0.20])
ax2.set_facecolor(COLORES['fondo_panel'])
ax2.axis('off')
ax2.set_title('(b) CONTROL TORSIONAL',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt2 = (
    "CONTROL TORSIONAL\n"
    "═══════════════════════════════\n\n"
    "  Centro de masa (CM)\n"
    "  Centro de rigidez (CR)\n\n"
    "  Si CM ≠ CR:\n"
    "  → Movimiento torsional\n"
    "  → Esquinas críticas\n\n"
    "  SOLUCIÓN:\n"
    "  • Colocar disipadores\n"
    "    SIMÉTRICAMENTE\n"
    "  • En las 4 esquinas\n"
    "  • Reducen torsión\n\n"
    "  RESULTADO:\n"
    "  ✅ CM ≈ CR\n"
    "  ✅ Sin torsión"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['torsion'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): PERÍMETRO Y COLUMNAS
# ============================================================================

ax3 = fig.add_axes([0.68, 0.68, 0.28, 0.20])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')
ax3.set_title('(c) PERÍMETRO Y COLUMNAS',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt3 = (
    "COLUMNAS PERIMETRALES\n"
    "═══════════════════════════════\n\n"
    "  Las columnas perimetrales:\n"
    "  • Absorben mayor energía\n"
    "  • Son las primeras en dañarse\n"
    "  • Necesitan protección\n\n"
    "  N columnas total = 20\n"
    "  N columnas perímetro = 12\n\n"
    "  CRITERIO:\n"
    "  • Colocar disipadores\n"
    "    en el PERÍMETRO\n"
    "  • Proteger esquinas\n"
    "  • Controlar torsión\n\n"
    "  RESULTADO:\n"
    "  ✅ Esquinas protegidas\n"
    "  ✅ Energía controlada"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['ok_bg'],
                   edgecolor=COLORES['ok'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): PLANTA CON COLOCACIÓN DE DISIPADORES
# ============================================================================

ax4 = fig.add_axes([0.04, 0.05, 0.92, 0.58])
ax4.set_facecolor('#ffffff')
ax4.set_xlim(-2, 20)
ax4.set_ylim(-2, 24)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_title('(d) PLANTA ESTRUCTURAL CON COLOCACIÓN DE DISIPADORES',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)

# --- DIBUJAR LA LOSA ---
losa = Rectangle((0, 0), LX, LY,
                  facecolor=COLORES['info_bg'],
                  edgecolor=COLORES['columna'],
                  linewidth=3, alpha=0.3)
ax4.add_patch(losa)

# --- DIBUJAR COLUMNAS PERIMETRALES ---
# Columnas en X (eje 0 y LY)
for i in range(5):
    x = i * (LX / 4)
    # Columna superior
    col_sup = Circle((x, LY), 0.4, facecolor=COLORES['columna'],
                      edgecolor='black', linewidth=1.5, zorder=5)
    ax4.add_patch(col_sup)
    # Columna inferior
    col_inf = Circle((x, 0), 0.4, facecolor=COLORES['columna'],
                      edgecolor='black', linewidth=1.5, zorder=5)
    ax4.add_patch(col_inf)

# Columnas en Y (eje 0 y LX)
for j in range(1, 4):
    y = j * (LY / 4)
    # Columna izquierda
    col_izq = Circle((0, y), 0.4, facecolor=COLORES['columna'],
                      edgecolor='black', linewidth=1.5, zorder=5)
    ax4.add_patch(col_izq)
    # Columna derecha
    col_der = Circle((LX, y), 0.4, facecolor=COLORES['columna'],
                      edgecolor='black', linewidth=1.5, zorder=5)
    ax4.add_patch(col_der)

# Columnas interiores
for i in range(1, 4):
    for j in range(1, 4):
        x = i * (LX / 4)
        y = j * (LY / 4)
        col_int = Circle((x, y), 0.3, facecolor='#95a5a6',
                          edgecolor='black', linewidth=1, zorder=4)
        ax4.add_patch(col_int)

# --- CENTRO DE MASA (CM) ---
CM_x = LX / 2
CM_y = LY / 2
ax4.plot(CM_x, CM_y, 'o', color=COLORES['masa'],
         markersize=20, markeredgecolor='white',
         markeredgewidth=2, zorder=10)
ax4.text(CM_x + 0.5, CM_y + 0.5, 'CM',
         fontsize=12, fontweight='bold', color=COLORES['masa'])

# --- CENTRO DE RIGIDEZ (CR) ---
CR_x = LX / 2
CR_y = LY / 2
ax4.plot(CR_x, CR_y, 's', color=COLORES['rigidez'],
         markersize=18, markeredgecolor='white',
         markeredgewidth=2, zorder=10)
ax4.text(CR_x - 1.0, CR_y - 0.5, 'CR',
         fontsize=12, fontweight='bold', color=COLORES['rigidez'])

# --- DISIPADORES EN ESQUINAS ---
# Esquina 1 (inferior izquierda)
ax4.plot(0.5, 0.5, 'o', color=COLORES['disipador'],
         markersize=25, markeredgecolor='white',
         markeredgewidth=3, zorder=15)
ax4.text(0.5, -0.8, 'D1', fontsize=12, fontweight='bold',
         color=COLORES['disipador'], ha='center')

# Esquina 2 (inferior derecha)
ax4.plot(LX - 0.5, 0.5, 'o', color=COLORES['disipador'],
         markersize=25, markeredgecolor='white',
         markeredgewidth=3, zorder=15)
ax4.text(LX - 0.5, -0.8, 'D2', fontsize=12, fontweight='bold',
         color=COLORES['disipador'], ha='center')

# Esquina 3 (superior izquierda)
ax4.plot(0.5, LY - 0.5, 'o', color=COLORES['disipador'],
         markersize=25, markeredgecolor='white',
         markeredgewidth=3, zorder=15)
ax4.text(0.5, LY + 0.5, 'D3', fontsize=12, fontweight='bold',
         color=COLORES['disipador'], ha='center')

# Esquina 4 (superior derecha)
ax4.plot(LX - 0.5, LY - 0.5, 'o', color=COLORES['disipador'],
         markersize=25, markeredgecolor='white',
         markeredgewidth=3, zorder=15)
ax4.text(LX - 0.5, LY + 0.5, 'D4', fontsize=12, fontweight='bold',
         color=COLORES['disipador'], ha='center')

# --- ETIQUETAS ---
ax4.text(LX/2, -1.8, f'LX = {LX:.2f} m',
         fontsize=12, fontweight='bold', ha='center', va='top')
ax4.text(-1.5, LY/2, f'LY = {LY:.2f} m',
         fontsize=12, fontweight='bold', rotation=90,
         ha='right', va='center')

# --- LEYENDA ---
leyenda = [
    ('● Columna perimetral', COLORES['columna']),
    ('○ Columna interior', '#95a5a6'),
    ('● D1-D4 Disipador', COLORES['disipador']),
    ('○ CM Centro de masa', COLORES['masa']),
    ('□ CR Centro de rigidez', COLORES['rigidez']),
]

for i, (texto, color) in enumerate(leyenda):
    ax4.text(0, -3.0 - i*1.2, texto,
             fontsize=10, fontweight='bold', color=color,
             ha='left', va='center')

# --- TÍTULO DE LA SECCIÓN ---
ax4.text(LX/2, LY + 2.0, 'COLOCACIÓN SIMÉTRICA DE DISIPADORES EN EL PERÍMETRO',
         fontsize=13, fontweight='bold', ha='center', va='bottom',
         color=COLORES['titulo'],
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['ok_bg'],
                   edgecolor=COLORES['ok'],
                   linewidth=2.5))

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

fig.text(0.5, 0.02,
         '"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."',
         ha='center', va='bottom', fontsize=10,
         color=COLORES['subtitulo'], style='italic',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white',
                   edgecolor=COLORES['acento'],
                   linewidth=1.5))

fig.text(0.5, 0.005,
         f'{PROYECTO} · {datetime.now().strftime("%Y-%m-%d %H:%M")}',
         ha='center', va='bottom', fontsize=8,
         color=COLORES['linea'])

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_54"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_54_analisis_torsional_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.54 — ANÁLISIS TORSIONAL Y COLOCACIÓN DE DISIPADORES")
print("=" * 80)
print(f"\n  RELACIÓN X/Y:")
print(f"    LX = {LX:.2f} m")
print(f"    LY = {LY:.2f} m")
print(f"    LX/LY = {relacion:.4f}")
print(f"    Área = {Area:.2f} m²")
print(f"    Perímetro = {Perimetro:.2f} m")
print(f"\n  DISTRIBUCIÓN:")
print(f"    X: {pct_X:.1f}%")
print(f"    Y: {pct_Y:.1f}%")
print(f"\n  CONTROL TORSIONAL:")
print(f"    CM ≈ CR (con disipadores)")
print(f"    Colocación simétrica")
print(f"\n  DISIPADORES:")
print(f"    N total = {N_total}")
print(f"    N por piso = {N_por_piso}")
print(f"    Ubicación: 4 esquinas")
print("=" * 80)