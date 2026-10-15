# -*- coding: utf-8 -*-
"""
================================================================================
M07.4 — MATRIZ DE RIGIDEZ LATERAL DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.4 — Matriz de Rigidez
OBJETIVO: Desarrollo analítico paso a paso de la matriz de rigidez lateral

NOTA METODOLÓGICA:
    E = 12600 * raiz(fc)  (módulo de elasticidad estocástico)
    Método: Shear building (rigidez lateral = solo columnas)
    Hipótesis: columna biempotrada
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
# 2. CÁLCULO ANALÍTICO
# ============================================================================

E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
I_col = (B_COL * H_COL**3) / 12
I_col_cm4 = I_col * 100**4
k_columna = 12 * E_tm2 * I_col / He**3
k_columna_kgcm = k_columna * 10
k_entrepiso = N_COL_TOTAL * k_columna
k_entrepiso_kgcm = k_entrepiso * 10

K_X = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso,     k_entrepiso]
])

# ============================================================================
# 3. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.4 — MATRIZ DE RIGIDEZ LATERAL DEL PROYECTO PRINCIPAL")
print("=" * 80)
print(f"""
  DATOS:
    Seccion columna  = {B_COL*100:.0f} x {H_COL*100:.0f} cm
    He               = {He:.2f} m
    # Columnas       = {N_COL_TOTAL}
    E                = {E_kgcm2:.2f} kg/cm2

  CALCULOS:
    I_col    = {I_col_cm4:.2f} cm4
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
         'M07.4 — MATRIZ DE RIGIDEZ LATERAL DEL PROYECTO PRINCIPAL',
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
              height_ratios=[1.0, 1.2, 1.0])

# ============================================================================
# FILA 0: INFO
# ============================================================================

# --- Panel (a): DATOS ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
ax1.set_title('(a) DATOS DEL PROYECTO',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt1 = (
    f"LX = {LX_TOTAL:.2f} m\n"
    f"LY = {LY_TOTAL:.2f} m\n"
    f"Area = {LX_TOTAL*LY_TOTAL:.2f} m2\n"
    f"Columnas = {N_COL_TOTAL} u\n"
    f"He = {He:.2f} m\n"
    f"fc = {fc} kg/cm2"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2, alpha=0.95))

# --- Panel (b): FORMULA ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
ax2.set_title('(b) FORMULA DE RIGIDEZ',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt2 = (
    "k_col = 12 * E * I / He^3\n\n"
    "k_piso = N_col * k_col\n\n"
    "Shear building:\n"
    "  - Empotrada base\n"
    "  - Empotrada nudo"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=2, alpha=0.95))

# --- Panel (c): ESQUEMA ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(-1, 3); ax3.set_ylim(-0.5, 4)

ax3.plot([-0.5, 2.5], [0, 0], 'k-', linewidth=3)
for xx in np.linspace(-0.5, 2.5, 12):
    ax3.plot([xx, xx - 0.1], [0, -0.15], 'k-', linewidth=1.5)

ax3.add_patch(Rectangle((0.81, 0), 0.38, 3,
                          facecolor=COLORES['col_n1'],
                          edgecolor='black', linewidth=2))
ax3.add_patch(Rectangle((0, 3), 2, 0.3,
                          facecolor=COLORES['viga'],
                          edgecolor='black', linewidth=2))

ax3.plot(1, 0, marker='^', markersize=15, color='green')
ax3.plot(1, 3.3, marker='s', markersize=12, color='red')

