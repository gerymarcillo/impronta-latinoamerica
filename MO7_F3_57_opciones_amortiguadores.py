# -*- coding: utf-8 -*-
"""
================================================================================
M07.51 — RESUMEN DE OPCIONES DE AMORTIGUADORES (CORREGIDO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.51 — Resumen de Opciones
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
    'pequeno': '#3498db',
    'mediano': '#f39c12',
    'grande': '#e74c3c',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

W = 810.60
T1 = 0.389
beta_V_target = 0.10

phi1 = 0.235
phi2 = 1.000
suma_phi2 = phi1**2 + phi2**2

C_total_req = (beta_V_target * W * T1) / (4 * np.pi * suma_phi2)

# ============================================================================
# 2. DEFINICIÓN DE OPCIONES (CORREGIDO: int en lugar de float)
# ============================================================================

opciones = [
    {
        'id': 1,
        'nombre': '2 GRANDES',
        'detalle': '2 × C = 2.0 t·s/m',
        'N': 2,
        'C_total': 4.0,
        'beta_V': 16.82,
        'error': 68.2,
        'costo': 2,
        'instalacion': 2,
        'mantenimiento': 2,
        'color': COLORES['grande'],
        'estado': '⚠️ Excede',
    },
    {
        'id': 2,
        'nombre': '5 PEQUEÑOS',
        'detalle': '5 × C = 0.5 t·s/m',
        'N': 5,
        'C_total': 2.5,
        'beta_V': 10.51,
        'error': 5.1,
        'costo': 2,
        'instalacion': 5,
        'mantenimiento': 5,
        'color': COLORES['pequeno'],
        'estado': '✅ Óptimo',
    },
    {
        'id': 3,
        'nombre': '3 MEDIANOS',
        'detalle': '3 × C = 1.0 t·s/m',
        'N': 3,
        'C_total': 3.0,
        'beta_V': 12.62,
        'error': 26.2,
        'costo': 3,
        'instalacion': 3,
        'mantenimiento': 3,
        'color': COLORES['mediano'],
        'estado': '✅ Balance',
    },
    {
        'id': 4,
        'nombre': '1 GRANDE + 1 PEQUEÑO',
        'detalle': '1 × C=2.0 + 1 × C=0.5',
        'N': 2,
        'C_total': 2.5,
        'beta_V': 10.51,
        'error': 5.1,
        'costo': 2,
        'instalacion': 2,
        'mantenimiento': 2,
        'color': COLORES['ok'],
        'estado': '✅ RECOMENDADA',
    },
]

# ============================================================================
# 3. FIGURA
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
ax_header.text(0.98, 0.5, 'M07.51 — RESUMEN DE OPCIONES',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'RESUMEN DE OPCIONES DE AMORTIGUADORES',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.892,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): TABLA RESUMEN
# ============================================================================

ax1 = fig.add_axes([0.04, 0.62, 0.92, 0.24])
ax1.set_facecolor(COLORES['fondo_panel'])
ax1.axis('off')
ax1.set_title('(a) TABLA RESUMEN DE OPCIONES',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)

y_start = 0.85
headers = ["Opción", "Configuración", "N", "C_total", "β_V", "Error", "Costo", "Inst.", "Mant.", "Estado"]
x_cols = [0.02, 0.12, 0.32, 0.38, 0.46, 0.54, 0.62, 0.72, 0.82, 0.90]

for header, x in zip(headers, x_cols):
    ax1.text(x, y_start, header,
             fontsize=9, fontweight='bold', color=COLORES['titulo'],
             transform=ax1.transAxes, va='center', ha='center')

ax1.plot([0.01, 0.99], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=2,
         transform=ax1.transAxes, clip_on=False)

for i, op in enumerate(opciones):
    y = y_start - 0.18 - i * 0.16

    if op['id'] == 4:
        rect = FancyBboxPatch((0.005, y - 0.07), 0.99, 0.13,
                               boxstyle="round,pad=0.01",
                               facecolor=COLORES['ok_bg'],
                               edgecolor=COLORES['ok'], linewidth=2.5,
                               transform=ax1.transAxes)
        ax1.add_patch(rect)
        color_txt = COLORES['ok']
    else:
        color_txt = COLORES['titulo']

    ax1.text(x_cols[0], y, f"#{op['id']}",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[1], y, op['nombre'],
             fontsize=9, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[2], y, f"{op['N']}",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[3], y, f"{op['C_total']:.2f}",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[4], y, f"{op['beta_V']:.2f}%",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[5], y, f"{op['error']:.1f}%",
             fontsize=10, color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[6], y, "★" * int(op['costo']),
             fontsize=10, color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[7], y, "★" * int(op['instalacion']),
             fontsize=10, color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[8], y, "★" * int(op['mantenimiento']),
             fontsize=10, color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')
    ax1.text(x_cols[9], y, op['estado'],
             fontsize=9, fontweight='bold', color=color_txt,
             transform=ax1.transAxes, va='center', ha='center')

# ============================================================================
# PANEL (b): β_V
# ============================================================================

ax2 = fig.add_axes([0.04, 0.32, 0.44, 0.25])
ax2.set_facecolor(COLORES['fondo_panel'])

nombres = [f"#{op['id']}\n{op['nombre']}" for op in opciones]
betas = [op['beta_V'] for op in opciones]
colores_bar = [op['color'] for op in opciones]

x_pos = np.arange(len(nombres))
bars = ax2.bar(x_pos, betas, color=colores_bar,
               edgecolor='#333333', linewidth=2, width=0.6, alpha=0.85)

for bar, val in zip(bars, betas):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:.2f}%', ha='center', va='bottom',
             fontweight='bold', fontsize=11, color=COLORES['titulo'])

ax2.axhline(y=beta_V_target*100, color=COLORES['critica'], linestyle='--',
            linewidth=3, label=f'Objetivo β_V = {beta_V_target*100:.0f}%')
ax2.axvspan(3 - 0.4, 3 + 0.4, color=COLORES['ok'], alpha=0.2)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(nombres, fontsize=9, fontweight='bold')
ax2.set_ylabel('β_V real (%)', fontsize=12, fontweight='bold')
ax2.set_title('(b) COMPARACIÓN DE β_V',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=15)
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, axis='y', linestyle='--', alpha=0.4)
ax2.set_ylim(0, 22)

# ============================================================================
# PANEL (c): ERROR
# ============================================================================

ax3 = fig.add_axes([0.52, 0.32, 0.44, 0.25])
ax3.set_facecolor(COLORES['fondo_panel'])

errores = [op['error'] for op in opciones]

bars = ax3.bar(x_pos, errores, color=colores_bar,
               edgecolor='#333333', linewidth=2, width=0.6, alpha=0.85)

for bar, val in zip(bars, errores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f}%', ha='center', va='bottom',
             fontweight='bold', fontsize=11, color=COLORES['titulo'])

ax3.axvspan(3 - 0.4, 3 + 0.4, color=COLORES['ok'], alpha=0.2)
ax3.axhline(y=10, color=COLORES['ok'], linestyle='--',
            linewidth=3, label='Error aceptable ≤ 10%')

ax3.set_xticks(x_pos)
ax3.set_xticklabels(nombres, fontsize=9, fontweight='bold')
ax3.set_ylabel('Error vs objetivo (%)', fontsize=12, fontweight='bold')
ax3.set_title('(c) COMPARACIÓN DE ERROR',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=15)
ax3.legend(fontsize=10, loc='upper right')
ax3.grid(True, axis='y', linestyle='--', alpha=0.4)
ax3.set_ylim(0, 80)

# ============================================================================
# PANEL (d): CRITERIOS
# ============================================================================

ax4 = fig.add_axes([0.04, 0.05, 0.44, 0.22])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')
ax4.set_title('(d) CRITERIOS DE SELECCIÓN',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt4 = (
    "CRITERIOS EVALUADOS\n"
    "═══════════════════════════════════\n\n"
    "  ★ COSTO:\n"
    "    ★ = Bajo | ★★ = Medio | ★★★ = Alto\n\n"
    "  ★ INSTALACIÓN:\n"
    "    Complejidad de anclaje\n\n"
    "  ★ MANTENIMIENTO:\n"
    "    Frecuencia de inspección\n\n"
    "  β_V:\n"
    "    Cercanía al objetivo 10%\n\n"
    "  ERROR:\n"
    "    Diferencia porcentual\n\n"
    "═══════════════════════════════════\n"
    "  RECOMENDACIÓN: Opción #4"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (e): CONCLUSIÓN
# ============================================================================

ax5 = fig.add_axes([0.52, 0.05, 0.44, 0.22])
ax5.set_facecolor(COLORES['fondo_panel'])
ax5.axis('off')
ax5.set_title('(e) CONCLUSIÓN Y RECOMENDACIÓN',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt5 = (
    "OPCIÓN RECOMENDADA: #4\n"
    "═══════════════════════════════════\n\n"
    "  CONFIGURACIÓN:\n"
    "    1 GRANDE (Piso 2)\n"
    "    1 PEQUEÑO (Piso 1)\n\n"
    "  C_total = 2.5 t·s/m\n"
    "  β_V = 10.51%\n"
    "  Error = 5.1%\n\n"
    "  VENTAJAS:\n"
    "  ✅ Menos dispositivos (2)\n"
    "  ✅ Menor costo\n"
    "  ✅ Distribución eficiente\n"
    "  ✅ β_V cercano al objetivo\n\n"
    "═══════════════════════════════════\n"
    "  ✅ SELECCIÓN ÓPTIMA"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['ok_bg'],
                   edgecolor=COLORES['ok'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PIE
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
# 4. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_51"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_51_resumen_opciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 5. VERIFICACIÓN
# ============================================================================

print("\n" + "=" * 80)
print("M07.51 — RESUMEN DE OPCIONES DE AMORTIGUADORES")
print("=" * 80)
print(f"\n  DATOS DEL PROYECTO:")
print(f"    W          = {W:.2f} t")
print(f"    T₁         = {T1:.3f} s")
print(f"    β_V_target = {beta_V_target*100:.0f}%")
print(f"    C_requerido = {C_total_req:.4f} t·s/m")
print(f"\n  TABLA DE OPCIONES:")
print(f"    {'#':<3} {'Configuración':<22} {'N':<3} {'C_total':<9} {'β_V':<9} {'Error':<8} {'Estado':<20}")
print(f"    {'-'*80}")
for op in opciones:
    print(f"    {op['id']:<3} {op['nombre']:<22} {op['N']:<3} {op['C_total']:<9.2f} {op['beta_V']:<9.2f} {op['error']:<8.1f} {op['estado']:<20}")

print(f"\n  ✅ RECOMENDACIÓN FINAL: Opción #4")
print(f"    1 GRANDE (Piso 2) + 1 PEQUEÑO (Piso 1)")
print(f"    C_total = 2.5 t·s/m")
print(f"    β_V = 10.51%")
print(f"    Error = 5.1%")
print("=" * 80)