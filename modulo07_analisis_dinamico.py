# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 07 — ANÁLISIS DINÁMICO MODAL DE PÓRTICO DE 2 PISOS (CORREGIDO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Análisis dinámico modal (frecuencias, períodos, modos)
            CORREGIDO: Variable 'frec' en lugar de 'f' (sin conflicto con archivo)
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
TITULO = "ANÁLISIS DINÁMICO MODAL DE PÓRTICO DE 2 PISOS"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA
# ============================================================================

n_pisos = 2
He = 3.0
H_total = n_pisos * He

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

b_col = 0.38
h_col = 0.38
b_viga = 0.30
h_viga = 0.45

fc = 210
fy = 4200

Cu = 1.088
Fm = 1.2
g = 9.81

# ============================================================================
# 3. CÁLCULO DE PROPIEDADES
# ============================================================================

E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

I_col = (b_col * h_col**3) / 12
I_viga = (b_viga * h_viga**3) / 12

At = (L1/2 + L2/2) * (L3/2 + L4/2)

masa_piso = Cu * At / g

# ============================================================================
# 4. MATRIZ DE RIGIDEZ
# ============================================================================

n_columnas = 4
k_entrepiso = n_columnas * 12 * E_tm2 * I_col / He**3

K = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso, k_entrepiso]
])

M = np.array([
    [masa_piso, 0],
    [0, masa_piso]
])

# ============================================================================
# 5. ANÁLISIS MODAL
# ============================================================================

M_inv = np.linalg.inv(M)
A = M_inv @ K

eigenvalues, eigenvectors = np.linalg.eig(A)

idx = np.argsort(eigenvalues)
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

omega = np.sqrt(eigenvalues)

# CORRECCIÓN: 'frec' en lugar de 'f' (sin conflicto con archivo)
T = 2 * np.pi / omega
frec = omega / (2 * np.pi)

# ============================================================================
# 6. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M07] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 DATOS DEL MODELO:")
print(f"  n_pisos = {n_pisos}")
print(f"  He = {He:.2f} m | H_total = {H_total:.2f} m")
print(f"  L1, L2 = {L1}, {L2} m")
print(f"  L3, L4 = {L3}, {L4} m")
print(f"  b_col = {b_col:.2f} m | h_col = {h_col:.2f} m")
print(f"  b_viga = {b_viga:.2f} m | h_viga = {h_viga:.2f} m")
print(f"  fc = {fc} kg/cm² | fy = {fy} kg/cm²")

print(f"\n📐 PROPIEDADES:")
print(f"  E = {E_tm2:.2f} t/m²")
print(f"  I_col = {I_col:.6f} m⁴")
print(f"  I_viga = {I_viga:.6f} m⁴")
print(f"  At = {At:.2f} m²")
print(f"  masa_piso = {masa_piso:.4f} t·s²/m")
print(f"  k_entrepiso = {k_entrepiso:.2f} t/m")

print(f"\n📐 ANÁLISIS MODAL:")
print(f"  Modo 1:")
print(f"    ω₁ = {omega[0]:.4f} rad/s")
print(f"    T₁ = {T[0]:.4f} s")
print(f"    f₁ = {frec[0]:.4f} Hz")
print(f"  Modo 2:")
print(f"    ω₂ = {omega[1]:.4f} rad/s")
print(f"    T₂ = {T[1]:.4f} s")
print(f"    f₂ = {frec[1]:.4f} Hz")

print(f"\n📐 FORMAS MODALES:")
print(f"  Modo 1: φ₁ = [{eigenvectors[0,0]:.4f}, {eigenvectors[1,0]:.4f}]")
print(f"  Modo 2: φ₂ = [{eigenvectors[0,1]:.4f}, {eigenvectors[1,1]:.4f}]")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M07_dinamico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
    archivo.write("=" * 80 + "\n")
    archivo.write(f"[M07] {TITULO}\n")
    archivo.write(f"[PROYECTO] {PROYECTO}\n")
    archivo.write(f"[CASO] {CASO}\n")
    archivo.write(f"[DOCENTE] {DOCENTE}\n")
    archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    archivo.write("=" * 80 + "\n\n")
    archivo.write(f"DATOS DEL MODELO:\n")
    archivo.write(f"  n_pisos = {n_pisos}\n")
    archivo.write(f"  He = {He:.2f} m\n")
    archivo.write(f"  E = {E_tm2:.2f} t/m²\n")
    archivo.write(f"  masa_piso = {masa_piso:.4f} t·s²/m\n")
    archivo.write(f"  k_entrepiso = {k_entrepiso:.2f} t/m\n\n")
    archivo.write(f"ANÁLISIS MODAL:\n")
    archivo.write(f"  Modo 1: T1 = {T[0]:.4f} s | f1 = {frec[0]:.4f} Hz\n")
    archivo.write(f"  Modo 2: T2 = {T[1]:.4f} s | f2 = {frec[1]:.4f} Hz\n\n")
    archivo.write("=" * 80 + "\n")
    archivo.write(f"Frase: {FRASE}\n")
    archivo.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 8. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(18, 12))
fig.suptitle(
    f'DASHBOARD M07 — ANÁLISIS DINÁMICO MODAL\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 1],
              height_ratios=[1, 1, 1], hspace=0.45, wspace=0.30)

# ============================================================
# PANEL 1: Esquema del pórtico
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(-1, 2)
ax1.set_ylim(-0.5, H_total + 0.5)

for x_col in [0, 1]:
    for piso in range(n_pisos):
        y_ini = piso * He
        y_fin = (piso + 1) * He
        ax1.plot([x_col, x_col], [y_ini, y_fin], 'b-', linewidth=4)

for piso in range(n_pisos + 1):
    y = piso * He
    ax1.plot([0, 1], [y, y], 'r-', linewidth=3)

