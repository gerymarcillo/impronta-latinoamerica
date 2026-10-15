# -*- coding: utf-8 -*-
"""
================================================================================
ALGORITMO A — PASOS 1 AL 5 (FASE 1: ENTRADA Y DESPLAZAMIENTOS BÁSICOS)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
ALGORITMO: A — Pasos 1 al 5

OBJETIVO: Dashboard didáctico de los 5 primeros pasos del análisis:
    PASO 1: Datos del proyecto
    PASO 2: Modelo estructural
    PASO 3: Análisis modal
    PASO 4: Espectro NEC-15
    PASO 5: Desplazamiento elástico Sd

DATOS DEL PROYECTO:
    - LUCES_X = [6.00, 5.50, 6.30]
    - LUCES_Y = [4.80, 5.50, 5.00, 6.10]
    - He = 3.00 m
    - fc = 210 kg/cm²
    - Cm = 0.62 t/m², Cv = 0.20 t/m²
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'paso1': '#3498db',
    'paso2': '#9b59b6',
    'paso3': '#e67e22',
    'paso4': '#e74c3c',
    'paso5': '#27ae60',
    'flecha': '#34495e',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'texto_claro': '#ffffff',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

# Paso 1: Datos
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

# Paso 2: Modelo
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
I_col_cm4 = (38**4) / 12
I_col_m4 = I_col_cm4 / 100**4
k_col = 12 * E_tm2 * I_col_m4 / He**3
k_piso = N_COL_TOTAL * k_col
W_piso = Cu * AREA
g = 9.81
m_piso = W_piso / g

# Paso 3: Modal
omega1 = np.sqrt((k_piso / m_piso) * (2 - np.sqrt(2)))
T1 = 2 * np.pi / omega1

# Paso 4: Espectro
eta = 1.80
Z = 0.50
Fa = 1.00
Fd = 1.60
Fs = 1.90
r = 1.00
Sa_max = eta * Z * Fa
T0 = 0.1 * Fs * Fd / Fa
Tc = 0.55 * Fs * Fd / Fa
Sa_T1 = Sa_max * Fs  # T0 < T1 < Tc → meseta

# Paso 5: Sd
Sd = (Sa_T1 / omega1**2) * 981

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 14))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.980,
         'ALGORITMO A — PASOS 1 AL 5',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         'FASE 1: ENTRADA Y DESPLAZAMIENTOS BÁSICOS',
         ha='center', va='top', fontsize=14,
         color=COLORES['subtitulo'], style='italic', fontweight='bold')

fig.text(0.5, 0.930,
         'UNESUM-REZ-2026-JIPIJAPA-001',
         ha='center', va='top', fontsize=11,
         color='#7f8c8d')

# GridSpec: 2 filas x 5 columnas
gs = GridSpec(2, 5, figure=fig,
              hspace=0.35, wspace=0.20,
              left=0.04, right=0.97,
              top=0.90, bottom=0.05,
              height_ratios=[1.0, 1.0])

# ============================================================================
# PASO 1: DATOS
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('PASO 1: DATOS',
              fontsize=12, fontweight='bold',
              color=COLORES['paso1'], pad=10)

txt1 = (
    "DATOS DEL PROYECTO\n"
    "══════════════════════\n\n"
    f"  LUCES_X = {LUCES_X}\n"
    f"  LUCES_Y = {LUCES_Y}\n\n"
    f"  LX = {LX_TOTAL:.2f} m\n"
    f"  LY = {LY_TOTAL:.2f} m\n"
    f"  Área = {AREA:.2f} m²\n\n"
    f"  He = {He:.2f} m\n"
    f"  fc = {fc} kg/cm²\n"
    f"  Cm = {Cm} t/m²\n"
    f"  Cv = {Cv} t/m²\n\n"
    f"  Cu = {Cu:.3f} t/m²"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#ebf5fb',
                   edgecolor=COLORES['paso1'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 2: MODELO
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
ax2.set_title('PASO 2: MODELO',
              fontsize=12, fontweight='bold',
              color=COLORES['paso2'], pad=10)

txt2 = (
    "MODELO ESTRUCTURAL\n"
    "══════════════════════\n\n"
    f"  N columnas = {N_COL_TOTAL}\n"
    f"  Sección = 38×38 cm\n\n"
    f"  E = 12600·√{fc}\n"
    f"  E = {E_kgcm2:.0f} kg/cm²\n\n"
    f"  I = 38⁴/12\n"
    f"  I = {I_col_cm4:.0f} cm⁴\n\n"
    f"  k_piso = {k_piso:.0f} t/m\n"
    f"  W_piso = {W_piso:.1f} t\n"
    f"  m_piso = {m_piso:.3f} t·s²/m"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#f4ecf7',
                   edgecolor=COLORES['paso2'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 3: MODAL
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
ax3.set_title('PASO 3: MODAL',
              fontsize=12, fontweight='bold',
              color=COLORES['paso3'], pad=10)

txt3 = (
    "ANÁLISIS MODAL\n"
    "══════════════════════\n\n"
    "  2 GDL\n\n"
    f"  k_piso = {k_piso:.0f} t/m\n"
    f"  m_piso = {m_piso:.3f} t·s²/m\n\n"
    "  ω₁ = √(k/m)(2-√2)\n"
    f"  ω₁ = {omega1:.3f} rad/s\n\n"
    "  T₁ = 2π/ω₁\n"
    f"  T₁ = {T1:.4f} s\n\n"
    "  f₁ = 1/T₁\n"
    f"  f₁ = {1/T1:.3f} Hz"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fef5e7',
                   edgecolor=COLORES['paso3'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 4: ESPECTRO
# ============================================================================

ax4 = fig.add_subplot(gs[0, 3])
ax4.axis('off')
ax4.set_title('PASO 4: ESPECTRO',
              fontsize=12, fontweight='bold',
              color=COLORES['paso4'], pad=10)

txt4 = (
    "ESPECTRO NEC-15\n"
    "══════════════════════\n\n"
    f"  η = {eta} (Costa)\n"
    f"  Z = {Z} (Zona VI)\n"
    f"  Fa = {Fa}, Fd = {Fd}\n"
    f"  Fs = {Fs}, r = {r}\n\n"
    f"  T0 = {T0:.4f} s\n"
    f"  Tc = {Tc:.4f} s\n\n"
    f"  T₁ = {T1:.4f} s\n"
    f"  T0 < T₁ < Tc → MESETA\n\n"
    f"  Sa(T₁) = {Sa_T1:.4f} g"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['paso4'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PASO 5: Sd
# ============================================================================

ax5 = fig.add_subplot(gs[0, 4])
ax5.axis('off')
ax5.set_title('PASO 5: Sd',
              fontsize=12, fontweight='bold',
              color=COLORES['paso5'], pad=10)

txt5 = (
    "DESPLAZAMIENTO ELÁSTICO\n"
    "══════════════════════\n\n"
    "  Sd = Sa·g/ω²\n\n"
    "  Sd = Sa/ω² × 981\n\n"
    f"  Sa = {Sa_T1:.4f} g\n"
    f"  ω₁ = {omega1:.3f} rad/s\n"
    f"  ω₁² = {omega1**2:.3f}\n\n"
    f"  Sd = {Sa_T1:.4f}/{omega1**2:.2f}\n"
    f"      × 981\n\n"
    f"  Sd = {Sd:.4f} cm"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['paso5'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# FLUJO DE PASOS (FILA INFERIOR)
# ============================================================================

ax6 = fig.add_subplot(gs[1, :])
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 2)
ax6.axis('off')

# Cajas del flujo
pasos_flujo = [
    (1.0, "PASO 1\nDatos", COLORES['paso1']),
    (3.0, "PASO 2\nModelo", COLORES['paso2']),
    (5.0, "PASO 3\nModal", COLORES['paso3']),
    (7.0, "PASO 4\nEspectro", COLORES['paso4']),
    (9.0, "PASO 5\nSd", COLORES['paso5']),
]

for x, texto, color in pasos_flujo:
    caja = FancyBboxPatch((x - 0.7, 0.5), 1.4, 1.0,
                           boxstyle="round,pad=0.1",
                           facecolor=color, edgecolor='black',
                           linewidth=2.5, zorder=2)
    ax6.add_patch(caja)
    ax6.text(x, 1.0, texto, ha='center', va='center',
             fontsize=10, fontweight='bold',
             color='white', zorder=3, family='monospace')

# Flechas
for i in range(len(pasos_flujo) - 1):
    x1 = pasos_flujo[i][0] + 0.7
    x2 = pasos_flujo[i+1][0] - 0.7
    flecha = FancyArrowPatch((x1, 1.0), (x2, 1.0),
                              arrowstyle='->', mutation_scale=25,
                              color=COLORES['flecha'],
                              linewidth=3, zorder=1)
    ax6.add_patch(flecha)

# Etiquetas
ax6.text(5.0, 0.1, 'SECUENCIA DE LOS PASOS 1 AL 5',
         ha='center', fontsize=11, fontweight='bold',
         color=COLORES['titulo'])

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_Algoritmo_A"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"Algoritmo_A_pasos_1_5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("ALGORITMO A — PASOS 1 AL 5 COMPLETADO")
print("=" * 80)
print(f"  PASO 1: Datos      → Área = {AREA:.2f} m²")
print(f"  PASO 2: Modelo     → k_piso = {k_piso:.0f} t/m")
print(f"  PASO 3: Modal      → T₁ = {T1:.4f} s")
print(f"  PASO 4: Espectro   → Sa(T₁) = {Sa_T1:.4f} g")
print(f"  PASO 5: Sd         → Sd = {Sd:.4f} cm")
print("=" * 80)