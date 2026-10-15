# -*- coding: utf-8 -*-
"""
================================================================================
M07.52 — DISIPADOR TENSOR-PUNTAL DE 50 cm
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.52 — Disipador Tensor-Puntal

OBJETIVO: Diseñar disipadores de hasta 50 cm de longitud, con rótula,
          colocados hasta 2 por piso en diagonal tipo tensor-puntal.

CONFIGURACIÓN:
    - Longitud: ≤ 50 cm
    - Rótula: conexión articulada
    - Colocación: 2 por piso
    - Forma: diagonal (tensor-puntal)
    - Función: solo tracción

DATOS DEL PROYECTO:
    - C_total = 2.378 t·s/m
    - F_max = 231.02 t
    - β_V = 10%
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon, FancyArrowPatch
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
    'acero': '#495057',
    'acero_oscuro': '#212529',
    'aceite': '#f39c12',
    'piston': '#7f8c8d',
    'rotula': '#e74c3c',
    'diagonal': '#2c3e50',
    'box_datos': '#ffffff',
    'box_datos_borde': '#0d1b2a',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Datos
C_total = 2.378     # t·s/m
F_max = 231.02      # t
beta_V = 0.10       # 10%

# Configuración
N_pisos = 2
N_por_piso = 2
N_total = N_pisos * N_por_piso  # 4 disipadores

# Cálculo por disipador
C_unit = C_total / N_total
F_unit = F_max / N_total

# Longitud del disipador
L_disipador_max = 50  # cm
L_cilindro = 30       # cm
L_vastago = 15        # cm
L_rotula = 5          # cm
D_cilindro = 15       # cm
D_vastago = 6         # cm
stroke = 5            # cm (±)

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(28, 22))
fig.patch.set_facecolor(COLORES['fondo'])

# Encabezado
ax_header = fig.add_axes([0, 0.95, 1, 0.05])
ax_header.set_facecolor(COLORES['titulo'])
ax_header.axis('off')
ax_header.text(0.02, 0.5, '🏗️', fontsize=28, va='center')
ax_header.text(0.05, 0.5, 'UNESUM · REZ-2026 · JIPIJAPA-001',
               fontsize=15, fontweight='bold', color='white', va='center')
ax_header.text(0.98, 0.5, 'M07.52 — DISIPADOR TENSOR-PUNTAL 50 cm',
               fontsize=15, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.925,
         'DISEÑO DEL DISIPADOR TENSOR-PUNTAL DE 50 cm',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.905,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=11,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): ESQUEMA DEL DISIPADOR (50 cm)
# ============================================================================

ax1 = fig.add_axes([0.04, 0.62, 0.44, 0.26])
ax1.set_facecolor('#ffffff')
ax1.set_xlim(-10, 60)
ax1.set_ylim(-15, 15)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('(a) ESQUEMA DEL DISIPADOR (50 cm)',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# --- RÓTULA IZQUIERDA ---
rotula_izq = Circle((0, 0), 3, facecolor=COLORES['rotula'],
                     edgecolor='#922b21', linewidth=2, zorder=5)
ax1.add_patch(rotula_izq)

# --- CILINDRO ---
cilindro = Rectangle((3, -D_cilindro/2), L_cilindro, D_cilindro,
                      facecolor=COLORES['acero'], edgecolor=COLORES['acero_oscuro'],
                      linewidth=2.5, alpha=0.85, zorder=3)
ax1.add_patch(cilindro)

# --- ACEITE ---
aceite = Rectangle((5, -D_cilindro/2 + 2), L_cilindro - 4, D_cilindro - 4,
                    facecolor=COLORES['aceite'], edgecolor='#b9770e',
                    linewidth=1.5, alpha=0.5, zorder=4)
ax1.add_patch(aceite)

# --- PISTÓN ---
piston = Rectangle((18, -D_cilindro/2 + 3), 4, D_cilindro - 6,
                    facecolor=COLORES['piston'], edgecolor='#2c3e50',
                    linewidth=2, zorder=5)
ax1.add_patch(piston)

# --- VÁSTAGO ---
vastago = Rectangle((33, -D_vastago/2), L_vastago, D_vastago,
                     facecolor=COLORES['piston'], edgecolor='#2c3e50',
                     linewidth=2, zorder=5)
ax1.add_patch(vastago)

# --- RÓTULA DERECHA ---
rotula_der = Circle((50, 0), 3, facecolor=COLORES['rotula'],
                     edgecolor='#922b21', linewidth=2, zorder=5)
ax1.add_patch(rotula_der)

# --- FLECHAS DE MOVIMIENTO ---
ax1.annotate('', xy=(-8, 0), xytext=(-3, 0),
             arrowprops=dict(arrowstyle='->', color=COLORES['critica'],
                             lw=3, mutation_scale=20))
ax1.annotate('', xy=(58, 0), xytext=(53, 0),
             arrowprops=dict(arrowstyle='->', color=COLORES['critica'],
                             lw=3, mutation_scale=20))

# --- COTAS ---
# Cilindro
ax1.annotate('', xy=(3, -12), xytext=(33, -12),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(18, -14, f'Cilindro: {L_cilindro} cm',
         fontsize=9, fontweight='bold', ha='center', va='top')

# Vástago
ax1.annotate('', xy=(33, -12), xytext=(48, -12),
             arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax1.text(40.5, -14, f'Vástago: {L_vastago} cm',
         fontsize=9, fontweight='bold', ha='center', va='top')

# Longitud total
ax1.annotate('', xy=(0, 12), xytext=(50, 12),
             arrowprops=dict(arrowstyle='<->', color=COLORES['info'], lw=2))
ax1.text(25, 13.5, f'L_total = {L_disipador_max} cm',
         fontsize=10, fontweight='bold', ha='center', va='bottom',
         color=COLORES['info'])

# Rótulas
ax1.text(0, -5, f'Rótula\n{L_rotula} cm',
         fontsize=8, fontweight='bold', ha='center', va='top',
         color=COLORES['rotula'])
ax1.text(50, -5, f'Rótula\n{L_rotula} cm',
         fontsize=8, fontweight='bold', ha='center', va='top',
         color=COLORES['rotula'])

# ============================================================================
# PANEL (b): COLOCACIÓN EN EL PÓRTICO (DIAGONAL)
# ============================================================================

ax2 = fig.add_axes([0.52, 0.62, 0.44, 0.26])
ax2.set_facecolor('#ffffff')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.axis('off')
ax2.set_title('(b) COLOCACIÓN EN EL PÓRTICO (DIAGONAL)',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# --- PÓRTICO ---
# Columnas
ax2.plot([2, 2], [1, 8], '-', color='#2c3e50', linewidth=6)
ax2.plot([8, 8], [1, 8], '-', color='#2c3e50', linewidth=6)

# Vigas
ax2.plot([2, 8], [4.5, 4.5], '-', color='#7f8c8d', linewidth=8)
ax2.plot([2, 8], [8, 8], '-', color='#7f8c8d', linewidth=8)

# Base
ax2.plot([1, 9], [1, 1], 'k-', linewidth=6)

# --- DISIPADOR DIAGONAL PISO 1 (izquierda) ---
ax2.plot([2.5, 5], [4.5, 1.5], '-', color=COLORES['acento'],
         linewidth=4, alpha=0.8, zorder=5)
# Rótulas
ax2.plot(2.5, 4.5, 'o', color=COLORES['rotula'], markersize=10, zorder=6)
ax2.plot(5, 1.5, 'o', color=COLORES['rotula'], markersize=10, zorder=6)

# --- DISIPADOR DIAGONAL PISO 1 (derecha) ---
ax2.plot([7.5, 5], [4.5, 1.5], '-', color=COLORES['acento'],
         linewidth=4, alpha=0.8, zorder=5)
ax2.plot(7.5, 4.5, 'o', color=COLORES['rotula'], markersize=10, zorder=6)

# --- DISIPADOR DIAGONAL PISO 2 (izquierda) ---
ax2.plot([2.5, 5], [8, 4.5], '-', color=COLORES['acento'],
         linewidth=4, alpha=0.8, zorder=5)
ax2.plot(2.5, 8, 'o', color=COLORES['rotula'], markersize=10, zorder=6)
ax2.plot(5, 4.5, 'o', color=COLORES['rotula'], markersize=10, zorder=6)

# --- DISIPADOR DIAGONAL PISO 2 (derecha) ---
ax2.plot([7.5, 5], [8, 4.5], '-', color=COLORES['acento'],
         linewidth=4, alpha=0.8, zorder=5)
ax2.plot(7.5, 8, 'o', color=COLORES['rotula'], markersize=10, zorder=6)

# --- ETIQUETAS ---
ax2.text(1.5, 8, 'Piso 2', fontsize=10, fontweight='bold',
         ha='right', va='center')
ax2.text(1.5, 4.5, 'Piso 1', fontsize=10, fontweight='bold',
         ha='right', va='center')
ax2.text(1.5, 1, 'Base', fontsize=10, fontweight='bold',
         ha='right', va='center')

# --- CONFIGURACIÓN ---
ax2.text(5, 9.5, 'CONFIGURACIÓN: 2 por piso en diagonal',
         fontsize=11, fontweight='bold', ha='center', va='center',
         color=COLORES['titulo'],
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2))

# ============================================================================
# PANEL (c): CARACTERÍSTICAS DEL DISIPADOR
# ============================================================================

ax3 = fig.add_axes([0.04, 0.32, 0.28, 0.26])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')
ax3.set_title('(c) CARACTERÍSTICAS',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt3 = (
    "DISIPADOR\n"
    "═══════════════════════════════\n\n"
    f"  Longitud total  = {L_disipador_max} cm\n"
    f"  Cilindro        = {L_cilindro} cm\n"
    f"  Vástago         = {L_vastago} cm\n"
    f"  Rótula          = {L_rotula} cm\n"
    f"  Stroke          = ±{stroke} cm\n\n"
    f"  D_cilindro      = {D_cilindro} cm\n"
    f"  D_vástago       = {D_vastago} cm\n\n"
    "  C_unitario      = 0.5945 t·s/m\n"
    "  F_unitario      = 57.76 t\n\n"
    "  N_por_piso      = 2\n"
    "  N_total         = 4"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): DISTRIBUCIÓN POR PISO
# ============================================================================

ax4 = fig.add_axes([0.36, 0.32, 0.28, 0.26])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')
ax4.set_title('(d) DISTRIBUCIÓN',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt4 = (
    "DISTRIBUCIÓN\n"
    "═══════════════════════════════\n\n"
    "  PISO 1:\n"
    "    2 disipadores\n"
    "    C = 1.189 t·s/m\n"
    "    F = 115.51 t\n\n"
    "  PISO 2:\n"
    "    2 disipadores\n"
    "    C = 1.189 t·s/m\n"
    "    F = 115.51 t\n\n"
    "  TOTAL:\n"
    "    4 disipadores\n"
    "    C_total = 2.378 t·s/m\n"
    "    F_total = 231.02 t\n\n"
    "  β_V = 10%"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['ok_bg'],
                   edgecolor=COLORES['ok'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (e): TIPO TENSOR-PUNTAL
# ============================================================================

ax5 = fig.add_axes([0.68, 0.32, 0.28, 0.26])
ax5.set_facecolor(COLORES['fondo_panel'])
ax5.axis('off')
ax5.set_title('(e) SISTEMA TENSOR-PUNTAL',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt5 = (
    "TENSOR-PUNTAL\n"
    "═══════════════════════════════\n\n"
    "  FUNCIÓN:\n"
    "  • Solo trabaja a TRACCIÓN\n"
    "  • No trabaja a compresión\n\n"
    "  COMPONENTES:\n"
    "  • Tensor (cable/barra)\n"
    "  • Puntal (rigidizador)\n"
    "  • Rótulas en extremos\n\n"
    "  VENTAJAS:\n"
    "  • Simple instalación\n"
    "  • Bajo costo\n"
    "  • Fácil mantenimiento\n"
    "  • Reemplazable\n\n"
    "  DIAGONAL:\n"
    "  • 2 por piso\n"
    "  • Forma de X\n"
    "  • Simétrico"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (f): COMPARACIÓN DE ALTERNATIVAS
# ============================================================================

ax6 = fig.add_axes([0.04, 0.04, 0.92, 0.24])
ax6.set_facecolor(COLORES['fondo_panel'])
ax6.axis('off')
ax6.set_title('(f) COMPARACIÓN DE ALTERNATIVAS DE CONFIGURACIÓN',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)

# Tabla comparativa
y_start = 0.85
headers = ["Configuración", "N_por_piso", "N_total", "L_disipador", "C_unit", "F_unit", "β_V", "Estado"]
x_cols = [0.05, 0.22, 0.35, 0.48, 0.58, 0.68, 0.78, 0.88]

for header, x in zip(headers, x_cols):
    ax6.text(x, y_start, header,
             fontsize=10, fontweight='bold', color=COLORES['titulo'],
             transform=ax6.transAxes, va='center', ha='center')

ax6.plot([0.01, 0.99], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=1.5,
         transform=ax6.transAxes, clip_on=False)

# Alternativas
alternativas = [
    ("2 por piso (X)", 2, 4, "50 cm", 0.5945, 57.76, "10.00%", "✅ RECOMENDADA"),
    ("1 por piso", 1, 2, "50 cm", 1.189, 115.51, "10.00%", "✅ Válida"),
    ("3 por piso", 3, 6, "50 cm", 0.396, 38.50, "10.00%", "✅ Válida"),
    ("4 por piso", 4, 8, "50 cm", 0.297, 28.88, "10.00%", "⚠️ Muchos"),
]

for i, (config, n_pp, n_tot, l_disp, c_unit, f_unit, beta, estado) in enumerate(alternativas):
    y = y_start - 0.18 - i * 0.16

    if i == 0:
        rect = FancyBboxPatch((0.005, y - 0.07), 0.99, 0.13,
                               boxstyle="round,pad=0.01",
                               facecolor=COLORES['ok_bg'],
                               edgecolor=COLORES['ok'], linewidth=2.5,
                               transform=ax6.transAxes)
        ax6.add_patch(rect)
        color_txt = COLORES['ok']
    else:
        color_txt = COLORES['titulo']

    ax6.text(x_cols[0], y, config,
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[1], y, f"{n_pp}",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[2], y, f"{n_tot}",
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[3], y, l_disp,
             fontsize=10, color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[4], y, f"{c_unit:.4f}",
             fontsize=10, color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[5], y, f"{f_unit:.2f}",
             fontsize=10, color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[6], y, beta,
             fontsize=10, fontweight='bold', color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')
    ax6.text(x_cols[7], y, estado,
             fontsize=9, fontweight='bold', color=color_txt,
             transform=ax6.transAxes, va='center', ha='center')

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

fig.text(0.5, 0.015,
         '"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."',
         ha='center', va='bottom', fontsize=10,
         color=COLORES['subtitulo'], style='italic',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white',
                   edgecolor=COLORES['acento'],
                   linewidth=1.5))

fig.text(0.5, 0.002,
         f'{PROYECTO} · {datetime.now().strftime("%Y-%m-%d %H:%M")}',
         ha='center', va='bottom', fontsize=8,
         color=COLORES['linea'])

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_52"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_52_disipador_50cm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.52 — DISIPADOR TENSOR-PUNTAL DE 50 cm")
print("=" * 80)
print(f"\n  CONFIGURACIÓN:")
print(f"    Longitud total  = {L_disipador_max} cm")
print(f"    Cilindro        = {L_cilindro} cm")
print(f"    Vástago         = {L_vastago} cm")
print(f"    Rótula          = {L_rotula} cm")
print(f"    Stroke          = ±{stroke} cm")
print(f"    D_cilindro      = {D_cilindro} cm")
print(f"    D_vástago       = {D_vastago} cm")
print(f"\n  DISTRIBUCIÓN:")
print(f"    N_por_piso      = {N_por_piso}")
print(f"    N_total         = {N_total}")
print(f"    C_unitario      = {C_unit:.4f} t·s/m")
print(f"    F_unitario      = {F_unit:.2f} t")
print(f"\n  ALTERNATIVAS:")
for config, n_pp, n_tot, l_disp, c_unit, f_unit, beta, estado in alternativas:
    print(f"    {config:<20} N={n_tot} C={c_unit:.4f} F={f_unit:.2f} {estado}")
print("=" * 80)