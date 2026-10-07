# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 06 — ALGORITMO 2: MODELO ESTOCÁSTICO DE LOSA ALIVIANADA (CORREGIDO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Modelo estocástico Monte Carlo (100 simulaciones)
            CORREGIDO: As real calculado + Armadura negativa φ10 mm
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
TITULO = "MODELO ESTOCÁSTICO DE LOSA ALIVIANADA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (del M02 - Cu correcto)
# ============================================================================

h_eq = 18.06
H_losa = 25.0
bn = 10.0
bb = 50.0
tc = 5.0
hn = H_losa - tc

Cu = 1.088          # t/m² (CORRECTO - del M02)
L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0
fc, fy = 210, 4200
rec_losa = 2.0

# Armaduras
phi_pos = 8         # mm - Positiva en nervio
phi_neg = 10        # mm - Negativa en capa superior (CORREGIDO: 10 mm)
phi_temp = 8        # mm - Temperatura

# ============================================================================
# 3. CÁLCULOS NOMINALES
# ============================================================================

Lx = max(L1, L2, L3, L4)
Ly = Lx

paso_nervios = bb / 100
w_nervio = Cu * paso_nervios
d_nervio = H_losa - rec_losa - phi_pos/20
b_ef = min(bb, Lx*100/4)

M_pos_nervio = w_nervio * Lx**2 / 8
M_pos_metro = M_pos_nervio / paso_nervios
M_neg_metro = M_pos_metro * 0.8

# As mínimo por nervio y por metro
As_min_nervio = 0.0018 * bn * H_losa      # 0.45 cm²
As_min_metro = 0.0018 * 100 * H_losa       # 4.50 cm²/m

As_1phi8 = np.pi * (8/10)**2 / 4           # 0.503 cm²
As_1phi10 = np.pi * (10/10)**2 / 4         # 0.785 cm²

# As negativo por metro
As_neg_metro = max(M_neg_metro * 100000 / (0.9 * fy * (d_nervio - 2)) / 100, As_min_metro)

# As temperatura
As_temp = 0.0018 * 100 * H_losa  # 4.50 cm²/m

# ============================================================================
# 4. AS REAL (nominal calculado con bucle de 1500 iteraciones)
# ============================================================================

As_real_nervio = As_min_nervio
for j in range(1500):
    a_real = (As_real_nervio * fy) / (0.85 * fc * b_ef)
    Mn_real = As_real_nervio * fy * (d_nervio - a_real/2) / 100000
    Mr_real = 0.9 * Mn_real
    if Mr_real >= M_pos_nervio:
        break
    As_real_nervio += 0.01
As_real_nervio = max(As_real_nervio, As_min_nervio)

# ============================================================================
# 5. MODELO ESTOCÁSTICO
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
H_losa_sim = np.random.normal(H_losa, 0.03 * H_losa, n_sim)

Cu_sim = np.clip(Cu_sim, 0.87 * Cu, 1.31 * Cu)
fc_sim = np.clip(fc_sim, 150, 280)
fy_sim = np.clip(fy_sim, 3800, 4600)
H_losa_sim = np.clip(H_losa_sim, 0.95 * H_losa, 1.05 * H_losa)

# Cálculo vectorizado de As (bucle ampliado a 1500 iteraciones)
M_pos_sim = np.zeros(n_sim)
As_pos_sim = np.zeros(n_sim)

for i in range(n_sim):
    w_i = Cu_sim[i] * paso_nervios
    M_pos_sim[i] = w_i * Lx**2 / 8
    d_i = H_losa_sim[i] - rec_losa - phi_pos/20
    As_i = As_min_nervio
    for j in range(1500):
        a_i = (As_i * fy_sim[i]) / (0.85 * fc_sim[i] * b_ef)
        Mn_i = As_i * fy_sim[i] * (d_i - a_i/2) / 100000
        Mr_i = 0.9 * Mn_i
        if Mr_i >= M_pos_sim[i]:
            break
        As_i += 0.01
    As_pos_sim[i] = max(As_i, As_min_nervio)

# Estadísticos
As_media = np.mean(As_pos_sim)
As_std = np.std(As_pos_sim)
As_p5 = np.percentile(As_pos_sim, 5)
As_p95 = np.percentile(As_pos_sim, 95)

# ============================================================================
# 6. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - ALGORITMO 2] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 VALORES NOMINALES:")
print(f"  h_eq = {h_eq:.2f} cm")
print(f"  H_losa = {H_losa:.2f} cm")
print(f"  Cu = {Cu:.4f} t/m²")
print(f"  Lx = {Lx:.2f} m")
print(f"  w_nervio = {w_nervio:.4f} t/m")
print(f"  M_pos = {M_pos_nervio:.4f} t·m")
print(f"  M_neg = {M_neg_metro:.4f} t·m/m")

print(f"\n📐 AS REAL (calculado):")
print(f"  As_real (nervio) = {As_real_nervio:.2f} cm²")
print(f"  Armadura negativa = φ {phi_neg} mm")
print(f"  Armadura temperatura = φ {phi_temp} mm")
print(f"  As_min (metro) = {As_min_metro:.2f} cm²/m")

print(f"\n🎲 MODELO ESTOCÁSTICO — {n_sim} SIMULACIONES:")
print(f"  As medio = {As_media:.2f} cm²")
print(f"  As std   = {As_std:.2f} cm²")
print(f"  As P5    = {As_p5:.2f} cm²")
print(f"  As P95   = {As_p95:.2f} cm²")

