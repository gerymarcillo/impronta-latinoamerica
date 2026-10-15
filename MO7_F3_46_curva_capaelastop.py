# -*- coding: utf-8 -*-
"""
================================================================================
M07.26 — CURVA DE CAPACIDAD (MODELO ELASTOPLÁSTICO) — CON RESULTADOS
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.26 — Curva de Capacidad

FÓRMULA CORREGIDA:
    Fy = m · a · g · Ω / R

DATOS DEL PROYECTO:
    - Sa = 1.7100 g
    - m = 41.314 t·s²/m
    - Ω = 2.0
    - R = 6.0
    - g = 9.81 m/s²
    - Fy = 231.02 t
    - X diseño = 1.072 cm
    - XY = 2.144 cm
    - Sd = 6.434 cm
    - K = 107.75 t/cm
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'curva': '#111111',
    'fy': '#c0392b',
    'eje': '#c0392b',
    'xy': '#c0392b',
    'xdis': '#c0392b',
    'xelast': '#7f8c8d',
    'texto': '#1a1a1a',
    'resultado': '#27ae60',
    'resultado_borde': '#1e8449',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

Sa = 1.7100          # g
m = 41.314           # t·s²/m
Omega = 2.0
R = 6.0
g = 9.81             # m/s²

# Fórmula corregida
Fy = m * Sa * g * Omega / R   # t

# Desplazamientos
X_diseno = 1.072     # cm
XY = X_diseno * Omega  # cm
Sd = 6.434           # cm
X_inelastica = X_diseno * (0.75 * R)  # cm

# Rigidez
K = Fy / XY          # t/cm

# Deriva
Deriva = X_inelastica / 300 * 100  # %

# Rango
Delta_max = 8.0      # cm

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(18, 11))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.965,
         'MODELO ELASTOPLÁSTICO — CURVA DE CAPACIDAD',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color='#1a1a1a', style='italic')

fig.text(0.5, 0.930,
         'UNESUM-REZ-2026-JIPIJAPA-001',
         ha='center', va='top', fontsize=12,
         color='#7f8c8d', style='italic')

ax = fig.add_axes([0.08, 0.10, 0.60, 0.78])
ax.set_facecolor('#ffffff')

# ============================================================================
# CURVA ELASTOPLÁSTICA
# ============================================================================

# Fase elástica (A → B)
delta_elast = np.linspace(0, XY, 100)
V_elast = K * delta_elast

# Fase plástica (B → C)
delta_plast = np.linspace(XY, Delta_max, 100)
V_plast = np.full_like(delta_plast, Fy)

# Curva
ax.plot(delta_elast, V_elast, '-', color=COLORES['curva'],
        linewidth=12, solid_capstyle='round', zorder=3)
ax.plot(delta_plast, V_plast, '-', color=COLORES['curva'],
        linewidth=12, solid_capstyle='round', zorder=3)

# ============================================================================
# EJES ROJOS
# ============================================================================

ax.annotate('', xy=(0, Fy * 1.15), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=COLORES['eje'],
                            lw=4, mutation_scale=40))
ax.text(-0.4, Fy * 0.55, 'Fy\n(t)', fontsize=16, fontweight='bold',
        color=COLORES['fy'], ha='right', va='center')

ax.annotate('', xy=(Delta_max * 1.05, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color=COLORES['eje'],
                            lw=4, mutation_scale=40))

# ============================================================================
# PUNTOS CLAVE
# ============================================================================

ax.plot(0, 0, 'o', color=COLORES['curva'], markersize=15, zorder=5)
ax.text(-0.3, -0.2, 'A', fontsize=22, fontweight='bold',
        color='#1a1a1a', ha='right', va='top')

ax.plot(XY, Fy, 'o', color=COLORES['curva'], markersize=15, zorder=5)
ax.text(XY - 0.3, Fy + 0.1, 'B', fontsize=22, fontweight='bold',
        color='#1a1a1a', ha='right', va='bottom')

ax.plot(Delta_max, Fy, 'o', color=COLORES['curva'], markersize=15, zorder=5)
ax.text(Delta_max + 0.1, Fy + 0.1, 'C', fontsize=22, fontweight='bold',
        color='#1a1a1a', ha='left', va='bottom')

# ============================================================================
# LÍNEAS GUÍA
# ============================================================================

ax.axhline(y=Fy, color=COLORES['fy'], linestyle='-',
           linewidth=2, alpha=0.6, zorder=1)
ax.axvline(x=X_diseno, color=COLORES['xdis'], linestyle='--',
           linewidth=2, alpha=0.7, zorder=1)
ax.axvline(x=XY, color=COLORES['xy'], linestyle='--',
           linewidth=2, alpha=0.7, zorder=1)
ax.axvline(x=Sd, color=COLORES['xelast'], linestyle=':',
           linewidth=2, alpha=0.7, zorder=1)

# ============================================================================
# ANOTACIONES EN LA CURVA
# ============================================================================

# Fy
ax.annotate(f'Fy = {Fy:.2f} t',
            xy=(0.3, Fy),
            xytext=(0.8, Fy + 0.05),
            fontsize=14, fontweight='bold',
            color=COLORES['fy'],
            bbox=dict(boxstyle='round,pad=0.4',
                      facecolor='white',
                      edgecolor=COLORES['fy'],
                      linewidth=2))

# X diseño
ax.annotate(f'X diseño\n{X_diseno:.3f} cm',
            xy=(X_diseno, 0),
            xytext=(X_diseno, -0.12),
            fontsize=12, fontweight='bold',
            color=COLORES['xdis'],
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='white',
                      edgecolor=COLORES['xdis'],
                      linewidth=1.5))

# XY
ax.annotate(f'XY\n{XY:.3f} cm',
            xy=(XY, 0),
            xytext=(XY, -0.12),
            fontsize=12, fontweight='bold',
            color=COLORES['xy'],
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='white',
                      edgecolor=COLORES['xy'],
                      linewidth=1.5))

# Deformación de fluencia
ax.annotate('',
            xy=(XY + 0.15, Fy),
            xytext=(XY + 0.15, 0),
            arrowprops=dict(arrowstyle='<->',
                            color=COLORES['xy'], lw=2))
ax.text(XY + 0.35, Fy / 2, 'deformación\nde fluencia',
        fontsize=10, fontweight='bold',
        color=COLORES['xy'], rotation=90,
        va='center', ha='left')

# Ω
ax.annotate('',
            xy=(X_diseno, Fy * 0.35),
            xytext=(XY, Fy * 0.35),
            arrowprops=dict(arrowstyle='<->',
                            color='#c0392b', lw=2.5))
ax.text((X_diseno + XY) / 2, Fy * 0.38, 'Ω',
        fontsize=16, fontweight='bold',
        color='#c0392b', ha='center',
        bbox=dict(boxstyle='round,pad=0.3',
                  facecolor='white',
                  edgecolor='#c0392b',
                  linewidth=1.5))

# Luego pierde rigidez
ax.text(XY + 0.4, Fy * 1.06, 'Luego pierde rigidez',
        fontsize=11, fontweight='bold',
        color='#c0392b',
        bbox=dict(boxstyle='round,pad=0.3',
                  facecolor='#fadbd8',
                  edgecolor='#c0392b',
                  linewidth=1.5))

# x elástica
ax.annotate(f'x elástica\n{Sd:.3f} cm',
            xy=(Sd, 0),
            xytext=(Sd, -0.12),
            fontsize=11, fontweight='bold',
            color=COLORES['xelast'],
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.3',
                      facecolor='white',
                      edgecolor=COLORES['xelast'],
                      linewidth=1.5))

# ============================================================================
# CONFIGURACIÓN DE EJES
# ============================================================================

ax.set_xlim(-0.5, Delta_max * 1.1)
ax.set_ylim(-0.25, Fy * 1.25)
ax.set_xlabel('Desplazamiento Δ (cm)', fontsize=13, fontweight='bold',
              color='#c0392b')
ax.set_ylabel('Cortante V (t)', fontsize=13, fontweight='bold',
              color='#c0392b')
ax.grid(True, linestyle='--', alpha=0.2)
ax.tick_params(axis='both', labelsize=11)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

# ============================================================================
# PANEL DE RESULTADOS (LADO DERECHO)
# ============================================================================

resultados_txt = (
    "═══════════════════════════════\n"
    "   RESULTADOS DEL ANÁLISIS\n"
    "═══════════════════════════════\n\n"
    "  DATOS DE ENTRADA:\n"
    f"    Sa       = {Sa} g\n"
    f"    m        = {m} t·s²/m\n"
    f"    Ω        = {Omega}\n"
    f"    R        = {R}\n"
    f"    g        = {g} m/s²\n\n"
    "  ─────────────────────────────\n\n"
    "  RESULTADOS:\n"
    f"    Fy       = {Fy:.2f} t\n"
    f"    K        = {K:.2f} t/cm\n\n"
    "  ─────────────────────────────\n\n"
    "  DESPLAZAMIENTOS:\n"
    f"    X diseño = {X_diseno:.3f} cm\n"
    f"    XY       = {XY:.3f} cm\n"
    f"    Sd       = {Sd:.3f} cm\n"
    f"    X inel   = {X_inelastica:.3f} cm\n\n"
    "  ─────────────────────────────\n\n"
    "  VERIFICACIÓN:\n"
    f"    Deriva   = {Deriva:.3f} %\n"
    f"    Límite   = 2.00 %\n"
    f"    Cumple   = ✅ SÍ\n\n"
    "═══════════════════════════════"
)

fig.text(0.72, 0.50, resultados_txt,
         transform=fig.transFigure,
         fontsize=10, family='monospace',
         ha='left', va='center',
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor='#eafaf1',
                   edgecolor=COLORES['resultado_borde'],
                   linewidth=2.5))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_26"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_26_curva_capacidad_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.26 — CURVA DE CAPACIDAD CON RESULTADOS")
print("=" * 80)
print(f"\n  DATOS DE ENTRADA:")
print(f"    Sa       = {Sa} g")
print(f"    m        = {m} t·s²/m")
print(f"    Ω        = {Omega}")
print(f"    R        = {R}")
print(f"    g        = {g} m/s²")
print(f"\n  RESULTADOS:")
print(f"    Fy       = {Fy:.2f} t")
print(f"    K        = {K:.2f} t/cm")
print(f"\n  DESPLAZAMIENTOS:")
print(f"    X diseño = {X_diseno:.3f} cm")
print(f"    XY       = {XY:.3f} cm")
print(f"    Sd       = {Sd:.3f} cm")
print(f"    X inel   = {X_inelastica:.3f} cm")
print(f"\n  VERIFICACIÓN:")
print(f"    Deriva   = {Deriva:.3f} %")
print(f"    Límite   = 2.00 %")
print(f"    Cumple   = {'✅ SÍ' if Deriva <= 2.0 else '❌ NO'}")
print("=" * 80)