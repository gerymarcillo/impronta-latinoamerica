# -*- coding: utf-8 -*-
"""
================================================================================
M07.35 — REDi™ RESILIENCE OBJECTIVES (TABLA COMPLETA)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.35 — REDi™ Resilience Objectives

OBJETIVO: Dashboard con la tabla completa REDi™ (Platinum, Gold, Silver)
          y ubicación del proyecto.

REDi™ (Resilience-based Earthquake Design Initiative):
    - Autor: Arup (2013)

NIVELES:
    PLATINUM: Downtime < 72h | Pérdida < 2.5% | Lesiones improbables
    GOLD:     Downtime < 1 mes | Pérdida < 5% | Lesiones improbables
    SILVER:   Downtime < 6 meses | Pérdida < 10% | Lesiones posibles

DATOS DEL PROYECTO:
    - Deriva = 1.608%
    - Clasificación: Base (código)
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
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

Deriva = 1.608
Limite_NEC = 2.0

# ============================================================================
# 2. NIVELES REDi (TABLA COMPLETA)
# ============================================================================

niveles_redi = [
    {
        'nombre': 'PLATINUM',
        'deriva_max': 0.2,
        'downtime': 'Re-ocupación inmediata\n(Green Tag) +\nRecuperación < 72 horas',
        'perdida': '< 2.5%',
        'seguridad': 'Lesiones improbables',
        'color': COLORES['platinum'],
    },
    {
        'nombre': 'GOLD',
        'deriva_max': 0.5,
        'downtime': 'Re-ocupación inmediata\n(Green Tag) +\nRecuperación < 1 mes',
        'perdida': '< 5%',
        'seguridad': 'Lesiones improbables',
        'color': COLORES['gold'],
    },
    {
        'nombre': 'SILVER',
        'deriva_max': 1.5,
        'downtime': 'Re-ocupación < 6 meses\n(Yellow Tag posible) +\nRecuperación < 6 meses',
        'perdida': '< 10%',
        'seguridad': 'Lesiones posibles\n(pero no colapso)',
        'color': COLORES['silver'],
    },
    {
        'nombre': 'BASE (Código)',
        'deriva_max': 2.0,
        'downtime': '> 6 meses',
        'perdida': '> 10%',
        'seguridad': 'Colapso posible',
        'color': COLORES['base'],
    },
]

# ============================================================================
# 3. FIGURA
# ============================================================================

fig = plt.figure(figsize=(28, 18))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.985,
         'M07.35 — REDi™ RESILIENCE OBJECTIVES',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.962,
         'Baseline Resilience Objectives for Design Level Earthquake',
         ha='center', va='top', fontsize=14,
         color=COLORES['subtitulo'], style='italic')

fig.text(0.5, 0.942,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Deriva = {Deriva:.3f}%',
         ha='center', va='top', fontsize=12,
         color='#7f8c8d')

gs = GridSpec(2, 1, figure=fig,
              hspace=0.25, wspace=0.0,
              left=0.04, right=0.97,
              top=0.92, bottom=0.04,
              height_ratios=[1.0, 1.5])

# ============================================================================
# PANEL (a): GRÁFICA DE BARRAS HORIZONTALES
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('#ffffff')

for i, nivel in enumerate(niveles_redi):
    # Barra
    ax1.barh(i, nivel['deriva_max'], height=0.6,
             color=nivel['color'], alpha=0.7,
             edgecolor='black', linewidth=2)
    
    # Etiqueta del nivel
    ax1.text(-0.05, i, nivel['nombre'],
             ha='right', va='center',
             fontsize=14, fontweight='bold', color=nivel['color'])
    
    # Valor de deriva
    ax1.text(nivel['deriva_max'] + 0.05, i,
             f"Deriva < {nivel['deriva_max']}%",
             ha='left', va='center',
             fontsize=11, fontweight='bold')
    
    # Downtime
    ax1.text(nivel['deriva_max'] + 0.5, i,
             f"Downtime: {nivel['downtime'].replace(chr(10), ' ')}",
             ha='left', va='center',
             fontsize=9, color='#555555', style='italic')

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

# Anotación
ax1.annotate(f'PROYECTO\n{Deriva:.3f}%',
             xy=(Deriva, len(niveles_redi) - 0.5),
             xytext=(Deriva + 0.3, len(niveles_redi) - 0.2),
             fontsize=12, fontweight='bold',
             color=COLORES['proyecto'],
             arrowprops=dict(arrowstyle='->',
                             color=COLORES['proyecto'], lw=2.5),
             bbox=dict(boxstyle='round,pad=0.4',
                       facecolor='white',
                       edgecolor=COLORES['proyecto'],
                       linewidth=2.5),
             zorder=15)

ax1.set_xlim(-0.5, 4.0)
ax1.set_ylim(-0.8, len(niveles_redi) - 0.2)
ax1.set_xlabel('Deriva de entrepiso (%)', fontsize=13, fontweight='bold')
ax1.set_yticks([])
ax1.set_title('(a) NIVELES REDi™ — OBJETIVOS DE RESILIENCIA',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax1.legend(fontsize=11, loc='lower right')
ax1.grid(True, axis='x', linestyle='--', alpha=0.4)

# ============================================================================
# PANEL (b): TABLA COMPLETA REDi™
# ============================================================================

ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')
ax2.set_title('(b) TABLA COMPLETA REDi™ — BASELINE RESILIENCE OBJECTIVES',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)

# Construir tabla como texto
tabla_txt = (
    "═══════════════════════════════════════════════════════════════════════════════\n"
    "                    BASELINE RESILIENCE OBJECTIVES\n"
    "                    for Design Level Earthquake\n"
    "═══════════════════════════════════════════════════════════════════════════════\n\n"
    "  ┌──────────┬──────────────────────────────────────┬──────────────┬──────────────────────────────┐\n"
    "  │ NIVEL    │ DOWNTIME                             │ PÉRDIDA      │ SEGURIDAD OCUPANTES          │\n"
    "  ├──────────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤\n"
    "  │ PLATINUM │ Re-ocupación inmediata (Green Tag)   │ < 2.5%       │ Lesiones improbables         │\n"
    "  │          │ Recuperación funcional < 72 horas    │              │                              │\n"
    "  ├──────────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤\n"
    "  │ GOLD     │ Re-ocupación inmediata (Green Tag)   │ < 5%         │ Lesiones improbables         │\n"
    "  │          │ Recuperación funcional < 1 mes       │              │                              │\n"
    "  ├──────────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤\n"
    "  │ SILVER   │ Re-ocupación < 6 meses               │ < 10%        │ Lesiones posibles            │\n"
    "  │          │ (Yellow Tag posible)                 │              │ (pero no colapso)            │\n"
    "  │          │ Recuperación funcional < 6 meses     │              │ Fatalidades improbables      │\n"
    "  ├──────────┼──────────────────────────────────────┼──────────────┼──────────────────────────────┤\n"
    "  │ BASE     │ > 6 meses                            │ > 10%        │ Colapso posible              │\n"
    "  │ (Código) │                                      │              │                              │\n"
    "  └──────────┴──────────────────────────────────────┴──────────────┴──────────────────────────────┘\n\n"
    "═══════════════════════════════════════════════════════════════════════════════\n\n"
    f"  TU PROYECTO: Deriva = {Deriva:.3f}%\n\n"
    f"  CLASIFICACIÓN:\n"
    f"  • REDi™: Base (Código) — 1.608% > 1.5% (Silver)\n"
    f"  • NEC-15: ✅ Cumple\n"
    f"  • HAZUZ: Extenso\n"
    f"  • Vision 2000: Near collapse\n\n"
    "  NORMA: REDi™ (Arup, 2013)\n"
    "═══════════════════════════════════════════════════════════════════════════════"
)

ax2.text(0.5, 0.5, tabla_txt, transform=ax2.transAxes,
         ha='center', va='center', fontsize=8, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 4. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_35"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_35_REDi_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 5. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.35 — REDi™ RESILIENCE OBJECTIVES")
print("=" * 80)
print(f"\n  TABLA COMPLETA REDi™:")
print(f"\n  PLATINUM:")
print(f"    Downtime: Re-ocupación inmediata + Recuperación < 72h")
print(f"    Pérdida:  < 2.5%")
print(f"    Seguridad: Lesiones improbables")
print(f"    Deriva:   < 0.2%")
print(f"\n  GOLD:")
print(f"    Downtime: Re-ocupación inmediata + Recuperación < 1 mes")
print(f"    Pérdida:  < 5%")
print(f"    Seguridad: Lesiones improbables")
print(f"    Deriva:   < 0.5%")
print(f"\n  SILVER:")
print(f"    Downtime: Re-ocupación < 6 meses + Recuperación < 6 meses")
print(f"    Pérdida:  < 10%")
print(f"    Seguridad: Lesiones posibles (no colapso)")
print(f"    Deriva:   < 1.5%")
print(f"\n  BASE (Código):")
print(f"    Downtime: > 6 meses")
print(f"    Pérdida:  > 10%")
print(f"    Seguridad: Colapso posible")
print(f"    Deriva:   < 2.0%")
print(f"\n  TU PROYECTO:")
print(f"    Deriva = {Deriva:.3f}%")
print(f"    Clasificación: Base (Código)")
print(f"    ✅ Cumple NEC-15")
print("=" * 80)