for piso in range(1, n_pisos + 1):
    y = piso * He
    ax1.plot(0.5, y, 'ko', markersize=15)

ax1.plot(0, -0.3, marker='^', markersize=20, color='green')
ax1.plot(1, -0.3, marker='^', markersize=20, color='green')

ax1.set_title('(a) Esquema del pórtico', fontsize=11, fontweight='bold')
ax1.set_xlabel('X (m)', fontsize=10)
ax1.set_ylabel('Y (m)', fontsize=10)
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Períodos modales
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
modos = ['Modo 1', 'Modo 2']
colores = ['#3498db', '#e74c3c']
bars = ax2.bar(modos, T, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, T):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{val:.4f} s', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax2.set_ylabel('Período (s)', fontsize=10)
ax2.set_title('(b) Períodos modales', fontsize=11, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 3: Frecuencias modales
# ============================================================
ax3 = fig.add_subplot(gs[0, 2])
bars = ax3.bar(modos, frec, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, frec):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.4f} Hz', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax3.set_ylabel('Frecuencia (Hz)', fontsize=10)
ax3.set_title('(c) Frecuencias modales', fontsize=11, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 4: Modo 1
# ============================================================
ax4 = fig.add_subplot(gs[1, 0])
alturas = [0, He, H_total]
forma1 = [0, eigenvectors[0, 0], eigenvectors[1, 0]]
forma1_norm = [x / max(abs(eigenvectors[:, 0])) for x in forma1]
ax4.plot(forma1_norm, alturas, 'bo-', linewidth=3, markersize=10, label='Modo 1')
ax4.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax4.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax4.set_ylabel('Altura (m)', fontsize=10)
ax4.set_title(f'(d) Modo 1: T1 = {T[0]:.4f} s', fontsize=11, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

# ============================================================
# PANEL 5: Modo 2
# ============================================================
ax5 = fig.add_subplot(gs[1, 1])
forma2 = [0, eigenvectors[0, 1], eigenvectors[1, 1]]
forma2_norm = [x / max(abs(eigenvectors[:, 1])) for x in forma2]
ax5.plot(forma2_norm, alturas, 'ro-', linewidth=3, markersize=10, label='Modo 2')
ax5.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax5.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax5.set_ylabel('Altura (m)', fontsize=10)
ax5.set_title(f'(e) Modo 2: T2 = {T[1]:.4f} s', fontsize=11, fontweight='bold')
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# ============================================================
# PANEL 6: Formas modales superpuestas
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])
ax6.plot(forma1_norm, alturas, 'bo-', linewidth=3, markersize=10, label=f'Modo 1 (T1={T[0]:.3f}s)')
ax6.plot(forma2_norm, alturas, 'ro-', linewidth=3, markersize=10, label=f'Modo 2 (T2={T[1]:.3f}s)')
ax6.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax6.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax6.set_ylabel('Altura (m)', fontsize=10)
ax6.set_title('(f) Formas modales superpuestas', fontsize=11, fontweight='bold')
ax6.legend(fontsize=9)
ax6.grid(True, alpha=0.3)

# ============================================================
# PANEL 7: Matriz de rigidez
# ============================================================
ax7 = fig.add_subplot(gs[2, 0])
ax7.axis('off')
matriz_k = (
    f"MATRIZ DE RIGIDEZ K (t/m)\n"
    f"{'-' * 30}\n"
    f"       | {K[0,0]:>10.0f}  {K[0,1]:>10.0f} |\n"
    f"  K =  |                        |\n"
    f"       | {K[1,0]:>10.0f}  {K[1,1]:>10.0f} |\n"
    f"{'-' * 30}\n"
    f"k_entrepiso = {k_entrepiso:.0f} t/m"
)
ax7.text(0.5, 0.5, matriz_k, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 8: Matriz de masa
# ============================================================
ax8 = fig.add_subplot(gs[2, 1])
ax8.axis('off')
matriz_m = (
    f"MATRIZ DE MASA M (t.s2/m)\n"
    f"{'-' * 30}\n"
    f"       | {M[0,0]:>10.4f}  {M[0,1]:>10.4f} |\n"
    f"  M =  |                        |\n"
    f"       | {M[1,0]:>10.4f}  {M[1,1]:>10.4f} |\n"
    f"{'-' * 30}\n"
    f"masa_piso = {masa_piso:.4f} t.s2/m"
)
ax8.text(0.5, 0.5, matriz_m, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 9: Ficha técnica
# ============================================================
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

ficha = (
    f"FICHA TECNICA DINAMICA\n"
    f"{'-' * 32}\n"
    f"Proyecto:\n"
    f"  UNESUM-REZ-2026\n"
    f"Caso: {CASO}\n"
    f"{'-' * 32}\n"
    f"MODELO:\n"
    f"  n_pisos = {n_pisos}\n"
    f"  He = {He:.2f} m\n"
    f"  H_total = {H_total:.2f} m\n"
    f"{'-' * 32}\n"
    f"PROPIEDADES:\n"
    f"  E = {E_tm2:.0f} t/m2\n"
    f"  masa_piso = {masa_piso:.4f} t.s2/m\n"
    f"  k_entrepiso = {k_entrepiso:.0f} t/m\n"
    f"{'-' * 32}\n"
    f"MODOS:\n"
    f"  T1 = {T[0]:.4f} s | f1 = {frec[0]:.4f} Hz\n"
    f"  T2 = {T[1]:.4f} s | f2 = {frec[1]:.4f} Hz\n"
    f"{'-' * 32}\n"
    f"Estado: OK"
)

ax9.text(0.02, 0.98, ficha, transform=ax9.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.96])

nombre_img = f"dashboard_M07_dinamico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120)
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)