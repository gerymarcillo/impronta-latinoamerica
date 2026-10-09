# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 07 — ALGORITMO: MATRICES DE RIGIDEZ Y MASA (ANÁLISIS ANALÍTICO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Construcción analítica paso a paso de:
            1. Matriz de rigidez K (2x2)
            2. Matriz de masa M (2x2)
            3. Análisis modal (ω, T, f, formas modales)
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
TITULO = "MATRICES DE RIGIDEZ Y MASA — ANÁLISIS ANALÍTICO"
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
# 3. CÁLCULO DE PROPIEDADES (PASO A PASO)
# ============================================================================

print("=" * 80)
print(f"[M07 - MATRICES] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n" + "=" * 80)
print("PASO 1: PROPIEDADES DE LOS MATERIALES Y SECCIONES")
print("=" * 80)

# Módulo de elasticidad (NEC-15)
E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

print(f"\n  Módulo de elasticidad (NEC-15):")
print(f"    E = 15100 · √(fc)")
print(f"    E = 15100 · √({fc})")
print(f"    E = {E_kgcm2:.2f} kg/cm²")
print(f"    E = {E_tm2:.2f} t/m²")

# Inercia de columna
I_col = (b_col * h_col**3) / 12

print(f"\n  Inercia de columna:")
print(f"    I_col = b · h³ / 12")
print(f"    I_col = {b_col} · {h_col}³ / 12")
print(f"    I_col = {I_col:.6f} m⁴")

# Inercia de viga
I_viga = (b_viga * h_viga**3) / 12

print(f"\n  Inercia de viga:")
print(f"    I_viga = b · h³ / 12")
print(f"    I_viga = {b_viga} · {h_viga}³ / 12")
print(f"    I_viga = {I_viga:.6f} m⁴")

# Área tributaria
At = (L1/2 + L2/2) * (L3/2 + L4/2)

print(f"\n  Área tributaria:")
print(f"    At = (L1/2 + L2/2) · (L3/2 + L4/2)")
print(f"    At = (5.5/2 + 6.0/2) · (5.5/2 + 6.0/2)")
print(f"    At = {At:.4f} m²")

# ============================================================================
# 4. CONSTRUCCIÓN DE LA MATRIZ DE RIGIDEZ K (PASO A PASO)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 2: CONSTRUCCIÓN DE LA MATRIZ DE RIGIDEZ K")
print("=" * 80)

print("\n  Modelo de cortante (shear building):")
print("    Cada piso tiene una rigidez de entrepiso k_i")
print("    La matriz de rigidez es tridiagonal")

# Número de columnas
n_columnas = 4

print(f"\n  Número de columnas por piso: {n_columnas}")

# Rigidez de entrepiso
k_entrepiso = n_columnas * 12 * E_tm2 * I_col / He**3

print(f"\n  Rigidez de entrepiso k:")
print(f"    k = n_col · 12 · E · I_col / He³")
print(f"    k = {n_columnas} · 12 · {E_tm2:.0f} · {I_col:.6f} / {He}³")
print(f"    k = {k_entrepiso:.2f} t/m")

# Matriz de rigidez K (2x2)
K = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso, k_entrepiso]
])

print(f"\n  Matriz de rigidez K (2x2):")
print(f"    K = [ 2k   -k  ]")
print(f"        [ -k    k  ]")
print(f"\n    K = [ {K[0,0]:>10.2f}  {K[0,1]:>10.2f} ]")
print(f"        [ {K[1,0]:>10.2f}  {K[1,1]:>10.2f} ]")

# ============================================================================
# 5. CONSTRUCCIÓN DE LA MATRIZ DE MASA M (PASO A PASO)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 3: CONSTRUCCIÓN DE LA MATRIZ DE MASA M")
print("=" * 80)

print("\n  Modelo de masa concentrada (lumped mass):")
print("    Cada piso tiene una masa m_i")
print("    La matriz de masa es diagonal")

# Masa por piso
masa_piso = Cu * At / g

print(f"\n  Masa por piso m:")
print(f"    m = Cu · At / g")
print(f"    m = {Cu} · {At:.4f} / {g}")
print(f"    m = {masa_piso:.4f} t·s²/m")

# Matriz de masa M (2x2)
M = np.array([
    [masa_piso, 0],
    [0, masa_piso]
])

print(f"\n  Matriz de masa M (2x2):")
print(f"    M = [ m   0  ]")
print(f"        [ 0   m  ]")
print(f"\n    M = [ {M[0,0]:>10.4f}  {M[0,1]:>10.4f} ]")
print(f"        [ {M[1,0]:>10.4f}  {M[1,1]:>10.4f} ]")

