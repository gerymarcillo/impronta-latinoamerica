# -*- coding: utf-8 -*-
"""
================================================================================
M07.33 — RESUMEN EXPLICATIVO ORDENADO (TABLA INTEGRADORA)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.33 — Resumen Explicativo Ordenado

OBJETIVO: Dashboard con el resumen explicativo ordenado del M07.32,
          estructurado en 7 pasos lógicos.

ESTRUCTURA:
    1. Datos del proyecto
    2. Normas integradas
    3. Clasificación por norma
    4. Visualización gráfica
    5. Interpretación
    6. Conclusiones
    7. Recomendaciones

DATOS DEL PROYECTO:
    - Deriva = 1.608%
    - Límite NEC-15 = 2.00%
    - Cumple = ✅ SÍ
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'proyecto': '#e74c3c',
    'nec': '#c0392b',
    'resultado': '#27ae60',
    'alerta': '#e67e22',
    'hazuz': '#f39c12',
    'vision': '#16a085',
    'fema': '#3498db',
    'atc': '#9b59b6',
    'bertero': '#e67e22',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_alerta': '#fadbd8',
    'box_alerta_borde': '#c0392b',
    'box_norma': '#f4ecf7',
    'box_norma_borde': '#8e44ad',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

Deriva = 1.608
Limite_NEC = 2.0

# ============================================================================
# 2. NORMAS ORDENADAS
# ============================================================================

tabla_integradora = [
    ("HAZUZ 1999", 0.33, 4.00, "Platino → Completo", COLORES['hazuz']),
    ("Vision 2000", 0.20, 2.50, "Fully op. → Near collapse", COLORES['vision']),
    ("FEMA 273/356", 0.50, 2.00, "Slight → Complete", COLORES['fema']),
    ("ATC-40", 1.00, 2.00, "Ocupación → Seguridad", COLORES['atc']),
    ("BERTERO (1994)", 0.20, 2.00, "Ocupación → Seguridad", COLORES['bertero']),
    ("NEC-15", 0.00, 2.00, "Límite de diseño", COLORES['nec']),
]

# ============================================================================
# 3. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.985,
         'M07.33 — RESUMEN EXPLICATIVO ORDENADO (TABLA INTEGRADORA)',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.962,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Deriva = {Deriva:.3f}% | Límite NEC-15 = {Limite_NEC:.2f}%',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

# GridSpec: 4 filas x 3 columnas
gs = GridSpec(4, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.04, right=0.97,
              top=0.92, bottom=0.04,
              height_ratios=[0.8, 1.0, 1.0, 1.0])

# ============================================================================
# PASO 1: DATOS DEL PROYECTO
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('1. DATOS DEL PROYECTO',
              fontsize=12, fontweight='bold', color=COLORES['proyecto'])

txt1 = (
    "DATOS DEL PROYECTO\n"
    "═══════════════════════════════\n\n"
    f"  Deriva       = {Deriva:.3f} %\n"
    f"  Límite NEC   = {Limite_NEC:.2f} %\n\n"
    f"  ¿Cumple?     = ✅ SÍ\n\n"
    "═══════════════════════════════\n"
    "  Proyecto:\n"
    "  UNESUM-REZ-2026-JIPIJAPA-001"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 2: NORMAS INTEGRADAS
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
ax2.set_title('2. NORMAS INTEGRADAS',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])

txt2 = (
    "NORMAS INTEGRADAS\n"
    "═══════════════════════════════\n\n"
    "  #  Norma          Rango\n"
    "  ─────────────────────────────────\n"
)

for i, (norma, rb, ra, desc, color) in enumerate(tabla_integradora, 1):
    txt2 += f"  {i}  {norma:<14} {rb:.2f}%-{ra:.2f}%\n"

txt2 += "\n═══════════════════════════════\n"
txt2 += "  6 normas integradas"

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_norma'],
                   edgecolor=COLORES['box_norma_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 3: CLASIFICACIÓN POR NORMA
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
ax3.set_title('3. CLASIFICACIÓN POR NORMA',
              fontsize=12, fontweight='bold', color=COLORES['resultado'])

txt3 = (
    "CLASIFICACIÓN\n"
    "═══════════════════════════════\n\n"
    "  Norma         Clasificación\n"
    "  ─────────────────────────────────\n"
    "  HAZUZ 1999    Extenso\n"
    "  Vision 2000   Near collapse\n"
    "  FEMA 273      Extensive\n"
    "  ATC-40        Seguridad Vida\n"
    "  BERTERO       Seguridad Vida\n"
    "  NEC-15        ✅ CUMPLE\n\n"
    "═══════════════════════════════\n"
    "  Deriva = 1.608%"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 4: VISUALIZACIÓN GRÁFICA (GRÁFICA DE BARRAS)
# ============================================================================

ax4 = fig.add_subplot(gs[1, :])
ax4.set_facecolor('#ffffff')

for i, (norma, rango_bajo, rango_alto, desc, color) in enumerate(tabla_integradora):
    ax4.barh(i, rango_alto - rango_bajo, left=rango_bajo,
             height=0.5, color=color, alpha=0.7,
             edgecolor='black', linewidth=1.5)
    
    ax4.text(-0.15, i, norma, ha='right', va='center',
             fontsize=11, fontweight='bold', color=color)
    
    ax4.text(rango_bajo + 0.05, i, f'{rango_bajo:.2f}%',
             ha='left', va='center', fontsize=9, fontweight='bold')
    ax4.text(rango_alto - 0.05, i, f'{rango_alto:.2f}%',
             ha='right', va='center', fontsize=9, fontweight='bold')
    
    ax4.text(rango_alto + 0.10, i, desc,
             ha='left', va='center', fontsize=8.5,
             color='#555555', style='italic')

# Línea del proyecto
ax4.axvline(x=Deriva, color=COLORES['proyecto'],
            linestyle='-', linewidth=4, zorder=10,
            label=f'Proyecto: {Deriva:.3f}%')

# Línea del límite NEC
ax4.axvline(x=Limite_NEC, color=COLORES['nec'],
            linestyle='--', linewidth=3, zorder=10,
            label=f'Límite NEC-15: {Limite_NEC:.2f}%')

# Zona del proyecto
ax4.axvspan(Deriva - 0.05, Deriva + 0.05,
            color=COLORES['proyecto'], alpha=0.2, zorder=1)

# Anotación
ax4.annotate(f'PROYECTO\n{Deriva:.3f}%',
             xy=(Deriva, len(tabla_integradora) - 0.5),
             xytext=(Deriva + 0.4, len(tabla_integradora) - 0.2),
             fontsize=12, fontweight='bold',
             color=COLORES['proyecto'],
             arrowprops=dict(arrowstyle='->',
                             color=COLORES['proyecto'], lw=2.5),
             bbox=dict(boxstyle='round,pad=0.4',
                       facecolor='white',
                       edgecolor=COLORES['proyecto'],
                       linewidth=2.5),
             zorder=15)

ax4.set_xlim(-0.5, 4.8)
ax4.set_ylim(-0.8, len(tabla_integradora) - 0.2)
ax4.set_xlabel('Deriva de entrepiso (%)', fontsize=12, fontweight='bold')
ax4.set_yticks([])
ax4.set_title('4. VISUALIZACIÓN GRÁFICA — RANGOS DE DERIVA POR NORMA',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=15)
ax4.legend(fontsize=10, loc='lower right')
ax4.grid(True, axis='x', linestyle='--', alpha=0.4)

# ============================================================================
# PASO 5: INTERPRETACIÓN
# ============================================================================

ax5 = fig.add_subplot(gs[2, 0])
ax5.axis('off')
ax5.set_title('5. INTERPRETACIÓN',
              fontsize=12, fontweight='bold', color=COLORES['alerta'])

txt5 = (
    "INTERPRETACIÓN\n"
    "═══════════════════════════════\n\n"
    f"  Deriva = {Deriva:.3f}%\n"
    "  Rango = 1.5% - 2.0%\n\n"
    "  SIGNIFICADO:\n"
    "  • Daño severo\n"
    "  • Colapso prevenido\n"
    "  • Seguridad de vidas OK\n\n"
    "  SEGÚN VISION 2000:\n"
    "  • Near collapse\n\n"
    "  SEGÚN HAZUZ 1999:\n"
    "  • Extenso (Silver)"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_alerta'],
                   edgecolor=COLORES['box_alerta_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 6: CONCLUSIONES
# ============================================================================

ax6 = fig.add_subplot(gs[2, 1])
ax6.axis('off')
ax6.set_title('6. CONCLUSIONES',
              fontsize=12, fontweight='bold', color=COLORES['resultado'])

txt6 = (
    "CONCLUSIONES\n"
    "═══════════════════════════════\n\n"
    "  1. Deriva = parámetro\n"
    "     universal\n\n"
    "  2. 6 normas convergen\n"
    "     0.2% a 4.0%\n\n"
    "  3. NEC-15 límite\n"
    "     2.00%\n\n"
    "  4. Proyecto cumple\n"
    "     ✅ NEC-15\n\n"
    "  5. Daño severo\n"
    "     aceptable\n\n"
    "  6. Colapso prevenido"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 7: RECOMENDACIONES
# ============================================================================

ax7 = fig.add_subplot(gs[2, 2])
ax7.axis('off')
ax7.set_title('7. RECOMENDACIONES',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])

txt7 = (
    "RECOMENDACIONES\n"
    "═══════════════════════════════\n\n"
    "  1. Monitorear después\n"
    "     de sismos\n\n"
    "  2. Considerar disipador\n"
    "     para Life safety\n"
    "     (< 1.5%)\n\n"
    "  3. Documentar en\n"
    "     memoria de cálculo\n\n"
    "  4. Verificar anclaje\n"
    "     de no estructurales"
)

ax7.text(0.5, 0.5, txt7, transform=ax7.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fef9e7',
                   edgecolor='#f39c12',
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL INFERIOR: RESUMEN FINAL
# ============================================================================

ax8 = fig.add_subplot(gs[3, :])
ax8.axis('off')
ax8.set_title('RESUMEN FINAL DEL PROYECTO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'])

txt8 = (
    "═══════════════════════════════════════════════════════════════════════════════\n"
    "                    RESUMEN FINAL — PROYECTO UNESUM-REZ-2026-JIPIJAPA-001\n"
    "═══════════════════════════════════════════════════════════════════════════════\n\n"
    f"  DERIVA DEL PROYECTO:  {Deriva:.3f}%\n"
    f"  LÍMITE NEC-15:        {Limite_NEC:.2f}%\n"
    f"  ¿CUMPLE?              ✅ SÍ\n\n"
    "  CLASIFICACIÓN:\n"
    "  • HAZUZ 1999:    Extenso (Silver)\n"
    "  • Vision 2000:   Near collapse\n"
    "  • FEMA 273:      Extensive\n"
    "  • ATC-40:        Seguridad de Vida\n"
    "  • BERTERO:       Seguridad de Vida\n"
    "  • NEC-15:        ✅ CUMPLE\n\n"
    "  CONCLUSIÓN FINAL:\n"
    "  ✅ Estructura ACEPTABLE\n"
    "  ✅ Daño severo pero controlado\n"
    "  ✅ Colapso prevenido\n"
    "  ✅ Seguridad de vidas garantizada\n"
    "═══════════════════════════════════════════════════════════════════════════════"
)

ax8.text(0.5, 0.5, txt8, transform=ax8.transAxes,
         ha='center', va='center', fontsize=10, family='monospace',
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['resultado'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 4. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_33"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_33_resumen_explicativo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 5. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.33 — RESUMEN EXPLICATIVO ORDENADO")
print("=" * 80)
print(f"\n  PASO 1: DATOS DEL PROYECTO")
print(f"    Deriva = {Deriva:.3f}%")
print(f"    Límite NEC-15 = {Limite_NEC:.2f}%")
print(f"    ✅ CUMPLE")
print(f"\n  PASO 2: NORMAS INTEGRADAS (6)")
for norma, rb, ra, desc, color in tabla_integradora:
    print(f"    {norma:<15} {rb:.2f}% - {ra:.2f}%")
print(f"\n  PASO 3: CLASIFICACIÓN")
print(f"    HAZUZ 1999:    Extenso")
print(f"    Vision 2000:   Near collapse")
print(f"    NEC-15:        ✅ CUMPLE")
print(f"\n  PASO 4: VISUALIZACIÓN GRÁFICA")
print(f"  PASO 5: INTERPRETACIÓN")
print(f"  PASO 6: CONCLUSIONES")
print(f"  PASO 7: RECOMENDACIONES")
print("=" * 80)