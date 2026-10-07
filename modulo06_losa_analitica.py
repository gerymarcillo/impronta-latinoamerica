# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 06 — ALGORITMO 1: DISEÑO ANALÍTICO DE LOSA ALIVIANADA
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Diseño analítico de losa alivianada con nervios tipo T
            Predimensionamiento, momentos, acero positivo y negativo
            Verificación de deflexión (NEC-15)
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
    from matplotlib.patches import Rectangle, Circle
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
TITULO = "DISEÑO ANALÍTICO DE LOSA ALIVIANADA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (heredados de M01, M02, M03)
# ============================================================================

# Del M01 - Inercia Equivalente
h_eq = 18.06        # cm
H_losa = 25.0       # cm
bn = 10.0           # cm
bb = 50.0           # cm
tc = 5.0            # cm
hn = H_losa - tc    # cm (altura del nervio)

# Del M02 - Carga
Cu = 1.088          # t/m²

# Del M03 - Luces
L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

# Materiales
fc = 210            # kg/cm²
fy = 4200           # kg/cm²

# Recubrimiento
rec_losa = 2.0      # cm

# Diámetros
phi_pos = 8         # mm (varilla positiva en nervio)
phi_neg = 10        # mm (varilla negativa en capa superior)
phi_temp = 8        # mm (varilla de temperatura)

# ============================================================================
# 3. CÁLCULOS
# ============================================================================

# --- Paño crítico ---
Lx = max(L1, L2, L3, L4)
Ly = Lx

# --- Paso entre nervios ---
paso_nervios = bb / 100      # m
w_nervio = Cu * paso_nervios # t/m

# --- Relación luz/espesor ---
relacion = Lx * 100 / H_losa

# --- Momento positivo (viga simplemente apoyada) ---
M_pos_nervio = w_nervio * Lx**2 / 8      # t·m por nervio
M_pos_metro = M_pos_nervio / paso_nervios  # t·m/m

# --- Momento negativo (apoyos) ---
M_neg = M_pos_metro * 0.8  # t·m/m

# --- Momento fórmula del docente ---
M_docente = 0.08 * Cu * (L1/2 + L2/2) * Lx**2

# --- Diseño del nervio (viga T) ---
b_w = bn
d_nervio = H_losa - rec_losa - phi_pos/20

# Ancho efectivo del patín
b_ef = min(bb, Lx*100/4)
b_ef = min(b_ef, bb)

# --- Cálculo de As por iteración ---
def calcular_as_viga_T(M, b_w, b_ef, d, fc, fy, phi_flex=0.9):
    As = 0.5
    for i in range(50):
        a = (As * fy) / (0.85 * fc * b_ef)
        Mn = As * fy * (d - a/2) / 100000
        Mr = phi_flex * Mn
        if Mr >= M:
            break
        As += 0.01
    return As

As_pos_nervio = calcular_as_viga_T(M_pos_nervio, b_w, b_ef, d_nervio, fc, fy)
As_pos_metro = As_pos_nervio / paso_nervios

# --- As mínimo ---
As_min = 0.0018 * 100 * H_losa  # cm²/m
As_min_nervio = 0.0018 * b_w * H_losa
As_1phi8 = np.pi * (8/10)**2 / 4
As_diseno = max(As_pos_nervio, As_min_nervio, As_1phi8)
n_varillas_nervio = max(int(np.ceil(As_diseno / As_1phi8)), 1)

# --- As negativo (capa superior) ---
As_neg_metro = M_neg * 100000 / (0.9 * fy * (d_nervio - 2)) / 100
As_neg_metro = max(As_neg_metro, As_min)
n_neg, s_neg = 1, 100.0  # 1 φ10 @ 20 cm aprox

# --- As temperatura ---
As_temp = 0.0018 * 100 * H_losa
n_temp = max(int(np.ceil(As_temp / As_1phi8)), 1)
s_temp = 100 / n_temp

# --- Verificación de deflexión ---
E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
I_nervio = b_w * hn**3 / 12 + b_ef * tc**3 / 12
I_nervio = I_nervio / 1e8  # m⁴

delta_max = 5 * w_nervio * Lx**4 / (384 * E_tm2 * I_nervio)
delta_adm = Lx / 240

