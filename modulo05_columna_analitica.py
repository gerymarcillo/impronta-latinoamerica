# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 05 — ALGORITMO 1: DISEÑO ANALÍTICO DE COLUMNA
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Diseño analítico de columna (replica del Excel)
            Área tributaria, Cu, Pu, Ag_req, As, ρ
            Zona protegida, s_prot, s_cent
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
TITULO = "DISEÑO ANALÍTICO DE COLUMNA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (replica del Excel)
# ============================================================================

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

Cm1, Cv1 = 0.62, 0.20
Pisos = 2

He, H_viga = 3.0, 0.30
Fm = 1.2

fc, fy = 210, 4200

rec = 2.5
phi_long = 14
phi_esq = 16
phi_est = 10

# ============================================================================
# 3. CÁLCULOS
# ============================================================================

# --- Área tributaria ---
At = (L1/2 + L2/2) * (L3/2 + L4/2)

# --- Carga última ---
Cu = 1.2 * (Cm1 * Pisos) + 1.6 * (Cv1 * Pisos)

# --- Carga axial ---
Pu = At * Cu * Fm

# --- Predimensionamiento ---
Ag_req = 3 * Pu * 1000 / (0.85 * fc + 0.012 * fy)

# --- Sección de columna ---
ancho_col = 38
prof_col = 38
Ag_col = ancho_col * prof_col

# --- Ancho confinado ---
bc = ancho_col - 2 * rec - phi_est / 10
pc = prof_col - 2 * rec - phi_est / 10

# --- Número de varillas ---
var_a = 4
var_p = 4
num_varillas = var_a * 2 + (var_p - 2) * 2

# --- Área de acero ---
As = 4 * 0.00785 * phi_esq**2 + (num_varillas - 4) * 0.00785 * phi_long**2

# --- Cuantía ---
cuantia = As / Ag_col

# --- Separación de varillas ---
sep_a = (bc - phi_est/10 - 2*phi_esq/10 - (var_a - 2)*phi_long/10) / (var_a - 1)
sep_p = (pc - phi_est/10 - 2*phi_esq/10 - (var_p - 2)*phi_long/10) / (var_p - 1)

# --- Zona protegida ---
Lo = max(45, max(ancho_col, prof_col), He * 16.6666666666667)

# --- Separación zona protegida ---
s_prot = min(6 * min(phi_long, phi_esq) / 10, 10)

# --- Ash zona protegida ---
Ash = max(
    0.3 * bc * Lo * fc / fy * (Ag_col / bc / pc - 1),
    0.09 * bc * Lo * fc / fy
)

# --- Ramas ---
ramas = Ash / (0.00785 * phi_est**2)

# --- Zona central ---
Lc = He * 100 - H_viga * 100 - 2 * phi_long

# --- Ash zona central ---
Ash_central = max(
    0.3 * bc * Lc * fc / fy * (Ag_col / bc / pc - 1),
    0.09 * bc * Lc * fc / fy
)

# --- Ramas zona central ---
ramas_central = Ash_central / (0.00785 * phi_est**2)

# --- Separación zona central ---
s_cent = min(6 * min(phi_long, phi_esq) / 10, 15)

# ============================================================================
# 4. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M05 - ALGORITMO 1] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 ÁREA TRIBUTARIA:")
print(f"  At = ({L1}/2 + {L2}/2) × ({L3}/2 + {L4}/2) = {At:.4f} m²")

print(f"\n📐 CARGA ÚLTIMA:")
print(f"  Cu = 1.2×({Cm1}×{Pisos}) + 1.6×({Cv1}×{Pisos}) = {Cu:.4f} t/m²")

print(f"\n📐 CARGA AXIAL:")
print(f"  Pu = At × Cu × Fm = {At:.2f} × {Cu:.4f} × {Fm} = {Pu:.4f} t")

print(f"\n📐 PREDIMENSIONAMIENTO:")
print(f"  Ag_req = 3×{Pu:.2f}×1000 / (0.85×{fc} + 0.012×{fy}) = {Ag_req:.2f} cm²")

