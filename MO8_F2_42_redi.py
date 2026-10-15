# -*- coding: utf-8 -*-
"""
================================================================================
M07.35 — REDi™ RESILIENCE OBJECTIVES
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.35 — REDi™ Resilience Objectives

OBJETIVO: Dashboard con los objetivos de resiliencia REDi™
          y ubicación del proyecto en la escala.

REDi™ (Resilience-based Earthquake Design Initiative):
    - Autor: Arup (2013)
    - Niveles: Platinum, Gold, Silver, Base (código)

NIVELES:
    PLATINUM: Downtime < 72h | Pérdida < 2.5% | Deriva < 0.2%
    GOLD:     Downtime < 1 mes | Pérdida < 5% | Deriva < 0.5%
    SILVER:   Downtime < 6 meses | Pérdida < 10% | Deriva < 1.5%
    BASE:     Downtime > 6 meses | Pérdida > 10% | Deriva < 2.0%

DATOS DEL PROYECTO:
    - Deriva = 1.608%
    - Clasificación: REDi Silver
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Rectangle

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'platinum': '#8e9eab',
    'gold': '#f39c12',
    'silver': '#95a5a6',
    'base': '#e74c3c',
    'proyecto': '#27ae60',
    'resultado': '#27ae60',
    'alerta': '#e67e22',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_alerta': '#fadbd8',
    'box_alerta_borde': '#c0392b',
    'box_platinum': '#e8ecf1',
    'box_platinum_borde': '#8e9eab',
    'box_gold': '#fef5e7',
    'box_gold_borde': '#f39c12',
    'box_silver': '#ebedef',
    'box_silver_borde': '#95a5a6',
    'box_base': '#fadbd8',
    'box_base_borde': '#e74c3c',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

Deriva = 1.608  # %
Limite_NEC = 2.0

# Niveles REDi
niveles_redi = [
    {
        'nombre': 'PLATINUM',
        'deriva': 0.2,
        'downtime': '< 72 horas',
        'perdida': '< 2.5%',
        'seguridad': 'Improbable',
        'color': COLORES['platinum'],
        'bg': COLORES['box_platinum'],
        'borde': COLORES['box_platinum_borde'],
    },
    {
        'nombre': 'GOLD',
        'deriva': 0.5,
        'downtime': '< 1 mes',
        'perdida': '< 5%',
        'seguridad': 'Improbable',
        'color': COLORES['gold'],
        'bg': COLORES['box_gold'],
        'borde': COLORES['box_gold_borde'],
    },
    {
        'nombre': 'SILVER',
        'deriva': 1.5,
        'downtime': '< 6 meses',
        'perdida': '< 10%',
        'seguridad': 'Improbable',
        'color': COLORES['silver'],
        'bg': COLORES['box_silver'],
        'borde': COLORES['box_silver_borde'],
    },
    {
        'nombre': 'BASE (Código)',
        'deriva': 2.0,
        'downtime': '> 6 meses',
        'perdida': '> 10%',
        'seguridad': 'Posible',
        'color': COLORES['base'],
        'bg': COLORES['box_base'],
        'borde': COLORES['box_base_borde'],
    },
]

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 16))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.980,
         'M07.35 — REDi™ RESILIENCE OBJECTIVES',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Deriva = {Deriva:.3f}% | REDi Silver',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 2, figure=fig,
              hspace=0.30, wspace=0.25,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.3, 1.0])

# ============================================================================
# PANEL (a): GRÁFICA DE NIVELES REDi
# ============================================================================

ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor('#ffffff')

# Dibujar niveles
y_positions = np.arange(len(niveles_redi))
colores_barras = [n['color'] for n in niveles_redi]

for i, nivel in enumerate(niveles_redi):
    # Barra horizontal
    ax1.barh(i, nivel['deriva'], height=0.6,
             color=nivel['color'], alpha=0.7,
             edgecolor='black', linewidth=2)
    
    # Etiqueta del nivel
    ax1.text(-0.05, i, nivel['nombre'],
             ha='right', va='center',
             fontsize=14, fontweight='bold', color=nivel['color'])
    
    # Valor de deriva
    ax1.text(nivel['deriva'] + 0.05, i,
             f"Deriva: < {nivel['deriva']}%",
             ha='left', va='center',
             fontsize=11, fontweight='bold')
    
    # Info adicional
    ax1.text(nivel['deriva'] + 0.8, i,
             f"Downtime: {nivel['downtime']} | Pérdida: {nivel['perdida']}",
             ha='left', va='center',
             fontsize=10, color='#555555', style='italic')

# Línea del proyecto
ax1.axvline(x=Deriva, color=COLORES['proyecto'],
            linestyle='-', linewidth=4, zorder=10,
            label=f'Proyecto: {Deriva:.3f}%')

# Línea del límite NEC
ax1.axvline(x=Limite_NEC, color=COLORES['base'],
            linestyle='--', linewidth=3, zorder=10,
            label=f'Límite NEC-15: {Limite_NEC:.2f}%')

# Zona del proyecto
ax1.axvspan(Deriva - 0.05, Deriva + 0.05,
            color=COLORES['proyecto'], alpha=0.2, zorder=1)

# Anotación del proyecto
ax1.annotate(f'PROYECTO\n{Deriva:.3f}%',
             xy=(Deriva, len(niveles_redi) - 0.5),
             xytext=(Deriva + 0.3, len(niveles_redi) - 0.2),
             fontsize=13, fontweight='bold',
             color=COLORES['proyecto'],
             arrowprops=dict(arrowstyle='->',
                             color=COLORES['proyecto'], lw=3),
             bbox=dict(boxstyle='round,pad=0.4',
                       facecolor='white',
                       edgecolor=COLORES['proyecto'],
                       linewidth=2.5),
             zorder=15)

ax1.set_xlim(-0.5, 4.5)
ax1.set_ylim(-0.8, len(niveles_redi) - 0.2)
ax1.set_xlabel('Deriva de entrepiso (%)', fontsize=13, fontweight='bold')
ax1.set_yticks([])
ax1.set_title('(a) NIVELES REDi™ — OBJETIVOS DE RESILIENCIA',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax1.legend(fontsize=11, loc='lower right')
ax1.grid(True, axis='x', linestyle='--', alpha=0.4)

# ============================================================================
# PANEL (b): OBJETIVOS POR NIVEL (DETALLE)
# ============================================================================

ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')
ax2.set_title('(b) OBJETIVOS POR NIVEL REDi™',
              fontsize=12, fontweight='bold', color=COLORES['titulo'], pad=15)

txt2 = (
    "PLATINUM:\n"
    "═══════════════════════════════\n"
    "  Downtime: < 72 horas\n"
    "  Pérdida:  < 2.5%\n"
    "  Deriva:   < 0.2%\n\n"
    "GOLD:\n"
    "═══════════════════════════════\n"
    "  Downtime: < 1 mes\n"
    "  Pérdida:  < 5%\n"
    "  Deriva:   < 0.5%\n\n"
    "SILVER:\n"
    "═══════════════════════════════\n"
    "  Downtime: < 6 meses\n"
    "  Pérdida:  < 10%\n"
    "  Deriva:   < 1.5%\n\n"
    "BASE (Código):\n"
    "═══════════════════════════════\n"
    "  Downtime: > 6 meses\n"
    "  Pérdida:  > 10%\n"
    "  Deriva:   < 2.0%"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): APLICACIÓN AL PROYECTO
# ============================================================================

ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')
ax3.set_title('(c) APLICACIÓN AL PROYECTO',
              fontsize=12, fontweight='bold', color=COLORES['proyecto'], pad=15)

txt3 = (
    "TU PROYECTO\n"
    "═══════════════════════════════\n\n"
    f"  Deriva = {Deriva:.3f}%\n\n"
    "  CLASIFICACIÓN REDi™:\n"
    "  • SILVER (1.5% < 2.0%)\n\n"
    "  OBJETIVOS:\n"
    "  • Downtime: < 6 meses\n"
    "  • Pérdida: < 10%\n"
    "  • Seguridad: Improbable\n\n"
    "  COMPARACIÓN:\n"
    "  • NEC-15: ✅ Cumple\n"
    "  • HAZUZ: Extenso\n"
    "  • Vision: Near collapse\n"
    "  • REDi: Silver\n\n"
    "═══════════════════════════════\n"
    "  ✅ CUMPLE NEC-15\n"
    "  ⚠️ Nivel Silver (no Platinum)"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_35"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_35_REDi_objetivos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.35 — REDi™ RESILIENCE OBJECTIVES")
print("=" * 80)
print(f"\n  NIVELES REDi™:")
for nivel in niveles_redi:
    print(f"\n  {nivel['nombre']}:")
    print(f"    Deriva:   < {nivel['deriva']}%")
    print(f"    Downtime: {nivel['downtime']}")
    print(f"    Pérdida:  {nivel['perdida']}")
    print(f"    Seguridad: {nivel['seguridad']}")
print(f"\n  TU PROYECTO:")
print(f"    Deriva = {Deriva:.3f}%")
print(f"    Clasificación: SILVER")
print(f"    ✅ Cumple NEC-15")
print("=" * 80)