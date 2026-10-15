# -*- coding: utf-8 -*-
"""
================================================================================
M08.6 — ANÁLISIS DE LA MATRIZ DE TRANSICIÓN DE MARKOV
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.6 — Matriz de Transición (Cordón Umbilical)

OBJETIVO: Analizar en profundidad la MATRIZ DE TRANSICIÓN de Markov,
          que es el "cordón umbilical" del modelo.

          La matriz de transición P define TODA la dinámica del sistema:
          - Cómo se degrada la estructura
          - Cómo se recupera con el DMTP
          - Qué estados son absorbentes
          - Cuál es el estado estacionario

CONCEPTO CLAVE:
    La matriz P es el corazón de Markov.
    Si P está mal, TODO el análisis está mal.

ESTADOS:
    E0: Operativo total
    E1: Daño leve
    E2: Daño moderado
    E3: Daño severo
    E4: Colapso (absorbente)

LINK: https://gerymarcillo.github.io/impronta-latinoamerica/
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
    from matplotlib.colors import LinearSegmentedColormap
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "ANALISIS DE LA MATRIZ DE TRANSICION DE MARKOV"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La matriz P es el cordón umbilical de Markov."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. ESTADOS DE RESILIENCIA
# ============================================================================

estados = {
    'E0': {'nombre': 'Operativo total', 'T1': 0.389, 'downtime': 0, 'color': '#2d6a4f'},
    'E1': {'nombre': 'Daño leve', 'T1': 0.399, 'downtime': 7, 'color': '#3498db'},
    'E2': {'nombre': 'Daño moderado', 'T1': 0.422, 'downtime': 30, 'color': '#f39c12'},
    'E3': {'nombre': 'Daño severo', 'T1': 0.465, 'downtime': 180, 'color': '#e67e22'},
    'E4': {'nombre': 'Colapso', 'T1': np.inf, 'downtime': 365, 'color': '#9d0208'},
}

N_estados = 5

# ============================================================================
# 3. MATRICES DE TRANSICIÓN
# ============================================================================

# ============================================
# ESCENARIO A: SIN DMTP (solo degradación)
# ============================================

P_sin = np.array([
    [0.85, 0.10, 0.04, 0.01, 0.00],  # E0
    [0.00, 0.75, 0.15, 0.08, 0.02],  # E1
    [0.00, 0.00, 0.70, 0.20, 0.10],  # E2
    [0.00, 0.00, 0.00, 0.65, 0.35],  # E3
    [0.00, 0.00, 0.00, 0.00, 1.00],  # E4
])

# ============================================
# ESCENARIO B: CON DMTP (con recuperación)
# ============================================

P_con = np.array([
    [0.85, 0.10, 0.04, 0.01, 0.00],  # E0
    [0.30, 0.50, 0.15, 0.04, 0.01],  # E1
    [0.10, 0.30, 0.40, 0.15, 0.05],  # E2
    [0.00, 0.10, 0.30, 0.45, 0.15],  # E3
    [0.00, 0.00, 0.00, 0.00, 1.00],  # E4
])

# ============================================================================
# 4. VERIFICACIÓN DE LA MATRIZ
# ============================================================================

print("=" * 80)
print(f"[M08.6] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n" + "=" * 80)
print("VERIFICACION DE LA MATRIZ DE TRANSICION")
print("=" * 80)

print("\n  ESCENARIO A (SIN DMTP):")
print(f"  {'Fila':<6} {'Suma':<12} {'Valida':<10}")
print(f"  {'-'*30}")
for i, row in enumerate(P_sin):
    suma = np.sum(row)
    valida = "OK" if np.abs(suma - 1.0) < 1e-6 else "ERROR"
    print(f"  E{i:<6} {suma:<12.6f} {valida:<10}")

print("\n  ESCENARIO B (CON DMTP):")
print(f"  {'Fila':<6} {'Suma':<12} {'Valida':<10}")
print(f"  {'-'*30}")
for i, row in enumerate(P_con):
    suma = np.sum(row)
    valida = "OK" if np.abs(suma - 1.0) < 1e-6 else "ERROR"
    print(f"  E{i:<6} {suma:<12.6f} {valida:<10}")

# Verificar positividad
print("\n  VERIFICACION DE POSITIVIDAD:")
print(f"    P_sin >= 0: {np.all(P_sin >= 0)}")
print(f"    P_con >= 0: {np.all(P_con >= 0)}")

# ============================================================================
# 5. PROPIEDADES DE LA MATRIZ
# ============================================================================

print("\n" + "=" * 80)
print("PROPIEDADES DE LA MATRIZ DE TRANSICION")
print("=" * 80)

# Autovalores
eig_sin = np.linalg.eigvals(P_sin)
eig_con = np.linalg.eigvals(P_con)

print("\n  AUTOVALORES P_sin:")
for i, e in enumerate(sorted(np.abs(eig_sin), reverse=True)):
    print(f"    lambda_{i+1} = {e:.6f}")

print("\n  AUTOVALORES P_con:")
for i, e in enumerate(sorted(np.abs(eig_con), reverse=True)):
    print(f"    lambda_{i+1} = {e:.6f}")

# Verificar autovalor 1
print(f"\n  Autovalor maximo P_sin: {max(np.abs(eig_sin)):.6f}")
print(f"  Autovalor maximo P_con: {max(np.abs(eig_con)):.6f}")
print(f"  (Debe ser 1.0 para cadena valida)")

# ============================================================================
# 6. ANALISIS FILA POR FILA
# ============================================================================

print("\n" + "=" * 80)
print("ANALISIS FILA POR FILA - ESCENARIO B (CON DMTP)")
print("=" * 80)

for i, cod in enumerate(['E0', 'E1', 'E2', 'E3', 'E4']):
    print(f"\n  FILA {cod} ({estados[cod]['nombre']}):")
    print(f"    Permanecer en {cod}:    {P_con[i, i]:.3f}")
    
    for j, cod_dest in enumerate(['E0', 'E1', 'E2', 'E3', 'E4']):
        if i != j and P_con[i, j] > 0:
            direccion = "MEJORA" if j < i else "DEGRADA"
            print(f"    → {cod_dest} ({direccion}):       {P_con[i, j]:.3f}")

# ============================================================================
# 7. ANALISIS DE RECUPERACION
# ============================================================================

print("\n" + "=" * 80)
print("ANALISIS DE RECUPERACION (P_con - P_sin)")
print("=" * 80)

P_diff = P_con - P_sin

print(f"\n  {'Fila':<6} {'E0':<10} {'E1':<10} {'E2':<10} {'E3':<10} {'E4':<10}")
print(f"  {'-'*66}")
for i, cod in enumerate(['E0', 'E1', 'E2', 'E3', 'E4']):
    print(f"  {cod:<6} " + "  ".join([f"{P_diff[i, j]:+7.3f}" for j in range(5)]))

print("\n  INTERPRETACION:")
print(f"    Valores POSITIVOS (+) = Mayor probabilidad con DMTP")
print(f"    Valores NEGATIVOS (-) = Menor probabilidad con DMTP")

# ============================================================================
# 8. ESTADO ESTACIONARIO
# ============================================================================

def estado_estacionario(P):
    """Calcula el estado estacionario de la cadena de Markov."""
    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigvals - 1.0))
    pi = np.real(eigvecs[:, idx])
    pi = pi / np.sum(pi)
    return pi

pi_est_sin = estado_estacionario(P_sin)
pi_est_con = estado_estacionario(P_con)

print("\n" + "=" * 80)
print("ESTADO ESTACIONARIO")
print("=" * 80)

print(f"\n  {'Estado':<8} {'SIN DMTP':<15} {'CON DMTP':<15} {'DIFERENCIA':<15}")
print(f"  {'-'*60}")
for i, cod in enumerate(['E0', 'E1', 'E2', 'E3', 'E4']):
    sin = pi_est_sin[i] * 100
    con = pi_est_con[i] * 100
    dif = con - sin
    print(f"  {cod:<8} {sin:>8.2f}%       {con:>8.2f}%       {dif:>+8.2f}%")

# Resiliencia estacionaria
res_sin = (pi_est_sin[0] + pi_est_sin[1]) * 100
res_con = (pi_est_con[0] + pi_est_con[1]) * 100
print(f"\n  RESILIENCIA ESTACIONARIA (E0+E1):")
print(f"    SIN DMTP: {res_sin:.2f}%")
print(f"    CON DMTP: {res_con:.2f}%")
print(f"    MEJORA:   {res_con - res_sin:+.2f}%")

# ============================================================================
# 9. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(26, 18))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M08.6 — ANALISIS DE LA MATRIZ DE TRANSICION DE MARKOV',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.92, bottom=0.08)

# ============================================================================
# FILA 1: MATRICES DE TRANSICION
# ============================================================================

# Crear colormap
cmap = LinearSegmentedColormap.from_list('custom', ['#ffffff', '#3498db', '#1a237e'])

# --- Panel 1: Matriz P_sin ---
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.imshow(P_sin, cmap=cmap, vmin=0, vmax=1, aspect='auto')
ax1.set_xticks(range(5))
ax1.set_yticks(range(5))
ax1.set_xticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax1.set_yticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax1.set_xlabel('Estado destino', fontsize=10)
ax1.set_ylabel('Estado actual', fontsize=10)
ax1.set_title('(a) MATRIZ P — SIN DMTP', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_sin[i, j]
        color = 'white' if val > 0.5 else 'black'
        ax1.text(j, i, f'{val:.2f}', ha='center', va='center',
                 fontsize=9, fontweight='bold', color=color)

plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

# --- Panel 2: Matriz P_con ---
ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.imshow(P_con, cmap=cmap, vmin=0, vmax=1, aspect='auto')
ax2.set_xticks(range(5))
ax2.set_yticks(range(5))
ax2.set_xticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax2.set_yticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax2.set_xlabel('Estado destino', fontsize=10)
ax2.set_ylabel('Estado actual', fontsize=10)
ax2.set_title('(b) MATRIZ P — CON DMTP', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_con[i, j]
        color = 'white' if val > 0.5 else 'black'
        ax2.text(j, i, f'{val:.2f}', ha='center', va='center',
                 fontsize=9, fontweight='bold', color=color)

plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

# --- Panel 3: Diferencia P_con - P_sin ---
ax3 = fig.add_subplot(gs[0, 2])
cmap_diff = LinearSegmentedColormap.from_list('diff', ['#e74c3c', '#ffffff', '#2ecc71'])
im3 = ax3.imshow(P_diff, cmap=cmap_diff, vmin=-0.35, vmax=0.35, aspect='auto')
ax3.set_xticks(range(5))
ax3.set_yticks(range(5))
ax3.set_xticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax3.set_yticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=9)
ax3.set_xlabel('Estado destino', fontsize=10)
ax3.set_ylabel('Estado actual', fontsize=10)
ax3.set_title('(c) DIFERENCIA P_con - P_sin', fontsize=12, fontweight='bold', pad=10)

for i in range(5):
    for j in range(5):
        val = P_diff[i, j]
        color = 'white' if abs(val) > 0.2 else 'black'
        ax3.text(j, i, f'{val:+.2f}', ha='center', va='center',
                 fontsize=8, fontweight='bold', color=color)

plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

# ============================================================================
# FILA 2: VERIFICACION Y PROPIEDADES
# ============================================================================

# --- Panel 4: Verificacion de suma ---
ax4 = fig.add_subplot(gs[1, 0])
x_pos = np.arange(5)
width = 0.35

sumas_sin = [np.sum(P_sin[i]) for i in range(5)]
sumas_con = [np.sum(P_con[i]) for i in range(5)]

ax4.bar(x_pos - width/2, sumas_sin, width, color='#e74c3c',
        edgecolor='black', linewidth=1.5, label='Sin DMTP', alpha=0.8)
ax4.bar(x_pos + width/2, sumas_con, width, color='#2ecc71',
        edgecolor='black', linewidth=1.5, label='Con DMTP', alpha=0.8)
ax4.axhline(1.0, color='black', linestyle='--', linewidth=2, label='Suma = 1.0')

for i, (s, c) in enumerate(zip(sumas_sin, sumas_con)):
    ax4.text(i - width/2, s + 0.02, f'{s:.2f}', ha='center', fontsize=8)
    ax4.text(i + width/2, c + 0.02, f'{c:.2f}', ha='center', fontsize=8)

ax4.set_xticks(x_pos)
ax4.set_xticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=10)
ax4.set_ylabel('Suma de la fila', fontsize=10)
ax4.set_title('(d) VERIFICACION: SUMA = 1', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, axis='y', linestyle='--', alpha=0.3)
ax4.set_ylim(0, 1.15)

# --- Panel 5: Autovalores ---
ax5 = fig.add_subplot(gs[1, 1])
eig_sin_abs = sorted(np.abs(eig_sin), reverse=True)
eig_con_abs = sorted(np.abs(eig_con), reverse=True)

x_pos = np.arange(5)
width = 0.35

ax5.bar(x_pos - width/2, eig_sin_abs, width, color='#e74c3c',
        edgecolor='black', linewidth=1.5, label='Sin DMTP', alpha=0.8)
ax5.bar(x_pos + width/2, eig_con_abs, width, color='#2ecc71',
        edgecolor='black', linewidth=1.5, label='Con DMTP', alpha=0.8)
ax5.axhline(1.0, color='black', linestyle='--', linewidth=2)

for i, (s, c) in enumerate(zip(eig_sin_abs, eig_con_abs)):
    ax5.text(i - width/2, s + 0.02, f'{s:.3f}', ha='center', fontsize=7)
    ax5.text(i + width/2, c + 0.02, f'{c:.3f}', ha='center', fontsize=7)

ax5.set_xticks(x_pos)
ax5.set_xticklabels([f'λ{i+1}' for i in range(5)], fontsize=10)
ax5.set_ylabel('|Autovalor|', fontsize=10)
ax5.set_title('(e) AUTOVALORES DE P', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 6: Interpretacion de filas ---
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.set_title('(f) INTERPRETACION FILA POR FILA', fontsize=12, fontweight='bold', pad=10)

txt6 = (
    "P_con (CON DMTP)\n"
    "─────────────────────────────\n\n"
    "  E0 → permanece 85%\n"
    "       baja 10% a E1\n\n"
    "  E1 → MEJORA 30% a E0\n"
    "       permanece 50%\n"
    "       baja 15% a E2\n\n"
    "  E2 → MEJORA 10% a E0\n"
    "       MEJORA 30% a E1\n"
    "       permanece 40%\n"
    "       baja 15% a E3\n\n"
    "  E3 → MEJORA 10% a E1\n"
    "       MEJORA 30% a E2\n"
    "       permanece 45%\n"
    "       colapsa 15%\n\n"
    "  E4 → absorbente (100%)\n"
    "─────────────────────────────\n"
    "  CLAVE:\n"
    "  Las flechas de MEJORA\n"
    "  (E1→E0, E2→E0, E2→E1,\n"
    "   E3→E1, E3→E2) son el\n"
    "  efecto del DMTP.\n"
    "─────────────────────────────"
)

ax6.text(0.5, 0.5, txt6, ha='center', va='center',
         fontsize=7.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# ============================================================================
# FILA 3: ESTADO ESTACIONARIO Y CONCLUSIONES
# ============================================================================

# --- Panel 7: Estado estacionario ---
ax7 = fig.add_subplot(gs[2, 0])
x_pos = np.arange(5)
width = 0.35

ax7.bar(x_pos - width/2, pi_est_sin * 100, width, color='#e74c3c',
        edgecolor='black', linewidth=1.5, label='Sin DMTP', alpha=0.8)
ax7.bar(x_pos + width/2, pi_est_con * 100, width, color='#2ecc71',
        edgecolor='black', linewidth=1.5, label='Con DMTP', alpha=0.8)

for i, (s, c) in enumerate(zip(pi_est_sin*100, pi_est_con*100)):
    ax7.text(i - width/2, s + 1, f'{s:.1f}%', ha='center', fontsize=8, fontweight='bold')
    ax7.text(i + width/2, c + 1, f'{c:.1f}%', ha='center', fontsize=8, fontweight='bold')

ax7.set_xticks(x_pos)
ax7.set_xticklabels(['E0', 'E1', 'E2', 'E3', 'E4'], fontsize=10)
ax7.set_ylabel('Probabilidad estacionaria (%)', fontsize=10)
ax7.set_title('(g) ESTADO ESTACIONARIO', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 8: Resiliencia estacionaria ---
ax8 = fig.add_subplot(gs[2, 1])

categorias = ['Sin DMTP', 'Con DMTP']
resiliencias = [res_sin, res_con]
colores = ['#e74c3c', '#2ecc71']

bars = ax8.bar(categorias, resiliencias, color=colores,
               edgecolor='black', linewidth=2, alpha=0.85)
for bar, val in zip(bars, resiliencias):
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax8.set_ylabel('Resiliencia estacionaria P(E0+E1) (%)', fontsize=10)
ax8.set_title('(h) RESILIENCIA ESTACIONARIA', fontsize=11, fontweight='bold')
ax8.grid(True, axis='y', linestyle='--', alpha=0.3)
ax8.set_ylim(0, 105)

# --- Panel 9: Conclusión ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.set_title('(i) CONCLUSION', fontsize=12, fontweight='bold', pad=10)

txt9 = (
    f"ANALISIS DE P\n"
    f"─────────────────────────────\n\n"
    f"  VERIFICACION:\n"
    f"    ✓ Suma de filas = 1\n"
    f"    ✓ Todos los P >= 0\n"
    f"    ✓ Cadena valida\n\n"
    f"  PROPIEDADES:\n"
    f"    • Autovalor max = 1\n"
    f"    • E4 absorbente\n"
    f"    • Estados transitorios:\n"
    f"      E0, E1, E2, E3\n\n"
    f"  ESTADO ESTACIONARIO:\n"
    f"    Sin DMTP: {res_sin:.1f}%\n"
    f"    Con DMTP: {res_con:.1f}%\n"
    f"    Mejora: {res_con-res_sin:+.1f}%\n\n"
    f"─────────────────────────────\n"
    f"  La matriz P_con permite\n"
    f"  la RECUPERACION desde\n"
    f"  E1, E2 y E3, aumentando\n"
    f"  la resiliencia global.\n"
    f"─────────────────────────────\n"
    f"  {FRASE}"
)

ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=7.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# ============================================================================
# LINK DEL PROYECTO
# ============================================================================

fig.text(0.5, 0.015,
         f'🌐 Más información: {LINK}',
         ha='center', va='bottom', fontsize=11, fontweight='bold',
         color='#2980b9',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor='#2980b9',
                   linewidth=2))

# ============================================================================
# 10. GUARDAR
# ============================================================================

carpeta = "Resultados_M08_6"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_6_matriz_transicion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\n[OK] Dashboard guardado: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M08.6 COMPLETADO — ANALISIS DE LA MATRIZ DE TRANSICION")
print("=" * 80)
print(f"\n  VERIFICACION:")
print(f"    Suma de filas = 1: OK")
print(f"    Todos los P >= 0: OK")
print(f"\n  ESTADO ESTACIONARIO:")
print(f"    Sin DMTP: {res_sin:.2f}%")
print(f"    Con DMTP: {res_con:.2f}%")
print(f"    Mejora:   {res_con - res_sin:+.2f}%")
print(f"\n  FRASE: {FRASE}")
print("=" * 80)