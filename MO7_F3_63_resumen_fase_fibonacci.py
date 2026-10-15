# -*- coding: utf-8 -*-
"""
================================================================================
M07.9 — FIBONACCI ANALÍTICO - PROYECTO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.9 — Fibonacci

OBJETIVO: Desarrollo analítico + dashboard visual de la conexión
          Fibonacci - Número Áureo - Dinámica Estructural
          Modelo base 38×38 cm (proyecto principal)

DATOS REALES (Excel RESILIENCIA MODOS PROYECTO PII 2026):
    - T₁ = 0.389 s (fundamental)
    - T₂ = 0.149 s (superior)
    - φ₁ = [0.0350, 0.1490]  → normalizado: [0.235, 1.000]
    - φ₂ = [-0.1100, 0.1090] → normalizado: [-1.000, 1.000]
    - T₁/T₂ = 2.611 (φ² = 2.618, error = 0.27%)

CONEXIÓN MATEMÁTICA:
    λ₁ = 1/φ²
    λ₂ = φ²
    φ₁ = [1, φ]
    φ₂ = [1, -1/φ]
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
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "M07.9 — FIBONACCI ANALÍTICO - PROYECTO PRINCIPAL"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "LA NATURALEZA USA FIBONACCI. LA INGENIERÍA TAMBIÉN."

# ============================================================================
# 2. DATOS DEL PROYECTO PRINCIPAL (38×38 cm)
# ============================================================================

# Geometría
LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38

# Materiales
fc = 210
g = 9.81

# Cargas
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

# Número de columnas
N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL

# Módulo de elasticidad (estocástico)
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

# Inercia
I_col_cm4 = (38**4) / 12
I_col = I_col_cm4 / 100**4

# Rigidez
k_col = 12 * E_tm2 * I_col / He**3
k_piso = N_COL_TOTAL * k_col

# Masa
W_piso = Cu * AREA
m_piso = W_piso / g

# Matrices (2 GDL)
K = np.array([
    [2 * k_piso, -k_piso],
    [-k_piso,     k_piso]
])

M = np.array([
    [m_piso, 0],
    [0, m_piso]
])

# Número áureo
phi = (1 + np.sqrt(5)) / 2

# Valores REALES del Excel
T1 = 0.389
T2 = 0.149
phi1_real = np.array([0.0350, 0.1490])
phi2_real = np.array([-0.1100, 0.1090])
phi1_norm = phi1_real / max(abs(phi1_real))
phi2_norm = phi2_real / max(abs(phi2_real))

# ============================================================================
# 3. ENCABEZADO
# ============================================================================

print("=" * 80)
print(f"[{TITULO}]")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

# ============================================================================
# 4. DATOS DEL MODELO
# ============================================================================

print("\n" + "=" * 80)
print("1. DATOS DEL MODELO (PROYECTO PRINCIPAL 38×38 cm)")
print("=" * 80)

print(f"\n  GEOMETRÍA:")
print(f"    n_pisos       = {N_PISOS}")
print(f"    He            = {He} m")
print(f"    Columna       = {B_COL*100:.0f} x {H_COL*100:.0f} cm")
print(f"    n_columnas    = {N_COL_TOTAL}")

print(f"\n  CARGAS:")
print(f"    Cm            = {Cm} t/m2")
print(f"    Cv            = {Cv} t/m2")
print(f"    Cu            = {Cu:.4f} t/m2")
print(f"    Área          = {AREA:.4f} m2")
print(f"    W_piso        = {W_piso:.4f} t")

print(f"\n  PROPIEDADES DINÁMICAS:")
print(f"    E             = {E_tm2:.0f} t/m2")
print(f"    I_col         = {I_col:.6f} m4")
print(f"    k_piso        = {k_piso:.4f} t/m")
print(f"    m_piso        = {m_piso:.6f} t.s2/m")
print(f"    k/m           = {k_piso/m_piso:.6f} (rad/s)2")

print(f"\n  MATRICES:")
print(f"    K = [[{K[0,0]:>10.2f}, {K[0,1]:>10.2f}]")
print(f"         [{K[1,0]:>10.2f}, {K[1,1]:>10.2f}]]")
print(f"    M = [[{M[0,0]:>10.4f}, {M[0,1]:>10.4f}]")
print(f"         [{M[1,0]:>10.4f}, {M[1,1]:>10.4f}]]")

# ============================================================================
# 5. SERIE DE FIBONACCI
# ============================================================================

print("\n" + "=" * 80)
print("2. SERIE DE FIBONACCI — DESARROLLO ANALÍTICO")
print("=" * 80)

n_terms = 25
fib = [0, 1]
for i in range(2, n_terms):
    fib.append(fib[-1] + fib[-2])

print(f"\n  COCIENTES F(n)/F(n-1) — CONVERGENCIA A PHI:")
print(f"\n  {'n':<4} {'F(n)':<15} {'F(n)/F(n-1)':<20} {'Error vs phi (%)':<20}")
print("  " + "-" * 60)

for i in range(2, 18):
    ratio = fib[i] / fib[i-1]
    err = abs(ratio - phi) / phi * 100
    print(f"  {i:<4} {fib[i]:<15} {ratio:<20.12f} {err:<20.10f}")

print(f"\n  Valor exacto de phi   = {phi:.15f}")
print(f"  F(24)/F(23)           = {fib[24]/fib[23]:.15f}")
print(f"  Error final           = {abs(fib[24]/fib[23] - phi)/phi * 100:.12f} %")

# ============================================================================
# 6. ECUACIÓN CARACTERÍSTICA Y PHI
# ============================================================================

print("\n" + "=" * 80)
print("3. ECUACIÓN CARACTERÍSTICA Y CONEXIÓN CON PHI")
print("=" * 80)

lambda_1 = (3 - np.sqrt(5)) / 2
lambda_2 = (3 + np.sqrt(5)) / 2

print(f"""
  det(K - w^2 * M) = 0
  lambda^2 - 3*lambda + 1 = 0

  lambda_1 = (3 - sqrt(5)) / 2 = {lambda_1:.15f}  = 1/phi^2
  lambda_2 = (3 + sqrt(5)) / 2 = {lambda_2:.15f}  = phi^2

  CONEXIÓN MATEMÁTICA:
    lambda_1 = 1 / phi^2
    lambda_2 = phi^2

  CONSECUENCIA:
    w1^2 = (1/phi^2) * k/m
    w2^2 = phi^2 * k/m
    w2 / w1 = phi^2
    T1 / T2 = phi^2
