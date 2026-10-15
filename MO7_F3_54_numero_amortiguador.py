# -*- coding: utf-8 -*-
"""
================================================================================
M07.47 — NÚMERO DE AMORTIGUADORES SEGÚN β
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.47 — Número de Amortiguadores

OBJETIVO: Calcular el número de amortiguadores necesarios para
          lograr el amortiguamiento objetivo β_V = 10%.

FÓRMULAS:
    β_V+I = β_I + β_V
    C = (β_V · W · T) / (4π · Σφ²)
    N = C_total / C_unitario

DATOS DEL PROYECTO:
    - β_I = 5% (hormigón)
    - β_V = 10% (objetivo)
    - β_V+I = 15% (total)
    - W = 810.60 t
    - T = 0.389 s
    - Σφ² = 1.055
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
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Datos
W = 810.60      # t
T1 = 0.389      # s
beta_I = 0.05   # 5%
beta_V = 0.10   # 10%
beta_total = beta_I + beta_V  # 15%

# Modos
phi1 = 0.235
phi2 = 1.000
suma_phi2 = phi1**2 + phi2**2  # 1.055

# Cálculo de C (coeficiente de amortiguamiento)
C_total = (beta_V * W * T1) / (4 * np.pi * suma_phi2)

# Distribución por piso
C_piso1 = (beta_V * W * T1 * phi1**2) / (4 * np.pi * suma_phi2)
C_piso2 = (beta_V * W * T1 * phi2**2) / (4 * np.pi * suma_phi2)

# Amortiguadores
amortiguadores = [
    ("Pequeño", 0.5, C_total / 0.5),
    ("Mediano", 1.0, C_total / 1.0),
    ("Grande", 2.0, C_total / 2.0),
    ("Muy grande", 5.0, C_total / 5.0),
]

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
ax_header.text(0.98, 0.5, 'M07.47 — NÚMERO DE AMORTIGUADORES',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'NÚMERO DE AMORTIGUADORES SEGÚN β',
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

ax1.set_title('(a) FÓRMULA DEL AMORTIGUADOR',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt1 = (
    "FÓRMULAS:\n"
    "═══════════════════════════════════════════\n"
    "  β_V+I = β_I + β_V\n\n"
    "  C = (β_V · W · T) / (4π · Σφ²)\n\n"
    "  N = C_total / C_unitario\n\n"
    "DONDE:\n"
    "═══════════════════════════════════════════\n"
    "  β_V = amortiguamiento del disipador\n"
    "  W = peso total\n"
    "  T = período fundamental\n"
    "  Σφ² = suma de modos al cuadrado"
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
    f"  W         = {W:.2f} t\n"
    f"  T₁        = {T1:.3f} s\n"
    f"  β_I       = {beta_I*100:.0f}%\n"
    f"  β_V       = {beta_V*100:.0f}%\n"
    f"  β_V+I     = {beta_total*100:.0f}%\n"
    f"  Σφ²       = {suma_phi2:.4f}\n\n"
    "CÁLCULO DE C:\n"
    "═══════════════════════════════════════════\n"
    f"  C = ({beta_V:.2f} × {W:.2f} × {T1:.3f})\n"
    f"      / (4π × {suma_phi2:.4f})\n"
    f"  C = {C_total:.4f} t·s/m"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): DISTRIBUCIÓN POR PISO
# ============================================================================

ax3 = fig.add_axes([0.04, 0.38, 0.44, 0.25])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')

ax3.set_title('(c) DISTRIBUCIÓN POR PISO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt3 = (
    "PISO 1 (φ₁ = 0.235):\n"
    "═══════════════════════════════════════════\n"
    f"  C₁ = {C_piso1:.4f} t·s/m\n"
    f"  %  = {C_piso1/C_total*100:.1f}%\n\n"
    "PISO 2 (φ₂ = 1.000):\n"
    "═══════════════════════════════════════════\n"
    f"  C₂ = {C_piso2:.4f} t·s/m\n"
    f"  %  = {C_piso2/C_total*100:.1f}%\n\n"
    "TOTAL:\n"
    "═══════════════════════════════════════════\n"
    f"  C_total = {C_total:.4f} t·s/m"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): NÚMERO DE AMORTIGUADORES
# ============================================================================

ax4 = fig.add_axes([0.52, 0.38, 0.44, 0.25])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')

ax4.set_title('(d) NÚMERO DE AMORTIGUADORES',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

y_start = 0.85
headers = ["Tipo", "C_unit", "Cantidad"]
x_cols = [0.10, 0.45, 0.75]

for header, x in zip(headers, x_cols):
    ax4.text(x, y_start, header,
             fontsize=11, fontweight='bold', color=COLORES['titulo'],
             transform=ax4.transAxes, va='center', ha='center')

ax4.plot([0.05, 0.95], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=1.5,
         transform=ax4.transAxes, clip_on=False)

for i, (tipo, c_unit, n) in enumerate(amortiguadores):
    y = y_start - 0.16 - i * 0.14

    ax4.text(x_cols[0], y, tipo,
             fontsize=10, fontweight='bold', color=COLORES['titulo'],
             transform=ax4.transAxes, va='center', ha='center')
    ax4.text(x_cols[1], y, f"{c_unit:.1f}",
             fontsize=10, color=COLORES['subtitulo'],
             transform=ax4.transAxes, va='center', ha='center')
    ax4.text(x_cols[2], y, f"{np.ceil(n):.0f}",
             fontsize=11, fontweight='bold', color=COLORES['acento'],
             transform=ax4.transAxes, va='center', ha='center')

# ============================================================================
# PANEL (e): GRÁFICA
# ============================================================================

ax5 = fig.add_axes([0.04, 0.05, 0.92, 0.28])
ax5.set_facecolor(COLORES['fondo_panel'])

# Datos
tipos = [a[0] for a in amortiguadores]
cantidades = [a[2] for a in amortiguadores]
colores_bar = [COLORES['ok'], COLORES['info'],
               COLORES['advertencia'], COLORES['critica']]

x_pos = np.arange(len(tipos))
bars = ax5.bar(x_pos, cantidades, color=colores_bar,
               edgecolor='#333333', linewidth=2, width=0.6, alpha=0.85)

for bar, val in zip(bars, cantidades):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{np.ceil(val):.0f}', ha='center', va='bottom',
             fontweight='bold', fontsize=14, color=COLORES['titulo'])

ax5.set_xticks(x_pos)
ax5.set_xticklabels(tipos, fontsize=12, fontweight='bold')
ax5.set_ylabel('Número de amortiguadores', fontsize=13, fontweight='bold')
ax5.set_title('(e) NÚMERO DE AMORTIGUADORES SEGÚN TIPO',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax5.grid(True, axis='y', linestyle='--', alpha=0.4)
ax5.set_ylim(0, max(cantidades) * 1.3)

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

carpeta = "Resultados_M07_47"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_47_amortiguadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.47 — NÚMERO DE AMORTIGUADORES SEGÚN β")
print("=" * 80)
print(f"\n  DATOS:")
print(f"    W         = {W:.2f} t")
print(f"    T₁        = {T1:.3f} s")
print(f"    β_I       = {beta_I*100:.0f}%")
print(f"    β_V       = {beta_V*100:.0f}%")
print(f"    β_V+I     = {beta_total*100:.0f}%")
print(f"    Σφ²       = {suma_phi2:.4f}")
print(f"\n  COEFICIENTE DE AMORTIGUAMIENTO:")
print(f"    C_total   = {C_total:.4f} t·s/m")
print(f"    C_piso1   = {C_piso1:.4f} t·s/m")
print(f"    C_piso2   = {C_piso2:.4f} t·s/m")
print(f"\n  NÚMERO DE AMORTIGUADORES:")
for tipo, c_unit, n in amortiguadores:
    print(f"    {tipo:<12} C = {c_unit:.1f} → {np.ceil(n):.0f} unidades")
print("=" * 80)