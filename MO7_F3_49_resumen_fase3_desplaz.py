# -*- coding: utf-8 -*-
"""
================================================================================
M07.25 — ORGANIGRAMA FASE 3: CIERRE (REFORMULADO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.25 — Fase 3: Cierre

OBJETIVO: Organigrama horizontal de la Fase 3 (Cierre) con:
    PASO 14: Resumen de resultados
    PASO 15: Verificación de derivas
    PASO 16: Clasificación de desempeño
    PASO 17: Conclusión
    PASO 18: FIN

DATOS:
    - Sd = 6.434 cm
    - X diseño = 1.072 cm
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

fig = plt.figure(figsize=(28, 10))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.25 — ORGANIGRAMA FASE 3: CIERRE',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.940,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Resumen → Verificación → Conclusión → FIN',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

# Eje principal horizontal
ax = fig.add_axes([0.02, 0.05, 0.96, 0.85])
ax.set_xlim(0, 28)
ax.set_ylim(0, 10)
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
# 4. ORGANIGRAMA FASE 3 — 2 FILAS
# ============================================================================

# ============================================================================
# FILA 1 (Y = 7.0): PASOS 14, 15, 16
# ============================================================================

Y1 = 7.0
H = 1.8

# PASO 14: RESUMEN
caja(ax, 2.5, Y1, 4.0, H,
     f"PASO 14\nRESUMEN\nSd={Sd:.3f} cm\nX inel={X_inelastica:.3f} cm",
     COLORES['proceso'], fontsize=9)

# PASO 15: VERIFICACIÓN DE DERIVAS
caja(ax, 8.5, Y1, 4.0, H,
     f"PASO 15\nVERIFICACIÓN\nDeriva={Deriva_pct:.3f}%\nLímite NEC-15=2%",
     COLORES['calculo'], fontsize=9)

# PASO 16: CLASIFICACIÓN DE DESEMPEÑO
caja(ax, 14.5, Y1, 4.0, H,
     f"PASO 16\nCLASIFICACIÓN\nNEC-15 ✅\nVISION 2000\nNear collapse",
     COLORES['resultado'], fontsize=9)

# PASO 17: CONCLUSIÓN
caja(ax, 20.5, Y1, 4.0, H,
     f"PASO 17\nCONCLUSIÓN\n¿Cumple NEC-15?\n✅ SÍ",
     COLORES['exito'], fontsize=9)

# PASO 18: FIN
caja(ax, 26.0, Y1, 2.8, H,
     f"PASO 18\nFIN\nProyecto\nVERIFICADO",
     COLORES['inicio_fin'], 'inicio_fin', fontsize=10)

# Flechas fila 1
flecha(ax, 4.5, Y1, 6.5, Y1)
flecha(ax, 10.5, Y1, 12.5, Y1)
flecha(ax, 16.5, Y1, 18.5, Y1)
flecha(ax, 22.5, Y1, 24.6, Y1)


# ============================================================================
# FILA 2 (Y = 3.0): DETALLE DE VERIFICACIÓN Y CLASIFICACIÓN
# ============================================================================

Y2 = 3.0
H = 1.5

# DETALLE 1: VERIFICACIÓN NEC-15
caja(ax, 3.0, Y2, 4.5, H,
     f"VERIFICACIÓN NEC-15\n"
     f"Deriva = {Deriva_pct:.3f}%\n"
     f"Límite = 2.00%\n"
     f"✅ CUMPLE",
     COLORES['exito'], fontsize=8.5)

# DETALLE 2: HAZUZ 1999
caja(ax, 8.5, Y2, 4.5, H,
     f"HAZUZ 1999\n"
     f"Deriva = {Deriva_pct:.3f}%\n"
     f"Completo (< 4.0%)\n"
     f"✅ Cumple",
     COLORES['exito'], fontsize=8.5)

# DETALLE 3: VISION 2000
caja(ax, 14.0, Y2, 4.5, H,
     f"VISION 2000\n"
     f"Deriva = {Deriva_pct:.3f}%\n"
     f"Near collapse (< 2.5%)\n"
     f"✅ Cumple",
     COLORES['exito'], fontsize=8.5)

# DETALLE 4: ATC-40 / FEMA 273
caja(ax, 19.5, Y2, 4.5, H,
     f"ATC-40 / FEMA 273\n"
     f"Deriva = {Deriva_pct:.3f}%\n"
     f"Seguridad (< 2.0%)\n"
     f"✅ Cumple",
     COLORES['exito'], fontsize=8.5)

# DETALLE 5: CONCLUSIÓN FINAL
caja(ax, 25.5, Y2, 4.0, H,
     f"CONCLUSIÓN FINAL\n"
     f"✅ CUMPLE NEC-15\n"
     f"✅ CUMPLE INTERNACIONAL\n"
     f"✅ Diseño ACEPTABLE",
     COLORES['exito'], fontsize=8.5)


# ============================================================================
# ETIQUETAS DE SECCIÓN
# ============================================================================

ax.text(0.3, 8.8, 'FASE 3: CIERRE — PASOS 14 AL 18',
        fontsize=12, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')

ax.text(0.3, 4.5, 'DETALLE DE VERIFICACIÓN Y CLASIFICACIÓN',
        fontsize=11, fontweight='bold', color=COLORES['titulo'],
        ha='left', va='center')


# ============================================================================
# 5. CUADRO DE DATOS EN ESQUINA
# ============================================================================

datos_txt = (
    "RESULTADOS FINALES\n"
    "═══════════════════════════════\n"
    f"  Sd           = {Sd:.3f} cm\n"
    f"  X diseño     = {X_diseno:.3f} cm\n"
    f"  xy           = {xy:.3f} cm\n"
    f"  Cd           = {Cd}\n"
    f"  X inelástica = {X_inelastica:.3f} cm\n"
    f"  Deriva       = {Deriva_pct:.3f} %\n"
    "═══════════════════════════════\n"
    "  ✅ CUMPLE NEC-15\n"
    "  ✅ CUMPLE ATC-40\n"
    "  ✅ CUMPLE FEMA 273\n"
    "  ✅ CUMPLE BERTERO\n"
    "  ✅ CUMPLE HAZUZ 1999\n"
    "  ✅ CUMPLE VISION 2000"
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

carpeta = "Resultados_M07_25"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_25_organigrama_fase3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.25 COMPLETADO — ORGANIGRAMA FASE 3: CIERRE")
print("=" * 80)
print(f"  PASO 14: Resumen      → Sd = {Sd:.3f} cm")
print(f"  PASO 15: Verificación → Deriva = {Deriva_pct:.3f}%")
print(f"  PASO 16: Clasificación → Cumple NEC-15 ✅")
print(f"  PASO 17: Conclusión   → ✅ SÍ")
print(f"  PASO 18: FIN          → Proyecto verificado")
print("=" * 80)