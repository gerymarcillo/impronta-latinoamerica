# -*- coding: utf-8 -*-
"""
================================================================================
M07.43 — CLASIFICACIÓN SILVER Y DESPLAZAMIENTO ENCONTRADO
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.43 — SILVER y Desplazamiento

OBJETIVO: Calcular el desplazamiento objetivo (x obj) cuando la
          deriva calculada clasifica como SILVER.

LÓGICA:
    1. der = 0.0161
    2. Clasificación HAZUZ: SILVER
    3. der obj = 0.0156
    4. x obj = 0.0156 × He × 100 = 4.68 cm
    5. β = der / der obj = 1.03

DATOS:
    - He = 3.00 m
    - der = 0.01608
    - tipo = SILVER
    - der obj = 0.0156
    - x obj = 4.68 cm
    - β = 1.0308
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
    'silver': '#495057',
    'silver_bg': '#e9ecef',
    'beta': '#8e44ad',
    'beta_bg': '#f4ecf7',
    'box_datos': '#ffffff',
    'box_datos_borde': '#0d1b2a',
    'box_resultado': '#d8f3dc',
    'box_resultado_borde': '#2d6a4f',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Datos
He = 3.00
X_inel = 4.83  # cm
der = X_inel / He / 100  # 0.0161

# Clasificación HAZUZ
tipo = "SILVER"
der_obj = 0.0156

# Desplazamiento objetivo
X_obj = der_obj * He * 100  # 4.68 cm

# Factor β
beta = der / der_obj  # 1.0308

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
ax_header.text(0.98, 0.5, 'M07.43 — SILVER Y DESPLAZAMIENTO',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'CLASIFICACIÓN SILVER Y DESPLAZAMIENTO ENCONTRADO',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.892,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): LÓGICA DEL CÁLCULO
# ============================================================================

ax1 = fig.add_axes([0.04, 0.68, 0.44, 0.18])
ax1.set_facecolor(COLORES['fondo_panel'])
ax1.axis('off')

ax1.set_title('(a) LÓGICA DEL CÁLCULO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt1 = (
    "PASO A PASO:\n"
    "═══════════════════════════════════════════\n"
    "  1. der = 0.0161\n"
    "  2. Clasificación HAZUZ: SILVER\n"
    "  3. der obj = 0.0156\n"
    "  4. x obj = der obj × He × 100\n"
    "  5. β = der / der obj\n\n"
    "RESULTADO:\n"
    "═══════════════════════════════════════════\n"
    "  x obj = 0.0156 × 3.00 × 100\n"
    "  x obj = 4.68 cm\n\n"
    "  β = 0.0161 / 0.0156 = 1.03"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (b): DATOS Y CÁLCULOS
# ============================================================================

ax2 = fig.add_axes([0.52, 0.68, 0.44, 0.18])
ax2.set_facecolor(COLORES['fondo_panel'])
ax2.axis('off')

ax2.set_title('(b) DATOS Y CÁLCULOS',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt2 = (
    "DATOS:\n"
    "═══════════════════════════════════════════\n"
    f"  He        = {He:.2f} m\n"
    f"  X inel    = {X_inel:.2f} cm\n"
    f"  der       = {der:.5f}\n\n"
    "CLASIFICACIÓN:\n"
    "═══════════════════════════════════════════\n"
    f"  tipo      = {tipo}\n"
    f"  der obj   = {der_obj:.4f}\n\n"
    "DESPLAZAMIENTO:\n"
    "═══════════════════════════════════════════\n"
    f"  x obj     = {X_obj:.2f} cm\n"
    f"  β         = {beta:.4f}"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): TABLA HAZUZ
# ============================================================================

ax3 = fig.add_axes([0.04, 0.38, 0.60, 0.25])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')

ax3.set_title('(c) TABLA HAZUZ 1999 — DESPLAZAMIENTOS OBJETIVO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

tabla_hazuz = [
    ("PLATINUM", 0.0033, 0.99, "< 0.33%"),
    ("GOLD", 0.0058, 1.74, "0.33% - 0.58%"),
    ("SILVER", 0.0156, 4.68, "0.58% - 1.56%"),
    ("COMPLETO", 0.0400, 12.00, "> 1.56%"),
]

y_start = 0.80
headers = ["Tipo", "Deriva objetivo", "X objetivo (cm)", "Rango"]
x_cols = [0.05, 0.25, 0.50, 0.75]

for header, x in zip(headers, x_cols):
    ax3.text(x, y_start, header,
             fontsize=11, fontweight='bold', color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')

ax3.plot([0.03, 0.97], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=1.5,
         transform=ax3.transAxes, clip_on=False)

for i, (tipo_row, der_row, x_row, rango) in enumerate(tabla_hazuz):
    y = y_start - 0.16 - i * 0.16

    if tipo_row == tipo:
        rect = FancyBboxPatch((0.02, y - 0.07), 0.96, 0.14,
                               boxstyle="round,pad=0.01",
                               facecolor=COLORES['silver_bg'],
                               edgecolor=COLORES['silver'], linewidth=2,
                               transform=ax3.transAxes)
        ax3.add_patch(rect)
        color_txt = COLORES['silver']
    else:
        color_txt = COLORES['subtitulo']

    ax3.text(x_cols[0], y, tipo_row,
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[1], y, f"{der_row:.4f}",
             fontsize=10, color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[2], y, f"{x_row:.2f}",
             fontsize=10, color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[3], y, rango,
             fontsize=10, color=COLORES['subtitulo'],
             transform=ax3.transAxes, va='center')

# ============================================================================
# PANEL (d): RESULTADO
# ============================================================================

ax4 = fig.add_axes([0.68, 0.38, 0.28, 0.25])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')

ax4.set_title('(d) RESULTADO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# Cuadro grande
rect = FancyBboxPatch((0.05, 0.50), 0.90, 0.40,
                       boxstyle="round,pad=0.03",
                       facecolor=COLORES['silver_bg'],
                       edgecolor=COLORES['silver'], linewidth=3,
                       transform=ax4.transAxes)
ax4.add_patch(rect)

ax4.text(0.5, 0.78, 'SILVER',
         fontsize=28, fontweight='bold', color=COLORES['silver'],
         ha='center', va='center', transform=ax4.transAxes)

ax4.text(0.5, 0.60, f'x obj = {X_obj:.2f} cm',
         fontsize=18, fontweight='bold', color=COLORES['titulo'],
         ha='center', va='center', transform=ax4.transAxes)

txt4 = (
    f"der       = {der:.5f}\n"
    f"der obj   = {der_obj:.4f}\n"
    f"x obj     = {X_obj:.2f} cm\n"
    f"β         = {beta:.4f}"
)

ax4.text(0.5, 0.22, txt4,
         fontsize=10, family='monospace',
         ha='center', va='center', transform=ax4.transAxes,
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor=COLORES['silver'],
                   linewidth=2))

# ============================================================================
# PANEL (e): GRÁFICA COMPARATIVA
# ============================================================================

ax5 = fig.add_axes([0.04, 0.05, 0.92, 0.28])
ax5.set_facecolor(COLORES['fondo_panel'])

# Datos
tipos = ["PLATINUM", "GOLD", "SILVER", "COMPLETO"]
x_objs = [0.99, 1.74, 4.68, 12.00]
colores_barras = ['#6c757d', '#e07a00', '#495057', '#9d0208']

x_pos = np.arange(len(tipos))
bars = ax5.bar(x_pos, x_objs, color=colores_barras,
               edgecolor='#333333', linewidth=2, width=0.6, alpha=0.85)

# Etiquetas
for bar, val in zip(bars, x_objs):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val:.2f} cm', ha='center', va='bottom',
             fontweight='bold', fontsize=12, color=COLORES['titulo'])

# Línea del desplazamiento real
ax5.axhline(y=X_inel, color=COLORES['beta'], linestyle='-',
            linewidth=3, label=f'X inel real = {X_inel:.2f} cm')

# Anotación
ax5.annotate(f'X inel = {X_inel:.2f} cm\n> x obj (SILVER) = {X_obj:.2f} cm\nβ = {beta:.4f}',
             xy=(2, X_inel),
             xytext=(2.5, X_inel + 2),
             fontsize=12, fontweight='bold',
             color=COLORES['beta'],
             arrowprops=dict(arrowstyle='->',
                             color=COLORES['beta'], lw=3),
             bbox=dict(boxstyle='round,pad=0.5',
                       facecolor='white',
                       edgecolor=COLORES['beta'],
                       linewidth=2.5),
             zorder=15)

ax5.set_xticks(x_pos)
ax5.set_xticklabels(tipos, fontsize=12, fontweight='bold')
ax5.set_ylabel('Desplazamiento objetivo (cm)', fontsize=13, fontweight='bold')
ax5.set_title('(e) DESPLAZAMIENTO OBJETIVO POR TIPO HAZUZ',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax5.legend(fontsize=11, loc='upper left')
ax5.grid(True, axis='y', linestyle='--', alpha=0.4)
ax5.set_ylim(0, 15)

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

carpeta = "Resultados_M07_43"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_43_silver_desplazamiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.43 — SILVER Y DESPLAZAMIENTO ENCONTRADO")
print("=" * 80)
print(f"\n  DATOS:")
print(f"    He        = {He:.2f} m")
print(f"    X inel    = {X_inel:.2f} cm")
print(f"    der       = {der:.5f}")
print(f"\n  CLASIFICACIÓN:")
print(f"    tipo      = {tipo}")
print(f"    der obj   = {der_obj:.4f}")
print(f"\n  DESPLAZAMIENTO:")
print(f"    x obj     = {X_obj:.2f} cm")
print(f"    β         = {beta:.4f}")
print(f"\n  INTERPRETACIÓN:")
print(f"    β = {beta:.4f} > 1 → Excede SILVER")
print(f"    Pero CUMPLE NEC-15 (der < 0.02)")
print("=" * 80)