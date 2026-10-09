# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 06 - ALGORITMO 1: DISENO ANALITICO DE LOSA ALIVIANADA (CORREGIDO)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 + NEC-15
OBJETIVO: Diseno analitico de losa alivianada
          - Inercia equivalente por Steiner
          - Bloque de compresion "a"
          - Momento positivo y negativo
          - Acero positivo y negativo
          - Verificacion de deflexion L/240
          - DASHBOARD MEJOR QUE REVIT
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
    from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("matplotlib no esta instalado. Ejecute: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Losa del Colegio Alejo Lascano"
TITULO = "DISENO ANALITICO DE LOSA ALIVIANADA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 + NEC-15"
FRASE = "La losa es el diafragma que une todo. Sin ella, no hay portico. Sin portico, no hay resiliencia."

# ============================================================================
# 2. DATOS DE ENTRADA (de la GUIA OFICIAL M06)
# ============================================================================

# Geometria
L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0
He = 2.6
Pisos = 2

# Cargas
Cm = 0.62
Cv = 0.20

# Losa
H_losa = 25.0
h_eq = 18.06
bn = 10.0
bb = 50.0
tc = 5.0
hn = H_losa - tc

# Materiales
fc = 210
fy = 4200

# Recubrimiento
rec_losa = 2.5

# Diametros
phi_pos = 8
phi_neg = 10
phi_temp = 8

# ============================================================================
# 3. CALCULOS SEGUN GUIA OFICIAL
# ============================================================================

# --- PASO 1: Area tributaria ---
At = (L1/2 + L2/2) * (L3/2 + L4/2)

# --- PASO 2: Carga ultima ---
Cu = 1.2 * (Cm * Pisos) + 1.6 * (Cv * Pisos)

# --- PASO 3: Predimensionamiento (NEC-15) ---
Lx = max(L1, L2, L3, L4)  # Luz critica
Ly = Lx

# --- PASO 4: Inercia equivalente (Steiner) ---
# Capa de compresion
A1 = bb * tc
y1 = H_losa - tc/2
I1 = bb * tc**3 / 12

# Nervio
A2 = bn * hn
y2 = hn / 2
I2 = bn * hn**3 / 12

# Centroide
At_seccion = A1 + A2
ycg = (A1*y1 + A2*y2) / At_seccion

# Inercia total
I_total = I1 + A1*(y1-ycg)**2 + I2 + A2*(y2-ycg)**2

# Altura equivalente
h_eq_calc = (12 * I_total / bb)**(1/3)

# --- PASO 5: Momento formula del docente ---
M_docente = 0.08 * Cu * (L1/2 + L2/2) * Lx**2

# --- PASO 6: Momento por metro (ETABS) ---
w_nervio = Cu * (bb/100)
M_pos_metro = w_nervio * Lx**2 / 8
M_neg_metro = M_pos_metro * 0.8

# --- PASO 7: Acero de refuerzo ---
d_nervio = H_losa - rec_losa - phi_pos/20
b_ef = min(bb, Lx*100/4)

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

As_pos_nervio = calcular_as_viga_T(M_pos_metro * (bb/100), bn, b_ef, d_nervio, fc, fy)
As_pos_metro = As_pos_nervio / (bb/100)

# --- PASO 8: Acero minimo ---
As_min = 0.0018 * 100 * H_losa

# --- PASO 9: Verificacion de deflexion (USANDO I_eq) ---
I_eq = bb * h_eq**3 / 12  # cm4
I_eq_m4 = I_eq / 1e8       # m4

E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
EI = E_tm2 * I_eq_m4

# Deflexion con Cu total y Lx critica
delta_max = 5 * Cu * Lx**4 / (384 * EI)
delta_adm = Lx * 1000 / 240

# --- PASO 10: Bloque de compresion "a" ---
a_cm = As_pos_nervio * fy / (0.85 * fc * b_ef)
rel_a_h = a_cm / H_losa

# --- Diametros de varillas ---
As_1phi8 = np.pi * (8/10)**2 / 4
As_1phi10 = np.pi * (10/10)**2 / 4

# --- Separacion de varillas ---
n_pos = max(int(np.ceil(As_pos_metro / As_1phi8)), 1)
s_pos = 100 / n_pos

n_neg = max(int(np.ceil(M_neg_metro * 100000 / (0.9 * fy * (d_nervio - 2)) / 100 / As_1phi10)), 1)
s_neg = 100 / n_neg

# --- Verificaciones ---
tic_relacion = Lx * 100 / H_losa <= 28
tic_deflexion = delta_max < delta_adm
tic_bloque_a = 15 <= rel_a_h*100 <= 25

# ============================================================================
# 4. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M06 - A1] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- DATOS DE ENTRADA ---")
print(f"  L1, L2 = {L1}, {L2} m")
print(f"  L3, L4 = {L3}, {L4} m")
print(f"  Cm = {Cm} t/m2 | Cv = {Cv} t/m2 | Pisos = {Pisos}")
print(f"  H_losa = {H_losa} cm | h_eq = {h_eq} cm")
print(f"  bn = {bn} cm | bb = {bb} cm | tc = {tc} cm")

print(f"\n--- PASO 1: AREA TRIBUTARIA ---")
print(f"  At = ({L1}/2 + {L2}/2) x ({L3}/2 + {L4}/2) = {At:.2f} m2")

print(f"\n--- PASO 2: CARGA ULTIMA ---")
print(f"  Cu = 1.2*({Cm}*{Pisos}) + 1.6*({Cv}*{Pisos}) = {Cu:.3f} t/m2")

print(f"\n--- PASO 3: PREDIMENSIONAMIENTO ---")
print(f"  Lx critica = {Lx:.2f} m")
print(f"  Espesor = {H_losa:.0f} cm (segun NEC-15)")

print(f"\n--- PASO 4: INERCIA EQUIVALENTE ---")
print(f"  A1 = {A1:.1f} cm2 | A2 = {A2:.1f} cm2")
print(f"  y_cg = {ycg:.2f} cm")
print(f"  I_total = {I_total:.1f} cm4")
print(f"  h_eq = {h_eq_calc:.2f} cm")
print(f"  I_eq = {I_eq:.1f} cm4 = {I_eq_m4:.6f} m4")
print(f"  EI = {EI:.2f} t.m2")

print(f"\n--- PASO 5: MOMENTO (docente) ---")
print(f"  M = 0.08 x Cu x Lt x Lx^2 = {M_docente:.2f} t.m")

print(f"\n--- PASO 6: MOMENTOS POR METRO ---")
print(f"  w_nervio = Cu x (bb/100) = {w_nervio:.4f} t/m")
print(f"  M_pos = {M_pos_metro:.3f} t.m/m")
print(f"  M_neg = {M_neg_metro:.3f} t.m/m")

print(f"\n--- PASO 7: ACERO DE REFUERZO ---")
print(f"  As_pos = {As_pos_metro:.3f} cm2/m")
print(f"  n_pos = {n_pos} varillas phi{phi_pos}")
print(f"  s_pos = {s_pos:.1f} cm")

print(f"\n--- PASO 8: ACERO MINIMO ---")
print(f"  As_min = {As_min:.2f} cm2/m")

print(f"\n--- PASO 9: VERIFICACION DE DEFLEXION ---")
print(f"  delta_max = {delta_max*1000:.2f} mm")
print(f"  delta_adm = {delta_adm:.2f} mm")
print(f"  {'CUMPLE' if tic_deflexion else 'NO CUMPLE'}")

print(f"\n--- PASO 10: BLOQUE DE COMPRESION ---")
print(f"  a = {a_cm:.2f} cm")
print(f"  a/h = {rel_a_h*100:.1f}% (ideal ~20%)")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 5. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M06"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M06_algoritmo1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M06 - A1] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[NORMA] {NORMA}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"At = {At:.2f} m2\n")
    f.write(f"Cu = {Cu:.3f} t/m2\n")
    f.write(f"I_total = {I_total:.1f} cm4\n")
    f.write(f"h_eq = {h_eq_calc:.2f} cm\n")
    f.write(f"I_eq = {I_eq_m4:.6f} m4\n")
    f.write(f"EI = {EI:.2f} t.m2\n")
    f.write(f"M_docente = {M_docente:.2f} t.m\n")
    f.write(f"M_pos = {M_pos_metro:.3f} t.m/m\n")
    f.write(f"As_pos = {As_pos_metro:.3f} cm2/m\n")
    f.write(f"delta_max = {delta_max*1000:.2f} mm\n")
    f.write(f"delta_adm = {delta_adm:.2f} mm\n")
    f.write(f"Estado = {'CUMPLE' if tic_deflexion else 'NO CUMPLE'}\n")
    f.write("\n" + "=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 6. DASHBOARD 2D (6 PANELES) - MEJOR QUE REVIT
# ============================================================================

fig1 = plt.figure(figsize=(20, 14), num='M06-A1: Dashboard Losa Alivianada')
fig1.suptitle(
    f"M06 - ALGORITMO 1: DISENO ANALITICO DE LOSA ALIVIANADA\n"
    f"{PROYECTO} | {NORMA}",
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs1 = GridSpec(3, 2, figure=fig1,
               width_ratios=[1, 1], height_ratios=[1, 1, 1],
               hspace=0.45, wspace=0.30)

# ------------------------------------------------------------------
# (a) SECCION TRANSVERSAL + BLOQUE "a"
# ------------------------------------------------------------------
ax1 = fig1.add_subplot(gs1[0, 0])
ax1.set_xlim(-8, bb + 20)
ax1.set_ylim(-5, H_losa + 8)
ax1.set_aspect('equal')

# Capa de compresion
ax1.add_patch(Rectangle((0, H_losa - tc), bb, tc,
                         facecolor='#3498db', edgecolor='black', lw=1.5, alpha=0.8))

# Nervio
x_nervio = (bb - bn) / 2
ax1.add_patch(Rectangle((x_nervio, 0), bn, hn,
                         facecolor='#95a5a6', edgecolor='black', lw=1.5, alpha=0.9))

# Bloque "a" (zona que trabaja)
y_a = H_losa - a_cm
ax1.add_patch(Rectangle((0, y_a), bb, a_cm,
                         facecolor='green', alpha=0.3, edgecolor='darkgreen', lw=2))

# Varilla positiva
ax1.add_patch(Circle((bb/2, rec_losa + phi_pos/20), phi_pos/20,
                      color='red', zorder=10))

# Varilla temperatura
ax1.add_patch(Circle((bb/2, H_losa - rec_losa - phi_temp/20), phi_temp/20,
                      color='blue', zorder=10))

ax1.text(bb/2, H_losa - tc/2, "Capa de compresion",
         ha="center", va="center", fontsize=8, fontweight="bold", color="white")
ax1.text(bb/2, hn/2, f"Nervio\n{bn}x{hn:.0f}",
         ha="center", va="center", fontsize=8, fontweight="bold")
ax1.text(bb/2, y_a + a_cm/2, f"BLOQUE a = {a_cm:.2f} cm",
         ha="center", va="center", fontsize=9, fontweight="bold", color='darkgreen')
ax1.text(bb/2, y_a/2, f"NO TRABAJA",
         ha="center", va="center", fontsize=8, color='gray', style='italic')

ax1.text(bb + 3, rec_losa + phi_pos/20, f"1 phi{phi_pos}",
         ha='left', va='center', fontsize=8, color='red', fontweight='bold')
ax1.text(bb + 3, H_losa - rec_losa - phi_temp/20, f"phi{phi_temp} @ {s_pos:.0f}",
         ha='left', va='center', fontsize=8, color='blue', fontweight='bold')

ax1.set_title(f'(a) Seccion del nervio + bloque a', fontsize=11, fontweight='bold')
ax1.set_xlabel('Ancho (cm)', fontsize=10)
ax1.set_ylabel('Altura (cm)', fontsize=10)
ax1.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# (b) DIAGRAMA DE MOMENTOS
# ------------------------------------------------------------------
ax2 = fig1.add_subplot(gs1[0, 1])

x = np.linspace(0, Lx, 100)
M_diagrama = w_nervio * x * (Lx - x) / 2

ax2.plot(x, M_diagrama, 'b-', linewidth=2.5, label='M(x)')
ax2.fill_between(x, M_diagrama, alpha=0.15, color='blue')
ax2.axhline(y=0, color='black', linewidth=0.8)
ax2.axhline(y=M_pos_metro * (bb/100), color='red', linestyle='--', linewidth=2,
            label=f'M_pos = {M_pos_metro*(bb/100):.3f} t.m')

ax2.set_xlabel('x (m)', fontsize=10)
ax2.set_ylabel('Momento M (t.m)', fontsize=10)
ax2.set_title('(b) Diagrama de momentos del nervio', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# (c) BARRAS COMPARATIVAS
# ------------------------------------------------------------------
ax3 = fig1.add_subplot(gs1[1, 0])
categorias = ['M_pos', 'M_neg', 'As_pos', 'As_neg', 'As_min']
valores = [M_pos_metro, M_neg_metro, As_pos_metro, 0.98, As_min]
colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
bars = ax3.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax3.set_ylabel('Magnitud', fontsize=10)
ax3.set_title('(c) Momentos y Aceros de Diseno', fontsize=11, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.set_ylim(0, max(valores) * 1.3)

# ------------------------------------------------------------------
# (d) CURVA H vs h_eq (5 ESPESORES)
# ------------------------------------------------------------------
ax4 = fig1.add_subplot(gs1[1, 1])

espesores = [15, 20, 25, 30, 35]
h_eqs = []
for H_test in espesores:
    hn_test = H_test - tc
    A1_t = bb * tc
    y1_t = H_test - tc/2
    I1_t = bb * tc**3 / 12
    A2_t = bn * hn_test
    y2_t = hn_test / 2
    I2_t = bn * hn_test**3 / 12
    At_t = A1_t + A2_t
    ycg_t = (A1_t*y1_t + A2_t*y2_t) / At_t
    It_t = I1_t + A1_t*(y1_t-ycg_t)**2 + I2_t + A2_t*(y2_t-ycg_t)**2
    h_eq_t = (12 * It_t / bb)**(1/3)
    h_eqs.append(h_eq_t)

ax4.plot(espesores, h_eqs, 'o-', color='#9b59b6', linewidth=2.5,
         markersize=10, markerfacecolor='white', markeredgewidth=2)
for xx, yy in zip(espesores, h_eqs):
    ax4.annotate(f'{yy:.2f}', (xx, yy), textcoords="offset points",
                 xytext=(0, 10), ha="center", fontsize=9, fontweight='bold')
ax4.axvline(x=H_losa, color='red', linestyle='--', linewidth=2,
            label=f'H_losa = {H_losa} cm')
ax4.axhline(y=h_eq, color='green', linestyle='--', linewidth=2,
            label=f'h_eq = {h_eq:.2f} cm')

ax4.set_xlabel('H real (cm)', fontsize=10)
ax4.set_ylabel('h_eq (cm)', fontsize=10)
ax4.set_title('(d) Relacion H vs h_eq', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# ------------------------------------------------------------------
# (e) VERIFICACION DE DEFLEXION
# ------------------------------------------------------------------
ax5 = fig1.add_subplot(gs1[2, 0])
categorias_def = ['delta_max', 'delta_adm']
valores_def = [delta_max*1000, delta_adm]
colores_def = ['#2ecc71' if tic_deflexion else '#e74c3c', '#2ecc71']
bars = ax5.bar(categorias_def, valores_def, color=colores_def,
               edgecolor='black', linewidth=1.5, width=0.5)
for bar, val in zip(bars, valores_def):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f'{val:.2f} mm', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax5.set_ylabel('Deflexion (mm)', fontsize=10)
ax5.set_title(f'(e) Verificacion de deflexion\n{"CUMPLE" if tic_deflexion else "NO CUMPLE"}',
              fontsize=11, fontweight='bold')
ax5.grid(axis='y', linestyle='--', alpha=0.3)
ax5.set_ylim(0, max(valores_def) * 1.3)

# ------------------------------------------------------------------
# (f) FICHA TECNICA
# ------------------------------------------------------------------
ax6 = fig1.add_subplot(gs1[2, 1])
ax6.axis('off')

ficha = (
    f"FICHA TECNICA - LOSA ALIVIANADA\n"
    f"{'-' * 40}\n"
    f"Proyecto: UNESUM-REZ-2026\n"
    f"Norma: {NORMA}\n"
    f"{'-' * 40}\n"
    f"GEOMETRIA:\n"
    f"  At = {At:.2f} m2\n"
    f"  Cu = {Cu:.3f} t/m2\n"
    f"  H_losa = {H_losa:.0f} cm\n"
    f"  h_eq = {h_eq:.2f} cm\n"
    f"  bn = {bn:.0f} | bb = {bb:.0f} | tc = {tc:.0f}\n"
    f"{'-' * 40}\n"
    f"INERCIA:\n"
    f"  I_total = {I_total:.0f} cm4\n"
    f"  I_eq = {I_eq_m4:.6f} m4\n"
    f"  EI = {EI:.2f} t.m2\n"
    f"{'-' * 40}\n"
    f"MOMENTOS:\n"
    f"  M_docente = {M_docente:.2f} t.m\n"
    f"  M_pos = {M_pos_metro:.3f} t.m/m\n"
    f"  M_neg = {M_neg_metro:.3f} t.m/m\n"
    f"{'-' * 40}\n"
    f"ACERO:\n"
    f"  As_pos = {As_pos_metro:.2f} cm2/m\n"
    f"  As_min = {As_min:.2f} cm2/m\n"
    f"  Positiva: phi{phi_pos} @ {s_pos:.1f} cm\n"
    f"{'-' * 40}\n"
    f"DEFLEXION:\n"
    f"  delta_max = {delta_max*1000:.2f} mm\n"
    f"  delta_adm = {delta_adm:.2f} mm\n"
    f"{'-' * 40}\n"
    f"{'CUMPLE' if tic_deflexion else 'REVISAR'}"
)

ax6.text(0.02, 0.98, ficha, transform=ax6.transAxes,
         fontsize=8.5, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))

plt.tight_layout()
plt.savefig('M06_A1_dashboard_analitico.png', dpi=150, bbox_inches='tight')
print(f"\nDashboard 2D guardado: M06_A1_dashboard_analitico.png")
plt.show(block=False)

# ============================================================================
# 7. MODELO 3D DEL NERVIO
# ============================================================================

fig2 = plt.figure(figsize=(16, 12), num='M06-A1: Modelo 3D Nervio')
ax = fig2.add_subplot(111, projection='3d')

fig2.suptitle(
    f"M06 - ALGORITMO 1: MODELO 3D DEL NERVIO\n"
    f"Seccion {bn}x{hn:.0f} cm | Armadura 1 phi{phi_pos} | H_losa = {H_losa:.0f} cm",
    fontsize=14, fontweight='bold', color='#2c3e50'
)

b_3d = bb / 100
h_3d = H_losa / 100
L_3d = Lx

vertices = [[0,0,0],[L_3d,0,0],[L_3d,b_3d,0],[0,b_3d,0],
            [0,0,h_3d],[L_3d,0,h_3d],[L_3d,b_3d,h_3d],[0,b_3d,h_3d]]
caras_idx = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
caras = [[vertices[i] for i in cara] for cara in caras_idx]

ax.add_collection3d(Poly3DCollection(caras, facecolors='#95a5a6', linewidths=1.5, edgecolors='black', alpha=0.35))

# Varilla positiva (1 phi8)
z_pos = rec_losa/100 + phi_pos/2000
ax.plot([0, L_3d], [b_3d/2, b_3d/2], [z_pos, z_pos],
        color='red', linewidth=6, solid_capstyle='round')

# Capa de compresion
ax.plot([0, L_3d], [0, 0], [h_3d, h_3d], color='black', linewidth=2)
ax.plot([0, L_3d], [b_3d, b_3d], [h_3d, h_3d], color='black', linewidth=2)

# Bloque "a"
ax.plot([0, L_3d], [0, 0], [h_3d - a_cm/100, h_3d - a_cm/100], color='green', linewidth=2, linestyle='--')
ax.plot([0, L_3d], [b_3d, b_3d], [h_3d - a_cm/100, h_3d - a_cm/100], color='green', linewidth=2, linestyle='--')

tic_3d = (
    f"LOSA ALIVIANADA\n"
    f"At = {At:.2f} m2\n"
    f"Cu = {Cu:.3f} t/m2\n"
    f"H_losa = {H_losa:.0f} cm\n"
    f"h_eq = {h_eq:.2f} cm\n"
    f"a = {a_cm:.2f} cm ({rel_a_h*100:.0f}%)\n"
    f"As_pos = {As_pos_metro:.2f} cm2/m\n"
    f"delta_max = {delta_max*1000:.2f} mm"
)
ax.text(L_3d/2, b_3d/2, h_3d + 0.15, tic_3d, color='darkgreen',
        fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                  edgecolor='green', linewidth=2))

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.set_title('Modelo 3D - Nervio de losa alivianada', fontsize=13, fontweight='bold')
ax.view_init(elev=20, azim=-55)

plt.tight_layout()
plt.savefig('M06_A1_modelo_3D.png', dpi=150, bbox_inches='tight')
print(f"Modelo 3D guardado: M06_A1_modelo_3D.png")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)