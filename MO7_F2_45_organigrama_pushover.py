# -*- coding: utf-8 -*-
"""
================================================================================
M07.12 — ORGANIGRAMA HORIZONTAL DEL PUSHOVER
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.12 — Organigrama del Pushover (horizontal)

OBJETIVO: Diagrama de flujo horizontal del procedimiento de Pushover,
          con los valores reales del proyecto principal.

DATOS DEL PROYECTO:
    - T₁ = 0.389 s
    - Sa(T₁) = 1.7100 g (suelo E crítico)
    - Sd = 6.434 cm
    - V_R = 231.02 t
    - X diseño = 1.072 cm
    - ΔM = 28.95 cm
    - Deriva = 9.65% ❌
================================================================================
"""

import os
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse, Polygon

# ============================================================================
# PALETA DEL PROYECTO
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'inicio_fin': '#2c3e50',
    'proceso': '#3498db',
    'decision': '#f39c12',
    'calculo': '#27ae60',
    'resultado': '#e74c3c',
    'documento': '#8e44ad',
    'flecha': '#34495e',
    'texto_claro': '#ffffff',
    'texto_oscuro': '#1a1a1a',
    'exito': '#27ae60',
    'alerta': '#e74c3c',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

T1 = 0.389
omega1 = 16.147
Sa_T1 = 1.7100
Sd = 6.434
V_R = 231.02
V_e = 1386.13
K_rigidez = 215.44
X_diseno = 1.072
Cd_dist = 5.362
Cd_factor = 6.0
Delta_M = 28.95
Deriva = 9.65

# ============================================================================
# 2. FIGURA HORIZONTAL
# ============================================================================

fig = plt.figure(figsize=(26, 11))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.12 — ORGANIGRAMA DEL PUSHOVER',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Análisis Estático No Lineal',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

fig.text(0.5, 0.920,
         f'T₁ = {T1} s  |  Sa(T₁) = {Sa_T1} g  |  Sd = {Sd} cm  |  V_R = {V_R} t  |  ΔM = {Delta_M} cm',
         ha='center', va='top', fontsize=11,
         color=COLORES['texto_oscuro'], fontweight='bold')

# Eje principal horizontal
ax = fig.add_axes([0.02, 0.05, 0.96, 0.84])
ax.set_xlim(0, 26)
ax.set_ylim(0, 11)
ax.axis('off')


# ============================================================================
# 3. FUNCIONES DE DIBUJO
# ============================================================================

def caja(ax, x, y, w, h, texto, color, tipo='proceso',
         fontsize=9, textcolor='white'):
    """Dibuja una caja con texto."""
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
# 4. ORGANIGRAMA HORIZONTAL — 3 FILAS
# ============================================================================

# -------- FILA 1 (Y = 9.0) — ENTRADA Y CÁLCULO BÁSICO --------
Y1 = 9.0
H = 1.3
W = 2.6

# PASO 0: INICIO
caja(ax, 1.3, Y1, 2.0, 1.0, "INICIO\nProyecto\nUNESUM",
     COLORES['inicio_fin'], 'inicio_fin', fontsize=9)

# PASO 1: DATOS
caja(ax, 4.5, Y1, W, H,
     f"1. DATOS\nT₁={T1}s\nSa={Sa_T1}g",
     COLORES['proceso'], fontsize=9)

# PASO 2: MODELO
caja(ax, 8.0, Y1, W, H,
     f"2. MODELO\nk=28,203 t/m\nm=41.314",
     COLORES['proceso'], fontsize=9)

# PASO 3: MODAL
caja(ax, 11.5, Y1, W, H,
     f"3. MODAL\nω₁={omega1}\nrad/s",
     COLORES['proceso'], fontsize=9)

# PASO 4: ESPECTRO
caja(ax, 15.0, Y1, W, H,
     f"4. ESPECTRO\nSa={Sa_T1}g\nsuelo E",
     COLORES['proceso'], fontsize=9)

