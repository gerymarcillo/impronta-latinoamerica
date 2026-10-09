# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 04 — ALGORITMO: DISEÑO DE ACERO A CORTANTE (CORREGIDO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Diseño de estribos en zona protegida y zona central
            CORREGIDO: s_prot = min(d/4, 6·φ_min, 10) sin s_est
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
TITULO = "DISEÑO DE ACERO A CORTANTE"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (heredados del M03)
# ============================================================================

Md = 17.32        # t·m (momento de diseño del M03)
As_sup = 16.08    # cm² (acero superior del M03)
b_viga = 0.30     # m
h_viga = 0.45     # m
b_col = 0.38      # m
rec = 0.025       # m
phi_est = 0.010   # m (10 mm)
phi_var = 0.016   # m (16 mm)
phi_long = 0.014  # m (14 mm) - para el criterio 6·φ
fc = 210          # kg/cm²
fy = 4200         # kg/cm²
Lv = 6.00         # m
Lt = 5.75         # m
Cu = 1.064        # t/m²
b_trib = 5.75     # m
Fm = 1.35

# ============================================================================
# 3. CÁLCULOS
# ============================================================================

# --- Peralte efectivo ---
d = h_viga - rec - phi_est - phi_var/2
d_cm = d * 100

# --- Carga lineal ---
w = Cu * b_trib

# --- Momento probable (Mpr) ---
Mpr = 1.25 * As_sup * fy * (d_cm - 1.25 * As_sup * fy / (1.7 * fc * b_viga * 100)) / 100000

# --- Cortante por giro (Vum) ---
Vum = (Mpr + Mpr) / (Lv - b_col)

# --- Cortante por gravedad (Vug) ---
Vug = (2 * Lv - b_col) * w * Lv / 4

# --- Cortante último ---
Vu = Vum + Vug

# --- Cortante del concreto (Vc) ---
Vc = 0.53 * np.sqrt(fc) * b_viga * 100 * d_cm * 100 / 1000

# --- Cortante del estribo (Vs) ---
Vs = (Vu - 0.75 * Vc) / 0.75

# --- Separación calculada (por cortante) ---
s_est = (d_cm * 0.00785 * phi_est*1000**2 * 2 * fy) / (Vs * 1000)

# --- Zona protegida ---
Z_prot = 2 * h_viga * 100

# --- Separación en zona protegida (CORREGIDO: sin s_est) ---
phi_min = min(phi_long, phi_var) * 1000  # mm
s_prot = min(d_cm/4, 6*phi_min/10, 10)

# --- Separación en zona central ---
s_cent = min(d_cm/2, 8*phi_min/10, 15)

# ============================================================================
# 4. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M04] {TITULO} — VERSIÓN CORREGIDA")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 DATOS DEL MODELO:")
print(f"  Md     = {Md:.2f} t·m")
print(f"  As_sup = {As_sup:.2f} cm²")
print(f"  b_viga = {b_viga:.2f} m")
print(f"  h_viga = {h_viga:.2f} m")
print(f"  d      = {d_cm:.2f} cm")
print(f"  φ_min  = {phi_min:.1f} mm")

print(f"\n📐 CORTANTES:")
print(f"  w    = {w:.3f} t/m")
print(f"  Mpr  = {Mpr:.2f} t·m")
print(f"  Vum  = {Vum:.2f} t")
print(f"  Vug  = {Vug:.2f} t")
print(f"  Vu   = {Vu:.2f} t")
print(f"  Vc   = {Vc:.2f} t")
print(f"  Vs   = {Vs:.2f} t")

print(f"\n📐 ESTRIBOS (CORREGIDO):")
print(f"  s_est   = {s_est:.2f} cm  (por cortante)")
print(f"  Z_prot  = {Z_prot:.0f} cm")
print(f"  s_prot  = {s_prot:.1f} cm  (confinamiento)")
print(f"  s_cent  = {s_cent:.1f} cm  (zona central)")

print(f"\n📌 VERIFICACIÓN:")
print(f"  s_prot ≤ 10 cm → {'✅ CUMPLE' if s_prot <= 10 else '⚠️ REVISAR'}")
print(f"  s_cent ≤ 15 cm → {'✅ CUMPLE' if s_cent <= 15 else '⚠️ REVISAR'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M04"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M04_cortante_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M04] {TITULO} — VERSIÓN CORREGIDA\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS DEL MODELO:\n")
    f.write(f"  Md = {Md:.2f} t·m\n")
    f.write(f"  As_sup = {As_sup:.2f} cm²\n")
    f.write(f"  d = {d_cm:.2f} cm\n")
    f.write(f"  φ_min = {phi_min:.1f} mm\n\n")
    f.write(f"CORTANTES:\n")
    f.write(f"  w = {w:.3f} t/m\n")
    f.write(f"  Mpr = {Mpr:.2f} t·m\n")
    f.write(f"  Vum = {Vum:.2f} t\n")
    f.write(f"  Vug = {Vug:.2f} t\n")
    f.write(f"  Vu = {Vu:.2f} t\n")
    f.write(f"  Vc = {Vc:.2f} t\n")
    f.write(f"  Vs = {Vs:.2f} t\n\n")
    f.write(f"ESTRIBOS (CORREGIDO):\n")
    f.write(f"  s_est = {s_est:.2f} cm\n")
    f.write(f"  Z_prot = {Z_prot:.0f} cm\n")
    f.write(f"  s_prot = {s_prot:.1f} cm\n")
    f.write(f"  s_cent = {s_cent:.1f} cm\n\n")
    f.write(f"VERIFICACION:\n")
    f.write(f"  s_prot <= 10 cm: {'CUMPLE' if s_prot <= 10 else 'REVISAR'}\n")
    f.write(f"  s_cent <= 15 cm: {'CUMPLE' if s_cent <= 15 else 'REVISAR'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(16, 10))
fig.suptitle(
    f'DASHBOARD M04 — DISEÑO DE ACERO A CORTANTE (CORREGIDO)\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(2, 2, figure=fig, width_ratios=[1, 1],
              height_ratios=[1, 1], hspace=0.35, wspace=0.30)

# ============================================================
# PANEL 1: Distribución de estribos
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, Lv * 100)
ax1.set_ylim(-5, 15)
ax1.add_patch(Rectangle((0, 0), Lv*100, 10, facecolor='#e8e8e8', edgecolor='black'))
ax1.axvspan(0, Z_prot, alpha=0.3, color='red')
ax1.axvspan(Lv*100 - Z_prot, Lv*100, alpha=0.3, color='red')
ax1.axvspan(Z_prot, Lv*100 - Z_prot, alpha=0.2, color='blue')

