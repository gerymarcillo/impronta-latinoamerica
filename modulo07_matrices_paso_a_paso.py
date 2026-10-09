# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 07 — MATRICES DE RIGIDEZ Y MASA (DESARROLLO PASO A PASO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Desarrollo analítico secuencial de:
            1. Coeficientes de rigidez K11, K21, K31, K41
               (integración de la ecuación de la elástica)
            2. Valores de masa desde la carga
            3. Método por cortante (shear building)
            SIN gráficas modales (esas están en el otro algoritmo)
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
TITULO = "MATRICES DE RIGIDEZ Y MASA — DESARROLLO PASO A PASO"
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
# 3. IMPRESIÓN EN CONSOLA — PARTE 1: COEFICIENTES DE RIGIDEZ
# ============================================================================

print("=" * 80)
print(f"[M07] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n" + "=" * 80)
print("PARTE 1: COEFICIENTES DE RIGIDEZ (INTEGRACIÓN DE LA ELÁSTICA)")
print("=" * 80)

print("\n📐 ECUACIÓN DIFERENCIAL DE LA ELÁSTICA:")
print("   EI · d²y/dx² = K₁₁·x - K₂₁")

print("\n📐 PRIMERA INTEGRACIÓN (rotación):")
print("   EI · dy/dx = K₁₁·x²/2 - K₂₁·x + C₁")

print("\n📐 SEGUNDA INTEGRACIÓN (deflexión):")
print("   EI · y = K₁₁·x³/6 - K₂₁·x²/2 + C₁·x + C₂")

print("\n📐 CONDICIONES DE BORDE:")
print("   i) dy/dx = 0 en x = 0  →  C₁ = 0")
print("   ii) y = 1 en x = 0      →  C₂ = EI")
print("   iii) dy/dx = 0 en x = L →  K₂₁ = K₁₁·L/2")
print("   iv) y = 0 en x = L      →  K₁₁ = 12EI/L³")

print("\n📐 APLICANDO CONDICIÓN iv):")
print("   0 = K₁₁·L³/6 - K₂₁·L²/2 + EI")
print("   0 = K₁₁·L³/6 - (K₁₁·L/2)·L²/2 + EI")
print("   0 = K₁₁·L³/6 - K₁₁·L³/4 + EI")
print("   0 = 2·K₁₁·L³/12 - 3·K₁₁·L³/12 + EI")
print("   0 = -K₁₁·L³/12 + EI")
print("   K₁₁·L³/12 = EI")
print("   K₁₁ = 12EI/L³  ✅")

print("\n📐 RESULTADOS:")
print("   K₁₁ = 12EI/L³")
print("   K₂₁ = 6EI/L²")
print("   K₃₁ = -12EI/L³")
print("   K₄₁ = 6EI/L²")

# ============================================================================
# 4. CÁLCULO NUMÉRICO DE PROPIEDADES
# ============================================================================

print("\n" + "=" * 80)
print("PARTE 2: PROPIEDADES DE LOS MATERIALES Y SECCIONES")
print("=" * 80)

E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

print(f"\n  E = 15100 · √({fc}) = {E_kgcm2:.2f} kg/cm²")
print(f"  E = {E_tm2:.2f} t/m²")

I_col = (b_col * h_col**3) / 12
I_viga = (b_viga * h_viga**3) / 12

print(f"\n  I_col = {b_col} · {h_col}³ / 12 = {I_col:.6f} m⁴")
print(f"  I_viga = {b_viga} · {h_viga}³ / 12 = {I_viga:.6f} m⁴")

At = (L1/2 + L2/2) * (L3/2 + L4/2)

print(f"\n  At = {At:.4f} m²")

# ============================================================================
# 5. PARTE 3: VALORES DE MASA DESDE LA CARGA
# ============================================================================

print("\n" + "=" * 80)
print("PARTE 3: VALORES DE MASA DESDE LA CARGA")
print("=" * 80)

masa_piso = Cu * At / g

print(f"\n  m = W/g = Cu · At / g")
print(f"  m = {Cu} · {At:.4f} / {g}")
print(f"  m = {masa_piso:.4f} t·s²/m")

M = np.array([
    [masa_piso, 0],
    [0, masa_piso]
])

print(f"\n  Matriz de masa M:")
print(f"    M = [ {M[0,0]:>10.4f}  {M[0,1]:>10.4f} ]")
print(f"        [ {M[1,0]:>10.4f}  {M[1,1]:>10.4f} ]")

# ============================================================================
# 6. PARTE 4: MÉTODO POR CORTANTE (SHEAR BUILDING)
# ============================================================================

print("\n" + "=" * 80)
print("PARTE 4: MÉTODO POR CORTANTE (SHEAR BUILDING)")
print("=" * 80)