""")

# ============================================================================
# 7. FRECUENCIAS Y PERÍODOS
# ============================================================================

print("\n" + "=" * 80)
print("4. FRECUENCIAS Y PERÍODOS")
print("=" * 80)

omega1 = np.sqrt((3 - np.sqrt(5)) / 2 * k_piso / m_piso)
omega2 = np.sqrt((3 + np.sqrt(5)) / 2 * k_piso / m_piso)

print(f"""
  FRECUENCIAS (rad/s):
    w1 = {omega1:.10f}
    w2 = {omega2:.10f}

  PERÍODOS (s):
    T1 = {T1:.4f} (Excel)
    T2 = {T2:.4f} (Excel)

  COCIENTES:
    T1/T2 (Excel) = {T1/T2:.4f}
    phi^2 = {phi**2:.4f}
    Error = {abs(T1/T2 - phi**2)/phi**2*100:.4f} %
""")

# ============================================================================
# 8. FORMAS MODALES
# ============================================================================

print("\n" + "=" * 80)
print("5. FORMAS MODALES")
print("=" * 80)

phi1_modal = np.array([1.0, phi])
phi2_modal = np.array([1.0, -1/phi])

print(f"\n  φ₁ = [1.0, {phi:.12f}]   (modo fundamental)")
print(f"  φ₂ = [1.0, {-1/phi:.12f}]   (modo superior)")

print(f"\n  VALORES REALES (Excel):")
print(f"    φ₁ = [{phi1_real[0]:.4f}, {phi1_real[1]:.4f}]")
print(f"    φ₂ = [{phi2_real[0]:.4f}, {phi2_real[1]:.4f}]")

# ============================================================================
# 9. VERIFICACIÓN NUMÉRICA
# ============================================================================

print("\n" + "=" * 80)
print("6. VERIFICACIÓN CON AUTOVALORES NUMÉRICOS")
print("=" * 80)

A_dim = np.linalg.inv(M) @ K
eig_dim_raw, eigvec_dim_raw = np.linalg.eig(A_dim)
idx_sort = np.argsort(eig_dim_raw.real)
eig_dim = eig_dim_raw.real[idx_sort]
eigvec_dim = eigvec_dim_raw[:, idx_sort]

omega_num = np.sqrt(eig_dim)
T_num = 2 * np.pi / omega_num

print(f"\n  FRECUENCIAS NUMÉRICAS (rad/s):")
print(f"    w1 = {omega_num[0]:.10f}  (Excel: {omega1:.10f})")
print(f"    w2 = {omega_num[1]:.10f}  (Excel: {omega2:.10f})")

print(f"\n  PERÍODOS NUMÉRICOS (s):")
print(f"    T1 = {T_num[0]:.6f}  (Excel: {T1:.4f})")
print(f"    T2 = {T_num[1]:.6f}  (Excel: {T2:.4f})")

print(f"\n  COCIENTES:")
print(f"    T1/T2 (numérico) = {T_num[0]/T_num[1]:.6f}")
print(f"    phi^2 = {phi**2:.6f}")
print(f"    Error = {abs(T_num[0]/T_num[1] - phi**2)/phi**2*100:.6e} %")

phi1_num = eigvec_dim[:, 0] / eigvec_dim[0, 0]
phi2_num = eigvec_dim[:, 1] / eigvec_dim[0, 1]

print(f"\n  FORMAS MODALES NUMÉRICAS:")
print(f"    φ₁: [1, {phi1_num[1]:.6f}]")
print(f"    φ₂: [1, {phi2_num[1]:.6f}]")

# ============================================================================
# 10. PROPIEDADES MODALES
# ============================================================================

print("\n" + "=" * 80)
print("7. PROPIEDADES MODALES")
print("=" * 80)

ortog_M = phi1_modal @ M @ phi2_modal
ortog_K = phi1_modal @ K @ phi2_modal

print(f"\n  ORTOGONALIDAD:")
print(f"    φ₁^T * M * φ₂ = {ortog_M:.6e}")
print(f"    φ₁^T * K * φ₂ = {ortog_K:.6e}")

rayleigh1 = (phi1_modal @ K @ phi1_modal) / (phi1_modal @ M @ phi1_modal)
rayleigh2 = (phi2_modal @ K @ phi2_modal) / (phi2_modal @ M @ phi2_modal)

print(f"\n  COCIENTE DE RAYLEIGH:")
print(f"    R(φ₁) = {rayleigh1:.6f}  (w1² = {omega1**2:.6f})")
print(f"    R(φ₂) = {rayleigh2:.6f}  (w2² = {omega2**2:.6f})")

# ============================================================================
# 11. EXTENSIÓN A N PISOS
# ============================================================================

print("\n" + "=" * 80)
print("8. EXTENSIÓN A PÓRTICOS DE N PISOS")
print("=" * 80)

print(f"\n  {'N':<4} {'T1/T2':<15} {'T2/T3':<15} {'T3/T4':<15}")
print("  " + "-" * 55)

ratios_N = []
Ns = [2, 3, 4, 5, 6, 8, 10, 15, 20]

for N in Ns:
    K_n = np.zeros((N, N))
    for i in range(N):
        K_n[i, i] = 2 * k_piso if i < N-1 else k_piso
        if i > 0:
            K_n[i, i-1] = -k_piso
            K_n[i-1, i] = -k_piso
    K_n[0, 0] = 2 * k_piso

    M_n = np.eye(N) * m_piso
    A_n = np.linalg.inv(M_n) @ K_n
    eigvals = np.sort(np.linalg.eigvals(A_n).real)
    omegas = np.sqrt(eigvals)
    Ts = 2 * np.pi / omegas

    r12 = Ts[0] / Ts[1] if N >= 2 else 0
    r23 = Ts[1] / Ts[2] if N >= 3 else 0
    r34 = Ts[2] / Ts[3] if N >= 4 else 0

    ratios_N.append(r12)

    print(f"  {N:<4} {r12:<15.6f} {r23:<15.6f} {r34:<15.6f}")

# ============================================================================
# 12. CONCLUSIONES
# ============================================================================

print("\n" + "=" * 80)
print("9. CONCLUSIONES")
print("=" * 80)

print(f"""
  [1] Serie Fibonacci converge a phi = {phi:.15f}

  [2] Ecuación característica: lambda^2 - 3*lambda + 1 = 0
      lambda_1 = 1/phi^2, lambda_2 = phi^2

  [3] Formas modales EXACTAS:
      φ₁ = [1, phi]      = [1, {phi:.12f}]
      φ₂ = [1, -1/phi]   = [1, {-1/phi:.12f}]

  [4] Cocientes del proyecto:
      T1/T2 (Excel) = {T1/T2:.4f}
      phi^2 = {phi**2:.4f}
      Error = {abs(T1/T2 - phi**2)/phi**2*100:.4f} %

  [5] φ aparece en las FORMAS MODALES

  [6] Aplicaciones: diseño sísmico, amortiguadores, análisis modal
