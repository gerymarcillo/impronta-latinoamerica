# -*- coding: utf-8 -*-
"""
================================================================================
M07.5 — RIGIDEZ LATERAL A CORTANTE DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.5 — Rigidez Lateral a Cortante
OBJETIVO: Cálculo de rigidez lateral a cortante (shear building, 2 GDL):
          - Rigidez de columna biempotrada
          - Rigidez del entrepiso (N columnas en paralelo)
          - Matriz de rigidez lateral K (2×2)
          - Verificación por pórticos

MÉTODO: Shear building (2 GDL)
    Hipótesis: columna biempotrada en cada entrepiso
    He = 3.00 m (altura de entrepiso)
================================================================================
"""

import os
import sys
from datetime import datetime
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
    from matplotlib.patches import Rectangle
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# PALETA DEL PROYECTO
# ============================================================================

COLORES = {
    'fondo_fig': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'box_datos_bg': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_calculo_bg': '#fef9e7',
    'box_calculo_borde': '#f39c12',
    'box_resultado_bg': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_ref_bg': '#f4ecf7',
    'box_ref_borde': '#8e44ad',
    'col_n1': '#2c3e50',
    'viga': '#7f8c8d',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38
B_VIGA = 0.30
H_VIGA = 0.45

fc = 210
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y

# ============================================================================
# 2. CÁLCULOS (2 GDL)
# ============================================================================

# E estocástico
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

# I
I_col = (B_COL * H_COL**3) / 12
I_col_cm4 = I_col * 100**4

# k_col (con He = altura de entrepiso)
k_columna = 12 * E_tm2 * I_col / He**3
k_columna_kgcm = k_columna * 10

# k_piso
k_entrepiso = N_COL_TOTAL * k_columna
k_entrepiso_kgcm = k_entrepiso * 10

# Matriz K (2 GDL)
K_X = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso,     k_entrepiso]
])

# Análisis por pórticos
N_PORTICOS_X = N_COL_Y
N_PORTICOS_Y = N_COL_X
N_COL_POR_PORTICO_X = N_COL_X
N_COL_POR_PORTICO_Y = N_COL_Y

k_portico_X = N_COL_POR_PORTICO_X * k_columna
k_portico_Y = N_COL_POR_PORTICO_Y * k_columna

# ============================================================================
# 3. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.5 — RIGIDEZ LATERAL A CORTANTE (2 GDL)")
print("=" * 80)
print(f"""
  MODELO: Shear building (2 GDL)
    Seccion columna  = {B_COL*100:.0f} x {H_COL*100:.0f} cm
    He (entrepiso)   = {He:.2f} m
    # Columnas       = {N_COL_TOTAL}

  CALCULOS:
    E        = {E_kgcm2:.2f} kg/cm2 = {E_tm2:.2f} t/m2
    I_col    = {I_col:.8f} m4
    k_col    = {k_columna:.2f} t/m
    k_piso   = {k_entrepiso:.2f} t/m

  MATRIZ K (2 GDL):
    K = [[{K_X[0,0]:.2f}, {K_X[0,1]:.2f}]
         [{K_X[1,0]:.2f}, {K_X[1,1]:.2f}]]
""")
print("=" * 80)

# ============================================================================
# 4. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 16))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.5 — RIGIDEZ LATERAL A CORTANTE (2 GDL)',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo base 38×38 cm | k_piso = {k_entrepiso:.0f} t/m',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# GridSpec: 3 filas
gs = GridSpec(3, 3, figure=fig,
              hspace=0.55, wspace=0.30,
              left=0.04, right=0.97,
              top=0.91, bottom=0.04,
              height_ratios=[1.0, 1.0, 1.0])

# ============================================================================
# FILA 0: ESQUEMA + FÓRMULA + DATOS
# ============================================================================

# --- Panel (a): ESQUEMA ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-1, 3); ax1.set_ylim(-0.5, 4)

ax1.plot([-0.5, 2.5], [0, 0], 'k-', linewidth=3)
for xx in np.linspace(-0.5, 2.5, 12):
    ax1.plot([xx, xx - 0.1], [0, -0.15], 'k-', linewidth=1.5)

ax1.add_patch(Rectangle((0.81, 0), 0.38, 3,
                          facecolor=COLORES['col_n1'],
                          edgecolor='black', linewidth=2))
ax1.add_patch(Rectangle((0, 3), 2, 0.3,
                          facecolor=COLORES['viga'],
                          edgecolor='black', linewidth=2))

ax1.plot(1, 0, marker='^', markersize=15, color='green')
ax1.plot(1, 3.3, marker='s', markersize=12, color='red')