# PASO 5: Sd
caja(ax, 18.5, Y1, W, H,
     f"5. Sd\n={Sd}cm\nSa·g/ω²",
     COLORES['calculo'], fontsize=9)

# PASO 6: V_R
caja(ax, 22.0, Y1, W, H,
     f"6. V_R\n={V_R}t\nI·Sa·W/(R·φ)",
     COLORES['calculo'], fontsize=9)

# Flechas horizontales fila 1
for x1, x2 in [(2.3, 3.2), (5.8, 6.7), (9.3, 10.2),
               (12.8, 13.7), (16.3, 17.2), (19.8, 20.7)]:
    flecha(ax, x1, Y1, x2, Y1)


# -------- FLECHA DE BAJADA DE FILA 1 A FILA 2 --------
flecha(ax, 22.0, Y1 - H/2, 22.0, 6.5)
ax.text(22.4, 7.8, '↓', fontsize=14, fontweight='bold',
        color=COLORES['flecha'])


# -------- FILA 2 (Y = 6.0) — DISEÑO Y FLUENCIA --------
Y2 = 6.0

# PASO 7: X DISEÑO
caja(ax, 1.3, Y2, W, H,
     f"7. X diseño\n={X_diseno}cm\nSd/R",
     COLORES['calculo'], fontsize=9)

# PASO 8: FLUENCIA
caja(ax, 4.8, Y2, W + 0.4, H,
     f"8. FLUENCIA\nV_y={V_R}t\nΔ_y={X_diseno}cm",
     COLORES['resultado'], fontsize=9)

# PASO 9: PUSHOVER
caja(ax, 8.7, Y2, W + 0.4, H,
     f"9. PUSHOVER\nV_e={V_e}t\n↓ V_y",
     COLORES['resultado'], fontsize=9)

# PASO 10: DECISIÓN
caja(ax, 12.5, Y2, 2.8, 1.5,
     f"¿Δ ≥ Δ_y?",
     COLORES['decision'], 'decision', fontsize=11)

# Rama SÍ → INELÁSTICO
caja(ax, 16.5, Y2 + 0.9, W, H - 0.3,
     f"SÍ → INELÁSTICO\nHierro fluye",
     COLORES['resultado'], fontsize=8.5)

# Rama NO → ELÁSTICO
caja(ax, 16.5, Y2 - 0.9, W, H - 0.3,
     f"NO → ELÁSTICO\nSin daño",
     COLORES['proceso'], fontsize=8.5)

# PASO 11: Cd
caja(ax, 20.3, Y2 + 0.9, W, H - 0.3,
     f"11. Cd\n={Cd_dist}cm\no Cd={Cd_factor}",
     COLORES['calculo'], fontsize=8.5)

# Rama NO → continúa al fin
caja(ax, 20.3, Y2 - 0.9, W, H - 0.3,
     f"Fin parcial\nDiseño OK",
     COLORES['exito'], fontsize=8.5)

# Flechas fila 2
flecha(ax, 2.7, Y2, 3.4, Y2)
flecha(ax, 6.3, Y2, 7.2, Y2)
flecha(ax, 10.2, Y2, 11.1, Y2)

# De decisión a ramas
flecha(ax, 13.9, Y2 + 0.4, 15.2, Y2 + 0.9, color=COLORES['alerta'])
ax.text(14.6, Y2 + 0.95, 'SÍ', fontsize=9, fontweight='bold',
        color=COLORES['alerta'])

flecha(ax, 13.9, Y2 - 0.4, 15.2, Y2 - 0.9, color=COLORES['exito'])
ax.text(14.6, Y2 - 0.95, 'NO', fontsize=9, fontweight='bold',
        color=COLORES['exito'])

flecha(ax, 17.9, Y2 + 0.9, 18.9, Y2 + 0.9)


# -------- FLECHA DE SUBIDA DE FILA 2 A FILA 3 --------
flecha(ax, 20.3, Y2 + 0.9 - (H - 0.3)/2, 20.3, 3.5)


