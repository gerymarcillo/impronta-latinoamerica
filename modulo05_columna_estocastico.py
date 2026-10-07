# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 05 — ALGORITMO 2: MODELO ESTOCÁSTICO DE COLUMNA
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Modelo estocástico Monte Carlo (100 simulaciones)
            Distribución de As, sensibilidad, curva As vs Cu
            Dashboard superior a Revit
            Corrida directa — Muestra gráfica en pantalla
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
    print("⚠️ matplotlib no está instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "MODELO ESTOCÁSTICO DE COLUMNA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (del Algoritmo 1)
# ============================================================================

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

Cm1, Cv1 = 0.62, 0.20
Pisos = 2

He = 3.0
Fm = 1.2

fc, fy = 210, 4200

rec = 2.5
phi_long = 14
phi_esq = 16
phi_est = 10

ancho_col = 38
prof_col = 38

# ============================================================================
# 3. CÁLCULOS NOMINALES
# ============================================================================

At = (L1/2 + L2/2) * (L3/2 + L4/2)
Cu = 1.2 * (Cm1 * Pisos) + 1.6 * (Cv1 * Pisos)
Pu = At * Cu * Fm

Ag_req = 3 * Pu * 1000 / (0.85 * fc + 0.012 * fy)
Ag_col = ancho_col * prof_col

As = 4 * 0.00785 * phi_esq**2 + 8 * 0.00785 * phi_long**2
cuantia = As / Ag_col

# ============================================================================
# 4. MODELO ESTOCÁSTICO
# ============================================================================

np.random.seed(42)
n_sim = 100

# Variables aleatorias
Cu_sim = np.random.normal(Cu, 0.10 * Cu, n_sim)
fc_sim = np.random.lognormal(
    np.log(fc) - 0.5 * np.log(1 + 0.15**2),
    np.sqrt(np.log(1 + 0.15**2)),
    n_sim
)
fy_sim = np.random.normal(fy, 0.05 * fy, n_sim)
ancho_sim = np.random.normal(ancho_col, 0.03 * ancho_col, n_sim)
prof_sim = np.random.normal(prof_col, 0.03 * prof_col, n_sim)

# Asegurar valores positivos y realistas
Cu_sim = np.clip(Cu_sim, 0.87 * Cu, 1.31 * Cu)
fc_sim = np.clip(fc_sim, 150, 280)
fy_sim = np.clip(fy_sim, 3800, 4600)
ancho_sim = np.clip(ancho_sim, 0.95 * ancho_col, 1.05 * ancho_col)
prof_sim = np.clip(prof_sim, 0.95 * prof_col, 1.05 * prof_col)

# Cálculo vectorizado de As
As_sim = np.zeros(n_sim)
for i in range(n_sim):
    Ag_i = ancho_sim[i] * prof_sim[i]
    As_sim[i] = 0.012 * Ag_i  # ρ mínimo = 1.2%

# Estadísticos
As_media = np.mean(As_sim)
As_std = np.std(As_sim)
As_p5 = np.percentile(As_sim, 5)
As_p95 = np.percentile(As_sim, 95)
As_min = np.min(As_sim)
As_max = np.max(As_sim)

# Probabilidad de falla
As_max_permitido = 0.04 * Ag_col  # ρ_max = 4%
P_falla = np.mean(As_sim > As_max_permitido)

# ============================================================================
# 5. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M05 - ALGORITMO 2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 VALORES NOMINALES:")
print(f"  At = {At:.2f} m²")
print(f"  Cu = {Cu:.4f} t/m²")
print(f"  Pu = {Pu:.2f} t")
print(f"  Sección = {ancho_col} × {prof_col} cm")
print(f"  As = {As:.2f} cm²")
print(f"  ρ = {cuantia*100:.2f}%")

print(f"\n🎲 MODELO ESTOCÁSTICO — {n_sim} SIMULACIONES:")
print(f"  As medio = {As_media:.2f} cm²")
print(f"  As std   = {As_std:.2f} cm²")
print(f"  As P5    = {As_p5:.2f} cm²")
print(f"  As P95   = {As_p95:.2f} cm²")
print(f"  As mín   = {As_min:.2f} cm²")
print(f"  As máx   = {As_max:.2f} cm²")
print(f"  P_falla  = {P_falla*100:.2f}%")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 6. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M05"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M05_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M05 - ALGORITMO 2] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"VALORES NOMINALES:\n")
    f.write(f"  At = {At:.2f} m²\n")
    f.write(f"  Cu = {Cu:.4f} t/m²\n")
    f.write(f"  Pu = {Pu:.2f} t\n")
    f.write(f"  As = {As:.2f} cm²\n")
    f.write(f"  ρ = {cuantia*100:.2f}%\n\n")
    f.write(f"MODELO ESTOCÁSTICO ({n_sim} SIMULACIONES):\n")
    f.write(f"  As medio = {As_media:.2f} cm²\n")
    f.write(f"  As std   = {As_std:.2f} cm²\n")
    f.write(f"  As P5    = {As_p5:.2f} cm²\n")
    f.write(f"  As P95   = {As_p95:.2f} cm²\n")
    f.write(f"  P_falla  = {P_falla*100:.2f}%\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 7. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'DASHBOARD M05 — MODELO ESTOCÁSTICO DE COLUMNA\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(
    2, 2,
    figure=fig,
    width_ratios=[1, 1],
    height_ratios=[1, 1],
    hspace=0.35,
    wspace=0.30
)

# ============================================================
# PANEL 1: Histograma de As
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(As_sim, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
ax1.axvline(x=As_media, color='red', linestyle='--', linewidth=2,
            label=f'Media = {As_media:.2f} cm²')
ax1.axvline(x=As_p95, color='orange', linestyle='--', linewidth=2,
            label=f'P95 = {As_p95:.2f} cm²')
ax1.axvline(x=As, color='green', linestyle='--', linewidth=2,
            label=f'As real = {As:.2f} cm²')
ax1.axvline(x=As_max_permitido, color='purple', linestyle=':', linewidth=2,
            label=f'As máx = {As_max_permitido:.2f} cm²')
ax1.set_xlabel('As (cm²)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title(f'(a) Distribución de As — {n_sim} simulaciones', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Sensibilidad
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

sensibilidad = {
    'Cu': np.corrcoef(Cu_sim, As_sim)[0, 1],
    'fc': np.corrcoef(fc_sim, As_sim)[0, 1],
    'fy': np.corrcoef(fy_sim, As_sim)[0, 1],
    'ancho': np.corrcoef(ancho_sim, As_sim)[0, 1],
    'prof': np.corrcoef(prof_sim, As_sim)[0, 1]
}

variables = list(sensibilidad.keys())
valores = list(sensibilidad.values())
colores = ['#e74c3c' if v > 0 else '#3498db' for v in valores]

bars = ax2.barh(variables, valores, color=colores, edgecolor='black')
for bar, val in zip(bars, valores):
    ax2.text(val + 0.02 if val > 0 else val - 0.02,
             bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center',
             ha='left' if val > 0 else 'right', fontsize=9)

ax2.axvline(x=0, color='black', linewidth=1)
ax2.set_xlabel('Coeficiente de correlación', fontsize=10)
ax2.set_title('(b) Sensibilidad de As', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Curva As vs Cu
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])

Cu_range = np.linspace(0.87 * Cu, 1.31 * Cu, 50)
As_range = []
for cu in Cu_range:
    Pu_i = At * cu * Fm
    Ag_i = 3 * Pu_i * 1000 / (0.85 * fc + 0.012 * fy)
    As_i = 0.012 * Ag_i
    As_range.append(As_i)

ax3.plot(Cu_range, As_range, 'b-', linewidth=2.5, label='As requerido')
ax3.axvline(x=Cu, color='red', linestyle='--', linewidth=2,
            label=f'Cu nominal = {Cu:.3f}')
ax3.axhline(y=As, color='green', linestyle='--', linewidth=1.5,
            label=f'As real = {As:.2f} cm²')
ax3.set_xlabel('Cu (t/m²)', fontsize=10)
ax3.set_ylabel('As (cm²)', fontsize=10)
ax3.set_title('(c) Sensibilidad As vs Cu', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# ============================================================
# PANEL 4: Ficha técnica + Resumen
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

ficha = (
    f"FICHA TÉCNICA ESTOCÁSTICA\n"
    f"{'-' * 35}\n"
    f"Proyecto:\n"
    f"  UNESUM-REZ-2026\n"
    f"Caso: {CASO}\n"
    f"{'-' * 35}\n"
    f"SIMULACIONES: {n_sim}\n"
    f"{'-' * 35}\n"
    f"VARIABLES ALEATORIAS:\n"
    f"  Cu    ~ Normal(μ={Cu:.3f}, CV=10%)\n"
    f"  fc    ~ Lognormal(μ={fc}, CV=15%)\n"
    f"  fy    ~ Normal(μ={fy}, CV=5%)\n"
    f"  ancho ~ Normal(μ={ancho_col}, CV=3%)\n"
    f"  prof  ~ Normal(μ={prof_col}, CV=3%)\n"
    f"{'-' * 35}\n"
    f"RESULTADOS:\n"
    f"  As medio = {As_media:.2f} cm²\n"
    f"  As std   = {As_std:.2f} cm²\n"
    f"  As P5    = {As_p5:.2f} cm²\n"
    f"  As P95   = {As_p95:.2f} cm²\n"
    f"  As real  = {As:.2f} cm²\n"
    f"{'-' * 35}\n"
    f"P_falla = {P_falla*100:.2f}%\n"
    f"{'-' * 35}\n"
    f"{'✅ CUMPLE' if P_falla < 0.05 else '⚠️ REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=8.5, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M05_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

# Mostrar gráfica en pantalla
print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)