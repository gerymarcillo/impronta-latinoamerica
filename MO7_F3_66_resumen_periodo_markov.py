# -*- coding: utf-8 -*-
"""
================================================================================
M07.8 — PERÍODO POR CADENAS DE MARKOV
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.8 — Período por Cadenas de Markov

OBJETIVO: Modelar la evolución del período fundamental (T₁) mediante una
          cadena de Markov, considerando que la estructura puede experimentar
          degradación progresiva (pérdida de rigidez) por:
          - Sismos recurrentes
          - Envejecimiento del concreto
          - Daño acumulado

ESTADOS DE RIGIDEZ:
    E0: Sin daño        (100% de rigidez) → T₁ = 0.389 s
    E1: Daño leve       (95% de rigidez)  → T₁ = 0.399 s
    E2: Daño moderado   (85% de rigidez)  → T₁ = 0.422 s
    E3: Daño severo     (70% de rigidez)  → T₁ = 0.465 s
    E4: Colapso         (0% de rigidez)   → T₁ = ∞

SALIDA:
    - Matriz de transición P
    - Evolución de la probabilidad de estados
    - Evolución del período T₁ en el tiempo
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
# PALETA DEL PROYECTO
# ============================================================================

COLORES = {
    'fondo_fig': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'box_datos_bg': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_calculo_bg': '#fef9e7',
    'box_calculo_borde': '#f39c12',
    'box_resultado_bg': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_ref_bg': '#f4ecf7',
    'box_ref_borde': '#8e44ad',
    'E0': '#27ae60',
    'E1': '#3498db',
    'E2': '#f39c12',
    'E3': '#e67e22',
    'E4': '#e74c3c',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

# Período nominal (sin daño)
T1_nominal = 0.389  # s

# Estados de rigidez y sus períodos asociados
# T = T_nominal / sqrt(factor_rigidez)
estados = {
    'E0': {'nombre': 'Sin daño', 'rigidez': 1.00, 'T1': T1_nominal},
    'E1': {'nombre': 'Daño leve', 'rigidez': 0.95, 'T1': T1_nominal / np.sqrt(0.95)},
    'E2': {'nombre': 'Daño moderado', 'rigidez': 0.85, 'T1': T1_nominal / np.sqrt(0.85)},
    'E3': {'nombre': 'Daño severo', 'rigidez': 0.70, 'T1': T1_nominal / np.sqrt(0.70)},
    'E4': {'nombre': 'Colapso', 'rigidez': 0.00, 'T1': np.inf},
}

# ============================================================================
# 2. MATRIZ DE TRANSICIÓN DE MARKOV
# ============================================================================

# Matriz de transición P (5x5)
# P[i,j] = probabilidad de pasar del estado i al estado j en un sismo
# Los valores son hipotéticos (deben calibrarse con datos reales)

P = np.array([
    # E0    E1    E2    E3    E4
    [0.85, 0.10, 0.04, 0.01, 0.00],  # E0
    [0.00, 0.75, 0.15, 0.08, 0.02],  # E1
    [0.00, 0.00, 0.70, 0.20, 0.10],  # E2
    [0.00, 0.00, 0.00, 0.65, 0.35],  # E3
    [0.00, 0.00, 0.00, 0.00, 1.00],  # E4 (absorbente)
])

# Verificar que las filas suman 1
assert np.allclose(P.sum(axis=1), 1.0), "Las filas de P deben sumar 1"

# ============================================================================
# 3. SIMULACIÓN DE LA CADENA DE MARKOV
# ============================================================================

# Número de sismos (pasos)
N_sismos = 30

# Estado inicial: E0 (sin daño)
pi_0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])

# Almacenar la evolución de las probabilidades
pi_evol = np.zeros((N_sismos + 1, 5))
pi_evol[0] = pi_0

# Iterar la cadena
for k in range(1, N_sismos + 1):
    pi_evol[k] = pi_evol[k-1] @ P

# ============================================================================
# 4. CÁLCULO DEL PERÍODO ESPERADO
# ============================================================================

# Períodos de cada estado (E4 → infinito)
T_estados = np.array([estados[e]['T1'] for e in ['E0', 'E1', 'E2', 'E3', 'E4']])

# Reemplazar E4 (infinito) por el período del último estado finito (E3)
T_estados_finito = np.array([estados['E0']['T1'],
                              estados['E1']['T1'],
                              estados['E2']['T1'],
                              estados['E3']['T1'],
                              estados['E3']['T1']])

# Período esperado en cada paso
T_esperado = pi_evol[:, :4] @ T_estados_finito[:4] / pi_evol[:, :4].sum(axis=1)

# ============================================================================
# 5. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.8 — PERÍODO POR CADENAS DE MARKOV")
print("=" * 80)

print(f"""
  ESTADOS DE RIGIDEZ:
    E0: Sin daño        (rigidez 100%) → T₁ = {estados['E0']['T1']:.4f} s
    E1: Daño leve       (rigidez  95%) → T₁ = {estados['E1']['T1']:.4f} s
    E2: Daño moderado   (rigidez  85%) → T₁ = {estados['E2']['T1']:.4f} s
    E3: Daño severo     (rigidez  70%) → T₁ = {estados['E3']['T1']:.4f} s
    E4: Colapso         (rigidez   0%) → T₁ = infinito
