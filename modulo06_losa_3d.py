# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 06 — ALGORITMO 3: DEFORMADA 3D DE LA LOSA ALIVIANADA
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Deformada 3D de la losa (estilo SAP2000/ETABS)
            Superficie con mapa de colores + nervios + apoyos + columnas
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
    from mpl_toolkits.mplot3d import Axes3D
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
TITULO = "DEFORMADA 3D DE LA LOSA ALIVIANADA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DE ENTRADA (del Algoritmo 1)
# ============================================================================

h_eq = 18.06       # cm
H_losa = 25.0      # cm
bn = 10.0          # cm
bb = 50.0          # cm
tc = 5.0           # cm
hn = H_losa - tc   # cm

Cu = 1.088         # t/m²
L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0
fc, fy = 210, 4200
rec_losa = 2.0

# ============================================================================
# 3. CÁLCULOS
# ============================================================================

Lx = max(L1, L2, L3, L4)
Ly = Lx

paso_nervios = bb / 100
w_nervio = Cu * paso_nervios

# Inercia equivalente de la losa (por metro de ancho)
h_eq_m = h_eq / 100  # m
I_eq = (1.0 * h_eq_m**3) / 12  # m⁴ por metro de ancho

# Módulo de elasticidad (NEC-15)
E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
EI = E_tm2 * I_eq

# Deflexión máxima (placa simplemente apoyada)
alpha = 0.00406
delta_max = alpha * Cu * Lx**4 / (E_tm2 * h_eq_m**3)
delta_adm = Lx * 1000 / 240

# ============================================================================
# 4. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - ALGORITMO 3] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 DATOS:")
print(f"  Lx = {Lx:.2f} m | Ly = {Ly:.2f} m")
print(f"  h_eq = {h_eq:.2f} cm")
print(f"  H_losa = {H_losa:.2f} cm")
print(f"  Cu = {Cu:.3f} t/m²")
print(f"  E (NEC-15) = {E_tm2:.2f} t/m²")
print(f"  I_eq = {I_eq:.6f} m⁴")
print(f"  EI = {EI:.2f} t·m²")

print(f"\n📐 DEFLEXIÓN:")
print(f"  δ_max = {delta_max*1000:.3f} mm")
print(f"  δ_adm = {delta_adm:.3f} mm")
print(f"  {'✅ CUMPLE' if delta_max*1000 < delta_adm else '❌ NO CUMPLE'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - ALGORITMO 3] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS:\n")
    f.write(f"  Lx = {Lx:.2f} m | Ly = {Ly:.2f} m\n")
    f.write(f"  h_eq = {h_eq:.2f} cm | H_losa = {H_losa:.2f} cm\n")
    f.write(f"  Cu = {Cu:.3f} t/m²\n")
    f.write(f"  E = {E_tm2:.2f} t/m²\n")
    f.write(f"  EI = {EI:.2f} t·m²\n\n")
    f.write(f"DEFLEXIÓN:\n")
    f.write(f"  δ_max = {delta_max*1000:.3f} mm\n")
    f.write(f"  δ_adm = {delta_adm:.3f} mm\n")
    f.write(f"  Estado = {'CUMPLE' if delta_max*1000 < delta_adm else 'NO CUMPLE'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD GRÁFICO (DEFORMADA 3D)
# ============================================================================

fig = plt.figure(figsize=(16, 10), facecolor='#1e1e2e')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#1e1e2e')

# Malla de la deformada
nx, ny = 40, 40
x = np.linspace(0, Lx, nx)
y = np.linspace(0, Ly, ny)
X, Y = np.meshgrid(x, y)

# Forma de la deformada (doble seno)
delta = delta_max * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)

# Superficie deformada (amplificada x10 para visualización)
surf = ax.plot_surface(X, Y, -delta * 10,
                        cmap='jet',
                        edgecolor='none',
                        alpha=0.95,
                        rstride=1, cstride=1,
                        linewidth=0)

# Colorbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label('Desplazamiento (mm x 10)', color='white', fontsize=10)
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Nervios visibles
for i in range(0, nx, 4):
    ax.plot(X[i, :], Y[i, :], -delta[i, :] * 10,
            color='white', alpha=0.2, linewidth=0.5)
for j in range(0, ny, 4):
    ax.plot(X[:, j], Y[:, j], -delta[:, j] * 10,
            color='white', alpha=0.2, linewidth=0.5)

# Bordes (apoyos)
ax.plot([0, Lx], [0, 0], [0, 0], color='cyan', linewidth=3)
ax.plot([0, Lx], [Ly, Ly], [0, 0], color='cyan', linewidth=3)
ax.plot([0, 0], [0, Ly], [0, 0], color='cyan', linewidth=3)
ax.plot([Lx, Lx], [0, Ly], [0, 0], color='cyan', linewidth=3)

# Columnas en las esquinas
for cx, cy in [(0, 0), (Lx, 0), (0, Ly), (Lx, Ly)]:
    ax.plot([cx, cx], [cy, cy], [0, -0.5], color='red', linewidth=5, alpha=0.9)

# Ejes
ax.set_xlabel('X (m)', color='white', fontsize=11, labelpad=10)
ax.set_ylabel('Y (m)', color='white', fontsize=11, labelpad=10)
ax.set_zlabel('Z (mm x 10)', color='white', fontsize=11, labelpad=10)

# Título
ax.set_title(
    f'DEFORMADA 3D DE LA LOSA - ESTILO SAP2000/ETABS\n'
    f'Proyecto UNESUM-REZ-2026-JIPIJAPA-001\n'
    f'd_max = {delta_max*1000:.2f} mm | L/240 = {delta_adm:.1f} mm',
    color='#5dade2', fontsize=13, fontweight='bold', pad=20
)

# Colores de ticks
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.tick_params(axis='z', colors='white')

# Vista
ax.view_init(elev=25, azim=-50)
ax.set_box_aspect([1, 1, 0.5])
ax.grid(True, alpha=0.2)

# Mensaje
fig.text(0.98, 0.01,
    '"La deformada no es un error.\n'
    'Es la estructura hablando, diciéndonos como trabaja."\n'
    ' - Proyecto UNESUM-REZ-2026-JIPIJAPA-001',
    ha='right', va='bottom',
    fontsize=8, style='italic', color='#f39c12',
    bbox=dict(boxstyle='round,pad=0.5',
              facecolor='#1e1e2e',
              edgecolor='#f39c12',
              linewidth=1.5,
              alpha=0.95))

plt.tight_layout()

nombre_img = f"dashboard_M06_3d_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120, facecolor='#1e1e2e')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando grafica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)