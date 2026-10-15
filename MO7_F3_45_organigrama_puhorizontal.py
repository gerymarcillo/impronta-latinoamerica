# -*- coding: utf-8 -*-
"""
================================================================================
M07.23 — ORGANIGRAMA HORIZONTAL DEL PUSHOVER (AJUSTADO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.23 — Organigrama del Pushover

ESENCIA:
    La curva de Pushover = comportamiento real de la estructura bajo
    cargas laterales incrementales, desde el rango elástico hasta
    la fluencia y el colapso.

DATOS CONFIRMADOS:
    - Sd = 6.434 cm
    - X diseño = 1.072 cm
    - Ω₀ = 2.0
    - xy = 2.144 cm
    - Cd = 4.50
    - X inelástica = 4.824 cm
    - Deriva = 1.608%
    - Cumple NEC-15 ✅
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Polygon

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'inicio_fin': '#2c3e50',
    'proceso': '#3498db',
    'calculo': '#27ae60',
    'decision': '#f39c12',
    'resultado': '#e74c3c',
    'exito': '#27ae60',
    'alerta': '#e74c3c',
    'flecha': '#34495e',
    'texto_claro': '#ffffff',
    'texto_oscuro': '#1a1a1a',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

T1 = 0.389
omega1 = 16.147
Sa_T1 = 1.7100
R = 6.0
Omega_0 = 2.0

Sd = (Sa_T1 / omega1**2) * 981
X_diseno = Sd / R
xy = X_diseno * Omega_0
Cd = 0.75 * R
X_inelastica = X_diseno * Cd
He = 3.00
Deriva = X_inelastica / He / 100
Deriva_pct = Deriva * 100

# ============================================================================
# 2. FIGURA HORIZONTAL
# ============================================================================

fig = plt.figure(figsize=(28, 12))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.23 — ORGANIGRAMA HORIZONTAL DEL PUSHOVER',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Comportamiento real: elástico → fluencia → colapso',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

fig.text(0.5, 0.920,
         f'Sd = {Sd:.3f} cm | X diseño = {X_diseno:.3f} cm | xy = {xy:.3f} cm | X inelástica = {X_inelastica:.3f} cm | Deriva = {Deriva_pct:.3f}% ✅',
         ha='center', va='top', fontsize=11,
         color=COLORES['texto_oscuro'], fontweight='bold')

# Eje principal horizontal
ax = fig.add_axes([0.02, 0.05, 0.96, 0.84])
ax.set_xlim(0, 28)
ax.set_ylim(0, 11)
ax.axis('off')


# ============================================================================
# 3. FUNCIONES DE DIBUJO
# ============================================================================

def caja(ax, x, y, w, h, texto, color, tipo='proceso',
         fontsize=9, textcolor='white'):
    if tipo == 'inicio_fin':
        e = Ellipse((x, y), w, h, facecolor=color,
                    edgecolor='black', linewidth=2.5, zorder=2)
        ax.add_patch(e)
    elif tipo == 'decision':
        pts = [(x, y + h/2), (x + w/2, y), (x, y - h/2), (x - w/2, y)]
        p = Polygon(pts, facecolor=color, edgecolor='black',
                    linewidth=2.5, zorder=2)
        ax.add_patch(p)
    else:
        b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                            boxstyle="round,pad=0.12",
                            facecolor=color, edgecolor='black',
                            linewidth=2.5, zorder=2)
        ax.add_patch(b)

    ax.text(x, y, texto, ha='center', va='center',
            fontsize=fontsize, fontweight='bold',
            color=textcolor, zorder=3, family='monospace')


def flecha(ax, x1, y1, x2, y2, color=None, lw=2.5):
    if color is None:
        color = COLORES['flecha']
    f = FancyArrowPatch((x1, y1), (x2, y2),
                         arrowstyle='->', mutation_scale=22,
                         color=color, linewidth=lw, zorder=1)
    ax.add_patch(f)


# ============================================================================
# 4. ORGANIGRAMA HORIZONTAL — 3 FILAS (5 FASES)
# ============================================================================

# ============================================================================
# FILA 1 (Y = 9.0): ENTRADA + DESPLAZAMIENTOS BÁSICOS
# ============================================================================

Y1 = 9.0
H = 1.4
W = 2.4

# FASE 1: INICIO
caja(ax, 1.2, Y1, 1.8, 1.0, "INICIO\nProyecto\nUNESUM",
     COLORES['inicio_fin'], 'inicio_fin', fontsize=9)

# FASE 2: DATOS
caja(ax, 4.2, Y1, W, H,
     f"DATOS\nT₁={T1}s\nSa={Sa_T1}g",
     COLORES['proceso'], fontsize=9)

# FASE 3: MODELO
caja(ax, 7.4, Y1, W, H,
     f"MODELO\nk=28,203\nm=41.314",
     COLORES['proceso'], fontsize=9)

# FASE 4: MODAL
caja(ax, 10.6, Y1, W, H,
     f"MODAL\nω₁={omega1}\nrad/s",
     COLORES['proceso'], fontsize=9)

# FASE 5: ESPECTRO
caja(ax, 13.8, Y1, W, H,
     f"ESPECTRO\nSa={Sa_T1}g\nsuelo E",
     COLORES['proceso'], fontsize=9)

# FASE 6: Sd
caja(ax, 17.0, Y1, W, H,
     f"Sd\n={Sd:.3f}cm\nSa·g/ω²",
     COLORES['calculo'], fontsize=9)

# FASE 7: X diseño
caja(ax, 20.2, Y1, W, H,
     f"X diseño\n={X_diseno:.3f}cm\nSd/R",
     COLORES['calculo'], fontsize=9)

# FASE 8: xy (fluencia)
caja(ax, 23.4, Y1, W + 0.2, H,
     f"xy (fluencia)\n={xy:.3f}cm\nX diseño × Ω₀",
     COLORES['resultado'], fontsize=9)

# FASE 9: Cd
caja(ax, 26.6, Y1, W, H,
     f"Cd\n={Cd}\n0.75 × R",
     COLORES['calculo'], fontsize=9)

# Flechas horizontales fila 1
for x1, x2 in [(2.1, 3.0), (5.4, 6.2), (8.6, 9.4),
               (11.8, 12.6), (15.0, 15.8), (18.2, 19.0),
               (21.4, 22.2), (24.6, 25.4)]:
    flecha(ax, x1, Y1, x2, Y1)


# ============================================================================
# FLECHA DE BAJADA DE FILA 1 A FILA 2
# ============================================================================

flecha(ax, 26.6, Y1 - H/2, 26.6, 7.0)
flecha(ax, 26.6, 6.6, 1.2, 6.6)


# ============================================================================
# FILA 2 (Y = 5.5): X INELÁSTICA + CURVA PUSHOVER
# ============================================================================

Y2 = 5.5
H = 1.4
W = 3.2

# FASE 10: X inelástica (REAL)
caja(ax, 2.0, Y2, W + 0.5, H + 0.2,
     f"X inelástica (REAL)\nX diseño × Cd = {X_inelastica:.3f} cm",
     COLORES['resultado'], fontsize=10)

# FASE 11: CURVA PUSHOVER
caja(ax, 7.0, Y2, W + 0.5, H + 0.2,
     f"CURVA PUSHOVER\nV vs Δ",
     COLORES['resultado'], fontsize=10)

# FASE 12: DERIVA
caja(ax, 12.0, Y2, W + 0.5, H + 0.2,
     f"DERIVA\nX inelástica/He/100\n= {Deriva_pct:.3f}%",
     COLORES['calculo'], fontsize=10)

# FASE 13: DECISIÓN DERIVA
caja(ax, 17.0, Y2, 3.0, 1.6,
     f"¿Deriva\n≤ 2%?",
     COLORES['decision'], 'decision', fontsize=11)

# Rama SÍ
caja(ax, 21.5, Y2 + 0.9, W, H - 0.3,
     f"SÍ → CUMPLE\nNEC-15 ✅",
     COLORES['exito'], fontsize=9)

# Rama NO
caja(ax, 21.5, Y2 - 0.9, W, H - 0.3,
     f"NO → DISIPADOR\nRequerido ❌",
     COLORES['alerta'], fontsize=9)

# Flechas fila 2
flecha(ax, 3.9, Y2, 5.2, Y2)
flecha(ax, 8.9, Y2, 10.2, Y2)
flecha(ax, 13.9, Y2, 15.3, Y2)

# De decisión a ramas
flecha(ax, 18.5, Y2 + 0.5, 19.7, Y2 + 0.9, color=COLORES['exito'])
ax.text(19.1, Y2 + 1.0, 'SÍ', fontsize=10, fontweight='bold',
        color=COLORES['exito'])

flecha(ax, 18.5, Y2 - 0.5, 19.7, Y2 - 0.9, color=COLORES['alerta'])
ax.text(19.1, Y2 - 1.0, 'NO', fontsize=10, fontweight='bold',
        color=COLORES['alerta'])


# ============================================================================
# FLECHA DE SUBIDA DE FILA 2 A FILA 3
# ============================================================================

flecha(ax, 21.5, Y2 + 0.9 - (H - 0.3)/2, 21.5, 3.0)


# ============================================================================
# FILA 3 (Y = 2.0): CIERRE
# ============================================================================

Y3 = 2.0
H = 1.4
W = 3.0

# FASE 14: RESUMEN
caja(ax, 2.0, Y3, W + 0.5, H,
     f"RESUMEN\nSd={Sd:.2f}\nX inel={X_inelastica:.2f}",
     COLORES['proceso'], fontsize=9)

# FASE 15: VERIFICACIÓN
caja(ax, 7.0, Y3, W + 0.5, H,
     f"VERIFICACIÓN\nDeriva={Deriva_pct:.3f}%\n≤ 2% ✅",
     COLORES['calculo'], fontsize=9)

# FASE 16: FIN
caja(ax, 13.0, Y3, 3.5, 1.4,
     "FIN\nProyecto\nVERIFICADO",
     COLORES['inicio_fin'], 'inicio_fin', fontsize=10)

# Flechas fila 3
flecha(ax, 3.9, Y3, 5.2, Y3)
flecha(ax, 8.9, Y3, 11.0, Y3)


# ============================================================================
# ETIQUETAS DE FASES (LATERALES)
# ============================================================================

ax.text(0.3, 10.2, 'FASE 1-5: ENTRADA Y DESPLAZAMIENTOS BÁSICOS',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')

ax.text(0.3, 7.2, 'FASE 6-13: X INELÁSTICA Y VERIFICACIÓN',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')

ax.text(0.3, 3.6, 'FASE 14-16: CIERRE',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')


# ============================================================================
# 5. CUADRO DE DATOS EN ESQUINA
# ============================================================================

datos_txt = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  Sd           = {Sd:.3f} cm\n"
    f"  X diseño     = {X_diseno:.3f} cm\n"
    f"  Ω₀           = {Omega_0}\n"
    f"  xy           = {xy:.3f} cm\n"
    f"  Cd           = {Cd}\n"
    f"  X inelástica = {X_inelastica:.3f} cm\n"
    f"  Deriva       = {Deriva_pct:.3f} %\n"
    "═══════════════════════════════\n"
    "  ✅ CUMPLE NEC-15"
)

fig.text(0.985, 0.10, datos_txt,
         transform=fig.transFigure,
         fontsize=8, family='monospace',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor=COLORES['titulo'],
                   linewidth=2))


# ============================================================================
# 6. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_23"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_23_organigrama_horizontal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.23 COMPLETADO — ORGANIGRAMA HORIZONTAL DEL PUSHOVER")
print("=" * 80)
print(f"  Sd           = {Sd:.4f} cm")
print(f"  X diseño     = {X_diseno:.4f} cm")
print(f"  xy           = {xy:.4f} cm")
print(f"  Cd           = {Cd}")
print(f"  X inelástica = {X_inelastica:.4f} cm")
print(f"  Deriva       = {Deriva_pct:.3f} % ✅")
print("=" * 80)