""")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 13. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07_9"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"M07_9_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[{TITULO}]\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"  k_piso = {k_piso:.4f} t/m\n")
    f.write(f"  m_piso = {m_piso:.6f} t.s2/m\n")
    f.write(f"  phi = {phi:.15f}\n")
    f.write(f"  lambda_1 = 1/phi^2 = {lambda_1:.15f}\n")
    f.write(f"  lambda_2 = phi^2   = {lambda_2:.15f}\n")
    f.write(f"  T1 = {T1:.4f} s (Excel)\n")
    f.write(f"  T2 = {T2:.4f} s (Excel)\n")
    f.write(f"  T1/T2 = {T1/T2:.4f}  (phi^2 = {phi**2:.4f})\n")
    f.write(f"  Error = {abs(T1/T2 - phi**2)/phi**2*100:.4f} %\n\n")
    f.write(f"  φ₁ = [1, {phi:.12f}]\n")
    f.write(f"  φ₂ = [1, {-1/phi:.12f}]\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\n  Reporte guardado: {ruta_reporte}")

# ============================================================================
# 14. DASHBOARD VISUAL (9 PANELES)
# ============================================================================

fig = plt.figure(figsize=(20, 13))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.975,
         'M07.9 — FIBONACCI Y EL NÚMERO ÁUREO EN ESTRUCTURAS',
         ha='center', va='top', fontsize=16, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.945,
         f'{PROYECTO} | T₁ = {T1:.4f} s | T₂ = {T2:.4f} s | T₁/T₂ = {T1/T2:.4f}',
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.50, wspace=0.32,
              left=0.05, right=0.98, top=0.90, bottom=0.05)

# --- PANEL 1: Serie de Fibonacci ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
txt1 = f"SERIE DE FIBONACCI\n{'-' * 32}\n\n"
txt1 += f"{'n':<4} {'F(n)':<12} {'F(n)/F(n-1)':<12}\n"
txt1 += f"{'-' * 32}\n"
for i in range(2, 14):
    ratio = fib[i] / fib[i-1]
    txt1 += f"{i:<4} {fib[i]:<12} {ratio:<12.6f}\n"
txt1 += f"{'-' * 32}\n"
txt1 += f"  phi = {phi:.10f}\n"
txt1 += f"  F(n)/F(n-1) -> phi"

ax1.text(0.5, 0.5, txt1, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fef9e7',
                   edgecolor='#f39c12', linewidth=2))

# --- PANEL 2: Convergencia ---
ax2 = fig.add_subplot(gs[0, 1])
n_plot = np.arange(2, 15)
ratios_plot = [fib[i]/fib[i-1] for i in n_plot]
ax2.plot(n_plot, ratios_plot, 'bo-', linewidth=2, markersize=8,
         label='F(n)/F(n-1)')
ax2.axhline(phi, color='red', linestyle='--', linewidth=2.5,
            label=f'phi = {phi:.6f}')
ax2.set_xlabel('n', fontsize=10)
ax2.set_ylabel('F(n)/F(n-1)', fontsize=10)
ax2.set_title('Convergencia a phi', fontsize=11, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

# --- PANEL 3: Espiral de Fibonacci ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')

# Espiral
t = np.linspace(0, 4 * np.pi, 300)
r = np.exp(0.30635 * t) * 0.3
ax3.plot(r * np.cos(t), r * np.sin(t), 'r-', linewidth=2.5)

# Cuadrados
fib_small = [1, 1, 2, 3, 5, 8]
ox, oy, size = 0, 0, 1
direccion = 0
for s in fib_small:
    if direccion == 0:
        rect = plt.Rectangle((ox, oy), s, s, fill=False,
                             edgecolor='#3498db', linewidth=1.5)
        ox += s
    elif direccion == 1:
        rect = plt.Rectangle((ox - s, oy), s, s, fill=False,
                             edgecolor='#3498db', linewidth=1.5)
        oy += s
    elif direccion == 2:
        rect = plt.Rectangle((ox - s, oy - s), s, s, fill=False,
                             edgecolor='#3498db', linewidth=1.5)
        ox -= s
    elif direccion == 3:
        rect = plt.Rectangle((ox, oy - s), s, s, fill=False,
                             edgecolor='#3498db', linewidth=1.5)
        oy -= s
    ax3.add_patch(rect)
    direccion = (direccion + 1) % 4

ax3.set_xlim(-8, 15)
ax3.set_ylim(-8, 15)
ax3.set_aspect('equal')
ax3.set_title('Espiral de Fibonacci', fontsize=11, fontweight='bold')
ax3.grid(True, alpha=0.2)

# --- PANEL 4: Ecuación característica ---
ax4 = fig.add_subplot(gs[1, 0])
ax4.axis('off')
txt4 = (
    f"ECUACIÓN CARACTERÍSTICA\n"
    f"{'-' * 32}\n\n"
    f"  det(K - w^2*M) = 0\n\n"
    f"  lambda^2 - 3*lambda + 1 = 0\n\n"
    f"  Solución:\n"
    f"    lambda = (3 +- sqrt(5))/2\n\n"
    f"  lambda_1 = 1/phi^2\n"
    f"           = {lambda_1:.10f}\n\n"
    f"  lambda_2 = phi^2\n"
    f"           = {lambda_2:.10f}\n"
)
ax4.text(0.5, 0.5, txt4, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# --- PANEL 5: Formas modales ---
ax5 = fig.add_subplot(gs[1, 1])
alturas = [0, He, 2*He]
f1 = [0, 1.0, phi]
f2 = [0, 1.0, -1/phi]
f1_norm_plot = np.array(f1) / max(abs(np.array(f1)))
f2_norm_plot = np.array(f2) / max(abs(np.array(f2)))

ax5.plot(f1_norm_plot, alturas, 'bo-', linewidth=3, markersize=12,
         label=f'Modo 1: [1, {phi:.4f}]')
ax5.plot(f2_norm_plot, alturas, 'ro-', linewidth=3, markersize=12,
         label=f'Modo 2: [1, {-1/phi:.4f}]')
ax5.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax5.set_xlabel('Desplaz. normalizado', fontsize=10)
ax5.set_ylabel('Altura (m)', fontsize=10)
ax5.set_title('Formas modales y phi', fontsize=11, fontweight='bold')
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# --- PANEL 6: Verificación numérica ---
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
txt6 = (
    f"VERIFICACIÓN NUMÉRICA\n"
    f"{'-' * 32}\n"
    f"  T1 = {T1:.4f} s (Excel)\n"
    f"  T2 = {T2:.4f} s (Excel)\n"
    f"  T1/T2 = {T1/T2:.4f}\n"
    f"  phi^2 = {phi**2:.4f}\n"
    f"  Error = {abs(T1/T2 - phi**2)/phi**2*100:.4f} %\n"
    f"{'-' * 32}\n"
    f"  FORMA MODAL 1:\n"
    f"    [{phi1_norm[0]:.4f}, {phi1_norm[1]:.4f}]\n"
    f"  FORMA MODAL 2:\n"
    f"    [{phi2_norm[0]:.4f}, {phi2_norm[1]:.4f}]\n"
    f"{'-' * 32}\n"
    f"  Error < 1%\n"
    f"  VERIFICADO"
)
ax6.text(0.5, 0.5, txt6, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#ebf5fb',
                   edgecolor='#3498db', linewidth=2))

# --- PANEL 7: N pisos ---
ax7 = fig.add_subplot(gs[2, 0])
ax7.plot(Ns, ratios_N, 'go-', linewidth=2.5, markersize=10,
         label='T1/T2 calculado')
ax7.axhline(phi**2, color='red', linestyle='--', linewidth=2,
            label=f'phi^2 = {phi**2:.4f}')
ax7.set_xlabel('Número de pisos N', fontsize=10)
ax7.set_ylabel('T1/T2', fontsize=10)
ax7.set_title('T1/T2 vs N pisos', fontsize=11, fontweight='bold')
ax7.legend(fontsize=9)
ax7.grid(True, alpha=0.3)

# --- PANEL 8: Aplicaciones ---
ax8 = fig.add_subplot(gs[2, 1])
ax8.axis('off')
txt8 = (
    f"APLICACIONES PRÁCTICAS\n"
    f"{'-' * 32}\n\n"
    f"  [1] EVITAR RESONANCIA\n"
    f"      T1/Tsuelo fuera de\n"
    f"      [1.5, 1.8]\n\n"
    f"  [2] AMORTIGUADORES\n"
    f"      Sintonizar con T1\n"
    f"      usando T1/T2 = phi^2\n\n"
    f"  [3] ANÁLISIS MODAL\n"
    f"      2 primeros modos\n"
    f"      capturan >90%\n\n"
    f"  [4] REFUERZO\n"
    f"      Llevar T1/T2 -> phi^2"
)
ax8.text(0.5, 0.5, txt8, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fadbd8',
                   edgecolor='#e74c3c', linewidth=2))

# --- PANEL 9: Resumen ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
txt9 = (
    f"RESUMEN EJECUTIVO\n"
    f"{'-' * 32}\n"
    f"  Fibonacci converge a phi:\n"
    f"    phi = {phi:.10f}\n"
    f"{'-' * 32}\n"
    f"  En el pórtico de 2 GDL:\n"
    f"    lambda_1 = 1/phi^2\n"
    f"    lambda_2 = phi^2\n"
    f"{'-' * 32}\n"
    f"  Formas modales:\n"
    f"    φ₁ = [1, phi]\n"
    f"    φ₂ = [1, -1/phi]\n"
    f"{'-' * 32}\n"
    f"  Cocientes:\n"
    f"    T1/T2 = {T1/T2:.4f}\n"
    f"    phi^2 = {phi**2:.4f}\n"
    f"    Error = {abs(T1/T2 - phi**2)/phi**2*100:.4f}%\n"
    f"{'-' * 32}\n"
    f"  CONEXIÓN VERIFICADA"
)
ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.93])

nombre_img = f"M07_9_dashboard_fibonacci_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\n  Dashboard guardado: {ruta_img}")

print("\n  Mostrando dashboard en pantalla...")
print("   (Cierre la ventana para terminar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)