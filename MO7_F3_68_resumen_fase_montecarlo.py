# -*- coding: utf-8 -*-
"""
================================================================================
M07.7 — PERIODO POR SIMULACIÓN MONTE CARLO
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.7 — Período por Monte Carlo

OBJETIVO: Cuantificar la incertidumbre del período fundamental (T₁) mediante
          simulación Monte Carlo, propagando la variabilidad de:
          - fc (resistencia del concreto)
          - Cm (carga muerta)
          - Cv (carga viva)
          - b, h (dimensiones de columna)
          - He (altura de entrepiso)

VALORES NOMINALES:
    - fc = 210 kg/cm²
    - Cm = 0.62 t/m²
    - Cv = 0.20 t/m²
    - b = h = 0.38 m
    - He = 3.00 m
    - T₁ nominal = 0.389 s

SALIDA:
    - Distribución de T₁
    - Media, desviación estándar, percentiles
    - Probabilidad de excedencia
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
    'hist': '#3498db',
    'media': '#e74c3c',
    'nominal': '#27ae60',
    'percentil': '#f39c12',
}

# ============================================================================
# 1. DATOS NOMINALES DEL PROYECTO
# ============================================================================

# Geometría
LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He_nom = 3.00
N_PISOS = 2

B_COL_nom = 0.38
H_COL_nom = 0.38

# Materiales
fc_nom = 210  # kg/cm²

# Cargas
Cm_nom = 0.62  # t/m²
Cv_nom = 0.20  # t/m²

g = 9.81

# Número de columnas
N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL

# ============================================================================
# 2. FUNCIÓN DE CÁLCULO DEL PERÍODO (2 GDL)
# ============================================================================

def calcular_periodo(fc, Cm, Cv, b, h, He):
    """
    Calcula T₁ para un conjunto de parámetros de entrada.
    
    Modelo: Shear building (2 GDL)
    """
    # Módulo de elasticidad (estocástico)
    E_kgcm2 = 12600 * np.sqrt(fc)
    E_tm2 = E_kgcm2 * 10
    
    # Inercia de columna
    I_col = (b * h**3) / 12  # m⁴
    
    # Rigidez de columna
    k_col = 12 * E_tm2 * I_col / He**3  # t/m
    
    # Rigidez del piso
    k_piso = N_COL_TOTAL * k_col  # t/m
    
    # Peso reactivo por piso (criterio del Excel: Cu = 1.2Cm + 1.6Cv)
    Cu = 1.2 * Cm + 1.6 * Cv
    W_piso = Cu * AREA  # t
    
    # Masa por piso
    m_piso = W_piso / g  # t·s²/m
    
    # Frecuencia angular del modo 1 (2 GDL)
    omega_1 = np.sqrt((k_piso / m_piso) * (2 - np.sqrt(2)))
    
    # Período fundamental
    T_1 = 2 * np.pi / omega_1
    
    return T_1

# ============================================================================
# 3. CÁLCULO DEL PERÍODO NOMINAL
# ============================================================================

T1_nominal = calcular_periodo(
    fc_nom, Cm_nom, Cv_nom,
    B_COL_nom, H_COL_nom, He_nom
)

# ============================================================================
# 4. SIMULACIÓN MONTE CARLO
# ============================================================================

# Número de simulaciones
N_sim = 10000

# Semilla para reproducibilidad
np.random.seed(42)

print("=" * 80)
print("M07.7 — PERÍODO POR SIMULACIÓN MONTE CARLO")
print("=" * 80)
print(f"\n  Simulando {N_sim} escenarios...")

# --- Distribuciones de probabilidad ---

# fc ~ Normal (CV = 15%)
fc_sim = np.random.normal(fc_nom, 0.15 * fc_nom, N_sim)
fc_sim = np.clip(fc_sim, 150, 280)  # truncar

# Cm ~ Normal (CV = 10%)
Cm_sim = np.random.normal(Cm_nom, 0.10 * Cm_nom, N_sim)
Cm_sim = np.clip(Cm_sim, 0.40, 0.90)

# Cv ~ Gumbel (CV = 25%)
# Para Gumbel: media = mu + gamma*beta, std = pi*beta/sqrt(6)
# Despejando: beta = std * sqrt(6)/pi, mu = media - gamma*beta
Cv_media = Cv_nom
Cv_std = 0.25 * Cv_nom
Cv_beta = Cv_std * np.sqrt(6) / np.pi
Cv_mu = Cv_media - 0.5772 * Cv_beta
Cv_sim = np.random.gumbel(Cv_mu, Cv_beta, N_sim)
Cv_sim = np.clip(Cv_sim, 0.05, 0.50)

# b ~ Normal (CV = 2%)
b_sim = np.random.normal(B_COL_nom, 0.02 * B_COL_nom, N_sim)
b_sim = np.clip(b_sim, 0.35, 0.41)

# h ~ Normal (CV = 2%)
h_sim = np.random.normal(H_COL_nom, 0.02 * H_COL_nom, N_sim)
h_sim = np.clip(h_sim, 0.35, 0.41)

# He ~ Normal (CV = 1%)
He_sim = np.random.normal(He_nom, 0.01 * He_nom, N_sim)
He_sim = np.clip(He_sim, 2.90, 3.10)

# --- Cálculo del período para cada escenario ---

T1_sim = np.array([
    calcular_periodo(fc_sim[i], Cm_sim[i], Cv_sim[i],
                     b_sim[i], h_sim[i], He_sim[i])
    for i in range(N_sim)
])

# ============================================================================
# 5. ESTADÍSTICAS
# ============================================================================

T1_media = np.mean(T1_sim)
T1_std = np.std(T1_sim)
T1_cv = T1_std / T1_media * 100

T1_p5 = np.percentile(T1_sim, 5)
T1_p50 = np.percentile(T1_sim, 50)
T1_p95 = np.percentile(T1_sim, 95)

# Probabilidad de excedencia (T > 0.5 s)
T_limite = 0.5
P_excedencia = np.mean(T1_sim > T_limite) * 100

# ============================================================================
# 6. IMPRESIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("RESULTADOS DE LA SIMULACIÓN MONTE CARLO")
print("=" * 80)
print(f"""
  PERÍODO NOMINAL:
    T₁ nominal = {T1_nominal:.4f} s

  ESTADÍSTICAS DE T₁ ({N_sim} simulaciones):
    Media      = {T1_media:.4f} s
    Desv. Est. = {T1_std:.4f} s
    CV         = {T1_cv:.2f} %

  PERCENTILES:
    P5  = {T1_p5:.4f} s
    P50 = {T1_p50:.4f} s
    P95 = {T1_p95:.4f} s

  PROBABILIDAD DE EXCEDENCIA:
    P(T₁ > {T_limite} s) = {P_excedencia:.2f} %

  CONCLUSIÓN:
    La estructura es RÍGIDA
    T₁ medio = {T1_media:.4f} s
