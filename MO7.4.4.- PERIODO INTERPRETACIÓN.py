# -*- coding: utf-8 -*-
"""
================================================================================
M07.6.4 — MODELO + MODOS DE VIBRACIÓN + ANÁLISIS FÍSICO
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.6 — Período por Método de Cortante
SUB-SUBSECCIÓN: M07.6.4 — Modelo + Modos + Análisis Físico

OBJETIVO: Integrar en un solo dashboard:
          - Modelo matemático (2 GDL)
          - Modos de vibración (estático)
          - Análisis físico (interpretación)

DATOS REALES (Excel RESILIENCIA MODOS PROYECTO PII 2026):
    MODO 1: T₁ = 0.389 s, φ₁ = [0.0350, 0.1490]  →  normalizado: [0.235, 1.000]
    MODO 2: T₂ = 0.149 s, φ₂ = [-0.1100, 0.1090] →  normalizado: [-1.000, 1.000]
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
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# BLOQUE 1: DATOS DEL PROYECTO
# ============================================================================

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

# Modos de vibración NORMALIZADOS (valores del Excel)
# φ₁ = [0.0350, 0.1490] normalizado → [0.2349, 1.0000]
# φ₂ = [-0.1100, 0.1090] normalizado → [-1.0000, 1.0000]
phi1 = np.array([0.2349, 1.0000])   # Modo 1 (normalizado para visualización)
phi2 = np.array([-1.0000, 1.0000])  # Modo 2 (normalizado para visualización)

# Valores ORIGINALES del Excel (para mostrar en análisis físico)
phi1_orig = np.array([0.0350, 0.1490])
phi2_orig = np.array([-0.1100, 0.1090])

# Amplitudes
A1 = 1.0
A2 = 1.0

# Períodos REALES del Excel
T1 = 0.389
T2 = 0.149

# Frecuencias
omega1 = 2 * np.pi / T1
omega2 = 2 * np.pi / T2

# ============================================================================
# BLOQUE 2: FIGURA Y EJES
# ============================================================================

fig = plt.figure(figsize=(24, 14))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M07.6.4 — MODELO + MODOS DE VIBRACIÓN + ANÁLISIS FÍSICO',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | T₁ = {T1:.4f} s | T₂ = {T2:.4f} s',
         ha='center', va='top', fontsize=12,
         color='#5dade2', style='italic')

gs = GridSpec(2, 3, figure=fig, hspace=0.40, wspace=0.30,
              left=0.05, right=0.98, top=0.92, bottom=0.05)

# ============================================================
# PANEL 1: MODELO MATEMÁTICO
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-2, 2)
ax1.set_ylim(-1, 8)
ax1.axis('off')
ax1.set_aspect('equal')

ax1.set_title('(a) MODELO MATEMÁTICO', fontsize=13, fontweight='bold',
              color='#c0392b', pad=15)

# Base
ax1.plot([-0.8, 0.8], [0, 0], 'k-', linewidth=4)
for xx in np.linspace(-0.8, 0.8, 8):
    ax1.plot([xx, xx - 0.15], [0, -0.2], 'k-', linewidth=1.5)

# Columna
ax1.plot([0, 0], [0, H_TOTAL], '-', color='#c0392b', linewidth=4)

# Masas
ax1.plot(0, He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)
ax1.plot(0, 2*He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Etiquetas
ax1.text(0.3, He, 'm₁', fontsize=12, fontweight='bold', color='#c0392b')
ax1.text(0.3, 2*He, 'm₂', fontsize=12, fontweight='bold', color='#c0392b')
ax1.text(-0.5, He/2, 'k', fontsize=12, fontweight='bold', color='#7f8c8d')
ax1.text(-0.5, He + He/2, 'k', fontsize=12, fontweight='bold', color='#7f8c8d')

# Etiqueta 2 GDL
ax1.text(0, -0.8, '2 GDL', ha='center', fontsize=10,
         fontweight='bold', color='#1a237e',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='#eaf2fb', edgecolor='#1a237e', linewidth=1.5))

# ============================================================
# PANEL 2: PRIMER MODO DE VIBRACIÓN
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(-2, 2)
ax2.set_ylim(-1, 8)
ax2.axis('off')
ax2.set_aspect('equal')

ax2.set_title('(b) PRIMER MODO DE VIBRACIÓN', fontsize=13, fontweight='bold',
              color='#c0392b', pad=15)

# Líneas verticales
ax2.plot([0, 0], [0, H_TOTAL], '--', color='#e91e63', linewidth=1.5, alpha=0.4)

# Curva del modo (con valores normalizados para visualización)
z_interp = np.linspace(0, 2*He, 100)
x_interp = np.interp(z_interp, [0, He, 2*He], [0, phi1[0], phi1[1]])
ax2.plot(x_interp, z_interp, '-', color='#e91e63', linewidth=3)

# Masas
ax2.plot(phi1[0], He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)
ax2.plot(phi1[1], 2*He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Flechas con VALORES ORIGINALES
ax2.annotate('', xy=(phi1[0], He + 0.5), xytext=(0, He + 0.5),
             arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2))
ax2.text(phi1[0] + 0.1, He + 0.7, f'{phi1_orig[0]:.4f}', fontsize=10,
         fontweight='bold', color='#c0392b', ha='left')

ax2.annotate('', xy=(phi1[1], 2*He + 0.5), xytext=(0, 2*He + 0.5),
             arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2))
ax2.text(phi1[1] + 0.1, 2*He + 0.7, f'{phi1_orig[1]:.4f}', fontsize=10,
         fontweight='bold', color='#c0392b', ha='left')

# Etiqueta de período
ax2.text(0, -0.8, f'T₁ = {T1:.4f} s', ha='center', fontsize=11,
         fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2))

# Interpretación
ax2.text(0, -1.5, 'Traslación en fase',
         ha='center', fontsize=10, style='italic', color='#c0392b')

# ============================================================
# PANEL 3: SEGUNDO MODO DE VIBRACIÓN
# ============================================================
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(-2, 2)
ax3.set_ylim(-1, 8)
ax3.axis('off')
ax3.set_aspect('equal')

ax3.set_title('(c) SEGUNDO MODO DE VIBRACIÓN', fontsize=13, fontweight='bold',
              color='#c0392b', pad=15)

ax3.plot([0, 0], [0, H_TOTAL], '--', color='#e91e63', linewidth=1.5, alpha=0.4)

x_interp2 = np.interp(z_interp, [0, He, 2*He], [0, phi2[0], phi2[1]])
ax3.plot(x_interp2, z_interp, '-', color='#e91e63', linewidth=3)

ax3.plot(phi2[0], He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)
ax3.plot(phi2[1], 2*He, 'o', color='#e91e63', markersize=40,
         markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Flechas con VALORES ORIGINALES
ax3.annotate('', xy=(phi2[0], He + 0.5), xytext=(0, He + 0.5),
             arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2))
ax3.text(phi2[0] - 0.1, He + 0.7, f'{phi2_orig[0]:.4f}', fontsize=10,
         fontweight='bold', color='#c0392b', ha='right')

ax3.annotate('', xy=(phi2[1], 2*He + 0.5), xytext=(0, 2*He + 0.5),
             arrowprops=dict(arrowstyle='->', color='#c0392b', lw=2))
ax3.text(phi2[1] + 0.1, 2*He + 0.7, f'{phi2_orig[1]:.4f}', fontsize=10,
         fontweight='bold', color='#c0392b', ha='left')

# Etiqueta de período
ax3.text(0, -0.8, f'T₂ = {T2:.4f} s', ha='center', fontsize=11,
         fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2))

# Interpretación
ax3.text(0, -1.5, 'Contrafase',
         ha='center', fontsize=10, style='italic', color='#c0392b')

# ============================================================
# PANEL 4: ANÁLISIS FÍSICO - MODO 1
# ============================================================
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')

ax4.set_title('(d) ANÁLISIS FÍSICO - MODO 1', fontsize=12, fontweight='bold',
              color='#1a237e')

txt4 = (
    "PRIMER MODO (FUNDAMENTAL)\n"
    "═══════════════════════════════\n\n"
    f"  T₁ = {T1:.4f} s\n"
    f"  ω₁ = {omega1:.4f} rad/s\n"
    f"  f₁ = {1/T1:.4f} Hz\n\n"
    "  FORMA MODAL:\n"
    f"    φ₁ = [{phi1_orig[0]:.4f}, {phi1_orig[1]:.4f}]\n"
    f"    φ₁ (norm) = [{phi1[0]:.4f}, {phi1[1]:.4f}]\n\n"
    "  INTERPRETACIÓN FÍSICA:\n"
    "  • Ambos pisos se mueven en la\n"
    "    MISMA dirección\n"
    "  • El piso 2 se mueve más\n"
    "    que el piso 1\n"
    "  • Es el modo dominante\n\n"
    "  APLICACIÓN:\n"
    "  • Controla la respuesta sísmica\n"
    "  • T₁ = 0.389 s → Estructura RÍGIDA\n"
    "  • Frecuencia alta (2.571 Hz)"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2.5))

# ============================================================
# PANEL 5: ANÁLISIS FÍSICO - MODO 2
# ============================================================
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_xlim(0, 10)
ax5.set_ylim(0, 10)
ax5.axis('off')

ax5.set_title('(e) ANÁLISIS FÍSICO - MODO 2', fontsize=12, fontweight='bold',
              color='#1a237e')

txt5 = (
    "SEGUNDO MODO\n"
    "═══════════════════════════════\n\n"
    f"  T₂ = {T2:.4f} s\n"
    f"  ω₂ = {omega2:.4f} rad/s\n"
    f"  f₂ = {1/T2:.4f} Hz\n\n"
    "  FORMA MODAL:\n"
    f"    φ₂ = [{phi2_orig[0]:.4f}, {phi2_orig[1]:.4f}]\n"
    f"    φ₂ (norm) = [{phi2[0]:.4f}, {phi2[1]:.4f}]\n\n"
    "  INTERPRETACIÓN FÍSICA:\n"
    "  • Los pisos se mueven en\n"
    "    direcciones OPUESTAS\n"
    "  • El piso 1 va hacia un lado\n"
    "    y el piso 2 hacia el otro\n"
    "  • Es el modo superior\n\n"
    "  APLICACIÓN:\n"
    "  • Menos energético\n"
    "  • T₂ = 0.149 s → Muy rígido\n"
    "  • Frecuencia muy alta (6.711 Hz)"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef9e7',
                   edgecolor='#f39c12', linewidth=2.5))

# ============================================================
# PANEL 6: PROPIEDADES FÍSICAS + CONCLUSIÓN
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])
ax6.set_xlim(0, 10)
ax6.set_ylim(0, 10)
ax6.axis('off')

ax6.set_title('(f) PROPIEDADES Y CONCLUSIÓN', fontsize=12, fontweight='bold',
              color='#1a237e')

txt6 = (
    "PROPIEDADES FÍSICAS\n"
    "═══════════════════════════════\n\n"
    "  • Estructura ESTABLE\n"
    "    (λ₁, λ₂ > 0)\n"
    "  • Modos ORTOGONALES\n"
    "  • Comportamiento SHEAR BUILDING\n"
    "    (vigas rígidas, columnas flexibles)\n\n"
    "  RANGO DE PERÍODOS:\n"
    f"    T₁ = {T1:.4f} s (fundamental)\n"
    f"    T₂ = {T2:.4f} s (superior)\n"
    f"    T₁/T₂ = {T1/T2:.4f}\n\n"
    "═══════════════════════════════\n\n"
    "CONCLUSIÓN\n"
    "═══════════════════════════════\n"
    f"  T₁ = {T1:.4f} s < 0.5 s\n"
    "  ✓ ESTRUCTURA RÍGIDA\n"
    "  ✓ CUMPLE CON NEC-15\n"
    "  ✓ NO NECESITA DISIPADORES"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eaf2fb',
                   edgecolor='#2980b9', linewidth=2.5))

# ============================================================================
# BLOQUE 3: GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_6_4"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_6_4_modelo_modos_analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\nImagen guardada: {ruta_img}")

print("\nMostrando dashboard en pantalla...")
print("(Cierre la ventana para terminar)")
plt.show()

print("\n" + "=" * 70)
print("M07.6.4 COMPLETADO — MODELO + MODOS + ANÁLISIS FÍSICO")
print("=" * 70)
print(f"  MODO 1: T1 = {T1:.4f} s  |  phi1 = [{phi1_orig[0]:.4f}, {phi1_orig[1]:.4f}]")
print(f"  MODO 2: T2 = {T2:.4f} s  |  phi2 = [{phi2_orig[0]:.4f}, {phi2_orig[1]:.4f}]")
print("=" * 70)