print("\n  Modelo de cortante (shear building):")
print("    - Las vigas son infinitamente rígidas")
print("    - Las columnas se deforman por cortante")
print("    - Los desplazamientos son horizontales")

n_columnas = 4

print(f"\n  Número de columnas por piso: {n_columnas}")

k_entrepiso = n_columnas * 12 * E_tm2 * I_col / He**3

print(f"\n  k = n_col · 12 · E · I_col / He³")
print(f"  k = {n_columnas} · 12 · {E_tm2:.0f} · {I_col:.6f} / {He}³")
print(f"  k = {k_entrepiso:.2f} t/m")

K = np.array([
    [2 * k_entrepiso, -k_entrepiso],
    [-k_entrepiso, k_entrepiso]
])

print(f"\n  Matriz de rigidez K:")
print(f"    K = [ 2k   -k  ]")
print(f"        [ -k    k  ]")
print(f"\n    K = [ {K[0,0]:>10.2f}  {K[0,1]:>10.2f} ]")
print(f"        [ {K[1,0]:>10.2f}  {K[1,1]:>10.2f} ]")

# ============================================================================
# 7. PARTE 5: ANÁLISIS MODAL (SOLO IMPRESIÓN)
# ============================================================================

print("\n" + "=" * 80)
print("PARTE 5: ANÁLISIS MODAL (VALORES NUMÉRICOS)")
print("=" * 80)

M_inv = np.linalg.inv(M)
A = M_inv @ K

eigenvalues, eigenvectors = np.linalg.eig(A)

idx = np.argsort(eigenvalues)
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

omega = np.sqrt(eigenvalues)
T = 2 * np.pi / omega
frec = omega / (2 * np.pi)

print(f"\n  ω₁ = {omega[0]:.4f} rad/s")
print(f"  ω₂ = {omega[1]:.4f} rad/s")
print(f"\n  T₁ = {T[0]:.4f} s")
print(f"  T₂ = {T[1]:.4f} s")
print(f"\n  f₁ = {frec[0]:.4f} Hz")
print(f"  f₂ = {frec[1]:.4f} Hz")

print(f"\n  Forma modal 1: φ₁ = [{eigenvectors[0,0]:.4f}, {eigenvectors[1,0]:.4f}]")
print(f"  Forma modal 2: φ₂ = [{eigenvectors[0,1]:.4f}, {eigenvectors[1,1]:.4f}]")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 8. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M07_matrices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
    archivo.write("=" * 80 + "\n")
    archivo.write(f"[M07] {TITULO}\n")
    archivo.write(f"[PROYECTO] {PROYECTO}\n")
    archivo.write(f"[CASO] {CASO}\n")
    archivo.write(f"[DOCENTE] {DOCENTE}\n")
    archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    archivo.write("=" * 80 + "\n\n")
    archivo.write("PARTE 1: COEFICIENTES DE RIGIDEZ\n")
    archivo.write("  K11 = 12EI/L3\n")
    archivo.write("  K21 = 6EI/L2\n")
    archivo.write("  K31 = -12EI/L3\n")
    archivo.write("  K41 = 6EI/L2\n\n")
    archivo.write("PARTE 2: PROPIEDADES\n")
    archivo.write(f"  E = {E_tm2:.2f} t/m2\n")
    archivo.write(f"  I_col = {I_col:.6f} m4\n")
    archivo.write(f"  At = {At:.4f} m2\n\n")
    archivo.write("PARTE 3: MASA\n")
    archivo.write(f"  masa_piso = {masa_piso:.4f} t.s2/m\n\n")
    archivo.write("PARTE 4: METODO POR CORTANTE\n")
    archivo.write(f"  k_entrepiso = {k_entrepiso:.2f} t/m\n")
    archivo.write(f"  K = [{K[0,0]:.2f}, {K[0,1]:.2f}]\n")
    archivo.write(f"      [{K[1,0]:.2f}, {K[1,1]:.2f}]\n\n")
    archivo.write("PARTE 5: ANALISIS MODAL\n")
    archivo.write(f"  T1 = {T[0]:.4f} s | f1 = {frec[0]:.4f} Hz\n")
    archivo.write(f"  T2 = {T[1]:.4f} s | f2 = {frec[1]:.4f} Hz\n\n")
    archivo.write("=" * 80 + "\n")
    archivo.write(f"Frase: {FRASE}\n")
    archivo.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 9. DASHBOARD GRÁFICO (SIN GRÁFICAS MODALES)
# ============================================================================

