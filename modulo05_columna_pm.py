# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 05 — ALGORITMO 3: DIAGRAMA P-M + MODELO 3D
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Diagrama de interacción P-M completo
            Curva de capacidad + Demanda
            Modelo 3D de la columna
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
TITULO = "DIAGRAMA P-M + MODELO 3D"
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

Ag_col = ancho_col * prof_col
As = 4 * 0.00785 * phi_esq**2 + 8 * 0.00785 * phi_long**2
cuantia = As / Ag_col

Md = 17.32  # t·m (del M03)

# ============================================================================
# 4. DIAGRAMA DE INTERACCIÓN P-M
# ============================================================================

def diagrama_interaccion(b, h, As, fc, fy, Es=2.1e6, rec=2.5, phi_est=1.0, phi_var=1.6):
    b_cm = b
    h_cm = h
    d = h_cm - rec - phi_est - phi_var/2
    d_prime = rec + phi_est + phi_var/2

    As_total = As
    As_traccion = As_total / 2
    As_compresion = As_total / 2

    if fc <= 280:
        beta1 = 0.85
    else:
        beta1 = 0.85 - 0.05 * (fc - 280) / 70
        beta1 = max(0.65, beta1)

    eps_cu = 0.003
    c_vals = np.linspace(0.1, 3 * h_cm, 500)

    P_vals, M_vals = [], []

    for c in c_vals:
        eps_s = eps_cu * (d - c) / c
        eps_s_prime = eps_cu * (c - d_prime) / c

        fs = min(max(eps_s * Es, -fy), fy)
        fs_prime = min(max(eps_s_prime * Es, -fy), fy)

        a = beta1 * c
        Cc = 0.85 * fc * b_cm * a
        Cs = As_compresion * (fs_prime - 0.85 * fc)
        Ts = As_traccion * fs

        Pn = Cc + Cs - Ts

        y_c = h_cm / 2
        M_c = Cc * (y_c - a / 2)
        M_s = Cs * (y_c - d_prime) + Ts * (d - y_c)
        Mn = M_c + M_s

        P_vals.append(Pn / 1000)
        M_vals.append(Mn / 100000)

    return np.array(P_vals), np.array(M_vals)

P_curve, M_curve = diagrama_interaccion(ancho_col, prof_col, As, fc, fy)

idx_bal = np.argmax(M_curve)
M_bal = M_curve[idx_bal]
P_bal = P_curve[idx_bal]

# ============================================================================
# 5. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M05 - ALGORITMO 3] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n📐 DATOS DEL MODELO:")
print(f"  At = {At:.2f} m²")
print(f"  Cu = {Cu:.4f} t/m²")
print(f"  Pu = {Pu:.2f} t")
print(f"  Md = {Md:.2f} t·m")
print(f"  Sección = {ancho_col} × {prof_col} cm")
print(f"  As = {As:.2f} cm²")
print(f"  ρ = {cuantia*100:.2f}%")

