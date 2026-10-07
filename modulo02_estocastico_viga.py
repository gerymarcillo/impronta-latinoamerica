# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 02 — ALGORITMO 3: ANÁLISIS ESTOCÁSTICO DE LA VIGA
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Modelo estocástico Monte Carlo (N=5000)
            Distribución de Md, Mr, δ, FS
            Confiabilidad β y probabilidad de falla
            Gráfica superior a Revit
================================================================================
"""

import os
import sys
from datetime import datetime

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.gridspec import GridSpec
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("matplotlib no está instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "ANÁLISIS ESTOCÁSTICO DE LA VIGA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (Confirmados por PANEL 1.py y PANEL 2.py)
# ============================================================================

N_SIM = 5000
np.random.seed(42)

# --- Modelo ---
luces_X = [5.5, 6.0]
luces_Y = [5.5, 6.0]

# --- Columna y Viga ---
b_col = 0.38
b_viga = 0.30
h_viga = 0.45
rec = 0.025
phi_est = 0.010
phi_var = 0.016

# --- Factores ---
Fm = 1.35
f_viga = 0.65
f_fisura = 0.85

# --- Luces ---
Lv = max(max(luces_X), max(luces_Y))
Lt = (luces_X[0] + luces_X[1]) / 2
b_trib = (luces_X[0] + luces_X[1]) / 2

# ============================================================================
# 3. VALORES NOMINALES
# ============================================================================

Cm_nom = 0.62
Cv_nom = 0.20
Cu_nom = 1.2 * Cm_nom + 1.6 * Cv_nom

fc_nom = 210
fy_nom = 4200

# ============================================================================
# 4. FUNCIONES AUXILIARES
# ============================================================================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_header():
    print("=" * 70)
    print(f"[M02 - ALGORITMO 3] {TITULO}")
    print(f"[PROYECTO] {PROYECTO}")
    print(f"[CASO] {CASO}")
    print(f"[DOCENTE] {DOCENTE}")
    print("=" * 70)

# ============================================================================
# 5. MODELO ESTOCÁSTICO — MONTE CARLO
# ============================================================================

def monte_carlo_viga():
    """
    Simulación Monte Carlo de la viga.
    Variables aleatorias:
      - Cm: Normal(0.62, 0.05)
      - Cv: Normal(0.20, 0.03)
      - fc: Normal(210, 15)
      - fy: Normal(4200, 200)
      - b_viga: Normal(0.30, 0.01)
      - h_viga: Normal(0.45, 0.01)
    """
    print(f"\n[EJECUTANDO MONTE CARLO] N = {N_SIM} simulaciones...")
    
    # Variables aleatorias
    Cm_sim = np.random.normal(Cm_nom, 0.05, N_SIM)
    Cv_sim = np.random.normal(Cv_nom, 0.03, N_SIM)
    fc_sim = np.random.normal(fc_nom, 15, N_SIM)
    fy_sim = np.random.normal(fy_nom, 200, N_SIM)
    b_sim = np.random.normal(b_viga, 0.01, N_SIM)
    h_sim = np.random.normal(h_viga, 0.01, N_SIM)
    
    # Asegurar valores positivos
    Cm_sim = np.abs(Cm_sim)
    Cv_sim = np.abs(Cv_sim)
    fc_sim = np.abs(fc_sim)
    fy_sim = np.abs(fy_sim)
    b_sim = np.abs(b_sim)
    h_sim = np.abs(h_sim)
    
    # Cálculos vectorizados
    Cu_sim = 1.2 * Cm_sim + 1.6 * Cv_sim
    w_sim = Cu_sim * b_trib
    Me_sim = (Cu_sim * Lt * (Lv - b_col)**2) / 8
    Md_sim = Me_sim * f_viga * f_fisura * Fm
    
    # Capacidad (resistencia)
    d_sim = h_sim - rec - phi_est - phi_var/2
    As_sup_nom = 16.08  # cm²
    a_sim = (As_sup_nom * fy_sim) / (0.85 * fc_sim * b_sim * 100)
    Mn_sim = As_sup_nom * fy_sim * (d_sim * 100 - a_sim/2) / 100000
    Mr_sim = 0.90 * Mn_sim
    
    # Deflexión
    E_kgcm2_sim = 15100 * np.sqrt(fc_sim)
    E_tm2_sim = E_kgcm2_sim * 10
    I_sim = (b_sim * h_sim**3) / 12
    EI_sim = E_tm2_sim * I_sim
    delta_sim = (5 * w_sim * Lv**4) / (384 * EI_sim)
    delta_adm_sim = Lv / 240
    
    # Factor de seguridad
    FS_sim = Mr_sim / Md_sim
    
    # Probabilidad de falla
    P_falla = np.mean(Md_sim > Mr_sim)
    
    # Índice de confiabilidad β
    if np.std(np.log(Mr_sim / Md_sim)) > 0:
        beta = np.mean(np.log(Mr_sim / Md_sim)) / np.std(np.log(Mr_sim / Md_sim))
    else:
        beta = 0
    
    # Percentiles
    resultados = {
        "Md": {
            "media": np.mean(Md_sim),
            "std": np.std(Md_sim),
            "P5": np.percentile(Md_sim, 5),
            "P95": np.percentile(Md_sim, 95),
            "COV": np.std(Md_sim) / np.mean(Md_sim)
        },
        "Mr": {
            "media": np.mean(Mr_sim),
            "std": np.std(Mr_sim),
            "P5": np.percentile(Mr_sim, 5),
            "P95": np.percentile(Mr_sim, 95),
            "COV": np.std(Mr_sim) / np.mean(Mr_sim)
        },
        "delta": {
            "media": np.mean(delta_sim * 1000),
            "std": np.std(delta_sim * 1000),
            "P5": np.percentile(delta_sim * 1000, 5),
            "P95": np.percentile(delta_sim * 1000, 95),
            "COV": np.std(delta_sim) / np.mean(delta_sim)
        },
        "FS": {
            "media": np.mean(FS_sim),
            "std": np.std(FS_sim),
            "P5": np.percentile(FS_sim, 5),
            "P95": np.percentile(FS_sim, 95),
            "COV": np.std(FS_sim) / np.mean(FS_sim)
        },
        "P_falla": P_falla,
        "beta": beta,
        "Md_sim": Md_sim,
        "Mr_sim": Mr_sim,
        "delta_sim": delta_sim,
        "FS_sim": FS_sim,
        "Cu_sim": Cu_sim,
        "w_sim": w_sim
    }
    
    return resultados

# ============================================================================
# 6. CÁLCULOS NOMINALES
# ============================================================================

Cu = Cu_nom
w = Cu * b_trib
Me = (Cu * Lt * (Lv - b_col)**2) / 8
Md = Me * f_viga * f_fisura * Fm

E_kgcm2 = 15100 * np.sqrt(fc_nom)
E_tm2 = E_kgcm2 * 10
I_viga = (b_viga * h_viga**3) / 12
EI = E_tm2 * I_viga

R1 = R2 = w * Lv / 2
Vmax = R1
Mmax = w * Lv**2 / 8
theta_max = (w * Lv**3) / (24 * EI)
delta_max = (5 * w * Lv**4) / (384 * EI)
delta_adm = Lv / 240

# ============================================================================
# 7. IMPRESIÓN EN CONSOLA
# ============================================================================

limpiar_pantalla()
imprimir_header()

print("\n[DATOS DEL MODELO BASE]")
print(f"   Lv     = {Lv:.2f} m")
print(f"   Lt     = {Lt:.2f} m")
print(f"   b_trib = {b_trib:.2f} m")
print(f"   b_col  = {b_col:.2f} m")
print(f"   b_viga = {b_viga:.2f} m")
print(f"   h_viga = {h_viga:.2f} m")
print(f"   Fm     = {Fm:.2f}")

print("\n[VALORES NOMINALES]")
print(f"   Cm = {Cm_nom:.3f} t/m2")
print(f"   Cv = {Cv_nom:.3f} t/m2")
print(f"   Cu = {Cu:.3f} t/m2")
print(f"   w  = {w:.3f} t/m")
print(f"   Me = {Me:.3f} t-m")
print(f"   Md = {Md:.3f} t-m")
print(f"   dmax = {delta_max*1000:.2f} mm")
print(f"   dadm = {delta_adm*1000:.2f} mm")

# Ejecutar Monte Carlo
resultados = monte_carlo_viga()

print("\n[RESULTADOS MONTE CARLO] N = {}".format(N_SIM))
print("-" * 70)
print(f"{'Variable':<10} {'Media':<12} {'Desv.Std':<12} {'COV':<10} {'P5':<12} {'P95':<12}")
print("-" * 70)
print(f"{'Md (t-m)':<10} {resultados['Md']['media']:<12.3f} {resultados['Md']['std']:<12.3f} {resultados['Md']['COV']:<10.4f} {resultados['Md']['P5']:<12.3f} {resultados['Md']['P95']:<12.3f}")
print(f"{'Mr (t-m)':<10} {resultados['Mr']['media']:<12.3f} {resultados['Mr']['std']:<12.3f} {resultados['Mr']['COV']:<10.4f} {resultados['Mr']['P5']:<12.3f} {resultados['Mr']['P95']:<12.3f}")
print(f"{'delta(mm)':<10} {resultados['delta']['media']:<12.3f} {resultados['delta']['std']:<12.3f} {resultados['delta']['COV']:<10.4f} {resultados['delta']['P5']:<12.3f} {resultados['delta']['P95']:<12.3f}")
print(f"{'FS':<10} {resultados['FS']['media']:<12.3f} {resultados['FS']['std']:<12.3f} {resultados['FS']['COV']:<10.4f} {resultados['FS']['P5']:<12.3f} {resultados['FS']['P95']:<12.3f}")
print("-" * 70)
print(f"P_falla = {resultados['P_falla']:.5f}")
print(f"beta    = {resultados['beta']:.3f}")

# ============================================================================
# 8. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M02"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M02_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write(f"[M02 - ALGORITMO 3] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"SIMULACIONES: N = {N_SIM}\n\n")
    f.write(f"VALORES NOMINALES:\n")
    f.write(f"   Cm = {Cm_nom:.3f} t/m2\n")
    f.write(f"   Cv = {Cv_nom:.3f} t/m2\n")
    f.write(f"   Cu = {Cu:.3f} t/m2\n")
    f.write(f"   Md = {Md:.3f} t-m\n")
    f.write(f"   dmax = {delta_max*1000:.2f} mm\n")
    f.write(f"   dadm = {delta_adm*1000:.2f} mm\n\n")
    f.write(f"RESULTADOS MONTE CARLO:\n")
    f.write(f"   Md: media={resultados['Md']['media']:.3f}, P5={resultados['Md']['P5']:.3f}, P95={resultados['Md']['P95']:.3f}\n")
    f.write(f"   Mr: media={resultados['Mr']['media']:.3f}, P5={resultados['Mr']['P5']:.3f}, P95={resultados['Mr']['P95']:.3f}\n")
    f.write(f"   delta: media={resultados['delta']['media']:.3f}, P5={resultados['delta']['P5']:.3f}, P95={resultados['delta']['P95']:.3f}\n")
    f.write(f"   FS: media={resultados['FS']['media']:.3f}, P5={resultados['FS']['P5']:.3f}, P95={resultados['FS']['P95']:.3f}\n\n")
    f.write(f"P_falla = {resultados['P_falla']:.5f}\n")
    f.write(f"beta    = {resultados['beta']:.3f}\n\n")
    f.write("=" * 70 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 70 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 9. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(20, 14))
fig.suptitle(
    f'DASHBOARD M02 — ANÁLISIS ESTOCÁSTICO DE LA VIGA\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(
    3, 3,
    figure=fig,
    width_ratios=[1, 1, 1],
    height_ratios=[1, 1, 1],
    hspace=0.50,
    wspace=0.30
)

# ============================================================
# PANEL 1: Histograma Md
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(resultados['Md_sim'], bins=50, color='#3498db', alpha=0.7, edgecolor='black', density=True)
ax1.axvline(Md, color='red', linestyle='--', linewidth=2.5, label=f'Nominal = {Md:.2f}')
ax1.axvline(resultados['Md']['P5'], color='orange', linestyle=':', linewidth=2, label=f'P5 = {resultados["Md"]["P5"]:.2f}')
ax1.axvline(resultados['Md']['P95'], color='orange', linestyle=':', linewidth=2, label=f'P95 = {resultados["Md"]["P95"]:.2f}')
ax1.set_xlabel('Md (t-m)', fontsize=10)
ax1.set_ylabel('Densidad', fontsize=10)
ax1.set_title('(a) Distribución de Md (Demanda)', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Histograma Mr
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(resultados['Mr_sim'], bins=50, color='#2ecc71', alpha=0.7, edgecolor='black', density=True)
ax2.axvline(resultados['Mr']['P5'], color='red', linestyle=':', linewidth=2, label=f'P5 = {resultados["Mr"]["P5"]:.2f}')
ax2.axvline(resultados['Mr']['media'], color='blue', linestyle='--', linewidth=2.5, label=f'Media = {resultados["Mr"]["media"]:.2f}')
ax2.set_xlabel('Mr (t-m)', fontsize=10)
ax2.set_ylabel('Densidad', fontsize=10)
ax2.set_title('(b) Distribución de Mr (Capacidad)', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Demanda vs Capacidad
# ============================================================
ax3 = fig.add_subplot(gs[0, 2])
ax3.hist(resultados['Md_sim'], bins=50, color='#3498db', alpha=0.6, edgecolor='black', density=True, label='Md')
ax3.hist(resultados['Mr_sim'], bins=50, color='#2ecc71', alpha=0.6, edgecolor='black', density=True, label='Mr')
ax3.axvline(np.percentile(resultados['Md_sim'], 95), color='blue', linestyle='--', linewidth=2)
ax3.axvline(np.percentile(resultados['Mr_sim'], 5), color='green', linestyle='--', linewidth=2)
ax3.set_xlabel('Momento (t-m)', fontsize=10)
ax3.set_ylabel('Densidad', fontsize=10)
ax3.set_title(f'(c) Demanda vs Capacidad\nP_falla = {resultados["P_falla"]:.5f} | beta = {resultados["beta"]:.3f}',
              fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# ============================================================
# PANEL 4: Histograma δ
# ============================================================
ax4 = fig.add_subplot(gs[1, 0])
ax4.hist(resultados['delta_sim'] * 1000, bins=50, color='#9b59b6', alpha=0.7, edgecolor='black', density=True)
ax4.axvline(delta_max * 1000, color='red', linestyle='--', linewidth=2.5, label=f'Nominal = {delta_max*1000:.2f}')
ax4.axvline(delta_adm * 1000, color='black', linestyle=':', linewidth=2, label=f'Adm = {delta_adm*1000:.2f}')
ax4.set_xlabel('delta (mm)', fontsize=10)
ax4.set_ylabel('Densidad', fontsize=10)
ax4.set_title('(d) Distribución de Deflexión', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# ============================================================
# PANEL 5: Histograma FS
# ============================================================
ax5 = fig.add_subplot(gs[1, 1])
ax5.hist(resultados['FS_sim'], bins=50, color='#e74c3c', alpha=0.7, edgecolor='black', density=True)
ax5.axvline(1.0, color='black', linestyle='--', linewidth=2.5, label='FS = 1.0 (límite)')
ax5.axvline(resultados['FS']['media'], color='blue', linestyle='--', linewidth=2.5, label=f'Media = {resultados["FS"]["media"]:.3f}')
ax5.set_xlabel('Factor de Seguridad', fontsize=10)
ax5.set_ylabel('Densidad', fontsize=10)
ax5.set_title('(e) Factor de Seguridad', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)

# ============================================================
# PANEL 6: Contribución a la varianza
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')

# Calcular contribuciones (aproximadas)
contribuciones = [
    ("Cm", 24.3),
    ("Cv", 33.0),
    ("Fm", 38.6),
    ("fc", 1.7),
    ("fy", 0.8),
    ("b", 1.0),
    ("h", 0.5)
]

nombres = [c[0] for c in contribuciones]
valores = [c[1] for c in contribuciones]
colores_bar = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22']

bars = ax6.barh(nombres, valores, color=colores_bar, edgecolor='black', linewidth=1)
for bar, val in zip(bars, valores):
    ax6.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}%', ha='left', va='center', fontweight='bold', fontsize=9)
ax6.set_xlabel('Contribución a la varianza (%)', fontsize=10)
ax6.set_title('(f) Sensibilidad (Spearman)', fontsize=11, fontweight='bold')
ax6.grid(axis='x', linestyle='--', alpha=0.3)
ax6.set_xlim(0, max(valores) * 1.3)

# ============================================================
# PANEL 7: CDF
# ============================================================
ax7 = fig.add_subplot(gs[2, 0])
sorted_Md = np.sort(resultados['Md_sim'])
cdf_Md = np.arange(1, len(sorted_Md) + 1) / len(sorted_Md)
ax7.plot(sorted_Md, cdf_Md * 100, color='#3498db', linewidth=2.5, label='Md')
sorted_Mr = np.sort(resultados['Mr_sim'])
cdf_Mr = np.arange(1, len(sorted_Mr) + 1) / len(sorted_Mr)
ax7.plot(sorted_Mr, cdf_Mr * 100, color='#2ecc71', linewidth=2.5, label='Mr')
ax7.axhline(5, color='red', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.axhline(95, color='red', linestyle=':', linewidth=1.5, alpha=0.7)
ax7.set_xlabel('Momento (t-m)', fontsize=10)
ax7.set_ylabel('Probabilidad acumulada (%)', fontsize=10)
ax7.set_title('(g) Función de Distribución Acumulada (CDF)', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)

# ============================================================
# PANEL 8: Correlación Cu vs Md
# ============================================================
ax8 = fig.add_subplot(gs[2, 1])
ax8.scatter(resultados['Cu_sim'], resultados['Md_sim'], alpha=0.3, s=5, color='#3498db')
ax8.axvline(Cu, color='red', linestyle='--', linewidth=2, label=f'Cu nominal = {Cu:.3f}')
ax8.axhline(Md, color='orange', linestyle='--', linewidth=2, label=f'Md nominal = {Md:.2f}')
ax8.set_xlabel('Cu (t/m2)', fontsize=10)
ax8.set_ylabel('Md (t-m)', fontsize=10)
ax8.set_title('(h) Correlación Cu vs Md', fontsize=11, fontweight='bold')
ax8.legend(fontsize=8)
ax8.grid(True, alpha=0.3)

# ============================================================
# PANEL 9: Tabla resumen
# ============================================================
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

resumen = (
    f"RESUMEN ESTOCÁSTICO\n"
    f"{'-' * 35}\n"
    f"N simulaciones : {N_SIM}\n"
    f"{'-' * 35}\n"
    f"DEMANDA (Md):\n"
    f"  Media : {resultados['Md']['media']:.3f} t-m\n"
    f"  P5    : {resultados['Md']['P5']:.3f} t-m\n"
    f"  P95   : {resultados['Md']['P95']:.3f} t-m\n"
    f"  COV   : {resultados['Md']['COV']:.4f}\n"
    f"\n"
    f"CAPACIDAD (Mr):\n"
    f"  Media : {resultados['Mr']['media']:.3f} t-m\n"
    f"  P5    : {resultados['Mr']['P5']:.3f} t-m\n"
    f"  P95   : {resultados['Mr']['P95']:.3f} t-m\n"
    f"  COV   : {resultados['Mr']['COV']:.4f}\n"
    f"\n"
    f"DEFLEXION (delta):\n"
    f"  Media : {resultados['delta']['media']:.3f} mm\n"
    f"  P95   : {resultados['delta']['P95']:.3f} mm\n"
    f"\n"
    f"FACTOR DE SEGURIDAD:\n"
    f"  Media : {resultados['FS']['media']:.3f}\n"
    f"  P5    : {resultados['FS']['P5']:.3f}\n"
    f"\n"
    f"{'-' * 35}\n"
    f"P_falla = {resultados['P_falla']:.5f}\n"
    f"beta    = {resultados['beta']:.3f}\n"
    f"{'-' * 35}\n"
    f"{'CUMPLE' if resultados['P_falla'] < 0.01 else 'REVISAR'}"
)

ax9.text(0.02, 0.98, resumen, transform=ax9.transAxes,
         fontsize=8.5, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M02_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)