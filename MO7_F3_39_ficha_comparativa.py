# -*- coding: utf-8 -*-
"""
================================================================================
M07.32 — TABLA INTEGRADORA CONCEPTUAL (SOLO GRÁFICA)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.32 — Tabla Integradora

OBJETIVO: Gráfica de barras horizontales con los rangos de deriva
          por norma, SIN tablas.

NORMAS INTEGRADAS:
    - HAZUZ 1999
    - Vision 2000
    - FEMA 273/356
    - ATC-40
    - BERTERO (1994)
    - NEC-15 (2015)

DATOS DEL PROYECTO:
    - Deriva = 1.608%
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
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
    'hazuz': '#f39c12',
    'vision': '#16a085',
    'fema': '#3498db',
    'atc': '#9b59b6',
    'bertero': '#e67e22',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

Deriva = 1.608
Limite_NEC = 2.0

# ============================================================================
# 2. TABLA DE RANGOS
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
# 3. FIGURA — SOLO GRÁFICA
# ============================================================================

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.32 — TABLA INTEGRADORA CONCEPTUAL DE NORMAS DE DERIVA',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Deriva del proyecto = {Deriva:.3f}%',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

# Eje principal
ax = fig.add_axes([0.18, 0.10, 0.78, 0.80])
ax.set_facecolor('#ffffff')

# ============================================================================
# GRÁFICA DE BARRAS HORIZONTALES
# ============================================================================

y_positions = np.arange(len(tabla_integradora))
bar_height = 0.5

for i, (norma, rango_bajo, rango_alto, desc, color) in enumerate(tabla_integradora):
    # Barra de rango
    ax.barh(i, rango_alto - rango_bajo, left=rango_bajo,
            height=bar_height, color=color, alpha=0.7,
            edgecolor='black', linewidth=1.5)
    
    # Etiqueta de la norma
    ax.text(-0.15, i, norma, ha='right', va='center',
            fontsize=13, fontweight='bold', color=color)
    
    # Etiqueta del rango (inicio y fin)
    ax.text(rango_bajo + 0.05, i, f'{rango_bajo:.2f}%',
            ha='left', va='center', fontsize=10, fontweight='bold')
    ax.text(rango_alto - 0.05, i, f'{rango_alto:.2f}%',
            ha='right', va='center', fontsize=10, fontweight='bold')
    
    # Descripción del rango
    ax.text(rango_alto + 0.10, i, desc,
            ha='left', va='center', fontsize=9,
            color='#555555', style='italic')

# Línea vertical del proyecto
ax.axvline(x=Deriva, color=COLORES['proyecto'],
           linestyle='-', linewidth=4, zorder=10,
           label=f'Proyecto: {Deriva:.3f}%')

# Línea vertical del límite NEC
ax.axvline(x=Limite_NEC, color=COLORES['nec'],
           linestyle='--', linewidth=3, zorder=10,
           label=f'Límite NEC-15: {Limite_NEC:.2f}%')

# Zona del proyecto
ax.axvspan(Deriva - 0.05, Deriva + 0.05,
           color=COLORES['proyecto'], alpha=0.2, zorder=1)

# Anotación del proyecto
ax.annotate(f'PROYECTO\n{Deriva:.3f}%',
            xy=(Deriva, len(tabla_integradora) - 0.5),
            xytext=(Deriva + 0.4, len(tabla_integradora) - 0.2),
            fontsize=13, fontweight='bold',
            color=COLORES['proyecto'],
            arrowprops=dict(arrowstyle='->',
                            color=COLORES['proyecto'], lw=3),
            bbox=dict(boxstyle='round,pad=0.5',
                      facecolor='white',
                      edgecolor=COLORES['proyecto'],
                      linewidth=2.5),
            zorder=15)

# Configuración de ejes
ax.set_xlim(-0.5, 4.8)
ax.set_ylim(-0.8, len(tabla_integradora) - 0.2)
ax.set_xlabel('Deriva de entrepiso (%)', fontsize=14, fontweight='bold')
ax.set_yticks([])
ax.set_title('RANGOS DE DERIVA POR NORMA — PROYECTO UBICADO',
             fontsize=15, fontweight='bold', color=COLORES['titulo'], pad=20)
ax.legend(fontsize=12, loc='lower right')
ax.grid(True, axis='x', linestyle='--', alpha=0.4)

# ============================================================================
# 4. CUADRO DE CLASIFICACIÓN (ESQUINA INFERIOR)
# ============================================================================

txt_clasificacion = (
    "CLASIFICACIÓN DEL PROYECTO\n"
    "═══════════════════════════════\n"
    f"  Deriva = {Deriva:.3f}%\n"
    "═══════════════════════════════\n"
    "  • HAZUZ 1999: Extenso\n"
    "  • Vision 2000: Near collapse\n"
    "  • FEMA 273: Extensive\n"
    "  • ATC-40: Seguridad de Vida\n"
    "  • BERTERO: Seguridad de Vida\n"
    "  • NEC-15: ✅ CUMPLE\n"
    "═══════════════════════════════"
)

fig.text(0.985, 0.08, txt_clasificacion,
         transform=fig.transFigure,
         fontsize=9, family='monospace',
         ha='right', va='bottom',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2))

# ============================================================================
# 5. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_32"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_32_tabla_integradora_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 6. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.32 — TABLA INTEGRADORA CONCEPTUAL (SOLO GRÁFICA)")
print("=" * 80)
print(f"\n  DERIVA DEL PROYECTO = {Deriva:.3f}%")
print(f"\n  RANGOS POR NORMA:")
for norma, rb, ra, desc, color in tabla_integradora:
    print(f"    {norma:<15} {rb:.2f}% - {ra:.2f}%  ({desc})")
print(f"\n  CLASIFICACIÓN DEL PROYECTO:")
print(f"    HAZUZ 1999:    Extenso (Silver)")
print(f"    Vision 2000:   Near collapse")
print(f"    FEMA 273:      Extensive")
print(f"    ATC-40:        Seguridad de Vida")
print(f"    BERTERO:       Seguridad de Vida")
print(f"    NEC-15:        ✅ CUMPLE")
print("=" * 80)