""")

print("  MATRIZ DE TRANSICIÓN P (5x5):")
print("  " + "─" * 60)
for i, row in enumerate(P):
    print(f"  E{i}: " + "  ".join([f"{p:.2f}" for p in row]))
print("  " + "─" * 60)

print(f"""
  EVOLUCIÓN DE PROBABILIDADES (primeros 10 sismos):
""")
print(f"  {'Sismo':<6} {'P(E0)':<10} {'P(E1)':<10} {'P(E2)':<10} {'P(E3)':<10} {'P(E4)':<10}")
print("  " + "─" * 70)
for k in range(min(11, N_sismos + 1)):
    print(f"  {k:<6} " + "  ".join([f"{p:.4f}" for p in pi_evol[k]]))

print(f"""
  EVOLUCIÓN DEL PERÍODO ESPERADO:
    T₁(0)  = {T_esperado[0]:.4f} s
    T₁(5)  = {T_esperado[5]:.4f} s
    T₁(10) = {T_esperado[10]:.4f} s
    T₁(20) = {T_esperado[20]:.4f} s
    T₁(30) = {T_esperado[30]:.4f} s

  P(COLAPSO) A 30 SISMOS:
    P(E4) = {pi_evol[30, 4]*100:.2f} %
""")
print("=" * 80)

# ============================================================================
# 6. FIGURA
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.8 — PERÍODO POR CADENAS DE MARKOV',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | N sismos = {N_sismos} | T₁ nominal = {T1_nominal:.4f} s',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.0, 1.0])

# ============================================================================
# PANEL (a): DIAGRAMA DE ESTADOS
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('(a) ESTADOS DE RIGIDEZ',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=10)

# Dibujar los 5 estados
estados_lista = [
    ('E0', 'Sin daño', 8.5, COLORES['E0']),
    ('E1', 'Daño leve', 6.5, COLORES['E1']),
    ('E2', 'Daño mod.', 4.5, COLORES['E2']),
    ('E3', 'Daño sev.', 2.5, COLORES['E3']),
    ('E4', 'Colapso', 0.5, COLORES['E4']),
]

for codigo, nombre, y, color in estados_lista:
    ax1.add_patch(plt.Rectangle((1, y - 0.4), 7, 0.8,
                                  facecolor=color, edgecolor='black',
                                  linewidth=2, alpha=0.7))
    ax1.text(1.2, y, f'{codigo}: {nombre}',
             fontsize=11, fontweight='bold', color='white', va='center')
    
    T_estado = estados[codigo]['T1']
    if T_estado == np.inf:
        T_texto = '∞'
    else:
        T_texto = f'{T_estado:.4f} s'
    ax1.text(8.2, y, T_texto,
             fontsize=10, fontweight='bold', color='#2c3e50', va='center')

ax1.text(5, -0.2, 'Estados absorbentes → E4',
         fontsize=9, style='italic', color=COLORES['E4'], ha='center')

# ============================================================================
# PANEL (b): MATRIZ DE TRANSICIÓN
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1:])
ax2.axis('off')
ax2.set_title('(b) MATRIZ DE TRANSICIÓN P (5×5)',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=10)

# Dibujar la matriz como heatmap de texto
n = 5
for i in range(n):
    for j in range(n):
        p = P[i, j]
        if p > 0.5:
            color = '#27ae60'
            text_color = 'white'
        elif p > 0.1:
            color = '#f39c12'
            text_color = 'white'
        elif p > 0:
            color = '#fadbd8'
            text_color = 'black'
        else:
            color = '#ecf0f1'
            text_color = 'gray'
        
        ax2.add_patch(plt.Rectangle((j * 1.5 + 2, (n - 1 - i) * 1.2 + 1),
                                      1.5, 1.2,
                                      facecolor=color, edgecolor='black',
                                      linewidth=1.5))
        ax2.text(j * 1.5 + 2.75, (n - 1 - i) * 1.2 + 1.6,
                 f'{p:.2f}',
                 fontsize=10, fontweight='bold',
                 color=text_color, ha='center', va='center')

# Etiquetas de filas (estados origen)
for i in range(n):
    ax2.text(1.7, (n - 1 - i) * 1.2 + 1.6,
             f'E{i}', fontsize=11, fontweight='bold',
             color=COLORES[f'E{i}'], ha='right', va='center')

# Etiquetas de columnas (estados destino)
for j in range(n):
    ax2.text(j * 1.5 + 2.75, n * 1.2 + 1.2,
             f'E{j}', fontsize=11, fontweight='bold',
             color=COLORES[f'E{j}'], ha='center', va='center')

ax2.text(5.5, 0.3, 'Filas: estado actual | Columnas: estado siguiente',
         fontsize=9, style='italic', color='#2c3e50', ha='center')

ax2.set_xlim(0, 11)
ax2.set_ylim(0, 8.5)

# ============================================================================
# PANEL (c): EVOLUCIÓN DE PROBABILIDADES
# ============================================================================

ax3 = fig.add_subplot(gs[1, 0:2])

sismos = np.arange(N_sismos + 1)

ax3.plot(sismos, pi_evol[:, 0], 'o-', color=COLORES['E0'],
         linewidth=2, markersize=4, label='E0 (Sin daño)')
ax3.plot(sismos, pi_evol[:, 1], 's-', color=COLORES['E1'],
         linewidth=2, markersize=4, label='E1 (Daño leve)')
ax3.plot(sismos, pi_evol[:, 2], '^-', color=COLORES['E2'],
         linewidth=2, markersize=4, label='E2 (Daño moderado)')
ax3.plot(sismos, pi_evol[:, 3], 'd-', color=COLORES['E3'],
         linewidth=2, markersize=4, label='E3 (Daño severo)')
ax3.plot(sismos, pi_evol[:, 4], 'v-', color=COLORES['E4'],
         linewidth=2, markersize=4, label='E4 (Colapso)')

ax3.set_xlabel('Número de sismos', fontsize=11)
ax3.set_ylabel('Probabilidad', fontsize=11)
ax3.set_title('(c) EVOLUCIÓN DE PROBABILIDADES DE ESTADO',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax3.legend(fontsize=9, loc='center right')
ax3.grid(alpha=0.3)
ax3.set_ylim(0, 1.05)

# ============================================================================
# PANEL (d): EVOLUCIÓN DEL PERÍODO ESPERADO
# ============================================================================

ax4 = fig.add_subplot(gs[1, 2])

ax4.plot(sismos, T_esperado, 'o-', color='#3498db',
         linewidth=2.5, markersize=5, label='T₁ esperado')

# Línea de referencia (T₁ nominal)
ax4.axhline(y=T1_nominal, color='#27ae60',
            linestyle='--', linewidth=2,
            label=f'T₁ nominal = {T1_nominal:.4f} s')

# Línea de T₁ crítico
ax4.axhline(y=0.5, color='#e74c3c',
            linestyle=':', linewidth=2,
            label='T₁ crítico = 0.5 s')

ax4.set_xlabel('Número de sismos', fontsize=11)
ax4.set_ylabel('Período T₁ (s)', fontsize=11)
ax4.set_title('(d) EVOLUCIÓN DEL PERÍODO ESPERADO',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax4.legend(fontsize=9)
ax4.grid(alpha=0.3)

# ============================================================================
# MENSAJES OPORTUNOS
# ============================================================================

msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Modelo de Markov\n"
    "  Estados E0-E4\n"
    "  E4: absorbente"
)

fig.text(0.015, 0.925, msg1, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=1.5, alpha=0.95))

msg2 = (
    "METODO\n"
    "═══════════════════════════\n"
    "  πₖ₊₁ = πₖ · P\n"
    "  N sismos = 30\n"
    "  P(E4) = colapso"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07_8"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"M07_8_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("M07.8 — PERÍODO POR CADENAS DE MARKOV\n")
    f.write("=" * 80 + "\n\n")
    f.write("ESTADOS:\n")
    for codigo, datos in estados.items():
        T = datos['T1']
        T_str = 'infinito' if T == np.inf else f'{T:.4f} s'
        f.write(f"  {codigo}: {datos['nombre']:<15} rigidez={datos['rigidez']*100:>5.1f}%  T₁={T_str}\n")
    f.write("\nMATRIZ DE TRANSICIÓN:\n")
    for i, row in enumerate(P):
        f.write(f"  E{i}: " + "  ".join([f"{p:.2f}" for p in row]) + "\n")
    f.write("\nEVOLUCIÓN DE PROBABILIDADES:\n")
    f.write(f"  {'Sismo':<6} {'P(E0)':<10} {'P(E1)':<10} {'P(E2)':<10} {'P(E3)':<10} {'P(E4)':<10}\n")
    for k in range(N_sismos + 1):
        f.write(f"  {k:<6} " + "  ".join([f"{p:.4f}" for p in pi_evol[k]]) + "\n")
    f.write("\nPERÍODO ESPERADO:\n")
    for k in range(0, N_sismos + 1, 5):
        f.write(f"  T₁({k}) = {T_esperado[k]:.4f} s\n")
    f.write(f"\nP(COLAPSO) A {N_sismos} SISMOS = {pi_evol[N_sismos, 4]*100:.2f} %\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 8. GUARDAR IMAGEN Y MOSTRAR
# ============================================================================

nombre_img = f"M07_8_markov_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.8 COMPLETADO — PERÍODO POR CADENAS DE MARKOV")
print("=" * 80)
print(f"  T₁(0)   = {T_esperado[0]:.4f} s")
print(f"  T₁(10)  = {T_esperado[10]:.4f} s")
print(f"  T₁(30)  = {T_esperado[30]:.4f} s")
print(f"  P(E4) a {N_sismos} sismos = {pi_evol[N_sismos, 4]*100:.2f} %")
print("=" * 80)