print(f"\n📐 DIAGRAMA DE INTERACCIÓN P-M:")
print(f"  Punto de balance: P = {P_bal:.2f} t, M = {M_bal:.2f} t·m")
print(f"  Demanda: P = {Pu:.2f} t, M = {Md:.2f} t·m")
print(f"  Verificación: {'✅ CUMPLE' if Md <= M_bal else '❌ NO CUMPLE'}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 6. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M05"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M05_pm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M05 - ALGORITMO 3] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS DEL MODELO:\n")
    f.write(f"  At = {At:.2f} m²\n")
    f.write(f"  Cu = {Cu:.4f} t/m²\n")
    f.write(f"  Pu = {Pu:.2f} t\n")
    f.write(f"  Md = {Md:.2f} t·m\n")
    f.write(f"  As = {As:.2f} cm²\n\n")
    f.write(f"DIAGRAMA P-M:\n")
    f.write(f"  P_bal = {P_bal:.2f} t\n")
    f.write(f"  M_bal = {M_bal:.2f} t·m\n")
    f.write(f"  Pu = {Pu:.2f} t | Md = {Md:.2f} t·m\n")
    f.write(f"  Verificación: {'CUMPLE' if Md <= M_bal else 'NO CUMPLE'}\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 7. DASHBOARD GRÁFICO
# ============================================================================

fig = plt.figure(figsize=(18, 12))
fig.suptitle(
    f'DASHBOARD M05 — DIAGRAMA P-M + MODELO 3D\n'
    f'{PROYECTO} | {CASO}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(
    2, 2,
    figure=fig,
    width_ratios=[1.2, 1],
    height_ratios=[1, 1],
    hspace=0.35,
    wspace=0.30
)

# ============================================================
# PANEL 1: Diagrama P-M
# ============================================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(M_curve, P_curve, 'b-', linewidth=2.5, label='Curva de interacción')
ax1.plot(Md, Pu, 'ro', markersize=14, label=f'Demanda: ({Md:.1f}, {Pu:.1f})')
ax1.plot(M_bal, P_bal, 'g*', markersize=20, label=f'Balance: ({M_bal:.1f}, {P_bal:.1f})')

ax1.axhline(y=Pu, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(x=Md, color='gray', linestyle='--', alpha=0.5)
ax1.fill_betweenx(P_curve, 0, M_curve, alpha=0.15, color='green')
ax1.axhspan(0, P_bal, alpha=0.1, color='red', label='Zona de tensión')
ax1.axhspan(P_bal, max(P_curve), alpha=0.1, color='blue', label='Zona de compresión')

ax1.set_xlabel('Momento M (t·m)', fontsize=11)
ax1.set_ylabel('Carga axial P (t)', fontsize=11)
ax1.set_title('(a) Diagrama de interacción P-M', fontsize=12, fontweight='bold')
ax1.legend(fontsize=9, loc='best')
ax1.grid(True, alpha=0.3)

# ============================================================
# PANEL 2: Sección transversal
# ============================================================
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(-5, ancho_col + 5)
ax2.set_ylim(-5, prof_col + 5)
ax2.set_aspect('equal')
ax2.add_patch(Rectangle((0, 0), ancho_col, prof_col,
                         linewidth=2, edgecolor='black', facecolor='#e8e8e8'))
ax2.add_patch(Rectangle((rec, rec), ancho_col - 2*rec, prof_col - 2*rec,
                         linewidth=1.5, edgecolor='blue', facecolor='none'))

# Varillas esquinas
for i in range(4):
    x = rec + phi_est/10 + phi_esq/20 + i * (ancho_col - 2*rec - 2*phi_est/10 - phi_esq/10) / 3
    y = rec + phi_est/10 + phi_esq/20
    ax2.add_patch(Circle((x, y), phi_esq/20, color='red', zorder=10))

for i in range(4):
    x = rec + phi_est/10 + phi_esq/20 + i * (ancho_col - 2*rec - 2*phi_est/10 - phi_esq/10) / 3
    y = prof_col - rec - phi_est/10 - phi_esq/20
    ax2.add_patch(Circle((x, y), phi_esq/20, color='red', zorder=10))

# Varillas laterales
for i in range(1, 3):
    y = rec + phi_est/10 + phi_long/20 + i * (prof_col - 2*rec - 2*phi_est/10 - phi_long/10) / 3
    x1 = rec + phi_est/10 + phi_long/20
    x2 = ancho_col - rec - phi_est/10 - phi_long/20
    ax2.add_patch(Circle((x1, y), phi_long/20, color='red', zorder=10))
    ax2.add_patch(Circle((x2, y), phi_long/20, color='red', zorder=10))

ax2.set_title('(b) Sección transversal', fontsize=12, fontweight='bold')
ax2.set_xlabel('b (cm)', fontsize=10)
ax2.set_ylabel('h (cm)', fontsize=10)
ax2.grid(True, alpha=0.3)

# ============================================================
# PANEL 3: Modelo 3D de la columna
# ============================================================
ax3 = fig.add_subplot(gs[1, :], projection='3d')

# Dimensiones
b_3d = ancho_col / 100
h_3d = prof_col / 100
L_3d = He

# Caras de la columna
x = np.array([0, b_3d, b_3d, 0, 0])
y = np.array([0, 0, h_3d, h_3d, 0])

for z in [0, L_3d]:
    ax3.plot(x, y, zs=z, color='black', linewidth=1.5)

for i in range(4):
    ax3.plot([x[i], x[i]], [y[i], y[i]], [0, L_3d], color='black', linewidth=1.5)

# Varillas longitudinales
n_var = 12
angulos = np.linspace(0, 2*np.pi, n_var, endpoint=False)
radio_x = (b_3d/2) - rec/100
radio_y = (h_3d/2) - rec/100

for ang in angulos:
    xv = b_3d/2 + radio_x * np.cos(ang)
    yv = h_3d/2 + radio_y * np.sin(ang)
    ax3.plot([xv, xv], [yv, yv], [0, L_3d], color='red', linewidth=4, zorder=10)

# Estribos (cada 0.15 m)
n_est = 20
for z in np.linspace(0, L_3d, n_est):
    ax3.plot(x, y, zs=z, color='gray', linewidth=1, alpha=0.4)

# Zona protegida (rojo en los extremos)
ax3.plot([0, b_3d, b_3d, 0, 0], [0, 0, h_3d, h_3d, 0], zs=0, color='red', linewidth=3)
ax3.plot([0, b_3d, b_3d, 0, 0], [0, 0, h_3d, h_3d, 0], zs=L_3d, color='red', linewidth=3)

ax3.set_xlabel('X (m)', fontsize=10)
ax3.set_ylabel('Y (m)', fontsize=10)
ax3.set_zlabel('Z (m)', fontsize=10)
ax3.set_title('(c) Modelo 3D de la columna', fontsize=12, fontweight='bold')
ax3.view_init(elev=20, azim=-50)

plt.tight_layout(rect=[0, 0, 1, 0.95])

nombre_img = f"dashboard_M05_pm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
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