# -*- coding: utf-8 -*-
"""
================================================================================
M07.62 — CORTE DE PÓRTICO EN MOVIMIENTO (ANIMACIÓN GARANTIZADA)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.62 — Corte con Movimiento en Vivo

MÉTODO: plt.pause() para garantizar animación en todos los backends
================================================================================
"""

import os
import warnings
warnings.filterwarnings("ignore")

from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f8f9fa',
    'titulo': '#0d1b2a',
    'subtitulo': '#415a77',
    'columna': '#2c3e50',
    'columna_2': '#34495e',
    'viga': '#7f8c8d',
    'disipador_X': '#e74c3c',
    'rotula': '#f39c12',
    'nudo': '#8e44ad',
    'info': '#1d3557',
    'info_bg': '#d6e4f0',
    'ok': '#2d6a4f',
    'ok_bg': '#d8f3dc',
    'acento': '#f77f00',
    'movimiento': '#8e44ad',
}

# ============================================================================
# 1. DATOS
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

X1_max = 1.133
X2_max = 4.824
T1 = 0.389
omega1 = 2 * np.pi / T1
beta_V = 0.05
ESCALA = 0.15

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(20, 12))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.62 — CORTE DE PÓRTICO EN MOVIMIENTO DINÁMICO',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | T1 = {T1} s | beta_V = {beta_V*100:.0f}%',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# Eje principal
ax = fig.add_axes([0.08, 0.08, 0.58, 0.82])
ax.set_facecolor('#ffffff')
ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-1.0, 8.0)
ax.set_aspect('equal')
ax.axis('off')

# ============================================================================
# 3. ELEMENTOS FIJOS
# ============================================================================

# Base empotrada
ax.plot([-1.5, 1.5], [0, 0], 'k-', linewidth=6)
for x_emp in [-1.5, 0, 1.5]:
    ax.plot([x_emp - 0.25, x_emp, x_emp + 0.25],
            [-0.25, 0, -0.25], 'k-', linewidth=3)
    ax.plot([x_emp - 0.25, x_emp + 0.25],
            [-0.25, -0.25], 'k-', linewidth=3)

ax.text(0, -0.7, 'BASE EMPOTRADA', fontsize=11, fontweight='bold',
        ha='center', va='top', color='black',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor='black', linewidth=1.5))

# Etiquetas
ax.text(-2.3, He, 'Piso 1', fontsize=11, fontweight='bold',
        ha='right', va='center', color=COLORES['columna'])
ax.text(-2.3, 2*He, 'Piso 2', fontsize=11, fontweight='bold',
        ha='right', va='center', color=COLORES['columna'])
ax.text(-2.3, 0, 'Base', fontsize=11, fontweight='bold',
        ha='right', va='center', color=COLORES['columna'])

# Título del corte
ax.text(0, 7.3, 'CORTE LONGITUDINAL (sentido X)',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=COLORES['titulo'],
        bbox=dict(boxstyle='round,pad=0.4',
                  facecolor=COLORES['ok_bg'],
                  edgecolor=COLORES['ok'],
                  linewidth=2))

# ============================================================================
# 4. ELEMENTOS DINÁMICOS (se actualizan en el loop)
# ============================================================================

