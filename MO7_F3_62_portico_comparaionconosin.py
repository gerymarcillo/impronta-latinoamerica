# -*- coding: utf-8 -*-
"""
================================================================================
M07.63 — CORTE DE PÓRTICO CON TABLA COMPARATIVA DE GANANCIA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.63 — Corte con Tabla Comparativa

OBJETIVO: Mostrar el corte del pórtico con disipadores y una tabla
          comparativa que demuestre la GANANCIA en:
          - Período
          - Aceleración
          - Desplazamiento
          - Características del disipador viscoso

SIN SÍMBOLO CENTRAL
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
    'sin_disipador': '#95a5a6',
    'con_disipador': '#27ae60',
    'mejora': '#2980b9',
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

# === DATOS COMPARATIVOS (SIN vs CON disipador) ===
# SIN disipador (β = 5%)
T1_sin = 0.389           # s
Sa_sin = 1.710            # g
Sd_sin = 6.434           # cm
X1_sin = 1.133           # cm
X2_sin = 4.824           # cm
Deriva_sin = 1.608       # %

# CON disipador (β = 10%)
T1_con = 0.389           # s (igual, el disipador no cambia T)
Sa_con = 0.8085          # g (reducido por amortiguamiento)
Sd_con = 3.042           # cm (reducido)
X1_con = 0.536           # cm (reducido)
X2_con = 2.281           # cm (reducido)
Deriva_con = 0.760       # %

# GANANCIA
ganancia_Sa = (1 - Sa_con / Sa_sin) * 100      # %
ganancia_Sd = (1 - Sd_con / Sd_sin) * 100      # %
ganancia_X1 = (1 - X1_con / X1_sin) * 100      # %
ganancia_X2 = (1 - X2_con / X2_sin) * 100      # %
ganancia_Deriva = (1 - Deriva_con / Deriva_sin) * 100  # %

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.975,
         'M07.63 — CORTE DE PÓRTICO CON TABLA COMPARATIVA DE GANANCIA',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | T1 = {T1} s | beta_V = {beta_V*100:.0f}%',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# 3. EJE PRINCIPAL — CORTE DEL PÓRTICO
# ============================================================================

ax = fig.add_axes([0.05, 0.08, 0.40, 0.82])
ax.set_facecolor('#ffffff')
ax.set_xlim(-3.0, 3.0)
ax.set_ylim(-1.0, 8.0)
ax.set_aspect('equal')
ax.axis('off')

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
ax.text(0, 7.3, 'CORTE LONGITUDINAL',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=COLORES['titulo'],
        bbox=dict(boxstyle='round,pad=0.4',
                  facecolor=COLORES['ok_bg'],
                  edgecolor=COLORES['ok'],
                  linewidth=2))

# === ELEMENTOS DINÁMICOS ===
col_izq_1, = ax.plot([], [], '-', color=COLORES['columna'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_izq_2, = ax.plot([], [], '-', color=COLORES['columna_2'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_der_1, = ax.plot([], [], '-', color=COLORES['columna'],
                      linewidth=6, solid_capstyle='round', zorder=3)
col_der_2, = ax.plot([], [], '-', color=COLORES['columna_2'],
                      linewidth=6, solid_capstyle='round', zorder=3)

viga_1, = ax.plot([], [], '-', color=COLORES['viga'],
                   linewidth=10, solid_capstyle='round', zorder=4)
viga_2, = ax.plot([], [], '-', color=COLORES['viga'],
                   linewidth=10, solid_capstyle='round', zorder=4)

d1_line, = ax.plot([], [], '-', color=COLORES['disipador_X'],
                    linewidth=8, alpha=1.0, zorder=8, solid_capstyle='round')
d1_rot1, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)
d1_rot2, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)

d2_line, = ax.plot([], [], '-', color=COLORES['disipador_X'],
                    linewidth=8, alpha=1.0, zorder=8, solid_capstyle='round')
d2_rot1, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)
d2_rot2, = ax.plot([], [], 'o', color=COLORES['rotula'],
                    markersize=14, markeredgecolor='#922b21',
                    markeredgewidth=2, zorder=12)

nudo_plot, = ax.plot([], [], 'o', color=COLORES['nudo'],
                      markersize=22, markeredgecolor='white',
                      markeredgewidth=3, zorder=15)

deformada, = ax.plot([], [], '--', color=COLORES['movimiento'],
                      linewidth=2.5, alpha=0.5, zorder=2)

tiempo_text = ax.text(0, 6.8, '', ha='center', fontsize=12,
                       fontweight='bold', color=COLORES['titulo'],
                       bbox=dict(boxstyle='round,pad=0.4',
                                 facecolor='white',
                                 edgecolor=COLORES['acento'],
                                 linewidth=2))

# ============================================================================
# 4. TABLA COMPARATIVA (REEMPLAZA EL SÍMBOLO CENTRAL)
# ============================================================================

ax_tabla = fig.add_axes([0.48, 0.08, 0.50, 0.82])
ax_tabla.set_facecolor('#ffffff')
ax_tabla.set_xlim(0, 10)
ax_tabla.set_ylim(0, 10)
ax_tabla.axis('off')

# Título de la tabla
ax_tabla.text(5, 9.6, 'TABLA COMPARATIVA DE GANANCIA',
              ha='center', va='top', fontsize=14, fontweight='bold',
              color=COLORES['titulo'],
              bbox=dict(boxstyle='round,pad=0.5',
                        facecolor=COLORES['info_bg'],
                        edgecolor=COLORES['info'],
                        linewidth=2))

# === Encabezados ===
y_header = 8.9
ax_tabla.text(1.0, y_header, 'PARÁMETRO',
              ha='center', va='center', fontsize=10, fontweight='bold',
              color='white',
              bbox=dict(boxstyle='round,pad=0.3',
                        facecolor=COLORES['titulo'],
                        edgecolor='black', linewidth=1.5))

ax_tabla.text(3.5, y_header, 'SIN DISIPADOR',
              ha='center', va='center', fontsize=10, fontweight='bold',
              color='white',
              bbox=dict(boxstyle='round,pad=0.3',
                        facecolor=COLORES['sin_disipador'],
                        edgecolor='black', linewidth=1.5))

ax_tabla.text(6.0, y_header, 'CON DISIPADOR',
              ha='center', va='center', fontsize=10, fontweight='bold',
              color='white',
              bbox=dict(boxstyle='round,pad=0.3',
                        facecolor=COLORES['con_disipador'],
                        edgecolor='black', linewidth=1.5))

ax_tabla.text(8.5, y_header, 'GANANCIA',
              ha='center', va='center', fontsize=10, fontweight='bold',
              color='white',
              bbox=dict(boxstyle='round,pad=0.3',
                        facecolor=COLORES['mejora'],
                        edgecolor='black', linewidth=1.5))

# === Línea separadora ===
ax_tabla.plot([0.2, 9.8], [8.5, 8.5], '-',
              color=COLORES['titulo'], linewidth=2)

# === FILAS DE DATOS ===
filas = [
    # (parámetro, sin, con, ganancia, unidad)
    ("Período (T₁)", f"{T1_sin:.3f}", f"{T1_con:.3f}", "0.0", "s"),
    ("Aceleración (Sa)", f"{Sa_sin:.3f}", f"{Sa_con:.3f}", f"{ganancia_Sa:.1f}", "g"),
    ("Desplazamiento (Sd)", f"{Sd_sin:.2f}", f"{Sd_con:.2f}", f"{ganancia_Sd:.1f}", "cm"),
    ("Desplaz. Piso 1 (X₁)", f"{X1_sin:.2f}", f"{X1_con:.2f}", f"{ganancia_X1:.1f}", "cm"),
    ("Desplaz. Piso 2 (X₂)", f"{X2_sin:.2f}", f"{X2_con:.2f}", f"{ganancia_X2:.1f}", "cm"),
    ("Deriva", f"{Deriva_sin:.2f}", f"{Deriva_con:.2f}", f"{ganancia_Deriva:.1f}", "%"),
]

y_inicio = 7.9
y_salto = 0.75

for i, (param, sin, con, gan, unidad) in enumerate(filas):
    y = y_inicio - i * y_salto
    
    # Fondo alternado
    if i % 2 == 0:
        ax_tabla.add_patch(plt.Rectangle((0.2, y - 0.28), 9.6, 0.55,
                                          facecolor='#f8f9fa',
                                          edgecolor='none', zorder=0))
    
    # Parámetro
    ax_tabla.text(1.0, y, param,
                  ha='center', va='center', fontsize=9, fontweight='bold',
                  color=COLORES['titulo'])
    
    # Sin disipador
    ax_tabla.text(3.5, y, f"{sin} {unidad}",
                  ha='center', va='center', fontsize=9,
                  color=COLORES['sin_disipador'])
    
    # Con disipador
    ax_tabla.text(6.0, y, f"{con} {unidad}",
                  ha='center', va='center', fontsize=9, fontweight='bold',
                  color=COLORES['con_disipador'])
    
    # Ganancia
    if gan != "0.0":
        ax_tabla.text(8.5, y, f"↓ {gan}%",
                      ha='center', va='center', fontsize=9, fontweight='bold',
                      color=COLORES['mejora'])
    else:
        ax_tabla.text(8.5, y, "—",
                      ha='center', va='center', fontsize=9,
                      color='#95a5a6')

# === Línea inferior ===
ax_tabla.plot([0.2, 9.8], [y_inicio - len(filas) * y_salto + 0.3,
                            y_inicio - len(filas) * y_salto + 0.3],
              '-', color=COLORES['titulo'], linewidth=2)

# ============================================================================
# 5. CARACTERÍSTICAS DEL DISIPADOR VISCOSO
# ============================================================================

y_carac = y_inicio - len(filas) * y_salto - 0.4

ax_tabla.text(5, y_carac, 'CARACTERÍSTICAS DEL DISIPADOR VISCOSO',
              ha='center', va='center', fontsize=12, fontweight='bold',
              color=COLORES['titulo'],
              bbox=dict(boxstyle='round,pad=0.4',
                        facecolor='#fadbd8',
                        edgecolor=COLORES['disipador_X'],
                        linewidth=2))

y_carac -= 0.7
caracteristicas = [
    ("Tipo", "Tensor-puntal"),
    ("Longitud", "50 cm"),
    ("Coeficiente C", "2.378 t·s/m"),
    ("Fuerza F", "231.02 t"),
    ("Exponente α", "0.40"),
    ("Amortiguamiento β_V", "10%"),
    ("Cantidad total", "16 (4 por esquinero)"),
    ("Rótulas", "Sí (extremos)"),
    ("Reparación", "Reemplazo directo"),
]

for i, (carac, valor) in enumerate(caracteristicas):
    y = y_carac - i * 0.45
    
    ax_tabla.text(2.0, y, f"• {carac}:",
                  ha='right', va='center', fontsize=9, fontweight='bold',
                  color=COLORES['titulo'])
    
    ax_tabla.text(2.3, y, valor,
                  ha='left', va='center', fontsize=9,
                  color=COLORES['con_disipador'])

# ============================================================================
# 6. CONCLUSIÓN
# ============================================================================

y_concl = y_carac - len(caracteristicas) * 0.45 - 0.5

ax_tabla.text(5, y_concl,
              f'GANANCIA PROMEDIO: {np.mean([ganancia_Sa, ganancia_Sd, ganancia_X1, ganancia_X2, ganancia_Deriva]):.1f}%',
              ha='center', va='center', fontsize=13, fontweight='bold',
              color='white',
              bbox=dict(boxstyle='round,pad=0.5',
                        facecolor=COLORES['con_disipador'],
                        edgecolor='black', linewidth=2))

# ============================================================================
# 7. FUNCIÓN DE ACTUALIZACIÓN
# ============================================================================

def actualizar_frame(t):
    decaimiento = np.exp(-beta_V * omega1 * t)
    u1 = X1_max * np.cos(omega1 * t) * decaimiento
    u2 = X2_max * np.cos(omega1 * t) * decaimiento

    dx1 = u1 * ESCALA
    dx2 = u2 * ESCALA

    col_izq_1.set_data([-1.5, -1.5 + dx1 * 0.7], [0, He])
    col_izq_2.set_data([-1.5 + dx1 * 0.7, -1.5 + dx2], [He, 2*He])
    col_der_1.set_data([1.5, 1.5 + dx1 * 0.7], [0, He])
    col_der_2.set_data([1.5 + dx1 * 0.7, 1.5 + dx2], [He, 2*He])

    viga_1.set_data([-1.5 + dx1 * 0.7, 1.5 + dx1 * 0.7], [He, He])
    viga_2.set_data([-1.5 + dx2, 1.5 + dx2], [2*He, 2*He])

    nudo_x = 1.5 + dx1 * 0.7
    nudo_y = He
    nudo_plot.set_data([nudo_x], [nudo_y])

    d1_x1 = -1.5 + dx2
    d1_y1 = 2 * He
    d1_line.set_data([d1_x1, nudo_x], [d1_y1, nudo_y])
    d1_rot1.set_data([d1_x1], [d1_y1])
    d1_rot2.set_data([nudo_x], [nudo_y])

    d2_x1 = -1.5 + dx1 * 0.3
    d2_y1 = 0.3
    d2_line.set_data([d2_x1, nudo_x], [d2_y1, nudo_y])
    d2_rot1.set_data([d2_x1], [d2_y1])
    d2_rot2.set_data([nudo_x], [nudo_y])

    z_curve = np.linspace(0, 2*He, 50)
    u_curve = np.interp(z_curve, [0, He, 2*He], [0, dx1*0.7, dx2])
    deformada.set_data(-1.5 + u_curve, z_curve)

    tiempo_text.set_text(f't = {t:.2f} s  |  X1 = {u1:.2f} cm  |  X2 = {u2:.2f} cm')


# ============================================================================
# 8. GUARDAR Y ANIMAR
# ============================================================================

carpeta = "Resultados_M07_63"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

actualizar_frame(0)
plt.draw()
nombre_png = os.path.join(carpeta, f"M07_63_comparativa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
plt.savefig(nombre_png, dpi=150, bbox_inches='tight', facecolor=COLORES['fondo'])
print(f"\n[OK] Imagen guardada: {nombre_png}")

# Animación
print("\n" + "=" * 80)
print("M07.63 — CORTE CON TABLA COMPARATIVA")
print("=" * 80)
print("\n>> Mostrando animacion en pantalla...")
print(">> (Cierre la ventana para terminar)\n")

plt.show(block=False)
plt.pause(0.5)

t = 0.0
dt = 0.025
duracion = 15.0

try:
    while t < duracion:
        actualizar_frame(t)
        plt.pause(0.025)
        t += dt
except KeyboardInterrupt:
    print("\n\n[!] Animacion detenida por el usuario")

print("\n[OK] Animacion completada")
print("\n(La ventana permanecera abierta hasta que la cierre)")
plt.show(block=True)