n_est_prot = int(Z_prot / s_prot) + 1
for i in range(n_est_prot):
    x = i * s_prot
    ax1.plot([x, x], [0, 10], color='red', linewidth=2)
for i in range(n_est_prot):
    x = Lv*100 - i * s_prot
    ax1.plot([x, x], [0, 10], color='red', linewidth=2)

n_est_cent = int((Lv*100 - 2*Z_prot) / s_cent)
for i in range(n_est_cent):
    x = Z_prot + i * s_cent
    ax1.plot([x, x], [0, 10], color='blue', linewidth=1.5)

ax1.text(Z_prot/2, 12, f's={s_prot:.1f} cm', ha='center', fontsize=9, color='red', fontweight='bold')
ax1.text(Lv*100/2, 12, f's={s_cent:.1f} cm', ha='center', fontsize=9, color='blue', fontweight='bold')
ax1.text(Lv*100 - Z_prot/2, 12, f's={s_prot:.1f} cm', ha='center', fontsize=9, color='red', fontweight='bold')
ax1.set_title('(a) Distribución de estribos', fontsize=12, fontweight='bold')
ax1.set_xlabel('Longitud (cm)', fontsize=10)
ax1.set_yticks([])
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Diagrama de cortante
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
x = np.linspace(0, Lv, 100)
V = w * (Lv/2 - x)
ax2.plot(x, V, 'b-', linewidth=2.5, label='V(x)')
ax2.fill_between(x, V, alpha=0.2, color='blue')
ax2.axhline(0, color='black', linewidth=1)
ax2.axhline(Vum, color='orange', linestyle='--', linewidth=1.5, label=f'Vum={Vum:.2f} t')
ax2.axhline(Vug, color='green', linestyle='--', linewidth=1.5, label=f'Vug={Vug:.2f} t')
ax2.axhline(Vu, color='red', linestyle='--', linewidth=2, label=f'Vu={Vu:.2f} t')
ax2.set_title('(b) Diagrama de cortante V(x)', fontsize=12, fontweight='bold')
ax2.set_xlabel('x (m)', fontsize=10)
ax2.set_ylabel('V (t)', fontsize=10)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Barras comparativas
# ============================================================
ax3 = fig.add_subplot(gs[1, 0])
categorias = ['Vc', 'Vs', 'Vu']
valores = [Vc, Vs, Vu]
colores = ['#2ecc71', '#e74c3c', '#3498db']
bars = ax3.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{val:.2f} t', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax3.set_ylabel('Cortante (t)', fontsize=10)
ax3.set_title('(c) Contribución Vc vs Vs', fontsize=12, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 4: Ficha técnica
# ============================================================
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

ficha = (
    f"FICHA TÉCNICA — CORREGIDA\n"
    f"{'-' * 35}\n"
    f"Proyecto: UNESUM-REZ-2026\n"
    f"Caso: {CASO}\n"
    f"{'-' * 35}\n"
    f"d      = {d_cm:.2f} cm\n"
    f"phi_min= {phi_min:.1f} mm\n"
    f"Mpr    = {Mpr:.2f} t·m\n"
    f"Vum    = {Vum:.2f} t\n"
    f"Vug    = {Vug:.2f} t\n"
    f"Vu     = {Vu:.2f} t\n"
    f"Vc     = {Vc:.2f} t\n"
    f"Vs     = {Vs:.2f} t\n"
    f"{'-' * 35}\n"
    f"Z_prot = {Z_prot:.0f} cm\n"
    f"s_est  = {s_est:.2f} cm\n"
    f"s_prot = {s_prot:.1f} cm\n"
    f"s_cent = {s_cent:.1f} cm\n"
    f"{'-' * 35}\n"
    f"s_prot = min(d/4, 6·phi_min, 10)\n"
    f"s_cent = min(d/2, 8·phi_min, 15)\n"
    f"{'-' * 35}\n"
    f"{'✅ CUMPLE' if s_prot <= 10 else '⚠️ REVISAR'}"
)

ax4.text(0.02, 0.98, ficha, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M04_cortante_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)