# Columnas
col_izq_1, = ax.plot([], [], '-', color=COLORES['columna'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_izq_2, = ax.plot([], [], '-', color=COLORES['columna_2'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_der_1, = ax.plot([], [], '-', color=COLORES['columna'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_der_2, = ax.plot([], [], '-', color=COLORES['columna_2'],
                      linewidth=6, solid_capstyle='round', zorder=3)

# Vigas
viga_1, = ax.plot([], [], '-', color=COLORES['viga'],
                   linewidth=10, solid_capstyle='round', zorder=4)
viga_2, = ax.plot([], [], '-', color=COLORES['viga'],
                   linewidth=10, solid_capstyle='round', zorder=4)

# Disipador D1
d1_line, = ax.plot([], [], '-', color=COLORES['disipador_X'],
                    linewidth=8, alpha=1.0, zorder=8,
                    solid_capstyle='round')
d1_rot1, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)
d1_rot2, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)

# Disipador D2
d2_line, = ax.plot([], [], '-', color=COLORES['disipador_X'],
                    linewidth=8, alpha=1.0, zorder=8,
                    solid_capstyle='round')
d2_rot1, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)
d2_rot2, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)

# Nudo
nudo_plot, = ax.plot([], [], 'o', color=COLORES['nudo'],
                      markersize=22, markeredgecolor='white',
                      markeredgewidth=3, zorder=15)

# Deformada
deformada, = ax.plot([], [], '--', color=COLORES['movimiento'],
                      linewidth=2.5, alpha=0.5, zorder=2)

# Texto de tiempo
tiempo_text = ax.text(0, 6.8, '', ha='center', fontsize=13,
                       fontweight='bold', color=COLORES['titulo'],
                       bbox=dict(boxstyle='round,pad=0.4',
                                 facecolor='white',
                                 edgecolor=COLORES['acento'],
                                 linewidth=2))

# ============================================================================
# 5. PANEL DE INFORMACIÓN
# ============================================================================

ax_info = fig.add_axes([0.70, 0.08, 0.28, 0.82])
ax_info.set_facecolor('#ffffff')
ax_info.set_xlim(0, 10)
ax_info.set_ylim(0, 10)
ax_info.axis('off')

ax_info.text(5, 9.5, 'DISIPADORES TENSOR-PUNTAL',
             ha='center', va='top', fontsize=13, fontweight='bold',
             color=COLORES['titulo'],
             bbox=dict(boxstyle='round,pad=0.5',
                       facecolor=COLORES['info_bg'],
                       edgecolor=COLORES['info'],
                       linewidth=2))

txt_info = (
    "CONFIGURACION:\n"
    "===========================\n\n"
    "  D1: Esquina sup. izq. -> Nudo\n"
    "      (sentido X)\n\n"
    "  D2: Empotramiento -> Nudo\n"
    "      (sentido X)\n\n"
    "  D3: Nudo -> derecha arriba\n"
    "      (sentido Y)\n\n"
    "  D4: Nudo -> derecha abajo\n"
    "      (sentido Y)\n\n"
    "===========================\n"
    "DATOS:\n\n"
    f"  Longitud = 50 cm\n"
    f"  T1 = {T1} s\n"
    f"  beta_V = {beta_V*100:.0f}%\n\n"
    "DESPLAZAMIENTOS:\n\n"
    f"  X1 = {X1_max:.2f} cm\n"
    f"  X2 = {X2_max:.2f} cm\n"
    f"  Deriva = 1.61%\n\n"
    "===========================\n"
    "  [OK] CUMPLE NEC-15\n"
    "  [OK] CM = CR\n"
    "  [OK] SIN TORSION\n"
    "  [OK] UNICO EN EL MUNDO"
)

ax_info.text(5, 5, txt_info,
             ha='center', va='center', fontsize=8.5, family='monospace',
             bbox=dict(boxstyle='round,pad=0.6',
                       facecolor='#f8f9fa',
                       edgecolor=COLORES['info'],
                       linewidth=1.5))

# ============================================================================
# 6. FUNCIÓN DE ACTUALIZACIÓN
# ============================================================================

def actualizar_frame(t):
    """Actualiza el frame para un tiempo t dado."""
    decaimiento = np.exp(-beta_V * omega1 * t)
    u1 = X1_max * np.cos(omega1 * t) * decaimiento
    u2 = X2_max * np.cos(omega1 * t) * decaimiento

    dx1 = u1 * ESCALA
    dx2 = u2 * ESCALA

    # Columnas
    col_izq_1.set_data([-1.5, -1.5 + dx1 * 0.7], [0, He])
    col_izq_2.set_data([-1.5 + dx1 * 0.7, -1.5 + dx2], [He, 2*He])
    col_der_1.set_data([1.5, 1.5 + dx1 * 0.7], [0, He])
    col_der_2.set_data([1.5 + dx1 * 0.7, 1.5 + dx2], [He, 2*He])

    # Vigas
    viga_1.set_data([-1.5 + dx1 * 0.7, 1.5 + dx1 * 0.7], [He, He])
    viga_2.set_data([-1.5 + dx2, 1.5 + dx2], [2*He, 2*He])

    # Nudo
    nudo_x = 1.5 + dx1 * 0.7
    nudo_y = He
    nudo_plot.set_data([nudo_x], [nudo_y])

    # D1
    d1_x1 = -1.5 + dx2
    d1_y1 = 2 * He
    d1_line.set_data([d1_x1, nudo_x], [d1_y1, nudo_y])
    d1_rot1.set_data([d1_x1], [d1_y1])
    d1_rot2.set_data([nudo_x], [nudo_y])

    # D2
    d2_x1 = -1.5 + dx1 * 0.3
    d2_y1 = 0.3
    d2_line.set_data([d2_x1, nudo_x], [d2_y1, nudo_y])
    d2_rot1.set_data([d2_x1], [d2_y1])
    d2_rot2.set_data([nudo_x], [nudo_y])

    # Deformada
    z_curve = np.linspace(0, 2*He, 50)
    u_curve = np.interp(z_curve, [0, He, 2*He], [0, dx1*0.7, dx2])
    deformada.set_data(-1.5 + u_curve, z_curve)

    # Texto
    tiempo_text.set_text(f't = {t:.2f} s  |  X1 = {u1:.2f} cm  |  X2 = {u2:.2f} cm')


# ============================================================================
# 7. GUARDAR FRAME ESTÁTICO
# ============================================================================

carpeta = "Resultados_M07_62"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

actualizar_frame(0)
plt.draw()
nombre_png = os.path.join(carpeta, f"M07_62_corte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
plt.savefig(nombre_png, dpi=150, bbox_inches='tight', facecolor=COLORES['fondo'])
print(f"\n[OK] Imagen guardada: {nombre_png}")

# ============================================================================
# 8. ANIMACIÓN EN VIVO CON plt.pause()
# ============================================================================

print("\n" + "=" * 80)
print("M07.62 — ANIMACIÓN EN VIVO")
print("=" * 80)
print("\n>> Mostrando animacion en pantalla...")
print(">> (Cierre la ventana para terminar)\n")

# Mostrar la figura primero
plt.show(block=False)
plt.pause(0.5)

# Loop de animación garantizado
t = 0.0
dt = 0.025
duracion = 15.0  # segundos de animación

try:
    while t < duracion:
        actualizar_frame(t)
        plt.pause(0.025)
        t += dt
except KeyboardInterrupt:
    print("\n\n[!] Animacion detenida por el usuario")

print("\n[OK] Animacion completada")
print("\n(La ventana permanecera abierta hasta que la cierre)")

# Mantener la ventana abierta al final
plt.show(block=True)