# -*- coding: utf-8 -*-
"""
================================================================================
M08.2 — METODO DE MONTE CARLO CON NUEVAS LUCES (hasta 6 m)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.2 — Monte Carlo

OBJETIVO: Cuantificar la incertidumbre en T1, T2 y formas modales
          para edificaciones de mediana altura con luces de hasta 6 m.

CARACTERÍSTICAS:
    - Edificación de 2 pisos (mediana altura)
    - Luces de hasta 6 m
    - 10,000 simulaciones Monte Carlo
    - Variables: fc, secciones, cargas, alturas
    - Distribuciones: Normal (geométricas), Gumbel (cargas)

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
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# Semilla para reproducibilidad
np.random.seed(42)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "METODO DE MONTE CARLO - LUCES HASTA 6 m"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La incertidumbre no se elimina: se cuantifica."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. VALORES NOMINALES (NUEVAS LUCES HASTA 6 m)
# ============================================================================

n_pisos = 2
He_nom = 3.0
b_col_nom, h_col_nom = 0.38, 0.38
Cm_nom, Cv_nom = 0.62, 0.20
fc_nom = 210
g = 9.81
n_columnas = 16  # 4x4 columnas

# NUEVAS LUCES (hasta 6 m)
LUCES_X = [6.00, 5.50, 6.00]       # 3 vanos
LUCES_Y = [5.00, 6.00, 5.00, 5.50] # 4 vanos

L1, L2, L3 = LUCES_X
L4, L5, L6, L7 = LUCES_Y

# Área tributaria por columna
At = (L1/2 + L2/2 + L3/2) / 3 * (L4/2 + L5/2 + L6/2 + L7/2) / 4

# ============================================================================
# 3. COEFICIENTES DE VARIACION (CoV)
# ============================================================================

CoV = {
    'fc': 0.15,       # 15% variabilidad del concreto
    'b_col': 0.03,    # 3% tolerancia dimensional
    'h_col': 0.03,
    'Cm': 0.08,       # 8% variabilidad carga muerta
    'Cv': 0.25,       # 25% variabilidad carga viva
    'He': 0.02,       # 2% tolerancia de encofrado
    'L': 0.02,        # 2% variabilidad de luces
}

# ============================================================================
# 4. ANALISIS DETERMINISTA (nominal)
# ============================================================================

def calcular_T(fc, b_col, h_col, Cm, Cv, He, factor_L=1.0):
    """Calcula T1 y T2 dados los parametros."""
    E_tm2 = 15100 * np.sqrt(fc) * 10
    I_col = (b_col * h_col**3) / 12
    Cu = 1.2 * Cm + 1.6 * Cv
    
    # Área tributaria con factor de luces
    At_local = At * factor_L**2
    
    W_piso = Cu * At_local
    m = W_piso / g
    k = n_columnas * 12 * E_tm2 * I_col / He**3

    K = np.array([[2*k, -k], [-k, k]])
    M = np.array([[m, 0], [0, m]])

    M_inv = np.linalg.inv(M)
    A = M_inv @ K
    eigenvalues = np.linalg.eigvals(A)
    eigenvalues = np.sort(eigenvalues)

    omega1 = np.sqrt(eigenvalues[0])
    omega2 = np.sqrt(eigenvalues[1])
    T1 = 2 * np.pi / omega1
    T2 = 2 * np.pi / omega2
    return T1, T2, k, m

# Nominal
T1_nom, T2_nom, k_nom, m_nom = calcular_T(
    fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom
)

print("=" * 80)
print(f"[M08.2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n VALORES NOMINALES:")
print(f"  fc    = {fc_nom} kg/cm2")
print(f"  b_col = {b_col_nom} m")
print(f"  h_col = {h_col_nom} m")
print(f"  Cm    = {Cm_nom} t/m2")
print(f"  Cv    = {Cv_nom} t/m2")
print(f"  He    = {He_nom} m")
print(f"  N columnas = {n_columnas}")
print(f"  LUCES_X = {LUCES_X}")
print(f"  LUCES_Y = {LUCES_Y}")
print(f"  Área tributaria = {At:.4f} m2")

print(f"\n  k = {k_nom:.2f} t/m")
print(f"  m = {m_nom:.6f} t.s2/m")
print(f"  T1_nom = {T1_nom:.4f} s")
print(f"  T2_nom = {T2_nom:.4f} s")

print("\n" + "=" * 80)
print("COEFICIENTES DE VARIACION (CoV)")
print("=" * 80)
for var, cov in CoV.items():
    print(f"  {var:<10} = {cov*100:>5.1f} %")

# ============================================================================
# 5. SIMULACION MONTE CARLO
# ============================================================================

N_SIM = 10000

print("\n" + "=" * 80)
print(f"SIMULACION MONTE CARLO ({N_SIM} corridas)")
print("=" * 80)

def norm_var(nom, cov):
    return np.random.normal(nom, nom * cov, N_SIM)

def gumbel_var(nom, cov):
    beta = nom * cov * np.sqrt(6) / np.pi
    mu = nom - 0.5772 * beta
    return np.random.gumbel(mu, beta, N_SIM)

# Generar muestras
fc_s = np.abs(norm_var(fc_nom, CoV['fc']))
b_col_s = np.abs(norm_var(b_col_nom, CoV['b_col']))
h_col_s = np.abs(norm_var(h_col_nom, CoV['h_col']))
Cm_s = np.abs(norm_var(Cm_nom, CoV['Cm']))
Cv_s = np.abs(gumbel_var(Cv_nom, CoV['Cv']))
He_s = np.abs(norm_var(He_nom, CoV['He']))
L_factor_s = np.abs(norm_var(1.0, CoV['L']))

print(f"  Distribuciones generadas")
print(f"  fc:  media={fc_s.mean():.2f}  std={fc_s.std():.2f}")
print(f"  Cm:  media={Cm_s.mean():.4f}  std={Cm_s.std():.4f}")
print(f"  Cv:  media={Cv_s.mean():.4f}  std={Cv_s.std():.4f}")

# Simulación vectorizada
E_s = 15100 * np.sqrt(fc_s) * 10
I_s = (b_col_s * h_col_s**3) / 12
Cu_s = 1.2 * Cm_s + 1.6 * Cv_s
At_s = At * L_factor_s**2
W_s = Cu_s * At_s
m_s = W_s / g
k_s = n_columnas * 12 * E_s * I_s / He_s**3

# Autovalores vectorizados
omega2_1_s = (3 - np.sqrt(5)) / 2 * k_s / m_s
omega2_2_s = (3 + np.sqrt(5)) / 2 * k_s / m_s

omega1_s = np.sqrt(omega2_1_s)
omega2_s = np.sqrt(omega2_2_s)
T1_s = 2 * np.pi / omega1_s
T2_s = 2 * np.pi / omega2_s

print(f"  Simulacion completa: {N_SIM} corridas")

# ============================================================================
# 6. ESTADISTICAS
# ============================================================================

def stats(x, nombre):
    media = np.mean(x)
    std = np.std(x, ddof=1)
    cv = std / media
    p5 = np.percentile(x, 5)
    p50 = np.percentile(x, 50)
    p95 = np.percentile(x, 95)
    return {
        'nombre': nombre,
        'media': media, 'std': std, 'cv': cv,
        'p5': p5, 'p50': p50, 'p95': p95,
        'min': np.min(x), 'max': np.max(x)
    }

stats_T1 = stats(T1_s, 'T1')
stats_T2 = stats(T2_s, 'T2')
stats_k = stats(k_s, 'k')
stats_m = stats(m_s, 'm')

print("\n" + "=" * 80)
print("ESTADISTICAS DE LOS RESULTADOS")
print("=" * 80)

for s in [stats_T1, stats_T2]:
    print(f"\n  {s['nombre']}:")
    print(f"    Media      = {s['media']:.4f} s")
    print(f"    Desv. std  = {s['std']:.4f} s")
    print(f"    CoV        = {s['cv']*100:.2f} %")
    print(f"    P5         = {s['p5']:.4f} s")
    print(f"    P50        = {s['p50']:.4f} s")
    print(f"    P95        = {s['p95']:.4f} s")

IC95_T1 = (stats_T1['p5'], stats_T1['p95'])
prob_T1_alto = np.mean(T1_s > T1_nom * 1.2) * 100

print(f"\n  COMPARACION CON NOMINAL:")
print(f"    T1_nom = {T1_nom:.4f} s")
print(f"    T1_media_MC = {stats_T1['media']:.4f} s")
print(f"    Diferencia  = {abs(stats_T1['media'] - T1_nom)/T1_nom*100:.2f} %")
print(f"\n  IC 95% T1: [{IC95_T1[0]:.4f}, {IC95_T1[1]:.4f}] s")
print(f"  P(T1 > 1.2 * T1_nom) = {prob_T1_alto:.2f} %")

# ============================================================================
# 7. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(20, 13))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.975,
         'M08.2 - MONTE CARLO - LUCES HASTA 6 m - MEDIANA ALTURA',
         ha='center', va='top', fontsize=16, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.945, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.90, bottom=0.08)

# --- Panel 1: Histograma T1 ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(T1_s, bins=50, color='#3498db', edgecolor='black', alpha=0.7)
ax1.axvline(T1_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Nominal = {T1_nom:.4f}')
ax1.axvline(stats_T1['media'], color='green', linestyle='-', linewidth=2.5,
            label=f'Media MC = {stats_T1["media"]:.4f}')
ax1.axvspan(stats_T1['p5'], stats_T1['p95'], alpha=0.2,
            color='orange', label='IC 95%')
ax1.set_xlabel('T1 (s)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title(f'Distribucion T1 ({N_SIM} sim.)',
              fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# --- Panel 2: Histograma T2 ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(T2_s, bins=50, color='#e74c3c', edgecolor='black', alpha=0.7)
ax2.axvline(T2_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Nominal = {T2_nom:.4f}')
ax2.axvline(stats_T2['media'], color='green', linestyle='-', linewidth=2.5,
            label=f'Media MC = {stats_T2["media"]:.4f}')
ax2.set_xlabel('T2 (s)', fontsize=10)
ax2.set_ylabel('Frecuencia', fontsize=10)
ax2.set_title(f'Distribucion T2 ({N_SIM} sim.)',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# --- Panel 3: Tabla resumen ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
txt3 = (
    f"RESUMEN DE ESTADISTICAS\n"
    f"{'-' * 36}\n"
    f"  Simulaciones: {N_SIM}\n"
    f"  Luces max: 6.00 m\n"
    f"{'-' * 36}\n"
    f"  T1 NOMINAL  = {T1_nom:.4f} s\n"
    f"  T1 MEDIA MC = {stats_T1['media']:.4f} s\n"
    f"  T1 STD      = {stats_T1['std']:.4f} s\n"
    f"  T1 CoV      = {stats_T1['cv']*100:.2f} %\n"
    f"  T1 P5       = {stats_T1['p5']:.4f} s\n"
    f"  T1 P95      = {stats_T1['p95']:.4f} s\n"
    f"{'-' * 36}\n"
    f"  T2 MEDIA MC = {stats_T2['media']:.4f} s\n"
    f"  T2 CoV      = {stats_T2['cv']*100:.2f} %\n"
    f"{'-' * 36}\n"
    f"  P(T1 > 1.2*T1_nom) = {prob_T1_alto:.2f} %\n"
    f"{'-' * 36}\n"
    f"  Incertidumbre T1\n"
    f"  = {stats_T1['cv']*100:.1f} %"
)
ax3.text(0.5, 0.5, txt3, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# --- Panel 4: Convergencia ---
ax4 = fig.add_subplot(gs[1, 0])
medias_acum = np.cumsum(T1_s) / np.arange(1, N_SIM + 1)
ax4.plot(np.arange(1, N_SIM + 1), medias_acum, 'b-', linewidth=1.5)
ax4.axhline(T1_nom, color='red', linestyle='--', linewidth=2,
            label=f'Nominal = {T1_nom:.4f}')
ax4.axhline(stats_T1['media'], color='green', linestyle=':',
            linewidth=2, label=f'Media MC = {stats_T1["media"]:.4f}')
ax4.set_xlabel('Numero de simulaciones', fontsize=10)
ax4.set_ylabel('Media acumulada de T1 (s)', fontsize=10)
ax4.set_title('Convergencia de la media',
              fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# --- Panel 5: Sensibilidad (tornado) ---
ax5 = fig.add_subplot(gs[1, 1])

vars_names = ['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L']
sens_values = []

for var in vars_names:
    params_nom = [fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom]
    if var == 'L':
        T1_hi = calcular_T(*params_nom, factor_L=1.10)[0]
        T1_lo = calcular_T(*params_nom, factor_L=0.90)[0]
    else:
        idx = vars_names.index(var)
        params_hi = params_nom.copy()
        params_hi[idx] *= 1.10
        params_lo = params_nom.copy()
        params_lo[idx] *= 0.90
        T1_hi = calcular_T(*params_hi)[0]
        T1_lo = calcular_T(*params_lo)[0]
    sens = (T1_hi - T1_lo) / (2 * T1_nom) * 100
    sens_values.append(sens)

order = np.argsort(np.abs(sens_values))
vars_sorted = [vars_names[i] for i in order]
sens_sorted = [sens_values[i] for i in order]

colores_sens = ['#2ecc71' if v > 0 else '#e74c3c' for v in sens_sorted]
ax5.barh(vars_sorted, sens_sorted, color=colores_sens,
         edgecolor='black', linewidth=1.5)
ax5.axvline(0, color='black', linestyle='-', linewidth=1)
ax5.set_xlabel('Cambio en T1 (%) cuando variable varia +-10%', fontsize=9)
ax5.set_title('Sensibilidad de T1 (luces 6 m)',
              fontsize=11, fontweight='bold')
ax5.grid(axis='x', linestyle='--', alpha=0.3)

# --- Panel 6: Boxplot ---
ax6 = fig.add_subplot(gs[1, 2])
bp = ax6.boxplot([T1_s, T2_s], labels=['T1', 'T2'],
                 patch_artist=True, widths=0.5)
for patch, color in zip(bp['boxes'], ['#3498db', '#e74c3c']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax6.axhline(T1_nom, color='blue', linestyle='--', linewidth=1.5,
            label=f'T1 nom = {T1_nom:.3f}')
ax6.axhline(T2_nom, color='red', linestyle='--', linewidth=1.5,
            label=f'T2 nom = {T2_nom:.3f}')
ax6.set_ylabel('Periodo (s)', fontsize=10)
ax6.set_title('Boxplot T1 y T2', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# --- Panel 7: Histograma k ---
ax7 = fig.add_subplot(gs[2, 0])
ax7.hist(k_s, bins=50, color='#9b59b6', edgecolor='black', alpha=0.7)
ax7.axvline(k_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Nominal = {k_nom:.0f}')
ax7.axvline(stats_k['media'], color='green', linestyle='-',
            linewidth=2.5, label=f'Media = {stats_k["media"]:.0f}')
ax7.set_xlabel('k (t/m)', fontsize=10)
ax7.set_ylabel('Frecuencia', fontsize=10)
ax7.set_title('Distribucion de rigidez k',
              fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)

# --- Panel 8: Histograma m ---
ax8 = fig.add_subplot(gs[2, 1])
ax8.hist(m_s, bins=50, color='#e67e22', edgecolor='black', alpha=0.7)
ax8.axvline(m_nom, color='red', linestyle='--', linewidth=2.5,
            label=f'Nominal = {m_nom:.3f}')
ax8.axvline(stats_m['media'], color='green', linestyle='-',
            linewidth=2.5, label=f'Media = {stats_m["media"]:.3f}')
ax8.set_xlabel('m (t.s2/m)', fontsize=10)
ax8.set_ylabel('Frecuencia', fontsize=10)
ax8.set_title('Distribucion de masa m',
              fontsize=11, fontweight='bold')
ax8.legend(fontsize=8)
ax8.grid(True, alpha=0.3)

# --- Panel 9: Conclusiones ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

txt9 = (
    f"CONCLUSIONES\n"
    f"{'-' * 36}\n"
    f"  INCERTIDUMBRE DE T1:\n"
    f"    CoV = {stats_T1['cv']*100:.2f} %\n"
    f"    IC 95% = [{stats_T1['p5']:.4f},\n"
    f"              {stats_T1['p95']:.4f}] s\n"
    f"{'-' * 36}\n"
    f"  FACTORES MAS INFLUYENTES:\n"
    f"    1. {vars_sorted[-1]}\n"
    f"    2. {vars_sorted[-2]}\n"
    f"    3. {vars_sorted[-3]}\n"
    f"{'-' * 36}\n"
    f"  INTERPRETACION:\n"
    f"    T1 varia entre\n"
    f"    {stats_T1['p5']:.3f} y {stats_T1['p95']:.3f} s\n"
    f"    con 95% de confianza.\n"
    f"{'-' * 36}\n"
    f"  RECOMENDACION:\n"
    f"    Disenar con T1 = {stats_T1['p95']:.4f} s\n"
    f"    (percentil 95)"
)
ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7', facecolor='#fadbd8',
                   edgecolor='#e74c3c', linewidth=2))

# ============================================================================
# 8. LINK DEL PROYECTO (MENSAJE ESTÁNDAR)
# ============================================================================

fig.text(0.5, 0.02,
         f'🌐 Más información: {LINK}',
         ha='center', va='bottom', fontsize=11, fontweight='bold',
         color='#2980b9',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor='#2980b9',
                   linewidth=2))

# ============================================================================
# 9. GUARDAR
# ============================================================================

carpeta = "Resultados_M08_2"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_2_montecarlo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\n✅ Dashboard guardado: {ruta_img}")

plt.show()

# ============================================================================
# 10. RESUMEN
# ============================================================================

print("\n" + "=" * 80)
print("M08.2 — MONTE CARLO CON LUCES HASTA 6 m")
print("=" * 80)
print(f"  Simulaciones: {N_SIM}")
print(f"  Luces máximas: 6.00 m")
print(f"  T1 nominal: {T1_nom:.4f} s")
print(f"  T1 media MC: {stats_T1['media']:.4f} s")
print(f"  T1 CoV: {stats_T1['cv']*100:.2f} %")
print(f"  IC 95%: [{IC95_T1[0]:.4f}, {IC95_T1[1]:.4f}] s")
print(f"  P(T1 > 1.2*T1_nom): {prob_T1_alto:.2f} %")
print(f"\n  LINK: {LINK}")
print("=" * 80)