print(f"\n📌 VERIFICACIÓN:")
print(f"  As_real = {As_real_nervio:.2f} cm²")
print(f"  As_P95  = {As_p95:.2f} cm²")
print(f"  Estado  = {'✅ CUMPLE' if As_real_nervio >= As_p95 else '⚠️ REVISAR'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - ALGORITMO 2] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"VALORES NOMINALES:\n")
    f.write(f"  Cu = {Cu:.3f} t/m²\n")
    f.write(f"  M_pos = {M_pos_nervio:.4f} t·m\n")
    f.write(f"  M_neg = {M_neg_metro:.4f} t·m/m\n\n")
    f.write(f"AS REAL:\n")
    f.write(f"  As_real = {As_real_nervio:.3f} cm²\n")
    f.write(f"  Arm. negativa = φ {phi_neg} mm\n")
    f.write(f"  Arm. temperatura = φ {phi_temp} mm\n\n")
    f.write(f"MODELO ESTOCÁSTICO ({n_sim} SIMULACIONES):\n")
    f.write(f"  As medio = {As_media:.2f} cm²\n")
    f.write(f"  As P95   = {As_p95:.2f} cm²\n")
    f.write(f"  Estado = {'CUMPLE' if As_real_nervio >= As_p95 else 'REVISAR'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 8. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'DASHBOARD M06 — MODELO ESTOCÁSTICO DE LOSA ALIVIANADA\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1],
              height_ratios=[1, 1], hspace=0.35, wspace=0.30)

# ============================================================
# PANEL 1: Histograma de As
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(As_pos_sim, bins=20, color='#3498db', edgecolor='black', alpha=0.7)
ax1.axvline(x=As_media, color='red', linestyle='--', linewidth=2,
            label=f'Media = {As_media:.2f} cm2')
ax1.axvline(x=As_p95, color='orange', linestyle='--', linewidth=2,
            label=f'P95 = {As_p95:.2f} cm2')
ax1.axvline(x=As_real_nervio, color='green', linestyle='--', linewidth=2,
            label=f'As real = {As_real_nervio:.2f} cm2')
ax1.set_xlabel('As (cm2)', fontsize=10)
ax1.set_ylabel('Frecuencia', fontsize=10)
ax1.set_title(f'(a) Distribucion de As - {n_sim} simulaciones', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Sensibilidad
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

sensibilidad = {
    'Cu': np.corrcoef(Cu_sim, As_pos_sim)[0, 1],
    'fc': np.corrcoef(fc_sim, As_pos_sim)[0, 1],
    'fy': np.corrcoef(fy_sim, As_pos_sim)[0, 1],
    'H_losa': np.corrcoef(H_losa_sim, As_pos_sim)[0, 1]
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
ax2.set_xlabel('Coeficiente de correlacion', fontsize=10)
ax2.set_title('(b) Sensibilidad de As', fontsize=11, fontweight='bold')
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Curva As vs Cu
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])

Cu_range = np.linspace(0.87 * Cu, 1.31 * Cu, 50)
As_range = []
for cu in Cu_range:
    M_i = cu * paso_nervios * Lx**2 / 8
    As_i = As_min_nervio
    for j in range(1500):
        a_i = (As_i * fy) / (0.85 * fc * b_ef)
        Mn_i = As_i * fy * (d_nervio - a_i/2) / 100000
        Mr_i = 0.9 * Mn_i
        if Mr_i >= M_i:
            break
        As_i += 0.01
    As_range.append(max(As_i, As_min_nervio))

ax3.plot(Cu_range, As_range, 'b-', linewidth=2.5, label='As requerido')
ax3.axvline(x=Cu, color='red', linestyle='--', linewidth=2,
            label=f'Cu nominal = {Cu:.3f}')
ax3.axhline(y=As_real_nervio, color='green', linestyle='--', linewidth=1.5,
            label=f'As real = {As_real_nervio:.2f} cm2')
ax3.set_xlabel('Cu (t/m2)', fontsize=10)
ax3.set_ylabel('As (cm2)', fontsize=10)
ax3.set_title('(c) Sensibilidad As vs Cu', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# ============================================================
# PANEL 4: Ficha técnica
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

ficha = (
    f"FICHA TECNICA ESTOCASTICA\n"
    f"{'-' * 35}\n"
    f"Proyecto:\n"
    f"  UNESUM-REZ-2026\n"
    f"Caso: {CASO}\n"
    f"{'-' * 35}\n"
    f"SIMULACIONES: {n_sim}\n"
    f"{'-' * 35}\n"
    f"VARIABLES ALEATORIAS:\n"
    f"  Cu     ~ Normal(mu={Cu:.3f}, CV=10%)\n"
    f"  fc     ~ Lognormal(mu={fc}, CV=15%)\n"
    f"  fy     ~ Normal(mu={fy}, CV=5%)\n"
    f"  H_losa ~ Normal(mu={H_losa}, CV=3%)\n"
    f"{'-' * 35}\n"
    f"ARMADURAS:\n"
    f"  As_pos (nervio) = {As_real_nervio:.2f} cm2\n"
    f"  As_neg (metro)  = {As_neg_metro:.2f} cm2\n"
    f"  Arm. negativa   = phi {phi_neg} mm\n"
    f"  Arm. temp       = phi {phi_temp} mm\n"
    f"{'-' * 35}\n"
    f"RESULTADOS:\n"
    f"  As medio = {As_media:.2f} cm2\n"
    f"  As P5    = {As_p5:.2f} cm2\n"
    f"  As P95   = {As_p95:.2f} cm2\n"
    f"  As real  = {As_real_nervio:.2f} cm2\n"
    f"{'-' * 35}\n"
    f"{'CUMPLE' if As_real_nervio >= As_p95 else 'REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout()

nombre_img = f"dashboard_M06_estocastico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120)
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)