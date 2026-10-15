# -*- coding: utf-8 -*-
"""
================================================================================
ALGORITMO A — PASO 2: MODELO ESTRUCTURAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
ALGORITMO: A — Paso 2

OBJETIVO: Dashboard didáctico del modelo estructural:
    - Geometría
    - Módulo de elasticidad (estocástico)
    - Inercia (dirección mayor)
    - Rigidez de columna
    - Rigidez del piso
    - Peso y masa

DATOS:
    - N columnas = 20
    - Sección = 38×38 cm
    - He = 3.00 m
    - fc = 210 kg/cm²
    - E = 12600·√fc
    - I = 38⁴/12
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'geometria': '#3498db',
    'elasticidad': '#9b59b6',
    'inercia': '#e67e22',
    'rigidez_col': '#e74c3c',
    'rigidez_piso': '#c0392b',
    'masa': '#27ae60',
    'flecha': '#34495e',
    'box': '#ffffff',
    'box_borde': '#1a237e',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

# Geometría
LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]
He = 3.00
fc = 210
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL
N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y
B_COL = 0.38
H_COL = 0.38

# Módulo de elasticidad
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

# Inercia
I_col_cm4 = (38**4) / 12
I_col_m4 = I_col_cm4 / 100**4

# Rigidez de columna
k_col = 12 * E_tm2 * I_col_m4 / He**3

# Rigidez del piso
k_piso = N_COL_TOTAL * k_col

# Peso y masa
W_piso = Cu * AREA
g = 9.81
m_piso = W_piso / g

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 15))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.980,
         'ALGORITMO A — PASO 2: MODELO ESTRUCTURAL',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Columna 38×38 cm | E = 12600·√fc',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

# GridSpec: 3 filas x 3 columnas
gs = GridSpec(3, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.0, 1.0, 1.0])

# ============================================================================
# SUB-PASO 2.1: GEOMETRÍA
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('2.1 GEOMETRÍA',
              fontsize=12, fontweight='bold',
              color=COLORES['geometria'], pad=10)

txt1 = (
    "GEOMETRÍA DEL PROYECTO\n"
    "═══════════════════════════\n\n"
    f"  LUCES_X = {LUCES_X}\n"
    f"  LUCES_Y = {LUCES_Y}\n\n"
    f"  LX = {LX_TOTAL:.2f} m\n"
    f"  LY = {LY_TOTAL:.2f} m\n"
    f"  Área = {AREA:.2f} m²\n\n"
    f"  N° columnas X = {N_COL_X}\n"
    f"  N° columnas Y = {N_COL_Y}\n"
    f"  N° total = {N_COL_TOTAL}\n\n"
    f"  Sección = {B_COL*100:.0f}×{H_COL*100:.0f} cm\n"
    f"  He = {He:.2f} m"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#ebf5fb',
                   edgecolor=COLORES['geometria'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# SUB-PASO 2.2: MÓDULO DE ELASTICIDAD
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
ax2.set_title('2.2 MÓDULO DE ELASTICIDAD',
              fontsize=12, fontweight='bold',
              color=COLORES['elasticidad'], pad=10)

txt2 = (
    "MÓDULO DE ELASTICIDAD (ESTOCÁSTICO)\n"
    "═══════════════════════════════════\n\n"
    "  E = 12600·√fc\n\n"
    f"  fc = {fc} kg/cm²\n"
    f"  √{fc} = {np.sqrt(fc):.4f}\n\n"
    f"  E = 12600 × {np.sqrt(fc):.4f}\n"
    f"  E = {E_kgcm2:.2f} kg/cm²\n\n"
    f"  E = {E_kgcm2:.2f} × 10\n"
    f"  E = {E_tm2:.0f} t/m²\n\n"
    "═══════════════════════════════════\n"
    f"  ✅ E = {E_kgcm2:.0f} kg/cm²"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#f4ecf7',
                   edgecolor=COLORES['elasticidad'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# SUB-PASO 2.3: INERCIA
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
ax3.set_title('2.3 INERCIA',
              fontsize=12, fontweight='bold',
              color=COLORES['inercia'], pad=10)

txt3 = (
    "INERCIA (DIRECCIÓN MAYOR)\n"
    "═══════════════════════════════\n\n"
    "  I = 38⁴ / 12\n\n"
    f"  38⁴ = {38**4}\n"
    f"  38⁴/12 = {I_col_cm4:.2f} cm⁴\n\n"
    f"  I = {I_col_cm4:.2f} cm⁴\n\n"
    f"  Convertir a m⁴:\n"
    f"  I = {I_col_cm4:.2f} / 100⁴\n"
    f"  I = {I_col_m4:.10f} m⁴\n\n"
    "═══════════════════════════════════\n"
    f"  ✅ I = {I_col_cm4:.0f} cm⁴"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fef5e7',
                   edgecolor=COLORES['inercia'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# SUB-PASO 2.4: RIGIDEZ DE COLUMNA
# ============================================================================

ax4 = fig.add_subplot(gs[1, 0])
ax4.axis('off')
ax4.set_title('2.4 RIGIDEZ DE COLUMNA',
              fontsize=12, fontweight='bold',
              color=COLORES['rigidez_col'], pad=10)

txt4 = (
    "RIGIDEZ DE COLUMNA\n"
    "═══════════════════════════════\n\n"
    "  k_col = 12·E·I / He³\n\n"
    f"  E = {E_tm2:.0f} t/m²\n"
    f"  I = {I_col_m4:.8f} m⁴\n"
    f"  He = {He} m\n\n"
    f"  k_col = 12 × {E_tm2:.0f}\n"
    f"          × {I_col_m4:.8f}\n"
    f"          / {He}³\n\n"
    f"  k_col = {k_col:.4f} t/m\n\n"
    "═══════════════════════════════════\n"
    f"  ✅ k_col = {k_col:.2f} t/m"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['rigidez_col'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# SUB-PASO 2.5: RIGIDEZ DEL PISO
# ============================================================================

ax5 = fig.add_subplot(gs[1, 1])
ax5.axis('off')
ax5.set_title('2.5 RIGIDEZ DEL PISO',
              fontsize=12, fontweight='bold',
              color=COLORES['rigidez_piso'], pad=10)

txt5 = (
    "RIGIDEZ DEL PISO\n"
    "═══════════════════════════════\n\n"
    "  k_piso = N_col × k_col\n\n"
    f"  N_col = {N_COL_TOTAL}\n"
    f"  k_col = {k_col:.4f} t/m\n\n"
    f"  k_piso = {N_COL_TOTAL} × {k_col:.4f}\n\n"
    f"  k_piso = {k_piso:.4f} t/m\n\n"
    "═══════════════════════════════════\n"
    f"  ✅ k_piso = {k_piso:.0f} t/m"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['rigidez_piso'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# SUB-PASO 2.6: PESO Y MASA
# ============================================================================

ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.set_title('2.6 PESO Y MASA',
              fontsize=12, fontweight='bold',
              color=COLORES['masa'], pad=10)

txt6 = (
    "PESO Y MASA\n"
    "═══════════════════════════════\n\n"
    f"  Cu = {Cu:.4f} t/m²\n"
    f"  Área = {AREA:.2f} m²\n\n"
    "  W_piso = Cu × Área\n"
    f"  W_piso = {Cu:.4f} × {AREA:.2f}\n"
    f"  W_piso = {W_piso:.4f} t\n\n"
    "  m_piso = W_piso / g\n"
    f"  m_piso = {W_piso:.4f} / {g}\n"
    f"  m_piso = {m_piso:.6f} t·s²/m\n\n"
    "═══════════════════════════════════\n"
    f"  ✅ m_piso = {m_piso:.4f} t·s²/m"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['masa'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL INFERIOR: RESUMEN
# ============================================================================

ax7 = fig.add_subplot(gs[2, :])
ax7.axis('off')
ax7.set_title('RESUMEN DEL PASO 2 — MODELO ESTRUCTURAL',
              fontsize=14, fontweight='bold',
              color=COLORES['titulo'], pad=15)

txt7 = (
    "═══════════════════════════════════════════════════════════════════════════\n\n"
    f"  GEOMETRÍA:          LX = {LX_TOTAL:.2f} m | LY = {LY_TOTAL:.2f} m | Área = {AREA:.2f} m²\n"
    f"                      Columnas = {N_COL_TOTAL} | Sección = {B_COL*100:.0f}×{H_COL*100:.0f} cm | He = {He} m\n\n"
    f"  ELASTICIDAD:        E = 12600·√{fc} = {E_kgcm2:.0f} kg/cm² = {E_tm2:.0f} t/m²\n\n"
    f"  INERCIA:            I = 38⁴/12 = {I_col_cm4:.0f} cm⁴ = {I_col_m4:.8f} m⁴\n\n"
    f"  RIGIDEZ COLUMNA:    k_col = 12·E·I/He³ = {k_col:.2f} t/m\n\n"
    f"  RIGIDEZ PISO:       k_piso = {N_COL_TOTAL} × {k_col:.2f} = {k_piso:.0f} t/m\n\n"
    f"  PESO Y MASA:        W_piso = {W_piso:.2f} t | m_piso = {m_piso:.4f} t·s²/m\n\n"
    "═══════════════════════════════════════════════════════════════════════════"
)

ax7.text(0.5, 0.5, txt7, transform=ax7.transAxes,
         ha='center', va='center', fontsize=10, family='monospace',
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor='#eafaf1',
                   edgecolor='#27ae60',
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_Algoritmo_A_Paso_2"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"Algoritmo_A_Paso_2_modelo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("ALGORITMO A — PASO 2: MODELO ESTRUCTURAL")
print("=" * 80)
print(f"  Geometría:")
print(f"    LX       = {LX_TOTAL:.2f} m")
print(f"    LY       = {LY_TOTAL:.2f} m")
print(f"    Área     = {AREA:.2f} m²")
print(f"    Columnas = {N_COL_TOTAL}")
print(f"  Elasticidad:")
print(f"    E        = {E_kgcm2:.2f} kg/cm²")
print(f"  Inercia:")
print(f"    I        = {I_col_cm4:.2f} cm⁴")
print(f"  Rigidez columna:")
print(f"    k_col    = {k_col:.4f} t/m")
print(f"  Rigidez piso:")
print(f"    k_piso   = {k_piso:.4f} t/m")
print(f"  Peso y masa:")
print(f"    W_piso   = {W_piso:.4f} t")
print(f"    m_piso   = {m_piso:.6f} t·s²/m")
print("=" * 80)