ax3.annotate('', xy=(1.5, 2), xytext=(2.3, 2),
             arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
ax3.text(2.4, 2, 'F', fontsize=11, color='red', fontweight='bold')

ax3.annotate('', xy=(0.5, 0), xytext=(0.5, 3),
             arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
ax3.text(0.2, 1.5, f'He\n{He} m', fontsize=9, color='blue',
         fontweight='bold', ha='right')

ax3.set_title('(c) COLUMNA BIEMPOTRADA',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)
ax3.axis('off')

# ============================================================================
# FILA 1: DESARROLLO ANALITICO
# ============================================================================

ax4 = fig.add_subplot(gs[1, :])
ax4.set_xlim(0, 10); ax4.set_ylim(0, 10); ax4.axis('off')
ax4.set_title('(d) DESARROLLO ANALITICO PASO A PASO',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

desarrollo = (
    f"PASO 1:  E = 12600 * raiz({fc}) = {E_kgcm2:.1f} kg/cm2\n"
    f"PASO 2:  I_col = {B_COL} * {H_COL}^3 / 12 = {I_col:.7f} m4\n"
    f"PASO 3:  k_col = 12 * E * I_col / He^3 = {k_columna:.2f} t/m\n"
    f"PASO 4:  k_piso = {N_COL_TOTAL} * {k_columna:.2f} = {k_entrepiso:.2f} t/m\n"
    f"PASO 5:  K = [[2*k_piso, -k_piso], [-k_piso, k_piso]]"
)

ax4.text(0.5, 0.5, desarrollo, transform=ax4.transAxes,
         ha='center', va='center', fontsize=11, family='monospace',
         linespacing=2.2,
         bbox=dict(boxstyle='round,pad=0.9',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# FILA 2: MATRIZ K + SIGNIFICADO
# ============================================================================

ax5 = fig.add_subplot(gs[2, 0:2])
ax5.axis('off')
ax5.set_title('(e) MATRIZ DE RIGIDEZ LATERAL K (2x2)',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

matriz_txt = (
    f"K = [[ {K_X[0,0]:>12.2f} , {K_X[0,1]:>12.2f} ]\n"
    f"     [ {K_X[1,0]:>12.2f} , {K_X[1,1]:>12.2f} ]]\n\n"
    f"k_piso = {k_entrepiso:.2f} t/m"
)

ax5.text(0.5, 0.5, matriz_txt, transform=ax5.transAxes,
         ha='center', va='center', fontsize=13, family='monospace',
         linespacing=2.0,
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor='white',
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.2, alpha=0.98))

ax6 = fig.add_subplot(gs[2, 2])
ax6.set_xlim(0, 10); ax6.set_ylim(0, 10); ax6.axis('off')
ax6.set_title('(f) SIGNIFICADO FISICO',
              fontsize=11, fontweight='bold',
              color=COLORES['titulo'], pad=8)

# Rigida
ax6.add_patch(Rectangle((1.0, 4.0), 1.5, 3.5,
                         facecolor='#e74c3c',
                         edgecolor='black',
                         linewidth=1.5, alpha=0.7))
ax6.text(1.75, 3.3, 'RIGIDA',
         ha='center', fontsize=8, fontweight='bold',
         color='#c62828')
ax6.text(1.75, 5.5, 'k\nALTA',
         ha='center', fontsize=8, fontweight='bold', color='white')

# Flexible
ax6.add_patch(Rectangle((4.0, 4.0), 0.5, 3.5,
                         facecolor='#3498db',
                         edgecolor='black',
                         linewidth=1.5, alpha=0.7))
ax6.text(4.25, 3.3, 'FLEXIBLE',
         ha='center', fontsize=8, fontweight='bold',
         color='#2471a3')
ax6.text(4.25, 5.5, 'k\nBAJA',
         ha='center', fontsize=8, fontweight='bold', color='white')

# Proyecto
ax6.add_patch(Rectangle((7.0, 4.0), 1.5, 3.5,
                         facecolor='#27ae60',
                         edgecolor='black',
                         linewidth=1.5, alpha=0.7))
ax6.text(7.75, 3.3, 'PROYECTO',
         ha='center', fontsize=8, fontweight='bold',
         color='#145a32')
ax6.text(7.75, 5.5, f'k\n{k_entrepiso:.0f}',
         ha='center', fontsize=8, fontweight='bold', color='white')

ax6.text(5, 1.5,
         'k_piso = rigidez del piso',
         ha='center', va='center', fontsize=8.5, style='italic',
         color='#2c3e50',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fff9c4',
                   edgecolor='#f9a825',
                   linewidth=1.5))

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
    "  Shear building\n"
    "  Rigidez lateral: solo columnas"
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

carpeta = "Resultados_M07_4"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_4_matriz_rigidez_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"\nImagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.4 COMPLETADO — MATRIZ DE RIGIDEZ LATERAL")
print("=" * 80)
print(f"  E        = {E_kgcm2:.2f} kg/cm2")
print(f"  I_col    = {I_col_cm4:.2f} cm4")
print(f"  k_col    = {k_columna:.2f} t/m")
print(f"  k_piso   = {k_entrepiso:.2f} t/m")
print(f"  K[0,0]   = {K_X[0,0]:.2f} t/m")
print(f"  K[0,1]   = {K_X[0,1]:.2f} t/m")
print(f"  K[1,1]   = {K_X[1,1]:.2f} t/m")
print("=" * 80)