# ============================================================================
# 6. ANÁLISIS MODAL (PASO A PASO)
# ============================================================================

print("\n" + "=" * 80)
print("PASO 4: ANÁLISIS MODAL")
print("=" * 80)

print("\n  Ecuación de autovalores:")
print("    K · φ = ω² · M · φ")
print("    M⁻¹ · K · φ = ω² · φ")

# Resolver problema de valores propios
M_inv = np.linalg.inv(M)
A = M_inv @ K

print(f"\n  Matriz A = M⁻¹ · K:")
print(f"    A = [ {A[0,0]:>10.4f}  {A[0,1]:>10.4f} ]")
print(f"        [ {A[1,0]:>10.4f}  {A[1,1]:>10.4f} ]")

# Autovalores y autovectores
eigenvalues, eigenvectors = np.linalg.eig(A)

# Ordenar de menor a mayor
idx = np.argsort(eigenvalues)
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

# Frecuencias naturales (rad/s)
omega = np.sqrt(eigenvalues)

# Períodos naturales (s)
T = 2 * np.pi / omega

# Frecuencias en Hz
frec = omega / (2 * np.pi)

print(f"\n  Autovalores (ω²):")
print(f"    λ₁ = {eigenvalues[0]:.4f} (rad/s)²")
print(f"    λ₂ = {eigenvalues[1]:.4f} (rad/s)²")

print(f"\n  Frecuencias naturales ω:")
print(f"    ω₁ = {omega[0]:.4f} rad/s")
print(f"    ω₂ = {omega[1]:.4f} rad/s")

print(f"\n  Períodos naturales T:")
print(f"    T₁ = 2π / ω₁ = {T[0]:.4f} s")
print(f"    T₂ = 2π / ω₂ = {T[1]:.4f} s")

print(f"\n  Frecuencias en Hz:")
print(f"    f₁ = ω₁ / 2π = {frec[0]:.4f} Hz")
print(f"    f₂ = ω₂ / 2π = {frec[1]:.4f} Hz")