# -------- FILA 3 (Y = 3.0) — VERIFICACIÓN Y CIERRE --------
Y3 = 3.0

# PASO 12: ΔM
caja(ax, 1.3, Y3, W, H,
     f"12. ΔM\n={Delta_M}cm\n0.75·R·Sd",
     COLORES['calculo'], fontsize=9)

# PASO 13: DERIVA
caja(ax, 4.8, Y3, W + 0.4, H,
     f"13. DERIVA\n={Deriva}%\nvs 2%",
     COLORES['resultado'], fontsize=9)

# PASO 14: DECISIÓN FINAL
caja(ax, 8.7, Y3, 3.0, 1.5,
     f"¿Deriva\n≤ 2%?",
     COLORES['decision'], 'decision', fontsize=11)

# Rama NO → DISIPADOR
caja(ax, 13.5, Y3 + 0.9, W + 0.4, H - 0.3,
     f"NO → DISIPADOR\nRequerido",
     COLORES['alerta'], fontsize=8.5)

# Rama SÍ → CUMPLE
caja(ax, 13.5, Y3 - 0.9, W + 0.4, H - 0.3,
     f"SÍ → CUMPLE\nDiseño OK",
     COLORES['exito'], fontsize=8.5)

# Optimización con disipador
caja(ax, 18.0, Y3 + 0.9, W, H - 0.3,
     f"Optimizar\nDisipador",
     COLORES['calculo'], fontsize=8.5)

# PASO 15: FIN
caja(ax, 22.0, Y3, 3.0, 1.3,
     "FIN\nProyecto\nOptimizado",
     COLORES['inicio_fin'], 'inicio_fin', fontsize=9)

# Flechas fila 3
flecha(ax, 2.7, Y3, 3.4, Y3)
flecha(ax, 6.3, Y3, 7.2, Y3)

# De decisión a ramas
flecha(ax, 10.2, Y3 + 0.4, 12.0, Y3 + 0.9, color=COLORES['exito'])
ax.text(11.1, Y3 + 1.0, 'SÍ', fontsize=9, fontweight='bold',
        color=COLORES['exito'])

flecha(ax, 10.2, Y3 - 0.4, 12.0, Y3 - 0.9, color=COLORES['alerta'])
ax.text(11.1, Y3 - 1.0, 'NO', fontsize=9, fontweight='bold',
        color=COLORES['alerta'])

# De disipador a optimización
flecha(ax, 15.7, Y3 + 0.9, 16.7, Y3 + 0.9)

# De optimización a FIN
flecha(ax, 19.3, Y3 + 0.9, 20.5, Y3 + 0.3)

# De CUMPLE a FIN
flecha(ax, 15.7, Y3 - 0.9, 21.0, Y3 - 0.3)


# ============================================================================
# 5. ETIQUETAS DE FILAS
# ============================================================================

ax.text(0.3, 9.8, 'FASE 1: ENTRADA Y CÁLCULO BÁSICO',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')

ax.text(0.3, 7.1, 'FASE 2: DISEÑO Y FLUENCIA',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')

ax.text(0.3, 4.1, 'FASE 3: VERIFICACIÓN Y CIERRE',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')


# ============================================================================
# 6. CUADRO DE DATOS EN ESQUINA
# ============================================================================

datos_txt = (
    "DATOS DEL PROYECTO\n"
    "══════════════════════════════\n"
    f"  T₁       = {T1} s\n"
    f"  Sa(T₁)   = {Sa_T1} g\n"
    f"  Sd       = {Sd} cm\n"
    f"  V_R      = {V_R} t\n"
    f"  X diseño = {X_diseno} cm\n"
    f"  ΔM       = {Delta_M} cm\n"
    f"  Deriva   = {Deriva} %\n"
    "══════════════════════════════\n"
    "  RESULTADO:\n"
    "  ❌ REQUIERE DISIPADOR"
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
# 7. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_12"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_12_organigrama_horizontal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.12 COMPLETADO — ORGANIGRAMA HORIZONTAL DEL PUSHOVER")
print("=" * 80)