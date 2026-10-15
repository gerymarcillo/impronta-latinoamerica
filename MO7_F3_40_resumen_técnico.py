# -*- coding: utf-8 -*-
"""
================================================================================
M07.31 — RESUMEN CONCEPTUAL: NIVELES DE DESEMPEÑO SÍSMICO (DIAPOSITIVAS 69-74)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.31 — Resumen Conceptual

OBJETIVO: Dashboard conceptual que integra las diapositivas 69-74:
    69: Damage States (FEMA)
    70: Límites de distorsión (ATC-40, FEMA 273, BERTERO, VISION 2000)
    71: Vision 2000 (estados de daño)
    72: Performance Levels (Vision 2000)
    73: Parámetro λ (ATC-40 / FEMA 356)
    74: HAZUZ 1999

CONCEPTO UNIFICADOR:
    La deriva de entrepiso es el parámetro universal para medir
    el desempeño sísmico de una estructura.

DATOS DEL PROYECTO:
    - Deriva = 1.608%
    - Clasificación: Near collapse / Extenso
    - Cumple NEC-15 ✅
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'concepto': '#8e44ad',
    'damage': '#3498db',
    'limites': '#e67e22',
    'vision': '#16a085',
    'performance': '#27ae60',
    'lambda': '#c0392b',
    'hazuz': '#f39c12',
    'proyecto': '#e74c3c',
    'resultado': '#27ae60',
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

Deriva = 1.608  # %
Limite_NEC = 2.0

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(28, 18))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.985,
         'M07.31 — RESUMEN CONCEPTUAL: NIVELES DE DESEMPEÑO SÍSMICO',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.962,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Diapositivas 69-74',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(3, 3, figure=fig,
              hspace=0.35, wspace=0.25,
              left=0.04, right=0.97,
              top=0.92, bottom=0.04,
              height_ratios=[0.6, 1.0, 1.0])

# ============================================================================
# PANEL SUPERIOR: CONCEPTO UNIFICADOR
# ============================================================================

ax0 = fig.add_subplot(gs[0, :])
ax0.axis('off')
ax0.set_facecolor('#ffffff')

txt_concepto = (
    "═══════════════════════════════════════════════════════════════════════\n"
    "  CONCEPTO UNIFICADOR\n"
    "═══════════════════════════════════════════════════════════════════════\n\n"
    "  ¿CUÁNTO SE PUEDE DEFORMAR UNA ESTRUCTURA SIN QUE PIERDA SU FUNCIÓN?\n\n"
    "  La DERIVA DE ENTREPISO es el parámetro universal para medir\n"
    "  el desempeño sísmico de una estructura.\n\n"
    "  Todas las normas (HAZUZ, Vision 2000, FEMA, ATC-40, BERTERO)\n"
    "  convergen en rangos similares de deriva admisible (0.2% a 2.5%).\n"
    "═══════════════════════════════════════════════════════════════════════"
)

ax0.text(0.5, 0.5, txt_concepto, transform=ax0.transAxes,
         ha='center', va='center', fontsize=11, family='monospace',
         fontweight='bold', color=COLORES['concepto'],
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#f4ecf7',
                   edgecolor=COLORES['concepto'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# FILA 1: DAMAGE STATES (69) + LÍMITES DE DISTORSIÓN (70)
# ============================================================================

# --- PANEL (a): DAMAGE STATES (Diapositiva 69) ---
ax1 = fig.add_subplot(gs[1, 0])
ax1.axis('off')
ax1.set_title('(a) DAMAGE STATES (Diapositiva 69)',
              fontsize=12, fontweight='bold', color=COLORES['damage'])

txt1 = (
    "FEMA — LIGHT-FRAME WOOD\n"
    "═══════════════════════════════\n\n"
    "  Slight:\n"
    "    Grietas pequeñas\n"
    "    Deriva: < 0.5%\n\n"
    "  Moderate:\n"
    "    Grietas grandes\n"
    "    Deriva: 0.5% - 1.0%\n\n"
    "  Extensive:\n"
    "    Grietas diagonales\n"
    "    Deriva: 1.0% - 2.0%\n\n"
    "  Complete:\n"
    "    Colapso inminente\n"
    "    Deriva: > 2.0%\n\n"
    "═══════════════════════════════\n"
    "  NORMA: FEMA 273/356\n"
    "  AUTOR: FEMA"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#ebf5fb',
                   edgecolor=COLORES['damage'],
                   linewidth=2.5, alpha=0.98))

# --- PANEL (b): LÍMITES DE DISTORSIÓN (Diapositiva 70) ---
ax2 = fig.add_subplot(gs[1, 1])
ax2.axis('off')
ax2.set_title('(b) LÍMITES DE DISTORSIÓN (Diapositiva 70)',
              fontsize=12, fontweight='bold', color=COLORES['limites'])

txt2 = (
    "TABLA COMPARATIVA\n"
    "═══════════════════════════════\n\n"
    "  Nivel      ATC-40  FEMA  VISION\n"
    "  ─────────────────────────────────\n"
    "  Ocupación  0.01    0.01  0.002\n"
    "  Seguridad  0.01-   0.01- 0.015\n"
    "             0.02    0.02\n"
    "  Prevención 0.33Vi  0.04  0.025\n\n"
    "═══════════════════════════════\n"
    "  NORMAS:\n"
    "  • ATC-40 (1996)\n"
    "  • FEMA 273 (1997)\n"
    "  • BERTERO (1994)\n"
    "  • VISION 2000 (1995)"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#fef5e7',
                   edgecolor=COLORES['limites'],
                   linewidth=2.5, alpha=0.98))

# --- PANEL (c): VISION 2000 (Diapositivas 71-72) ---
ax3 = fig.add_subplot(gs[1, 2])
ax3.axis('off')
ax3.set_title('(c) VISION 2000 (Diapositivas 71-72)',
              fontsize=12, fontweight='bold', color=COLORES['vision'])

txt3 = (
    "NIVELES DE DESEMPEÑO\n"
    "═══════════════════════════════\n\n"
    "  Fully operational\n"
    "    < 0.2%\n"
    "    Servicio continuo\n\n"
    "  Operational\n"
    "    < 0.5%\n"
    "    Seguro para ocupación\n\n"
    "  Life safety\n"
    "    < 1.5%\n"
    "    Protección de vidas\n\n"
    "  Near collapse\n"
    "    < 2.5%\n"
    "    Colapso prevenido\n\n"
    "  Collapse\n"
    "    > 2.5%\n\n"
    "═══════════════════════════════\n"
    "  NORMA: Vision 2000\n"
    "  AUTOR: SEAOC"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=8, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['vision'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# FILA 2: PARÁMETRO λ (73) + HAZUZ (74) + PROYECTO
# ============================================================================

# --- PANEL (d): PARÁMETRO λ (Diapositiva 73) ---
ax4 = fig.add_subplot(gs[2, 0])
ax4.axis('off')
ax4.set_title('(d) PARÁMETRO λ (Diapositiva 73)',
              fontsize=12, fontweight='bold', color=COLORES['lambda'])

txt4 = (
    "TABLA C9-4 (ATC-40)\n"
    "═══════════════════════════════\n\n"
    "  Exponente α    Parámetro λ\n"
    "  ─────────────────────────────\n"
    "  0.25           3.7\n"
    "  0.50           3.5\n"
    "  0.75           3.3\n"
    "  1.00           3.1  ← PROYECTO\n"
    "  1.25           3.0\n"
    "  1.50           2.9\n"
    "  1.75           2.8\n"
    "  2.00           2.7\n\n"
    "═══════════════════════════════\n"
    "  NORMA: ATC-40 / FEMA 356\n"
    "  AUTOR: Freeman (1978)"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['lambda'],
                   linewidth=2.5, alpha=0.98))

# --- PANEL (e): HAZUZ 1999 (Diapositiva 74) ---
ax5 = fig.add_subplot(gs[2, 1])
ax5.axis('off')
ax5.set_title('(e) HAZUZ 1999 (Diapositiva 74)',
              fontsize=12, fontweight='bold', color=COLORES['hazuz'])

txt5 = (
    "ESTADOS DE DAÑO\n"
    "═══════════════════════════════\n\n"
    "  Estado     Distorsión   Calif.\n"
    "  ─────────────────────────────────\n"
    "  Leve       0.0033       Platino\n"
    "  Moderado   0.0058       Gold\n"
    "  Extenso    0.0156       Silver\n"
    "  Completo   0.0400       —\n\n"
    "═══════════════════════════════\n\n"
    "  CALIFICACIONES:\n"
    "  • Platino → Leve\n"
    "  • Gold → Moderado\n"
    "  • Silver → Extenso\n\n"
    "═══════════════════════════════\n"
    "  AUTOR: Hazuz (1999)"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#fef9e7',
                   edgecolor=COLORES['hazuz'],
                   linewidth=2.5, alpha=0.98))

# --- PANEL (f): APLICACIÓN AL PROYECTO ---
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')
ax6.set_title('(f) APLICACIÓN AL PROYECTO',
              fontsize=12, fontweight='bold', color=COLORES['proyecto'])

txt6 = (
    "TU PROYECTO\n"
    "═══════════════════════════════\n\n"
    f"  Deriva = {Deriva:.3f}%\n\n"
    "  CLASIFICACIÓN:\n"
    "  • HAZUZ 1999: Extenso\n"
    "  • Vision 2000: Near collapse\n"
    "  • FEMA 273: Extensive\n"
    "  • ATC-40: Seguridad de Vida\n"
    "  • BERTERO: Seguridad de Vida\n\n"
    "  LÍMITE NEC-15:\n"
    "  • Deriva ≤ 2.00%\n\n"
    f"  RESULTADO:\n"
    f"  • {Deriva:.3f}% < 2.00%\n"
    "  • ✅ CUMPLE NEC-15\n\n"
    "═══════════════════════════════\n"
    "  CLASIFICACIÓN: Aceptable"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['resultado'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_31"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_31_resumen_conceptual_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.31 — RESUMEN CONCEPTUAL (DIAPOSITIVAS 69-74)")
print("=" * 80)
print(f"\n  CONCEPTO UNIFICADOR:")
print(f"    La deriva de entrepiso es el parámetro universal")
print(f"\n  DIAPOSITIVAS ASOCIADAS:")
print(f"    69: Damage States (FEMA)")
print(f"    70: Límites de distorsión (4 normas)")
print(f"    71: Vision 2000 (estados)")
print(f"    72: Performance Levels")
print(f"    73: Parámetro λ")
print(f"    74: HAZUZ 1999")
print(f"\n  APLICACIÓN AL PROYECTO:")
print(f"    Deriva = {Deriva:.3f}%")
print(f"    Clasificación: Near collapse / Extenso")
print(f"    ✅ CUMPLE NEC-15")
print("=" * 80)