print(f"\n  Formas modales (autovectores):")
print(f"    Modo 1: φ₁ = [{eigenvectors[0,0]:.4f}, {eigenvectors[1,0]:.4f}]")
print(f"    Modo 2: φ₂ = [{eigenvectors[0,1]:.4f}, {eigenvectors[1,1]:.4f}]")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M07_matrices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
    archivo.write("=" * 80 + "\n")
    archivo.write(f"[M07 - MATRICES] {TITULO}\n")
    archivo.write(f"[PROYECTO] {PROYECTO}\n")
    archivo.write(f"[CASO] {CASO}\n")
    archivo.write(f"[DOCENTE] {DOCENTE}\n")
    archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    archivo.write("=" * 80 + "\n\n")
    archivo.write(f"PROPIEDADES:\n")
    archivo.write(f"  E = {E_tm2:.2f} t/m²\n")
    archivo.write(f"  I_col = {I_col:.6f} m⁴\n")
    archivo.write(f"  I_viga = {I_viga:.6f} m⁴\n")
    archivo.write(f"  At = {At:.4f} m²\n")
    archivo.write(f"  masa_piso = {masa_piso:.4f} t·s²/m\n")
    archivo.write(f"  k_entrepiso = {k_entrepiso:.2f} t/m\n\n")
    archivo.write(f"MATRIZ DE RIGIDEZ K (t/m):\n")
    archivo.write(f"  K = [{K[0,0]:.2f}, {K[0,1]:.2f}]\n")
    archivo.write(f"      [{K[1,0]:.2f}, {K[1,1]:.2f}]\n\n")
    archivo.write(f"MATRIZ DE MASA M (t·s²/m):\n")
    archivo.write(f"  M = [{M[0,0]:.4f}, {M[0,1]:.4f}]\n")
    archivo.write(f"      [{M[1,0]:.4f}, {M[1,1]:.4f}]\n\n")
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
    f'DASHBOARD M07 — MATRICES DE RIGIDEZ Y MASA (ANÁLISIS ANALÍTICO)\n'
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
# PANEL 2: Matriz de rigidez K
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
matriz_k = (
    f"MATRIZ DE RIGIDEZ K (t/m)\n"
    f"{'-' * 30}\n"
    f"       | {K[0,0]:>10.2f}  {K[0,1]:>10.2f} |\n"
    f"  K =  |                        |\n"
    f"       | {K[1,0]:>10.2f}  {K[1,1]:>10.2f} |\n"
    f"{'-' * 30}\n"
    f"Fórmula:\n"
    f"  K = [ 2k  -k ]\n"
    f"      [ -k   k ]\n"
    f"{'-' * 30}\n"
    f"k_entrepiso = {k_entrepiso:.0f} t/m"
)
ax2.text(0.5, 0.5, matriz_k, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 3: Matriz de masa M
# ============================================================
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
matriz_m = (
    f"MATRIZ DE MASA M (t.s2/m)\n"
    f"{'-' * 30}\n"
    f"       | {M[0,0]:>10.4f}  {M[0,1]:>10.4f} |\n"
    f"  M =  |                        |\n"
    f"       | {M[1,0]:>10.4f}  {M[1,1]:>10.4f} |\n"
    f"{'-' * 30}\n"
    f"Fórmula:\n"
    f"  M = [ m  0 ]\n"
    f"      [ 0  m ]\n"
    f"{'-' * 30}\n"
    f"masa_piso = {masa_piso:.4f} t.s2/m"
)
ax3.text(0.5, 0.5, matriz_m, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 4: Períodos modales
# ============================================================
ax4 = fig.add_subplot(gs[1, 0])
modos = ['Modo 1', 'Modo 2']
colores = ['#3498db', '#e74c3c']
bars = ax4.bar(modos, T, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, T):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{val:.4f} s', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax4.set_ylabel('Período (s)', fontsize=10)
ax4.set_title('(d) Períodos modales', fontsize=11, fontweight='bold')
ax4.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 5: Frecuencias modales
# ============================================================
ax5 = fig.add_subplot(gs[1, 1])
bars = ax5.bar(modos, frec, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, frec):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.4f} Hz', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax5.set_ylabel('Frecuencia (Hz)', fontsize=10)
ax5.set_title('(e) Frecuencias modales', fontsize=11, fontweight='bold')
ax5.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 6: Ficha técnica
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ficha = (
    f"FICHA TECNICA ANALITICA\n"
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
    f"  I_col = {I_col:.6f} m4\n"
    f"  masa_piso = {masa_piso:.4f} t.s2/m\n"
    f"  k_entrepiso = {k_entrepiso:.0f} t/m\n"
    f"{'-' * 32}\n"
    f"MODOS:\n"
    f"  T1 = {T[0]:.4f} s | f1 = {frec[0]:.4f} Hz\n"
    f"  T2 = {T[1]:.4f} s | f2 = {frec[1]:.4f} Hz\n"
    f"{'-' * 32}\n"
    f"Estado: OK"
)
ax6.text(0.02, 0.98, ficha, transform=ax6.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 7: Modo 1 (forma modal)
# ============================================================
ax7 = fig.add_subplot(gs[2, 0])
alturas = [0, He, H_total]
forma1 = [0, eigenvectors[0, 0], eigenvectors[1, 0]]
forma1_norm = [x / max(abs(eigenvectors[:, 0])) for x in forma1]
ax7.plot(forma1_norm, alturas, 'bo-', linewidth=3, markersize=10, label='Modo 1')
ax7.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax7.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax7.set_ylabel('Altura (m)', fontsize=10)
ax7.set_title(f'(g) Modo 1: T1 = {T[0]:.4f} s', fontsize=11, fontweight='bold')
ax7.legend(fontsize=9)
ax7.grid(True, alpha=0.3)

# ============================================================
# PANEL 8: Modo 2 (forma modal)
# ============================================================
ax8 = fig.add_subplot(gs[2, 1])
forma2 = [0, eigenvectors[0, 1], eigenvectors[1, 1]]
forma2_norm = [x / max(abs(eigenvectors[:, 1])) for x in forma2]
ax8.plot(forma2_norm, alturas, 'ro-', linewidth=3, markersize=10, label='Modo 2')
ax8.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax8.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax8.set_ylabel('Altura (m)', fontsize=10)
ax8.set_title(f'(h) Modo 2: T2 = {T[1]:.4f} s', fontsize=11, fontweight='bold')
ax8.legend(fontsize=9)
ax8.grid(True, alpha=0.3)

# ============================================================
# PANEL 9: Formas modales superpuestas
# ============================================================
ax9 = fig.add_subplot(gs[2, 2])
ax9.plot(forma1_norm, alturas, 'bo-', linewidth=3, markersize=10, label=f'Modo 1 (T1={T[0]:.3f}s)')
ax9.plot(forma2_norm, alturas, 'ro-', linewidth=3, markersize=10, label=f'Modo 2 (T2={T[1]:.3f}s)')
ax9.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax9.set_xlabel('Desplazamiento normalizado', fontsize=10)
ax9.set_ylabel('Altura (m)', fontsize=10)
ax9.set_title('(i) Formas modales superpuestas', fontsize=11, fontweight='bold')
ax9.legend(fontsize=9)
ax9.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])

nombre_img = f"dashboard_M07_matrices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120)
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)