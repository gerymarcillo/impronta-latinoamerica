# -*- coding: utf-8 -*-
"""
================================================================================
M07.6.2 — PERIODO 2 (LAMBDA 2) DEL PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.6 — Período por Método de Cortante
SUB-SUBSECCIÓN: M07.6.2 — Período 2 (λ₂)

OBJETIVO: Cálculo del SEGUNDO autovalor (λ₂) y el período del modo 2 (T₂)
          usando los datos de masa y rigidez del proyecto principal.

VALORES DE REFERENCIA (Excel RESILIENCIA MODOS PROYECTO PII 2026):
    - λ₂ = 1,787.103
    - ω₂ = 42.274 rad/s
    - T₂ = 0.149 s
    - φ₂ = [1.000, -0.707]

DATOS DE ENTRADA:
    - Masa por piso: m_piso = 41.3149 t·s²/m
    - Rigidez del piso: k_piso = 28,209.20 t/m
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
    'modo2': '#e74c3c',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38

fc = 210
g = 9.81
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL

# ============================================================================
# 2. CÁLCULO DE MASA Y RIGIDEZ
# ============================================================================

# E estocástico
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

# I (usando 38 cm exactos como el Excel)
I_col_cm4 = (38**4) / 12
I_col = I_col_cm4 / 100**4

# k_col
k_columna = 12 * E_tm2 * I_col / He**3

# k_piso
k_entrepiso = N_COL_TOTAL * k_columna

# W y m
W_piso = Cu * AREA
m_piso = W_piso / g

# Matrices (2 GDL)
K = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso,     k_entrepiso]
])

M = np.array([
    [m_piso, 0],
    [0, m_piso]
])

# ============================================================================
# 3. CÁLCULO DE λ₂ (SEGUNDO AUTOVALOR)
# ============================================================================

# Problema de autovalores: det(K - λM) = 0
A = np.linalg.inv(M) @ K
eigenvalues = np.linalg.eigvals(A)
eigenvalues = np.sort(eigenvalues.real)  # λ₁ < λ₂

# λ₂ = SEGUNDO autovalor (el mayor)
lambda_2 = eigenvalues[1]

# Frecuencia angular del modo 2
omega_2 = np.sqrt(lambda_2)

# Frecuencia cíclica del modo 2
f_2 = omega_2 / (2 * np.pi)

# Período del modo 2
T_2 = 2 * np.pi / omega_2

# ============================================================================
# 4. FORMA MODAL DEL MODO 2 (φ₂)
# ============================================================================

eigenvalues_full, eigenvectors = np.linalg.eig(A)
idx = np.argsort(eigenvalues_full.real)
eigenvectors = eigenvectors[:, idx].real

phi_2 = eigenvectors[:, 1] / max(abs(eigenvectors[:, 1]))

# ============================================================================
# 5. VERIFICACIÓN ANALÍTICA
# ============================================================================

lambda_2_analitico = (k_entrepiso / m_piso) * (2 + np.sqrt(2))
omega_2_analitico = np.sqrt(lambda_2_analitico)
T_2_analitico = 2 * np.pi / omega_2_analitico

# ============================================================================
# 6. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.6.2 — PERIODO 2 (LAMBDA 2) DEL PROYECTO PRINCIPAL")
print("=" * 80)
print(f"""
  DATOS DE ENTRADA (MASA Y RIGIDEZ):
    Seccion columna  = {B_COL*100:.0f} x {H_COL*100:.0f} cm
    He               = {He:.2f} m
    # Pisos          = {N_PISOS}
    # Columnas       = {N_COL_TOTAL}
    E = 12600*raiz(fc) = {E_kgcm2:.2f} kg/cm2

  MASA:
    W_piso   = {W_piso:.2f} t
    m_piso   = {m_piso:.4f} t.s2/m

  RIGIDEZ:
    I_col    = {I_col_cm4:.2f} cm4 = {I_col:.8f} m4
    k_col    = {k_columna:.2f} t/m
    k_piso   = {k_entrepiso:.2f} t/m

  MATRIZ K:
    K = [[{K[0,0]:.2f}, {K[0,1]:.2f}]
         [{K[1,0]:.2f}, {K[1,1]:.2f}]]

  MATRIZ M:
    M = [[{M[0,0]:.4f}, {M[0,1]:.4f}]
         [{M[1,0]:.4f}, {M[1,1]:.4f}]]

  ────────────────────────────────────────────────────────────────
  SEGUNDO AUTOVALOR:
    lambda_2 = {lambda_2:.3f}
    (Excel: 1787.103)

  FRECUENCIA ANGULAR (Modo 2):
    omega_2 = {omega_2:.3f} rad/s
    (Excel: 42.274)

  FRECUENCIA CICLICA (Modo 2):
    f_2 = {f_2:.3f} Hz

  PERIODO DEL MODO 2:
    T_2 = {T_2:.3f} s
    (Excel: 0.149)

  FORMA MODAL (Modo 2):
    phi_2 = [{phi_2[0]:.3f}, {phi_2[1]:.3f}]
  ────────────────────────────────────────────────────────────────
  VERIFICACION ANALITICA:
    lambda_2 (analitico) = {lambda_2_analitico:.3f}
    omega_2  (analitico) = {omega_2_analitico:.3f} rad/s
    T_2      (analitico) = {T_2_analitico:.3f} s