print(f"\n📐 SECCIÓN DE COLUMNA:")
print(f"  Sección = {ancho_col} × {prof_col} cm")
print(f"  Ag = {Ag_col} cm²")
print(f"  {'✅ CUMPLE' if Ag_col >= Ag_req else '❌ NO CUMPLE'}")

print(f"\n📐 NÚMERO DE VARILLAS:")
print(f"  num = {num_varillas} varillas")

print(f"\n📐 ÁREA DE ACERO:")
print(f"  As = {As:.4f} cm²")

print(f"\n📐 CUANTÍA:")
print(f"  ρ = {cuantia*100:.2f}%")
print(f"  {'✅ CUMPLE' if cuantia >= 0.012 else '⚠️  ρ < 1.2%'}")

print(f"\n📐 ZONA PROTEGIDA:")
print(f"  Lo = {Lo:.2f} cm")

print(f"\n📐 SEPARACIÓN ZONA PROTEGIDA:")
print(f"  s_prot = {s_prot:.2f} cm")

print(f"\n📐 SEPARACIÓN ZONA CENTRAL:")
print(f"  s_cent = {s_cent:.2f} cm")

print(f"\n📐 ASH ZONA PROTEGIDA:")
print(f"  Ash = {Ash:.4f} cm²")

print(f"\n📐 RAMAS:")
print(f"  ramas = {ramas:.4f} u")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M05"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M05_analitico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M05 - ALGORITMO 1] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS DE ENTRADA:\n")
    f.write(f"  L1={L1} | L2={L2} | L3={L3} | L4={L4}\n")
    f.write(f"  Cm1={Cm1} | Cv1={Cv1} | Pisos={Pisos}\n")
    f.write(f"  He={He} | H_viga={H_viga} | Fm={Fm}\n")
    f.write(f"  fc={fc} | fy={fy}\n\n")
    f.write(f"CÁLCULOS:\n")
    f.write(f"  At = {At:.4f} m²\n")
    f.write(f"  Cu = {Cu:.4f} t/m²\n")
    f.write(f"  Pu = {Pu:.4f} t\n")
    f.write(f"  Ag_req = {Ag_req:.2f} cm²\n")
    f.write(f"  Sección = {ancho_col} × {prof_col} cm\n")
    f.write(f"  num = {num_varillas} varillas\n")
    f.write(f"  As = {As:.4f} cm²\n")
    f.write(f"  ρ = {cuantia*100:.4f}%\n")
    f.write(f"  Lo = {Lo:.2f} cm\n")
    f.write(f"  s_prot = {s_prot:.2f} cm\n")
    f.write(f"  s_cent = {s_cent:.2f} cm\n")
    f.write(f"  Ash = {Ash:.4f} cm²\n")
    f.write(f"  ramas = {ramas:.4f} u\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'DASHBOARD M05 — DISEÑO ANALÍTICO DE COLUMNA\n'
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
# PANEL 1: Sección transversal
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-5, ancho_col + 5)
ax1.set_ylim(-5, prof_col + 5)
ax1.set_aspect('equal')
ax1.add_patch(Rectangle((0, 0), ancho_col, prof_col,
                         linewidth=2, edgecolor='black', facecolor='#e8e8e8'))
ax1.add_patch(Rectangle((rec, rec), ancho_col - 2*rec, prof_col - 2*rec,
                         linewidth=1.5, edgecolor='blue', facecolor='none'))

# Varillas esquinas
for i in range(var_a):
    x = rec + phi_est/10 + phi_esq/20 + i * (ancho_col - 2*rec - 2*phi_est/10 - phi_esq/10) / (var_a - 1)
    y = rec + phi_est/10 + phi_esq/20
    ax1.add_patch(Circle((x, y), phi_esq/20, color='red', zorder=10))

