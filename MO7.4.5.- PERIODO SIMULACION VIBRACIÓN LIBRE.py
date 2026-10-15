# -*- coding: utf-8 -*-
"""
================================================================================
SIMULACIÓN DE VIBRACIÓN LIBRE CON SINUSOIDE - DOS MODOS
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
OBJETIVO: Animar la vibración libre de la estructura en sus dos modos,
          mostrando el sinusoide de la respuesta en el tiempo

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
    from matplotlib.animation import FuncAnimation
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
phi1 = np.array([0.2349, 1.0000])   # Modo 1 (normalizado)
phi2 = np.array([-1.0000, 1.0000])  # Modo 2 (normalizado)

# Amplitudes para visualización
A1 = 1.0
A2 = 1.0

# Períodos REALES del Excel
T1 = 0.389
T2 = 0.149

# Frecuencias angulares
omega1 = 2 * np.pi / T1
omega2 = 2 * np.pi / T2

# ============================================================================
# BLOQUE 2: FIGURA Y EJES
# ============================================================================

fig = plt.figure(figsize=(22, 12))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.975,
         'SIMULACIÓN DE VIBRACIÓN LIBRE CON SINUSOIDE',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | T₁ = {T1:.4f} s | T₂ = {T2:.4f} s',
         ha='center', va='top', fontsize=12,
         color='#5dade2', style='italic')

gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.20,
              left=0.05, right=0.98, top=0.88, bottom=0.06)

# ============================================================
# PANEL 1: MODO 1 - ESTRUCTURA (ANIMACIÓN)
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-2, 2)
ax1.set_ylim(-1, 8)
ax1.axis('off')
ax1.set_aspect('equal')

ax1.set_title('MODO 1 - ESTRUCTURA', fontsize=13, fontweight='bold',
              color='#c0392b', pad=10)

# Base empotrada
ax1.plot([-0.8, 0.8], [0, 0], 'k-', linewidth=4)
for xx in np.linspace(-0.8, 0.8, 8):
    ax1.plot([xx, xx - 0.15], [0, -0.2], 'k-', linewidth=1.5)

# Líneas verticales de referencia
ax1.plot([0, 0], [0, H_TOTAL], '--', color='#e91e63',
         linewidth=1.5, alpha=0.4)

# Curva de deformada
linea1, = ax1.plot([], [], '-', color='#e91e63', linewidth=3)

# Masas
masa1_p1, = ax1.plot([], [], 'o', color='#e91e63', markersize=35,
                      markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)
masa1_p2, = ax1.plot([], [], 'o', color='#e91e63', markersize=35,
                      markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Texto de tiempo
texto1 = ax1.text(0, 7.5, '', ha='center', fontsize=11,
                   fontweight='bold', color='#c0392b',
                   bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='#fff9c4', edgecolor='#f9a825', linewidth=1.5))

# Etiqueta de período
ax1.text(0, -0.8, f'T₁ = {T1:.4f} s', ha='center', fontsize=10,
         fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2))

# ============================================================
# PANEL 2: MODO 1 - SINUSOIDE (ANIMACIÓN)
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

t_max = 4 * T1  # 4 períodos
t_sweep = np.linspace(0, t_max, 2000)
u1_sweep = A1 * np.cos(omega1 * t_sweep) * phi1[1]

ax2.plot(t_sweep, u1_sweep, '-', color='#e91e63', linewidth=2, alpha=0.3,
         label='Modo 1 (Piso 2)')

# Punto que se mueve
punto1, = ax2.plot([], [], 'o', color='#e91e63', markersize=15,
                    markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Línea vertical de tiempo actual
linea_tiempo1 = ax2.axvline(x=0, color='#c0392b', linestyle='--', linewidth=2)

# Línea horizontal de referencia
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

ax2.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Desplazamiento (u)', fontsize=11, fontweight='bold')
ax2.set_title('MODO 1 - SINUSOIDE', fontsize=13, fontweight='bold',
              color='#c0392b', pad=10)
ax2.legend(fontsize=9, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.set_xlim(0, t_max)
ax2.set_ylim(-1.5, 1.5)

# ============================================================
# PANEL 3: MODO 2 - ESTRUCTURA (ANIMACIÓN)
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_xlim(-2, 2)
ax3.set_ylim(-1, 8)
ax3.axis('off')
ax3.set_aspect('equal')

ax3.set_title('MODO 2 - ESTRUCTURA', fontsize=13, fontweight='bold',
              color='#c0392b', pad=10)

# Base empotrada
ax3.plot([-0.8, 0.8], [0, 0], 'k-', linewidth=4)
for xx in np.linspace(-0.8, 0.8, 8):
    ax3.plot([xx, xx - 0.15], [0, -0.2], 'k-', linewidth=1.5)

# Líneas verticales de referencia
ax3.plot([0, 0], [0, H_TOTAL], '--', color='#e91e63',
         linewidth=1.5, alpha=0.4)

# Curva de deformada
linea2, = ax3.plot([], [], '-', color='#e91e63', linewidth=3)

# Masas
masa2_p1, = ax3.plot([], [], 'o', color='#e91e63', markersize=35,
                      markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)
masa2_p2, = ax3.plot([], [], 'o', color='#e91e63', markersize=35,
                      markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Texto de tiempo
texto2 = ax3.text(0, 7.5, '', ha='center', fontsize=11,
                   fontweight='bold', color='#c0392b',
                   bbox=dict(boxstyle='round,pad=0.3',
                             facecolor='#fff9c4', edgecolor='#f9a825', linewidth=1.5))

# Etiqueta de período
ax3.text(0, -0.8, f'T₂ = {T2:.4f} s', ha='center', fontsize=10,
         fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='#fff9c4', edgecolor='#f9a825', linewidth=2))

# ============================================================
# PANEL 4: MODO 2 - SINUSOIDE (ANIMACIÓN)
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])

t_max2 = 4 * T2  # 4 períodos
t_sweep2 = np.linspace(0, t_max2, 2000)
u2_sweep = A2 * np.cos(omega2 * t_sweep2) * phi2[1]

ax4.plot(t_sweep2, u2_sweep, '-', color='#e91e63', linewidth=2, alpha=0.3,
         label='Modo 2 (Piso 2)')

# Punto que se mueve
punto2, = ax4.plot([], [], 'o', color='#e91e63', markersize=15,
                    markeredgecolor='#880e4f', markeredgewidth=2, zorder=10)

# Línea vertical de tiempo actual
linea_tiempo2 = ax4.axvline(x=0, color='#c0392b', linestyle='--', linewidth=2)

# Línea horizontal de referencia
ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

ax4.set_xlabel('Tiempo (s)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Desplazamiento (u)', fontsize=11, fontweight='bold')
ax4.set_title('MODO 2 - SINUSOIDE', fontsize=13, fontweight='bold',
              color='#c0392b', pad=10)
ax4.legend(fontsize=9, loc='upper right')
ax4.grid(True, linestyle='--', alpha=0.3)
ax4.set_xlim(0, t_max2)
ax4.set_ylim(-1.5, 1.5)

# ============================================================
# FUNCIÓN DE ANIMACIÓN
# ============================================================

def animar(frame):
    t = frame * 0.01  # tiempo de simulación

    # --- MODO 1 ---
    u1_p1 = A1 * np.cos(omega1 * t) * phi1[0]
    u1_p2 = A1 * np.cos(omega1 * t) * phi1[1]

    # Curva suave
    z_curve = np.linspace(0, H_TOTAL, 50)
    u_curve1 = np.interp(z_curve, [0, He, 2*He], [0, u1_p1, u1_p2])

    linea1.set_data(u_curve1, z_curve)
    masa1_p1.set_data([u1_p1], [He])
    masa1_p2.set_data([u1_p2], [2*He])
    texto1.set_text(f't = {t:.2f} s')

    # Punto en el sinusoide (módulo del período)
    t_mod1 = t % t_max
    u1_actual = A1 * np.cos(omega1 * t_mod1) * phi1[1]
    punto1.set_data([t_mod1], [u1_actual])
    linea_tiempo1.set_xdata([t_mod1, t_mod1])

    # --- MODO 2 ---
    u2_p1 = A2 * np.cos(omega2 * t) * phi2[0]
    u2_p2 = A2 * np.cos(omega2 * t) * phi2[1]

    # Curva suave
    u_curve2 = np.interp(z_curve, [0, He, 2*He], [0, u2_p1, u2_p2])

    linea2.set_data(u_curve2, z_curve)
    masa2_p1.set_data([u2_p1], [He])
    masa2_p2.set_data([u2_p2], [2*He])
    texto2.set_text(f't = {t:.2f} s')

    # Punto en el sinusoide (módulo del período)
    t_mod2 = t % t_max2
    u2_actual = A2 * np.cos(omega2 * t_mod2) * phi2[1]
    punto2.set_data([t_mod2], [u2_actual])
    linea_tiempo2.set_xdata([t_mod2, t_mod2])

    return (linea1, masa1_p1, masa1_p2, texto1, punto1, linea_tiempo1,
            linea2, masa2_p1, masa2_p2, texto2, punto2, linea_tiempo2)

# ============================================================================
# CREAR ANIMACIÓN
# ============================================================================

anim = FuncAnimation(fig, animar, frames=2000,
                      interval=20, blit=True, repeat=True)

# ============================================================================
# GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_6_3"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

print("=" * 80)
print("SIMULACIÓN DE VIBRACIÓN LIBRE CON SINUSOIDE")
print("=" * 80)

print(f"""
  MODO 1:
    T₁ = {T1:.4f} s
    ω₁ = {omega1:.4f} rad/s
    φ₁ = [{phi1[0]:.4f}, {phi1[1]:.4f}] (normalizado)
    Amplitud = {A1}

  MODO 2:
    T₂ = {T2:.4f} s
    ω₂ = {omega2:.4f} rad/s
    φ₂ = [{phi2[0]:.4f}, {phi2[1]:.4f}] (normalizado)
    Amplitud = {A2}
""")

print("=" * 80)

print("\nMostrando animación en pantalla...")
print("(Cierre la ventana para terminar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)