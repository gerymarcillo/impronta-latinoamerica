# -*- coding: utf-8 -*-
"""
================================================================================
M07.30 — ANÁLISIS DE DERIVAS CON PÓRTICO Y DESPLAZAMIENTOS POR PISO
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.30 — Derivas por Piso

ESTRUCTURA DEL DASHBOARD:
    IZQUIERDA: Cuadro de resumen (simbología + datos)
    DERECHA:   Gráfica de pórtico con líneas de desplazamiento por piso

DATOS DEL PROYECTO:
    - T₁ = 0.389 s
    - Sa = 1.7100 g
    - R = 6.0
    - Ω₀ = 2.0
    - Sd = 6.434 cm
    - X diseño = 1.072 cm
    - xy = 2.144 cm
    - Cd = 4.50
    - X inelástica = 4.824 cm
    - He = 3.00 m
    - N pisos = 2
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'piso1': '#3498db',
    'piso2': '#e74c3c',
    'deriva': '#c0392b',
    'norma': '#8e44ad',
    'resultado': '#27ae60',
    'columna': '#2c3e50',
    'viga': '#7f8c8d',
    'desplazamiento': '#e67e22',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_alerta': '#fadbd8',
    'box_alerta_borde': '#c0392b',
    'box_simbologia': '#f4ecf7',
    'box_simbologia_borde': '#8e44ad',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

# Datos base
T1 = 0.389
Sa = 1.7100
R = 6.0
Omega_0 = 2.0
g = 9.81
omega1 = 2 * np.pi / T1

# Cálculos
Sd = (Sa / omega1**2) * 981
X_diseno = Sd / R
xy = X_diseno * Omega_0
Cd = 0.75 * R
X_inelastica = X_diseno * Cd

# Estructura
He = 3.00
N_PISOS = 2
H_total = N_PISOS * He

# Modos de vibración
phi1 = 0.235
phi2 = 1.000

# Desplazamientos por piso
X1 = X_inelastica * phi1
X2 = X_inelastica * phi2

# Derivas por piso
Deriva1 = X1 / He / 100
Deriva2 = X2 / He / 100
Deriva1_pct = Deriva1 * 100
Deriva2_pct = Deriva2 * 100
Deriva_max = max(Deriva1, Deriva2)
Deriva_max_pct = Deriva_max * 100

# Límite NEC-15
Limite_NEC = 0.02

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.30 — ANÁLISIS DE DERIVAS POR PISO',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Deriva máx = {Deriva_max_pct:.3f}% | He = {He} m',
         ha='center', va='top', fontsize=13,
         color=COLORES['subtitulo'], style='italic')

# GridSpec: 1 fila x 2 columnas
gs = GridSpec(1, 2, figure=fig,
              hspace=0.0, wspace=0.10,
              left=0.04, right=0.97,
              top=0.90, bottom=0.05,
              width_ratios=[1.0, 1.4])

# ============================================================================
# PANEL IZQUIERDO: CUADRO DE RESUMEN
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('RESUMEN DE SIMBOLOGÍA Y DATOS',
              fontsize=14, fontweight='bold',
              color=COLORES['titulo'], pad=15)

txt_resumen = (
    "═══════════════════════════════════════\n"
    "     SÍMBOLO         VALOR      UNIDAD\n"
    "═══════════════════════════════════════\n\n"
    "  DATOS SÍSMICOS:\n"
    f"    T₁             {T1:.4f}      s\n"
    f"    Sa(T₁)         {Sa:.4f}      g\n"
    f"    R              {R:.2f}        —\n"
    f"    Ω₀             {Omega_0:.2f}        —\n\n"
    "  DESPLAZAMIENTOS:\n"
    f"    Sd             {Sd:.3f}      cm\n"
    f"    X diseño       {X_diseno:.3f}      cm\n"
    f"    xy             {xy:.3f}      cm\n"
    f"    Cd             {Cd:.2f}        —\n"
    f"    X inelástica   {X_inelastica:.3f}      cm\n\n"
    "  ESTRUCTURA:\n"
    f"    He             {He:.2f}        m\n"
    f"    N pisos        {N_PISOS}           —\n"
    f"    H total        {H_total:.2f}        m\n\n"
    "  MODOS DE VIBRACIÓN:\n"
    f"    φ₁             {phi1:.3f}      —\n"
    f"    φ₂             {phi2:.3f}      —\n\n"
    "  DESPLAZAMIENTOS POR PISO:\n"
    f"    X₁             {X1:.3f}      cm\n"
    f"    X₂             {X2:.3f}      cm\n\n"
    "  DERIVAS POR PISO:\n"
    f"    Deriva₁        {Deriva1:.5f}    —\n"
    f"    Deriva₂        {Deriva2:.5f}    —\n"
    f"    Deriva₁ (%)    {Deriva1_pct:.3f}      %\n"
    f"    Deriva₂ (%)    {Deriva2_pct:.3f}      %\n"
    f"    Deriva máx     {Deriva_max_pct:.3f}      %\n\n"
    "═══════════════════════════════════════\n"
    "  LÍMITE NEC-15:  2.00 %\n"
    "  CLASIFICACIÓN:  Near collapse\n"
    "  ✅ CUMPLE NEC-15\n"
    "═══════════════════════════════════════"
)

ax1.text(0.5, 0.5, txt_resumen, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.8',
                   facecolor=COLORES['box_simbologia'],
                   edgecolor=COLORES['box_simbologia_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL DERECHO: GRÁFICA DEL PÓRTICO CON DESPLAZAMIENTOS
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_title('GRÁFICA DE DERIVAS — PÓRTICO CON DESPLAZAMIENTOS',
              fontsize=14, fontweight='bold',
              color=COLORES['titulo'], pad=15)

# --------------------------------------------------------------------------
# DIBUJAR EL PÓRTICO
# --------------------------------------------------------------------------

# Coordenadas del pórtico
x_izq = 0.0
x_der = 5.0
y_base = 0.0
y_piso1 = He
y_piso2 = 2 * He

# Fondo de la gráfica
ax2.set_facecolor('#ffffff')

# --- COLUMNAS ---
# Columna izquierda
ax2.plot([x_izq, x_izq], [y_base, y_piso1], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')
ax2.plot([x_izq, x_izq], [y_piso1, y_piso2], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')

# Columna derecha
ax2.plot([x_der, x_der], [y_base, y_piso1], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')
ax2.plot([x_der, x_der], [y_piso1, y_piso2], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')

# Columna central
x_centro = (x_izq + x_der) / 2
ax2.plot([x_centro, x_centro], [y_base, y_piso1], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')
ax2.plot([x_centro, x_centro], [y_piso1, y_piso2], '-',
         color=COLORES['columna'], linewidth=8, solid_capstyle='round')

# --- VIGAS ---
# Viga piso 1
ax2.plot([x_izq, x_der], [y_piso1, y_piso1], '-',
         color=COLORES['viga'], linewidth=10, solid_capstyle='round')

# Viga piso 2
ax2.plot([x_izq, x_der], [y_piso2, y_piso2], '-',
         color=COLORES['viga'], linewidth=10, solid_capstyle='round')

# --- BASE EMPOTRADA ---
ax2.plot([x_izq - 0.5, x_der + 0.5], [y_base, y_base], 'k-', linewidth=6)

# Símbolos de empotramiento
for x_emp in [x_izq, x_centro, x_der]:
    ax2.plot([x_emp - 0.3, x_emp, x_emp + 0.3],
             [y_base - 0.15, y_base, y_base - 0.15],
             'k-', linewidth=3)
    ax2.plot([x_emp - 0.3, x_emp + 0.3],
             [y_base - 0.15, y_base - 0.15],
             'k-', linewidth=3)

# --------------------------------------------------------------------------
# LÍNEAS DE DESPLAZAMIENTO POR PISO (DEFORMADA)
# --------------------------------------------------------------------------

# Escala visual de desplazamientos (amplificada para visualización)
escala = 0.15  # 1 cm = 0.15 unidades en la gráfica

# Desplazamiento piso 1
dx1 = X1 * escala
# Desplazamiento piso 2
dx2 = X2 * escala

# Línea de desplazamiento piso 1 (azul)
ax2.plot([x_izq + dx1, x_der + dx1], [y_piso1, y_piso1], '--',
         color=COLORES['piso1'], linewidth=3.5, alpha=0.9, zorder=5)

# Línea de desplazamiento piso 2 (rojo)
ax2.plot([x_izq + dx2, x_der + dx2], [y_piso2, y_piso2], '--',
         color=COLORES['piso2'], linewidth=3.5, alpha=0.9, zorder=5)

# Curva de deformada (línea suave)
z_curve = np.linspace(0, H_total, 50)
u_curve = np.interp(z_curve, [0, He, 2*He], [0, dx1, dx2])
ax2.plot(x_izq + u_curve, z_curve, '-', color=COLORES['desplazamiento'],
         linewidth=3, alpha=0.7, zorder=4)

# --------------------------------------------------------------------------
# FLECHAS DE DESPLAZAMIENTO
# --------------------------------------------------------------------------

# Flecha piso 1
ax2.annotate('', xy=(x_der + dx1, y_piso1), xytext=(x_der, y_piso1),
             arrowprops=dict(arrowstyle='->', color=COLORES['piso1'], lw=3))
ax2.text(x_der + dx1/2, y_piso1 + 0.15,
         f'X₁ = {X1:.3f} cm',
         ha='center', fontsize=11, fontweight='bold',
         color=COLORES['piso1'],
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor=COLORES['piso1'], linewidth=1.5))

# Flecha piso 2
ax2.annotate('', xy=(x_der + dx2, y_piso2), xytext=(x_der, y_piso2),
             arrowprops=dict(arrowstyle='->', color=COLORES['piso2'], lw=3))
ax2.text(x_der + dx2/2, y_piso2 + 0.15,
         f'X₂ = {X2:.3f} cm',
         ha='center', fontsize=11, fontweight='bold',
         color=COLORES['piso2'],
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor=COLORES['piso2'], linewidth=1.5))

# --------------------------------------------------------------------------
# ANOTACIONES DE DERIVAS
# --------------------------------------------------------------------------

# Deriva piso 1
ax2.text(x_der + 1.2, y_piso1,
         f'Deriva₁ = {Deriva1_pct:.3f}%',
         fontsize=11, fontweight='bold',
         color=COLORES['piso1'],
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor=COLORES['piso1'],
                   linewidth=2))

# Deriva piso 2
ax2.text(x_der + 1.2, y_piso2,
         f'Deriva₂ = {Deriva2_pct:.3f}%',
         fontsize=11, fontweight='bold',
         color=COLORES['piso2'],
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['piso2'],
                   linewidth=2))

# Deriva máxima
ax2.text(x_der + 1.2, (y_piso1 + y_piso2)/2,
         f'Deriva máx\n{Deriva_max_pct:.3f}%',
         fontsize=12, fontweight='bold',
         color=COLORES['deriva'],
         ha='center',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['deriva'],
                   linewidth=2.5))

# Límite NEC-15
ax2.text(x_der + 1.2, y_base + 0.5,
         f'Límite NEC-15\n2.00%',
         fontsize=11, fontweight='bold',
         color=COLORES['norma'],
         ha='center',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#f4ecf7',
                   edgecolor=COLORES['norma'],
                   linewidth=2))

# --------------------------------------------------------------------------
# COTAS DE ALTURA
# --------------------------------------------------------------------------

# Cota He (piso 1)
ax2.annotate('', xy=(x_izq - 0.8, 0), xytext=(x_izq - 0.8, y_piso1),
             arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax2.text(x_izq - 1.0, y_piso1/2, f'He = {He} m',
         fontsize=10, fontweight='bold',
         rotation=90, va='center', ha='center')

# Cota He (piso 2)
ax2.annotate('', xy=(x_izq - 0.8, y_piso1), xytext=(x_izq - 0.8, y_piso2),
             arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax2.text(x_izq - 1.0, (y_piso1 + y_piso2)/2, f'He = {He} m',
         fontsize=10, fontweight='bold',
         rotation=90, va='center', ha='center')

# Etiquetas de niveles
ax2.text(x_izq - 0.3, y_piso1, 'Piso 1',
         fontsize=10, fontweight='bold', ha='right', va='center')
ax2.text(x_izq - 0.3, y_piso2, 'Piso 2',
         fontsize=10, fontweight='bold', ha='right', va='center')
ax2.text(x_izq - 0.3, y_base, 'Base',
         fontsize=10, fontweight='bold', ha='right', va='center')

# --------------------------------------------------------------------------
# CONFIGURACIÓN DE EJES
# --------------------------------------------------------------------------

ax2.set_xlim(x_izq - 1.5, x_der + 3.5)
ax2.set_ylim(y_base - 0.8, y_piso2 + 1.0)
ax2.set_aspect('equal')
ax2.axis('off')

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_30"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_30_derivas_portico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.30 — ANÁLISIS DE DERIVAS POR PISO")
print("=" * 80)
print(f"\n  DATOS DEL PROYECTO:")
print(f"    T₁       = {T1} s")
print(f"    Sa(T₁)   = {Sa} g")
print(f"    Sd       = {Sd:.3f} cm")
print(f"    X diseño = {X_diseno:.3f} cm")
print(f"    xy       = {xy:.3f} cm")
print(f"    Cd       = {Cd}")
print(f"    X inel   = {X_inelastica:.3f} cm")
print(f"\n  DESPLAZAMIENTOS POR PISO:")
print(f"    X₁       = {X1:.3f} cm")
print(f"    X₂       = {X2:.3f} cm")
print(f"\n  DERIVAS POR PISO:")
print(f"    Deriva₁  = {Deriva1_pct:.3f} %")
print(f"    Deriva₂  = {Deriva2_pct:.3f} %")
print(f"    Máx      = {Deriva_max_pct:.3f} %")
print(f"\n  LÍMITE NEC-15 = {Limite_NEC*100:.2f} %")
print(f"  {'✅ CUMPLE' if Deriva_max <= Limite_NEC else '❌ NO CUMPLE'}")
print("=" * 80)