ax1.annotate('', xy=(1.5, 2), xytext=(2.3, 2),
             arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
ax1.text(2.4, 2, 'F', fontsize=11, color='red', fontweight='bold')

ax1.annotate('', xy=(0.5, 0), xytext=(0.5, 3),
             arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax1.text(0.2, 1.5, f'He\n{He} m', fontsize=9, color='blue',
         fontweight='bold', ha='right')

ax1.set_title('(a) COLUMNA BIEMPOTRADA (He = entrepiso)',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)
ax1.axis('off')

# --- Panel (b): FÓRMULA ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
ax2.set_title('(b) FORMULA DE RIGIDEZ (2 GDL)',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt2 = (
    "k_col = 12*E*I / He^3\n\n"
    "k_piso = N_col * k_col\n\n"
    "K (2 GDL):\n"
    "  K = [[2k, -k],\n"
    "       [-k,  k]]\n\n"
    "He = altura entrepiso"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=2, alpha=0.95))

# --- Panel (c): DATOS ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(0, 10); ax3.set_ylim(0, 10); ax3.axis('off')
ax3.set_title('(c) DATOS DEL PROYECTO',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt3 = (
    f"LX = {LX_TOTAL:.2f} m\n"
    f"LY = {LY_TOTAL:.2f} m\n"
    f"Columnas = {N_COL_TOTAL} u\n"
    f"He = {He:.2f} m\n"
    f"fc = {fc} kg/cm2\n"
    f"E = 12600*raiz(fc)"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2, alpha=0.95))

# ============================================================================
# FILA 1: RIGIDEZ DEL PISO
# ============================================================================

ax4 = fig.add_subplot(gs[1, :])
ax4.set_xlim(0, 10); ax4.set_ylim(0, 10); ax4.axis('off')
ax4.set_title('(d) RIGIDEZ DEL PISO (k_piso)',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

txt4 = (
    f"k_piso = N_col * k_col\n\n"
    f"k_piso = {N_COL_TOTAL} * {k_columna:.2f}\n\n"
    f"k_piso = {k_entrepiso:.2f} t/m"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=14, family='monospace',
         linespacing=2.0,
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# FILA 2: MATRIZ K + PÓRTICOS
# ============================================================================

# --- Panel (e): MATRIZ K ---
ax5 = fig.add_subplot(gs[2, 0:2])
ax5.axis('off')
ax5.set_title('(e) MATRIZ DE RIGIDEZ LATERAL K (2x2)',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

txt5 = (
    f"K = [[ {K_X[0,0]:>12.2f} , {K_X[0,1]:>12.2f} ]\n"
    f"     [ {K_X[1,0]:>12.2f} , {K_X[1,1]:>12.2f} ]]\n\n"
    f"k = {k_entrepiso:.0f} t/m"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=12, family='monospace',
         linespacing=2.0,
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor='white',
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.2, alpha=0.98))

# --- Panel (f): ANÁLISIS POR PÓRTICOS ---
ax6 = fig.add_subplot(gs[2, 2])
ax6.set_xlim(0, 10); ax6.set_ylim(0, 10); ax6.axis('off')
ax6.set_title('(f) VERIFICACION POR PORTICOS',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt6 = (
    f"Dir X:\n"
    f"  {N_PORTICOS_X} port. x {N_COL_POR_PORTICO_X} col\n"
    f"  k_portico = {k_portico_X:.0f}\n\n"
    f"Dir Y:\n"
    f"  {N_PORTICOS_Y} port. x {N_COL_POR_PORTICO_Y} col\n"
    f"  k_portico = {k_portico_Y:.0f}\n\n"
    f"Total: {N_COL_TOTAL} columnas"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=2, alpha=0.95))

# ============================================================================
# MENSAJES OPORTUNOS FLOTANTES
# ============================================================================

msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Excel PROYECTO.xlsx\n"
    "  Modelo base 38x38 cm"
)

fig.text(0.015, 0.925, msg1, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=1.5, alpha=0.95))

msg2 = (
    "METODO\n"
    "═══════════════════════════\n"
    "  Shear building (2 GDL)\n"
    "  He = altura entrepiso"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 5. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_5"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_5_rigidez_cortante_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"\nImagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 6. RESUMEN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.5 COMPLETADO — RIGIDEZ LATERAL A CORTANTE (2 GDL)")
print("=" * 80)
print(f"  E        = {E_kgcm2:.2f} kg/cm2")
print(f"  I_col    = {I_col_cm4:.2f} cm4")
print(f"  k_col    = {k_columna:.2f} t/m")
print(f"  k_piso   = {k_entrepiso:.2f} t/m")
print(f"  K[0,0]   = {K_X[0,0]:.2f} t/m")
print(f"  K[0,1]   = {K_X[0,1]:.2f} t/m")
print(f"  K[1,1]   = {K_X[1,1]:.2f} t/m")
print("=" * 80)