# ============================================================================
# 4. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - ALGORITMO 1] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 DATOS HEREDADOS:")
print(f"  h_eq   = {h_eq:.2f} cm")
print(f"  H_losa = {H_losa:.2f} cm")
print(f"  hn     = {hn:.2f} cm")
print(f"  bn     = {bn:.2f} cm")
print(f"  bb     = {bb:.2f} cm")
print(f"  tc     = {tc:.2f} cm")
print(f"  Cu     = {Cu:.3f} t/m²")
print(f"  Lx     = {Lx:.2f} m")

print(f"\n📐 CARGA POR NERVIO:")
print(f"  paso_nervios = {paso_nervios:.2f} m")
print(f"  w_nervio = {w_nervio:.4f} t/m")

print(f"\n📐 VERIFICACIÓN DE DEFLEXIÓN:")
print(f"  Relación L/H = {relacion:.2f} (límite 28)")
print(f"  {'✅ CUMPLE' if relacion <= 28 else '❌ NO CUMPLE'}")

print(f"\n📐 MOMENTOS:")
print(f"  M_pos (nervio) = {M_pos_nervio:.4f} t·m")
print(f"  M_pos (metro)  = {M_pos_metro:.4f} t·m/m")
print(f"  M_neg (metro)  = {M_neg:.4f} t·m/m")
print(f"  M (docente)    = {M_docente:.4f} t·m")

print(f"\n📐 ACERO POSITIVO (nervio):")
print(f"  As_pos (nervio) = {As_pos_nervio:.3f} cm²")
print(f"  As_pos (metro)  = {As_pos_metro:.3f} cm²/m")
print(f"  As_diseño       = {As_diseno:.3f} cm²")
print(f"  n varillas      = {n_varillas_nervio} φ {phi_pos} mm")

print(f"\n📐 ACERO NEGATIVO (capa superior):")
print(f"  As_neg = {As_neg_metro:.3f} cm²/m")
print(f"  Varilla: φ {phi_neg} mm")

print(f"\n📐 ACERO DE TEMPERATURA:")
print(f"  As_temp = {As_temp:.3f} cm²/m")
print(f"  φ {phi_temp} @ {s_temp:.1f} cm")

print(f"\n📏 DEFLEXIÓN:")
print(f"  δ_max = {delta_max*1000:.2f} mm")
print(f"  δ_adm = {delta_adm*1000:.2f} mm")
print(f"  {'✅ CUMPLE' if delta_max < delta_adm else '❌ NO CUMPLE'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_analitico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - ALGORITMO 1] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS:\n")
    f.write(f"  h_eq = {h_eq:.2f} cm | H_losa = {H_losa:.2f} cm\n")
    f.write(f"  Cu = {Cu:.3f} t/m² | Lx = {Lx:.2f} m\n\n")
    f.write(f"CARGA POR NERVIO:\n")
    f.write(f"  w_nervio = {w_nervio:.4f} t/m\n\n")
    f.write(f"MOMENTOS:\n")
    f.write(f"  M_pos = {M_pos_nervio:.4f} t·m\n")
    f.write(f"  M_neg = {M_neg:.4f} t·m/m\n\n")
    f.write(f"ACERO:\n")
    f.write(f"  As_pos = {As_diseno:.3f} cm² ({n_varillas_nervio} φ {phi_pos} mm)\n")
    f.write(f"  As_temp = φ {phi_temp} @ {s_temp:.1f} cm\n\n")
    f.write(f"DEFLEXIÓN:\n")
    f.write(f"  δ_max = {delta_max*1000:.2f} mm | δ_adm = {delta_adm*1000:.2f} mm\n")
    f.write(f"  {'CUMPLE' if delta_max < delta_adm else 'NO CUMPLE'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'DASHBOARD M06 — DISEÑO ANALÍTICO DE LOSA ALIVIANADA\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(
    2, 2,
    figure=fig,
    width_ratios=[1, 1],
    height_ratios=[1.2, 1],
    hspace=0.35,
    wspace=0.30
)

# ============================================================
# PANEL 1: Sección transversal del nervio
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-8, bb + 8)
ax1.set_ylim(-5, H_losa + 8)
ax1.set_aspect('equal')

# Capa de compresión
ax1.add_patch(Rectangle((0, H_losa - tc), bb, tc,
                         facecolor='#3498db', edgecolor='black', lw=1.5, alpha=0.8))
