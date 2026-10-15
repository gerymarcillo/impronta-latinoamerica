# -*- coding: utf-8 -*-
"""
================================================================================
M02 — MATRIZ DE MASA DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
OBJETIVO: Cálculo paso a paso de la masa del modelo base (38×38 cm)

NOTA METODOLÓGICA:
    El Excel PROYECTO.xlsx usa Cu = 1.2Cm + 1.6Cv como peso reactivo,
    en lugar del W sísmico NEC-15 (W = Cm + %Cv·Cv).
    Este criterio conservador se mantiene para coherencia con el Excel.

MÉTODO: Shear building
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
    from matplotlib.patches import FancyBboxPatch
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. DATOS DEL PROYECTO (CONFIRMADOS)
# ============================================================================

A = 17.80           # m (LX_TOTAL)
B = 21.40           # m (LY_TOTAL)
N_PISOS = 2
He = 3.00           # m

Cm = 0.62           # t/m²
Cv = 0.20           # t/m²
pct_cv = 0          # %

g = 9.81            # m/s²

# ============================================================================
# 2. CÁLCULOS PASO A PASO
# ============================================================================

print("=" * 80)
print("M02 — MATRIZ DE MASA DEL PROYECTO PRINCIPAL")
print("=" * 80)

# Paso 1: Área
Area = A * B
print(f"\n  PASO 1: Area = A × B = {A} × {B} = {Area:.2f} m²")

# Paso 2: Carga última (criterio Excel)
Cu = 1.2 * Cm + 1.6 * Cv
print(f"\n  PASO 2: Cu = 1.2×{Cm} + 1.6×{Cv} = {Cu:.4f} t/m²")

# Paso 3: Peso reactivo por piso
W_piso = Cu * Area
print(f"\n  PASO 3: W_piso = Cu × Area = {Cu:.4f} × {Area:.2f} = {W_piso:.2f} t")

# Paso 4: Peso reactivo total
W_total = N_PISOS * W_piso
print(f"\n  PASO 4: W_total = {N_PISOS} × {W_piso:.2f} = {W_total:.2f} t")

# Paso 5: Masa por piso
m_piso = W_piso / g
print(f"\n  PASO 5: m_piso = W_piso / g = {W_piso:.2f} / {g} = {m_piso:.4f} t·s²/m")

# Paso 6: Masa total
m_total = N_PISOS * m_piso
print(f"\n  PASO 6: m_total = {N_PISOS} × {m_piso:.4f} = {m_total:.4f} t·s²/m")

# Paso 7: Matriz de masa
M_matriz = np.array([[m_piso, 0],
                      [0, m_piso]])
print(f"\n  PASO 7: Matriz M = diag({m_piso:.4f}, {m_piso:.4f}) t·s²/m")

print("\n" + "=" * 80)

# ============================================================================
# 3. FIGURA PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(22, 13))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.975,
         'M02 — MATRIZ DE MASA DEL PROYECTO PRINCIPAL',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo base 38×38 cm | m_piso = {m_piso:.4f} t·s²/m',
         ha='center', va='top', fontsize=12,
         color='#5dade2', style='italic')

gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.30,
              left=0.05, right=0.98, top=0.88, bottom=0.06)

# ============================================================================
# PANEL (a): PASOS
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
ax1.set_title('(a) PASOS DEL CÁLCULO', fontsize=12, fontweight='bold', color='#1a237e')

pasos = (
    "PASO 1: DATOS\n"
    f"  A = {A} m\n"
    f"  B = {B} m\n"
    f"  N_pisos = {N_PISOS}\n"
    f"  Cm = {Cm} t/m²\n"
    f"  Cv = {Cv} t/m²\n\n"
    "PASO 2: CU\n"
    f"  Cu = {Cu:.4f} t/m²\n\n"
    "PASO 3: W_piso\n"
    f"  W_piso = {W_piso:.2f} t\n\n"
    "PASO 4: W_total\n"
    f"  W_total = {W_total:.2f} t\n\n"
    "PASO 5: m_piso\n"
    f"  m_piso = {m_piso:.4f}\n"
    "           t·s²/m\n\n"
    "PASO 6: m_total\n"
    f"  m_total = {m_total:.4f}\n"
    "            t·s²/m"
)

ax1.text(0.5, 0.5, pasos, transform=ax1.transAxes,
         ha='center', va='center', fontsize=8, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf2fb',
                   edgecolor='#2980b9', linewidth=2.5))

# ============================================================================
# PANEL (b): MATRIZ DE MASA
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
ax2.set_title('(b) MATRIZ DE MASA', fontsize=12, fontweight='bold', color='#1a237e')

matriz_txt = (
    "MATRIZ DE MASA M (2×2)\n"
    "═══════════════════════════════\n\n"
    f"  M = [[{m_piso:.4f}, 0.0000]\n"
    f"       [0.0000, {m_piso:.4f}]]\n\n"
    "═══════════════════════════════\n\n"
    "  Unidades: t·s²/m\n\n"
    "═══════════════════════════════\n\n"
    "FÓRMULA:\n"
    "  M = diag(m, m)\n\n"
    "  m = masa por piso\n"
    "  (misma masa en los 2 pisos)"
)

ax2.text(0.5, 0.5, matriz_txt, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2.5))

# ============================================================================
# PANEL (c): NOTA METODOLÓGICA
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(0, 10); ax3.set_ylim(0, 10); ax3.axis('off')
ax3.set_title('(c) NOTA METODOLÓGICA', fontsize=12, fontweight='bold', color='#1a237e')

nota_txt = (
    "CRITERIO DEL PESO REACTIVO\n"
    "═══════════════════════════════\n\n"
    "El Excel PROYECTO.xlsx usa:\n\n"
    "  W = Cu = 1.2Cm + 1.6Cv\n\n"
    "como peso reactivo, en lugar\n"
    "del W sísmico NEC-15:\n\n"
    "  W_NEC = Cm + %Cv·Cv\n\n"
    "═══════════════════════════════\n\n"
    "Este criterio conservador\n"
    "se mantiene para coherencia\n"
    "con el Excel del proyecto."
)

ax3.text(0.5, 0.5, nota_txt, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef9e7',
                   edgecolor='#f39c12', linewidth=2.5))

# ============================================================================
# PANEL (d): MODELO CON MASAS CONCENTRADAS (3D simplificado)
# ============================================================================

ax4 = fig.add_subplot(gs[1, :2])
ax4.set_xlim(-2, 22); ax4.set_ylim(-2, 12); ax4.axis('off')

# Columnas
for x in [2, 8, 14, 20]:
    ax4.plot([x, x], [2, 10], '-', color='#2c3e50', linewidth=4)

# Losas
ax4.plot([2, 20], [5, 5], '-', color='#7f8c8d', linewidth=3)
ax4.plot([2, 20], [10, 10], '-', color='#7f8c8d', linewidth=3)

# Masas concentradas
ax4.plot(11, 5.5, 'o', color='#e74c3c', markersize=22,
         markeredgecolor='black', markeredgewidth=2)
ax4.plot(11, 10.5, 'o', color='#e74c3c', markersize=22,
         markeredgecolor='black', markeredgewidth=2)

ax4.text(13, 5.5, f'm1 = {m_piso:.4f} t·s²/m',
         fontsize=11, fontweight='bold', color='#922b21')
ax4.text(13, 10.5, f'm2 = {m_piso:.4f} t·s²/m',
         fontsize=11, fontweight='bold', color='#922b21')

ax4.set_title('(d) MODELO CON MASAS CONCENTRADAS POR PISO',
              fontsize=12, fontweight='bold', color='#1a237e')

# ============================================================================
# PANEL (e): RESUMEN
# ============================================================================

ax5 = fig.add_subplot(gs[1, 2])
ax5.set_xlim(0, 10); ax5.set_ylim(0, 10); ax5.axis('off')
ax5.set_title('(e) RESUMEN', fontsize=12, fontweight='bold', color='#1a237e')

conclusion = (
    "RESULTADOS\n"
    "═══════════════════════════════\n\n"
    f"  Area     = {Area:.2f} m²\n"
    f"  Cu       = {Cu:.4f} t/m²\n"
    f"  W_piso   = {W_piso:.2f} t\n"
    f"  W_total  = {W_total:.2f} t\n"
    f"  m_piso   = {m_piso:.4f} t·s²/m\n"
    f"  m_total  = {m_total:.4f} t·s²/m\n\n"
    "═══════════════════════════════\n\n"
    "MATRIZ DE MASA:\n\n"
    f"  M = [[{m_piso:.4f}, 0.0000]\n"
    f"       [0.0000, {m_piso:.4f}]]\n\n"
    "═══════════════════════════════\n"
    "  Unidades: t·s²/m"
)

ax5.text(0.5, 0.5, conclusion, transform=ax5.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2.5))

# ============================================================================
# MENSAJES OPORTUNOS (FLOTANTES EN ESQUINAS)
# ============================================================================

# --- Mensaje 1: Referencia (esquina superior izquierda, fuera de los paneles) ---
msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Excel PROYECTO.xlsx\n"
    "  Celda F4 = 405.30 t\n"
    "  Celda F5 = 413.15\n"
    "  Modelo base 38×38 cm"
)

fig.text(0.015, 0.880, msg1,
         transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#f4ecf7',
                   edgecolor='#8e44ad',
                   linewidth=1.5))

# --- Mensaje 2: Método (esquina superior derecha, fuera de los paneles) ---
msg2 = (
    "MÉTODO\n"
    "═══════════════════════════\n"
    "  Shear building\n"
    "  Masa concentrada por piso\n"
    "  M = diag(m, m)"
)

fig.text(0.985, 0.880, msg2,
         transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#eaf2fb',
                   edgecolor='#2980b9',
                   linewidth=1.5))

# ============================================================================
# 4. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M02"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M02_matriz_masa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\nImagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 70)
print("M02 COMPLETADO — MATRIZ DE MASA DEL PROYECTO PRINCIPAL")
print("=" * 70)
print(f"  Area     = {Area:.2f} m²")
print(f"  Cu       = {Cu:.4f} t/m²")
print(f"  W_piso   = {W_piso:.2f} t")
print(f"  W_total  = {W_total:.2f} t")
print(f"  m_piso   = {m_piso:.4f} t·s²/m")
print(f"  m_total  = {m_total:.4f} t·s²/m")
print("=" * 70)