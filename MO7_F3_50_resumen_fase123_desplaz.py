# -*- coding: utf-8 -*-
"""
================================================================================
M07.28 — PARTE 1: CONSTRUCCIÓN DE LA CURVA DE PUSHOVER (PASO A PASO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.28 — Curva de Pushover Paso a Paso

OBJETIVO: Construir la curva de Pushover paso a paso, mostrando
          cómo cada parámetro contribuye a la curva final.

NORMAS APLICADAS:
    - SEAOC Blue Book (2009)
    - ATC-40 (1996)
    - FEMA 273 / 356
    - ASCE/SEI 7-10 (2010)
    - NEC-15 (2015)

DATOS DEL PROYECTO:
    - T₁ = 0.389 s
    - Sa(T₁) = 1.7100 g
    - R = 6.0
    - Ω₀ = 2.0
    - m = 41.314 t·s²/m
    - Sd = 6.434 cm
    - X diseño = 1.072 cm
    - xy = 2.144 cm
    - Cd = 4.50
    - X inelástica = 4.824 cm
    - Fy = 231.02 t
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
    'curva': '#111111',
    'fy': '#c0392b',
    'eje': '#c0392b',
    'xy': '#c0392b',
    'xdis': '#c0392b',
    'xelast': '#7f8c8d',
    'inelast': '#e67e22',
    'texto': '#1a1a1a',
    'resultado': '#27ae60',
    'resultado_borde': '#1e8449',
    'norma': '#8e44ad',
    'autor': '#2c3e50',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

T1 = 0.389
omega1 = 16.147
Sa = 1.7100
R = 6.0
Omega_0 = 2.0
m = 41.314
g = 9.81

# Cálculos
Fy = m * Sa * g * Omega_0 / R
Sd = (Sa / omega1**2) * 981
X_diseno = Sd / R
xy = X_diseno * Omega_0
Cd = 0.75 * R
X_inelastica = X_diseno * Cd
K = Fy / xy

# Rango
Delta_max = 8.0

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 16))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.980,
         'M07.28 — PARTE 1: CONSTRUCCIÓN DE LA CURVA DE PUSHOVER',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo Elastoplástico — Paso a Paso',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.35, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.5, 1.0])

# ============================================================================
# PANEL (a): CURVA DE PUSHOVER COMPLETA
# ============================================================================

ax1 = fig.add_subplot(gs[0, :])

# Curva
delta_elast = np.linspace(0, xy, 100)
V_elast = K * delta_elast
delta_plast = np.linspace(xy, Delta_max, 100)
V_plast = np.full_like(delta_plast, Fy)

ax1.plot(delta_elast, V_elast, '-', color=COLORES['curva'],
         linewidth=10, solid_capstyle='round', zorder=3)
ax1.plot(delta_plast, V_plast, '-', color=COLORES['curva'],
         linewidth=10, solid_capstyle='round', zorder=3)

# Ejes rojos
ax1.annotate('', xy=(0, Fy * 1.15), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color=COLORES['eje'],
                             lw=3, mutation_scale=35))
ax1.annotate('', xy=(Delta_max * 1.05, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle='->', color=COLORES['eje'],
                             lw=3, mutation_scale=35))

# Puntos
ax1.plot(0, 0, 'o', color=COLORES['curva'], markersize=12, zorder=5)
ax1.text(-0.3, -0.2, 'A', fontsize=20, fontweight='bold', color='#1a1a1a',
         ha='right', va='top')

ax1.plot(xy, Fy, 'o', color=COLORES['curva'], markersize=12, zorder=5)
ax1.text(xy - 0.3, Fy + 0.05, 'B', fontsize=20, fontweight='bold',
         color='#1a1a1a', ha='right', va='bottom')

ax1.plot(Delta_max, Fy, 'o', color=COLORES['curva'], markersize=12, zorder=5)
ax1.text(Delta_max + 0.1, Fy + 0.05, 'C', fontsize=20, fontweight='bold',
         color='#1a1a1a', ha='left', va='bottom')

# Líneas guía
ax1.axhline(y=Fy, color=COLORES['fy'], linestyle='-',
            linewidth=2, alpha=0.6, zorder=1)
ax1.axvline(x=X_diseno, color=COLORES['xdis'], linestyle='--',
            linewidth=2, alpha=0.7, zorder=1)
ax1.axvline(x=xy, color=COLORES['xy'], linestyle='--',
            linewidth=2, alpha=0.7, zorder=1)
ax1.axvline(x=Sd, color=COLORES['xelast'], linestyle=':',
            linewidth=2, alpha=0.7, zorder=1)

# Anotaciones
ax1.annotate(f'Fy = {Fy:.2f} t',
             xy=(0.3, Fy), xytext=(0.8, Fy + 0.05),
             fontsize=13, fontweight='bold', color=COLORES['fy'],
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor=COLORES['fy'], linewidth=2))

ax1.annotate(f'X diseño = {X_diseno:.3f} cm',
             xy=(X_diseno, 0), xytext=(X_diseno, -0.12),
             fontsize=12, fontweight='bold', color=COLORES['xdis'],
             ha='center', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=COLORES['xdis'], linewidth=1.5))

ax1.annotate(f'xy = {xy:.3f} cm',
             xy=(xy, 0), xytext=(xy, -0.12),
             fontsize=12, fontweight='bold', color=COLORES['xy'],
             ha='center', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=COLORES['xy'], linewidth=1.5))

ax1.annotate(f'x elástica = {Sd:.3f} cm',
             xy=(Sd, 0), xytext=(Sd, -0.12),
             fontsize=11, fontweight='bold', color=COLORES['xelast'],
             ha='center', va='top',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=COLORES['xelast'], linewidth=1.5))

# Ω en el diagrama
ax1.annotate('', xy=(X_diseno, Fy * 0.35), xytext=(xy, Fy * 0.35),
             arrowprops=dict(arrowstyle='<->', color='#c0392b', lw=2.5))
ax1.text((X_diseno + xy) / 2, Fy * 0.38, 'Ω₀',
         fontsize=14, fontweight='bold', color='#c0392b', ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor='#c0392b', linewidth=1.5))

# Cd en el diagrama
ax1.annotate('', xy=(X_inelastica, Fy * 0.55), xytext=(X_diseno, Fy * 0.55),
             arrowprops=dict(arrowstyle='<->', color=COLORES['inelast'], lw=2.5))
ax1.text((X_diseno + X_inelastica) / 2, Fy * 0.58, 'Cd = 4.50',
         fontsize=13, fontweight='bold', color=COLORES['inelast'], ha='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef5e7',
                   edgecolor=COLORES['inelast'], linewidth=1.5))

# Etiqueta de la meseta
ax1.text(xy + 1.5, Fy * 1.05, 'Luego pierde rigidez\n(Comportamiento inelástico)',
         fontsize=11, fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fadbd8',
                   edgecolor='#c0392b', linewidth=1.5))

# Fórmula
ax1.text(Delta_max * 0.70, Fy * 1.15,
         r'$Fy = \frac{m \cdot a \cdot g \cdot \Omega_0}{R}$',
         fontsize=15, fontweight='bold', color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor='#c0392b', linewidth=2))

ax1.set_xlim(-0.5, Delta_max * 1.1)
ax1.set_ylim(-0.25, Fy * 1.30)
ax1.set_xlabel('Desplazamiento Δ (cm)', fontsize=13, fontweight='bold',
               color='#c0392b')
ax1.set_ylabel('Cortante V (t)', fontsize=13, fontweight='bold',
               color='#c0392b')
ax1.grid(True, linestyle='--', alpha=0.2)
ax1.tick_params(axis='both', labelsize=11)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_linewidth(2)
ax1.spines['bottom'].set_linewidth(2)

# ============================================================================
# PANEL (b): PASO 1 — Fy
# ============================================================================

ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')
ax2.set_title('PASO 1: Fy (SEAOC Blue Book)',
              fontsize=12, fontweight='bold', color=COLORES['fy'])

txt2 = (
    "FUERZA DE FLUENCIA\n"
    "═══════════════════════════════\n\n"
    "  Fy = m·a·g·Ω₀/R\n\n"
    f"  m = {m} t·s²/m\n"
    f"  a = {Sa} g\n"
    f"  g = {g} m/s²\n"
    f"  Ω₀ = {Omega_0}\n"
    f"  R = {R}\n\n"
    f"  Fy = {Fy:.2f} t\n\n"
    "═══════════════════════════════\n"
    "  NORMA: SEAOC Blue Book\n"
    "  AUTOR: Seismology Committee"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['fy'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): PASO 2 — Ω₀
# ============================================================================

ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')
ax3.set_title('PASO 2: Ω₀ (Sobrerresistencia)',
              fontsize=12, fontweight='bold', color=COLORES['inelast'])

txt3 = (
    "FACTOR DE SOBRERRESISTENCIA\n"
    "═══════════════════════════════\n\n"
    "  Ω₀ = 2.0 (hormigón)\n\n"
    f"  xy = X diseño × Ω₀\n"
    f"  xy = {X_diseno:.3f} × {Omega_0}\n"
    f"  xy = {xy:.3f} cm\n\n"
    "═══════════════════════════════\n\n"
    "  NORMA: ASCE/SEI 7-10\n"
    "  AUTOR: Seismology Committee\n"
    "  Referencia: SEAOC Blue Book"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fef5e7',
                   edgecolor=COLORES['inelast'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): PASO 3 — Cd
# ============================================================================

ax4 = fig.add_subplot(gs[1, 2])
ax4.axis('off')
ax4.set_title('PASO 3: Cd (NEC-15)',
              fontsize=12, fontweight='bold', color=COLORES['resultado'])

txt4 = (
    "FACTOR DE AMPLIFICACIÓN\n"
    "═══════════════════════════════\n\n"
    "  Cd = 0.75 × R\n\n"
    f"  Cd = 0.75 × {R}\n"
    f"  Cd = {Cd}\n\n"
    f"  X inel = X dis × Cd\n"
    f"  X inel = {X_inelastica:.3f} cm\n\n"
    "═══════════════════════════════\n\n"
    "  NORMA: NEC-15 (Ecuador)\n"
    "  AUTOR: MIDUVI"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['resultado'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_28"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_28_parte1_pushover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.28 — PARTE 1: CONSTRUCCIÓN DE LA CURVA DE PUSHOVER")
print("=" * 80)
print(f"  Fy           = {Fy:.2f} t")
print(f"  X diseño     = {X_diseno:.3f} cm")
print(f"  xy           = {xy:.3f} cm")
print(f"  Cd           = {Cd}")
print(f"  X inelástica = {X_inelastica:.3f} cm")
print("=" * 80)