""")
print("=" * 80)

# ============================================================================
# 7. FIGURA
# ============================================================================

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.6.2 — PERIODO 2 (LAMBDA 2) DEL PROYECTO PRINCIPAL',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Modelo base 38×38 cm | T2 = {T_2:.3f} s',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.04, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.0, 1.0])

# ============================================================================
# FILA 0: MATRICES
# ============================================================================

# --- Panel (a): MATRIZ K ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis('off')
ax1.set_title('(a) MATRIZ DE RIGIDEZ K',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt1 = (
    f"K = [[{K[0,0]:>10.2f}, {K[0,1]:>10.2f}]\n"
    f"     [{K[1,0]:>10.2f}, {K[1,1]:>10.2f}]]\n\n"
    f"k_piso = {k_entrepiso:.2f} t/m\n\n"
    f"K = [[2k, -k], [-k, k]]"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=2, alpha=0.95))

# --- Panel (b): MATRIZ M ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis('off')
ax2.set_title('(b) MATRIZ DE MASA M',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt2 = (
    f"M = [[{M[0,0]:>8.4f}, {M[0,1]:>8.4f}]\n"
    f"     [{M[1,0]:>8.4f}, {M[1,1]:>8.4f}]]\n\n"
    f"m_piso = {m_piso:.4f}\n"
    f"         t.s2/m\n\n"
    f"M = diag(m, m)"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.8,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2, alpha=0.95))

# --- Panel (c): AUTOVALOR λ₂ ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_xlim(0, 10); ax3.set_ylim(0, 10); ax3.axis('off')
ax3.set_title('(c) SEGUNDO AUTOVALOR λ2',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=8)

txt3 = (
    "Ecuacion caracteristica:\n"
    "  det(K - λM) = 0\n\n"
    "Equivalente a:\n"
    "  det(M⁻¹K - λI) = 0\n\n"
    "Solucion:\n"
    f"  λ2 = {lambda_2:.3f}\n"
    f"  (Excel: 1787.103)\n\n"
    "Verificacion analitica:\n"
    f"  λ2 = (k/m)(2+√2)\n"
    f"  λ2 = {lambda_2_analitico:.3f}"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         linespacing=1.7,
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=2, alpha=0.95))

# ============================================================================
# FILA 1: RESULTADOS
# ============================================================================

# --- Panel (d): RESULTADOS DEL MODO 2 ---
ax4 = fig.add_subplot(gs[1, 0:2])
ax4.set_xlim(0, 10); ax4.set_ylim(0, 10); ax4.axis('off')
ax4.set_title('(d) RESULTADOS DEL MODO 2',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=10)

resultados = (
    "                    SEGUNDO MODO\n"
    "═══════════════════════════════════════════════\n\n"
    f"  lambda_2 = {lambda_2:>10.3f}   (Excel: 1787.103)\n\n"
    f"  omega_2  = {omega_2:>10.3f} rad/s   (Excel: 42.274)\n"
    f"  f_2      = {f_2:>10.3f} Hz\n"
    f"  T_2      = {T_2:>10.3f} s   (Excel: 0.149)\n\n"
    f"  phi_2    = [{phi_2[0]:>6.3f}, {phi_2[1]:>6.3f}]\n\n"
    "═══════════════════════════════════════════════\n"
    f"  k_piso = {k_entrepiso:>10.2f} t/m\n"
    f"  m_piso = {m_piso:>10.4f} t.s2/m"
)

ax4.text(0.5, 0.5, resultados, transform=ax4.transAxes,
         ha='center', va='center', fontsize=11, family='monospace',
         linespacing=2.0,
         bbox=dict(boxstyle='round,pad=0.9',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# --- Panel (e): FORMA MODAL ---
ax5 = fig.add_subplot(gs[1, 2])

ax5.plot([0, phi_2[0]], [0, 1], 's-', color=COLORES['modo2'],
         linewidth=2.5, markersize=12, label=f'Modo 2 (T2={T_2:.3f}s)')
ax5.plot([phi_2[0], phi_2[1]], [1, 2], 's-', color=COLORES['modo2'],
         linewidth=2.5, markersize=12)

ax5.text(phi_2[0] + 0.05, 1, f'{phi_2[0]:.3f}',
         fontsize=10, fontweight='bold', color=COLORES['modo2'], va='center')
ax5.text(phi_2[1] - 0.05, 2, f'{phi_2[1]:.3f}',
         fontsize=10, fontweight='bold', color=COLORES['modo2'],
         va='center', ha='right')

ax5.axhline(y=1, color='gray', linestyle=':', alpha=0.3)
ax5.axhline(y=2, color='gray', linestyle=':', alpha=0.3)
ax5.axvline(x=0, color='black', linestyle='-', linewidth=0.8)

ax5.set_xlabel('Desplazamiento relativo', fontsize=10)
ax5.set_ylabel('Nivel', fontsize=10)
ax5.set_yticks([1, 2])
ax5.set_yticklabels(['Piso 1', 'Piso 2'])
ax5.set_title('(e) FORMA MODAL DEL MODO 2',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax5.legend(fontsize=9, loc='upper left')
ax5.grid(alpha=0.3)

# ============================================================================
# MENSAJES OPORTUNOS FLOTANTES
# ============================================================================

msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Excel RESILIENCIA\n"
    "  Modelo base 38x38 cm"
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
    "  Shear building (2 GDL)\n"
    "  det(K - λM) = 0\n"
    "  λ1 < λ2"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# GUARDAR
# ============================================================================

carpeta = "Resultados_M07_6_2"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_6_2_periodo_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"\nImagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.6.2 COMPLETADO — PERIODO 2 (LAMBDA 2)")
print("=" * 80)
print(f"  lambda_2 = {lambda_2:.3f}   (Excel: 1787.103)")
print(f"  omega_2  = {omega_2:.3f} rad/s   (Excel: 42.274)")
print(f"  f_2      = {f_2:.3f} Hz")
print(f"  T_2      = {T_2:.3f} s   (Excel: 0.149)")
print(f"  phi_2    = [{phi_2[0]:.3f}, {phi_2[1]:.3f}]")
print("=" * 80)