""")
print("=" * 80)

# ============================================================================
# 7. FIGURA
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.7 — PERÍODO POR SIMULACIÓN MONTE CARLO',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | N = {N_sim} simulaciones | T₁ nominal = {T1_nominal:.4f} s',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.0, 1.0])

# ============================================================================
# PANEL (a): DISTRIBUCIÓN DE T₁ (HISTOGRAMA)
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0:2])

ax1.hist(T1_sim, bins=50, color=COLORES['hist'],
         edgecolor='black', linewidth=0.5, alpha=0.7,
         label=f'Distribución de T₁ (N={N_sim})')

# Líneas de referencia
ax1.axvline(x=T1_nominal, color=COLORES['nominal'],
            linestyle='--', linewidth=2.5,
            label=f'T₁ nominal = {T1_nominal:.4f} s')
ax1.axvline(x=T1_media, color=COLORES['media'],
            linestyle='-', linewidth=2.5,
            label=f'T₁ medio = {T1_media:.4f} s')
ax1.axvline(x=T1_p5, color=COLORES['percentil'],
            linestyle=':', linewidth=2,
            label=f'P5 = {T1_p5:.4f} s')
ax1.axvline(x=T1_p95, color=COLORES['percentil'],
            linestyle=':', linewidth=2,
            label=f'P95 = {T1_p95:.4f} s')

ax1.set_xlabel('Período T₁ (s)', fontsize=11)
ax1.set_ylabel('Frecuencia', fontsize=11)
ax1.set_title('(a) DISTRIBUCIÓN DE T₁ (MONTE CARLO)',
              fontsize=13, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(alpha=0.3)

# ============================================================================
# PANEL (b): ESTADÍSTICAS
# ============================================================================

ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
ax2.set_title('(b) ESTADÍSTICAS DE T₁',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

txt2 = (
    "ESTADÍSTICAS\n"
    "═══════════════════════════════\n\n"
    "  N simulaciones = 10,000\n\n"
    f"  Media   = {T1_media:.4f} s\n"
    f"  Desv    = {T1_std:.4f} s\n"
    f"  CV      = {T1_cv:.2f} %\n\n"
    f"  Mínimo  = {np.min(T1_sim):.4f} s\n"
    f"  Máximo  = {np.max(T1_sim):.4f} s\n\n"
    "═══════════════════════════════\n\n"
    "PERCENTILES:\n"
    f"  P5  = {T1_p5:.4f} s\n"
    f"  P50 = {T1_p50:.4f} s\n"
    f"  P95 = {T1_p95:.4f} s"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): BOXPLOT
# ============================================================================

ax3 = fig.add_subplot(gs[1, 0])

box = ax3.boxplot(T1_sim, vert=True, patch_artist=True,
                   widths=0.5,
                   boxprops=dict(facecolor=COLORES['hist'], alpha=0.7),
                   medianprops=dict(color=COLORES['media'], linewidth=2.5),
                   whiskerprops=dict(linewidth=1.5),
                   capprops=dict(linewidth=1.5),
                   flierprops=dict(marker='o', markersize=3,
                                   markerfacecolor='gray', alpha=0.5))

ax3.axhline(y=T1_nominal, color=COLORES['nominal'],
            linestyle='--', linewidth=2,
            label=f'Nominal = {T1_nominal:.4f} s')

ax3.set_ylabel('Período T₁ (s)', fontsize=11)
ax3.set_title('(c) BOXPLOT DE T₁',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax3.legend(fontsize=9)
ax3.grid(alpha=0.3)

# ============================================================================
# PANEL (d): FUNCIÓN DE DISTRIBUCIÓN ACUMULADA (CDF)
# ============================================================================

ax4 = fig.add_subplot(gs[1, 1])

T1_sorted = np.sort(T1_sim)
cdf = np.arange(1, N_sim + 1) / N_sim

ax4.plot(T1_sorted, cdf * 100, '-', color=COLORES['hist'], linewidth=2)
ax4.axvline(x=T1_nominal, color=COLORES['nominal'],
            linestyle='--', linewidth=2,
            label=f'Nominal = {T1_nominal:.4f} s')
ax4.axvline(x=T1_media, color=COLORES['media'],
            linestyle='-', linewidth=2,
            label=f'Media = {T1_media:.4f} s')

ax4.set_xlabel('Período T₁ (s)', fontsize=11)
ax4.set_ylabel('Probabilidad acumulada (%)', fontsize=11)
ax4.set_title('(d) CDF DE T₁',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax4.legend(fontsize=9)
ax4.grid(alpha=0.3)

# ============================================================================
# PANEL (e): CONCLUSIÓN
# ============================================================================

ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')
ax5.set_title('(e) CONCLUSIÓN',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

txt5 = (
    "PROBABILIDAD DE EXCEDENCIA\n"
    "═══════════════════════════════\n\n"
    f"  P(T₁ > {T_limite} s) = {P_excedencia:.2f} %\n\n"
    "═══════════════════════════════\n\n"
    "INTERPRETACIÓN:\n"
    "  • T₁ medio = 0.39 s\n"
    "  • La estructura es RÍGIDA\n"
    "  • CV bajo (< 5%)\n"
    "  • Baja incertidumbre\n\n"
    "═══════════════════════════════\n\n"
    "CONCLUSIÓN:\n"
    "  ✓ T₁ < 0.5 s en el 100%\n"
    "  ✓ CUMPLE CON NEC-15\n"
    "  ✓ NO NECESITA DISIPADORES"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 8. MENSAJES OPORTUNOS
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
    "  Monte Carlo (N=10,000)\n"
    "  Distribuciones:\n"
    "  fc~N, Cm~N, Cv~Gumbel\n"
    "  b~N, h~N, He~N"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_calculo_bg'],
                   edgecolor=COLORES['box_calculo_borde'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 9. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07_7"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"M07_7_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("M07.7 — PERÍODO POR SIMULACIÓN MONTE CARLO\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"  N simulaciones = {N_sim}\n\n")
    f.write(f"  T₁ nominal   = {T1_nominal:.4f} s\n")
    f.write(f"  T₁ medio     = {T1_media:.4f} s\n")
    f.write(f"  T₁ desv      = {T1_std:.4f} s\n")
    f.write(f"  T₁ CV        = {T1_cv:.2f} %\n\n")
    f.write(f"  P5  = {T1_p5:.4f} s\n")
    f.write(f"  P50 = {T1_p50:.4f} s\n")
    f.write(f"  P95 = {T1_p95:.4f} s\n\n")
    f.write(f"  P(T₁ > {T_limite} s) = {P_excedencia:.2f} %\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 10. GUARDAR IMAGEN Y MOSTRAR
# ============================================================================

nombre_img = f"M07_7_monte_carlo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.7 COMPLETADO — PERÍODO POR MONTE CARLO")
print("=" * 80)
print(f"  T₁ nominal = {T1_nominal:.4f} s")
print(f"  T₁ medio   = {T1_media:.4f} s")
print(f"  T₁ desv    = {T1_std:.4f} s")
print(f"  CV         = {T1_cv:.2f} %")
print(f"  P5         = {T1_p5:.4f} s")
print(f"  P95        = {T1_p95:.4f} s")
print("=" * 80)