for i in range(var_a):
    x = rec + phi_est/10 + phi_esq/20 + i * (ancho_col - 2*rec - 2*phi_est/10 - phi_esq/10) / (var_a - 1)
    y = prof_col - rec - phi_est/10 - phi_esq/20
    ax1.add_patch(Circle((x, y), phi_esq/20, color='red', zorder=10))

# Varillas laterales
for i in range(1, var_p - 1):
    y = rec + phi_est/10 + phi_long/20 + i * (prof_col - 2*rec - 2*phi_est/10 - phi_long/10) / (var_p - 1)
    x1 = rec + phi_est/10 + phi_long/20
    x2 = ancho_col - rec - phi_est/10 - phi_long/20
    ax1.add_patch(Circle((x1, y), phi_long/20, color='red', zorder=10))
    ax1.add_patch(Circle((x2, y), phi_long/20, color='red', zorder=10))

ax1.set_title(f'(a) Sección: {num_varillas} varillas', fontsize=12, fontweight='bold')
ax1.set_xlabel('b (cm)', fontsize=10)
ax1.set_ylabel('h (cm)', fontsize=10)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Distribución de estribos
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, He * 100)
ax2.set_ylim(-5, 15)
ax2.add_patch(Rectangle((0, 0), He * 100, 10, facecolor='#e8e8e8', edgecolor='black'))
ax2.axvspan(0, Lo, alpha=0.3, color='red')
ax2.axvspan(He * 100 - Lo, He * 100, alpha=0.3, color='red')
ax2.axvspan(Lo, He * 100 - Lo, alpha=0.2, color='blue')

n_est_prot = int(Lo / s_prot) + 1
for i in range(n_est_prot):
    x = i * s_prot
    ax2.plot([x, x], [0, 10], color='red', linewidth=2)
for i in range(n_est_prot):
    x = He * 100 - i * s_prot
    ax2.plot([x, x], [0, 10], color='red', linewidth=2)

n_est_cent = int((He * 100 - 2 * Lo) / s_cent)
for i in range(n_est_cent):
    x = Lo + i * s_cent
    ax2.plot([x, x], [0, 10], color='blue', linewidth=1.5)

ax2.text(Lo/2, 12, f'Lo={Lo:.0f}\ns={s_prot:.1f}', ha='center', fontsize=9, color='red')
ax2.text(He*100/2, 12, f's={s_cent:.1f}', ha='center', fontsize=9, color='blue')
ax2.text(He*100 - Lo/2, 12, f'Lo={Lo:.0f}\ns={s_prot:.1f}', ha='center', fontsize=9, color='red')
ax2.set_title('(b) Distribución de estribos', fontsize=12, fontweight='bold')
ax2.set_xlabel('Altura (cm)', fontsize=10)
ax2.set_yticks([])
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Barras comparativas
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])
categorias = ['Ag_req', 'Ag_col']
valores = [Ag_req, Ag_col]
colores = ['#e74c3c', '#2ecc71']
bars = ax3.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
            f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax3.set_ylabel('Área (cm²)', fontsize=10)
ax3.set_title(f'(c) Verificación de Sección', fontsize=12, fontweight='bold')
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
    f"At     = {At:.2f} m²\n"
    f"Cu     = {Cu:.3f} t/m²\n"
    f"Pu     = {Pu:.2f} t\n"
    f"{'-' * 32}\n"
    f"Ag_req = {Ag_req:.0f} cm²\n"
    f"Sección = {ancho_col} × {prof_col} cm\n"
    f"Ag     = {Ag_col} cm²\n"
    f"num    = {num_varillas} varillas\n"
    f"As     = {As:.2f} cm²\n"
    f"ρ      = {cuantia*100:.2f}%\n"
    f"{'-' * 32}\n"
    f"Lo     = {Lo:.0f} cm\n"
    f"s_prot = {s_prot:.1f} cm\n"
    f"s_cent = {s_cent:.1f} cm\n"
    f"{'-' * 32}\n"
    f"{'✅ CUMPLE' if Ag_col >= Ag_req and cuantia >= 0.012 else '⚠️ REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M05_analitico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
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