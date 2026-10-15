# -*- coding: utf-8 -*-
"""
================================================================================
M07.46 — CORTANTE MÍNIMO CON AMORTIGUAMIENTO (β_V+I)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.46 — Cortante Mínimo con Amortiguamiento

OBJETIVO: Calcular el cortante mínimo considerando el amortiguamiento
          total (β_V+I) y verificando el límite 0.75V.

FÓRMULAS:
    β_V+I = β_I + β_V
    B_V+I = 4 / (3.5 - ln(β_V+I × 100))
    V_min = V / B_V+I
    V_min ≥ 0.75V

DATOS DEL PROYECTO:
    - V = 231.02 t (sin disipador)
    - β_I = 0.05 (hormigón)
    - β_V = 0.10 (disipador)
    - β_V+I = 0.15 (total)
    - B_V+I = 5.05
    - V_min = 45.75 t
    - 0.75V = 173.27 t
    - V_min final = 173.27 t
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
V = 231.02      # t (cortante sin disipador)
beta_I = 0.05   # amortiguamiento inherente (hormigón)
beta_V = 0.10   # amortiguamiento viscoso (disipador)
beta_total = beta_I + beta_V  # 0.15


def B_xi(xi):
    """Factor de reducción por amortiguamiento."""
    return 4 / (3.5 - np.log(xi * 100))


# Cálculos
B_total = B_xi(beta_total)
V_min_calc = V / B_total
V_min_075 = 0.75 * V
V_min_final = max(V_min_calc, V_min_075)

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
ax_header.text(0.98, 0.5, 'M07.46 — CORTANTE MÍNIMO',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'CORTANTE MÍNIMO CON AMORTIGUAMIENTO (β_V+I)',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.892,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): FÓRMULA
# ============================================================================

ax1 = fig.add_axes([0.04, 0.68, 0.44, 0.18])
ax1.set_facecolor(COLORES['fondo_panel'])
ax1.axis('off')

ax1.set_title('(a) FÓRMULA DEL CORTANTE MÍNIMO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt1 = (
    "FÓRMULAS:\n"
    "═══════════════════════════════════════════\n"
    "  β_V+I = β_I + β_V\n\n"
    "  B_V+I = 4 / (3.5 - ln(β_V+I × 100))\n\n"
    "  V_min = V / B_V+I\n\n"
    "  V_min ≥ 0.75V\n\n"
    "DONDE:\n"
    "═══════════════════════════════════════════\n"
    "  β_I = amortiguamiento inherente\n"
    "  β_V = amortiguamiento viscoso\n"
    "  β_V+I = amortiguamiento total"
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
    f"  V         = {V:.2f} t\n"
    f"  β_I       = {beta_I:.2f}\n"
    f"  β_V       = {beta_V:.2f}\n"
    f"  β_V+I     = {beta_total:.2f}\n\n"
    "CÁLCULOS:\n"
    "═══════════════════════════════════════════\n"
    f"  B_V+I     = 4/(3.5-ln({beta_total*100:.0f}))\n"
    f"  B_V+I     = {B_total:.4f}\n\n"
    f"  V_min     = V / B_V+I\n"
    f"  V_min     = {V:.2f} / {B_total:.4f}\n"
    f"  V_min     = {V_min_calc:.2f} t\n\n"
    f"  0.75V     = {V_min_075:.2f} t"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): TABLA DE AMORTIGUAMIENTO
# ============================================================================

ax3 = fig.add_axes([0.04, 0.38, 0.44, 0.25])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')

ax3.set_title('(c) TABLA DE AMORTIGUAMIENTO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

tabla_beta = [
    ("β_I", 0.05, "Inherente (hormigón)"),
    ("β_V", 0.10, "Viscoso (disipador)"),
    ("β_V+I", 0.15, "Total"),
]

y_start = 0.85
headers = ["Parámetro", "Valor", "Descripción"]
x_cols = [0.05, 0.35, 0.55]

for header, x in zip(headers, x_cols):
    ax3.text(x, y_start, header,
             fontsize=10, fontweight='bold', color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')

ax3.plot([0.03, 0.97], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=1.5,
         transform=ax3.transAxes, clip_on=False)

for i, (param, val, desc) in enumerate(tabla_beta):
    y = y_start - 0.16 - i * 0.15

    if param == "β_V+I":
        rect = FancyBboxPatch((0.02, y - 0.06), 0.96, 0.12,
                               boxstyle="round,pad=0.01",
                               facecolor=COLORES['ok_bg'],
                               edgecolor=COLORES['ok'], linewidth=2,
                               transform=ax3.transAxes)
        ax3.add_patch(rect)

    color_txt = COLORES['ok'] if param == "β_V+I" else COLORES['titulo']

    ax3.text(x_cols[0], y, param,
             fontsize=11, fontweight='bold', color=color_txt,
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[1], y, f"{val:.2f}",
             fontsize=11, fontweight='bold', color=color_txt,
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[2], y, desc,
             fontsize=9, color=COLORES['subtitulo'],
             transform=ax3.transAxes, va='center')

# ============================================================================
# PANEL (d): RESULTADO
# ============================================================================

ax4 = fig.add_axes([0.52, 0.38, 0.44, 0.25])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')

ax4.set_title('(d) RESULTADO DEL CORTANTE MÍNIMO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# Cuadro grande
rect = FancyBboxPatch((0.05, 0.50), 0.90, 0.40,
                       boxstyle="round,pad=0.03",
                       facecolor=COLORES['ok_bg'],
                       edgecolor=COLORES['ok'], linewidth=3,
                       transform=ax4.transAxes)
ax4.add_patch(rect)

ax4.text(0.5, 0.78, f'V_min = {V_min_final:.2f} t',
         fontsize=28, fontweight='bold', color=COLORES['ok'],
         ha='center', va='center', transform=ax4.transAxes)

ax4.text(0.5, 0.62, f'Gobierna: 0.75V = {V_min_075:.2f} t',
         fontsize=13, fontweight='bold', color=COLORES['titulo'],
         ha='center', va='center', transform=ax4.transAxes)

txt4 = (
    f"V_min (cálculo) = {V_min_calc:.2f} t\n"
    f"0.75V (límite)  = {V_min_075:.2f} t\n"
    f"V_min final     = {V_min_final:.2f} t"
)

ax4.text(0.5, 0.25, txt4,
         fontsize=10, family='monospace',
         ha='center', va='center', transform=ax4.transAxes,
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='white',
                   edgecolor=COLORES['ok'],
                   linewidth=2))

# ============================================================================
# PANEL (e): GRÁFICA DE CORTANTE
# ============================================================================

ax5 = fig.add_axes([0.04, 0.05, 0.92, 0.28])
ax5.set_facecolor(COLORES['fondo_panel'])

# Datos
xis = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
labels_xi = [f'{x*100:.0f}%' for x in xis]
V_min_calcs = [V / B_xi(x) for x in xis]
V_min_075_array = [0.75 * V] * len(xis)
V_min_finales = [max(v, 0.75*V) for v in V_min_calcs]

x_pos = np.arange(len(xis))
width = 0.35

# Barras V_min cálculo
bars1 = ax5.bar(x_pos - width/2, V_min_calcs, width,
                color=COLORES['advertencia'], edgecolor='#333333',
                linewidth=1.5, alpha=0.8, label='V_min = V / B(ξ)')

# Barras V_min final
bars2 = ax5.bar(x_pos + width/2, V_min_finales, width,
                color=COLORES['ok'], edgecolor='#333333',
                linewidth=1.5, alpha=0.8, label='V_min final (max)')

# Línea de 0.75V
ax5.axhline(y=V_min_075, color=COLORES['critica'], linestyle='--',
            linewidth=3, label=f'0.75V = {V_min_075:.2f} t', zorder=10)

# Etiquetas
for bar, val in zip(bars1, V_min_calcs):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             f'{val:.1f}', ha='center', va='bottom',
             fontweight='bold', fontsize=9, color=COLORES['advertencia'])

for bar, val in zip(bars2, V_min_finales):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             f'{val:.1f}', ha='center', va='bottom',
             fontweight='bold', fontsize=9, color=COLORES['ok'])

ax5.set_xticks(x_pos)
ax5.set_xticklabels(labels_xi, fontsize=12, fontweight='bold')
ax5.set_xlabel('Amortiguamiento ξ', fontsize=13, fontweight='bold')
ax5.set_ylabel('Cortante mínimo V_min (t)', fontsize=13, fontweight='bold')
ax5.set_title('(e) CORTANTE MÍNIMO POR AMORTIGUAMIENTO',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax5.legend(fontsize=11, loc='upper right')
ax5.grid(True, axis='y', linestyle='--', alpha=0.4)
ax5.set_ylim(0, 250)

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

carpeta = "Resultados_M07_46"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_46_cortante_minimo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.46 — CORTANTE MÍNIMO CON AMORTIGUAMIENTO")
print("=" * 80)
print(f"\n  DATOS:")
print(f"    V         = {V:.2f} t")
print(f"    β_I       = {beta_I:.2f}")
print(f"    β_V       = {beta_V:.2f}")
print(f"    β_V+I     = {beta_total:.2f}")
print(f"\n  CÁLCULOS:")
print(f"    B_V+I     = {B_total:.4f}")
print(f"    V_min     = V / B_V+I = {V_min_calc:.2f} t")
print(f"    0.75V     = {V_min_075:.2f} t")
print(f"    V_min final = max(V_min, 0.75V) = {V_min_final:.2f} t")
print(f"\n  INTERPRETACIÓN:")
print(f"    El límite 0.75V gobierna")
print(f"    V_min final = {V_min_final:.2f} t")
print("=" * 80)