fig = plt.figure(figsize=(18, 12))
fig.suptitle(
    f'DASHBOARD M07 — MATRICES DE RIGIDEZ Y MASA (PASO A PASO)\n'
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
# PANEL 2: Coeficientes de rigidez
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
coefs = (
    f"COEFICIENTES DE RIGIDEZ\n"
    f"{'-' * 30}\n"
    f"Integración de la elástica:\n"
    f"  EI·d²y/dx² = K11·x - K21\n\n"
    f"Condiciones de borde:\n"
    f"  dy/dx=0 en x=0  →  C1=0\n"
    f"  y=1 en x=0      →  C2=EI\n"
    f"  dy/dx=0 en x=L  →  K21=K11·L/2\n"
    f"  y=0 en x=L      →  K11=12EI/L³\n\n"
    f"RESULTADOS:\n"
    f"  K11 = 12EI/L³\n"
    f"  K21 = 6EI/L²\n"
    f"  K31 = -12EI/L³\n"
    f"  K41 = 6EI/L²"
)
ax2.text(0.5, 0.5, coefs, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 3: Masa desde la carga
# ============================================================
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
masa_txt = (
    f"VALORES DE MASA\n"
    f"{'-' * 30}\n"
    f"Masa desde la carga:\n"
    f"  m = W/g = Cu·At/g\n\n"
    f"Datos:\n"
    f"  Cu = {Cu:.3f} t/m²\n"
    f"  At = {At:.4f} m²\n"
    f"  g  = {g} m/s²\n\n"
    f"Cálculo:\n"
    f"  m = {Cu:.3f}·{At:.4f}/{g}\n"
    f"  m = {masa_piso:.4f} t·s²/m\n\n"
    f"Matriz M:\n"
    f"  M = [{masa_piso:.4f}, 0]\n"
    f"      [0, {masa_piso:.4f}]"
)
ax3.text(0.5, 0.5, masa_txt, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 4: Matriz de rigidez K
# ============================================================
ax4 = fig.add_subplot(gs[1, 0])
ax4.axis('off')
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
ax4.text(0.5, 0.5, matriz_k, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 5: Matriz de masa M
# ============================================================
ax5 = fig.add_subplot(gs[1, 1])
ax5.axis('off')
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
ax5.text(0.5, 0.5, matriz_m, ha='center', va='center',
         fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 6: Método por cortante
# ============================================================
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
cortante = (
    f"MÉTODO POR CORTANTE\n"
    f"(SHEAR BUILDING)\n"
    f"{'-' * 30}\n"
    f"Hipótesis:\n"
    f"  - Vigas infinitamente rígidas\n"
    f"  - Columnas se deforman por cortante\n"
    f"  - Desplazamientos horizontales\n\n"
    f"Rigidez de entrepiso:\n"
    f"  k = n_col·12·E·I_col/He³\n"
    f"  k = {n_columnas}·12·{E_tm2:.0f}·{I_col:.6f}/{He}³\n"
    f"  k = {k_entrepiso:.2f} t/m\n\n"
    f"Matriz K:\n"
    f"  K = [2k, -k; -k, k]"
)
ax6.text(0.5, 0.5, cortante, ha='center', va='center',
         fontsize=9, family='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 7: Ficha técnica
# ============================================================
ax7 = fig.add_subplot(gs[2, 0])
ax7.axis('off')
ficha = (
    f"FICHA TECNICA\n"
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
    f"  T1 = {T[0]:.4f} s\n"
    f"  T2 = {T[1]:.4f} s\n"
    f"{'-' * 32}\n"
    f"Estado: OK"
)
ax7.text(0.02, 0.98, ficha, transform=ax7.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

# ============================================================
# PANEL 8: Diagonal de la matriz K
# ============================================================
ax8 = fig.add_subplot(gs[2, 1])
elementos_k = [K[0,0], K[1,1], K[0,1], K[1,0]]
etiquetas_k = ['K11', 'K22', 'K12', 'K21']
colores_k = ['#3498db', '#3498db', '#e74c3c', '#e74c3c']
bars_k = ax8.bar(etiquetas_k, elementos_k, color=colores_k, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars_k, elementos_k):
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
             f'{val:.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax8.set_ylabel('Rigidez (t/m)', fontsize=10)
ax8.set_title('(h) Elementos de la matriz K', fontsize=11, fontweight='bold')
ax8.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================
# PANEL 9: Diagonal de la matriz M
# ============================================================
ax9 = fig.add_subplot(gs[2, 2])
elementos_m = [M[0,0], M[1,1], M[0,1], M[1,0]]
etiquetas_m = ['M11', 'M22', 'M12', 'M21']
colores_m = ['#2ecc71', '#2ecc71', '#f39c12', '#f39c12']
bars_m = ax9.bar(etiquetas_m, elementos_m, color=colores_m, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars_m, elementos_m):
    ax9.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax9.set_ylabel('Masa (t.s2/m)', fontsize=10)
ax9.set_title('(i) Elementos de la matriz M', fontsize=11, fontweight='bold')
ax9.grid(axis='y', linestyle='--', alpha=0.3)

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