# Nervio
x_nervio = (bb - bn) / 2
ax1.add_patch(Rectangle((x_nervio, 0), bn, hn,
                         facecolor='#95a5a6', edgecolor='black', lw=1.5, alpha=0.9))

# Varilla positiva en el nervio
ax1.add_patch(Circle((bb/2, rec_losa + phi_pos/20), phi_pos/20,
                      color='red', zorder=10))

# Varilla de temperatura en capa superior
ax1.add_patch(Circle((bb/2, H_losa - rec_losa - phi_temp/20), phi_temp/20,
                      color='blue', zorder=10))

ax1.text(bb/2, H_losa - tc/2, "Capa de compresión",
         ha="center", va="center", fontsize=8, fontweight="bold", color="white")
ax1.text(bb/2, hn/2, f"Nervio\n{bn}×{hn:.0f}",
         ha="center", va="center", fontsize=8, fontweight="bold")
ax1.text(bb + 3, rec_losa + phi_pos/20, f"1 φ{phi_pos} (positivo)",
         ha="left", va="center", fontsize=8, color='red', fontweight='bold')
ax1.text(bb + 3, H_losa - rec_losa - phi_temp/20, f"φ{phi_temp} @ {s_temp:.0f} (temp)",
         ha='left', va='center', fontsize=8, color='blue', fontweight='bold')

ax1.set_title(f'(a) Sección de nervio con armadura', fontsize=11, fontweight='bold')
ax1.set_xlabel('Ancho (cm)', fontsize=10)
ax1.set_ylabel('Altura (cm)', fontsize=10)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Diagrama de momentos
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])

x = np.linspace(0, Lx, 100)
M_diagrama = w_nervio * x * (Lx - x) / 2

ax2.plot(x, M_diagrama, 'b-', linewidth=2.5, label='M(x)')
ax2.fill_between(x, M_diagrama, alpha=0.15, color='blue')
ax2.axhline(y=0, color='black', linewidth=0.8)
ax2.axhline(y=M_pos_nervio, color='red', linestyle='--', linewidth=2,
            label=f'M_pos = {M_pos_nervio:.3f} t·m')

ax2.set_xlabel('x (m)', fontsize=10)
ax2.set_ylabel('Momento M (t·m)', fontsize=10)
ax2.set_title('(b) Diagrama de momentos del nervio', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Barras comparativas
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])
categorias = ['M_pos', 'M_neg', 'As_pos', 'As_neg', 'As_min']
valores = [M_pos_metro, M_neg, As_pos_metro, As_neg_metro, As_min]
colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
bars = ax3.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax3.set_ylabel('Magnitud', fontsize=10)
ax3.set_title('(c) Momentos y Aceros de Diseño', fontsize=11, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.set_ylim(0, max(valores) * 1.3)

# ============================================================
# PANEL 4: Ficha técnica
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

ficha = (
    f"FICHA TÉCNICA\n"
    f"{'-' * 32}\n"
    f"Proyecto:\n"
    f"  UNESUM-REZ-2026\n"
    f"Caso: {CASO}\n"
    f"{'-' * 32}\n"
    f"h_eq   = {h_eq:.2f} cm\n"
    f"H_losa = {H_losa:.0f} cm\n"
    f"Cu     = {Cu:.3f} t/m²\n"
    f"Lx     = {Lx:.2f} m\n"
    f"Relación L/H = {relacion:.2f}\n"
    f"{'-' * 32}\n"
    f"w_nervio = {w_nervio:.3f} t/m\n"
    f"M_pos    = {M_pos_nervio:.3f} t·m\n"
    f"M_neg    = {M_neg:.3f} t·m/m\n"
    f"{'-' * 32}\n"
    f"As_pos   = {As_diseno:.2f} cm²\n"
    f"           ({n_varillas_nervio} φ {phi_pos} mm)\n"
    f"As_temp  = φ {phi_temp} @ {s_temp:.0f} cm\n"
    f"{'-' * 32}\n"
    f"δ_max = {delta_max*1000:.2f} mm\n"
    f"δ_adm = {delta_adm*1000:.2f} mm\n"
    f"{'-' * 32}\n"
    f"{'✅ CUMPLE' if delta_max < delta_adm else '⚠️ REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M06_analitico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
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