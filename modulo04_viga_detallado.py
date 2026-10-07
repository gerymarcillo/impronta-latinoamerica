# -*- coding: utf-8 -*-
"""
DISENO DE VIGA - FLEXION + CORTANTE + ARMADURA
AUTOR: ING. GERY LORENZO MARCILLO MERINO
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, Circle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# DATOS
luces_X = [5.5, 6.0]
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv
b_col = 0.38
b_viga = 0.30
h_viga = 0.45
rec = 0.025
phi_est = 0.010
phi_var = 0.016
fc = 210
fy = 4200
Fm = 1.35
f_viga = 0.65
f_fisura = 0.85

Lv = max(luces_X)
Lt = (luces_X[0] + luces_X[1]) / 2
b_trib = (luces_X[0] + luces_X[1]) / 2

# FLEXION
w = Cu * b_trib
Me = (Cu * Lt * (Lv - b_col)**2) / 8
Md = Me * f_viga * f_fisura * Fm
d = h_viga - rec - phi_est - phi_var/2

As_req = 10.0
for i in range(10):
    a_iter = (As_req * fy) / (0.85 * fc * b_viga * 100)
    As_req_new = (Md * 100000) / (0.9 * fy * (d * 100 - a_iter/2))
    if abs(As_req_new - As_req) < 0.01:
        break
    As_req = As_req_new

def seleccionar_varillas(As_req, b, rec, phi_est, phi_mm, s_min=2.5):
    As_varilla = np.pi * (phi_mm/10)**2 / 4
    n_var = int(np.ceil(As_req / As_varilla))
    n_var = max(n_var, 2)
    s_disponible = (b*100 - 2*rec*100 - 2*phi_est*100 - n_var*phi_mm) / (n_var - 1) if n_var > 1 else 0
    if s_disponible >= s_min:
        return n_var, n_var * As_varilla, s_disponible, 1
    else:
        n_var_capa = int(np.ceil(n_var / 2))
        n_var = n_var_capa * 2
        s_disponible = (b*100 - 2*rec*100 - 2*phi_est*100 - n_var_capa*phi_mm) / (n_var_capa - 1) if n_var_capa > 1 else 0
        return n_var, n_var * As_varilla, s_disponible, 2

opciones_sup = []
for phi_mm in [12, 14, 16, 18, 20, 22, 25]:
    n_var, As_real, s_disp, n_capas = seleccionar_varillas(As_req, b_viga, rec, phi_est, phi_mm)
    if As_real >= As_req and s_disp >= 2.5:
        opciones_sup.append((phi_mm, n_var, As_real, s_disp, n_capas))

if opciones_sup:
    phi_sup, n_sup, As_sup, s_sup, capas_sup = opciones_sup[0]
else:
    phi_sup, n_sup, As_sup, s_sup, capas_sup = 16, 8, 16.08, 1.5, 2

As_pos_nec = max(0.50 * As_req, 4.08)

opciones_inf = []
for phi_mm in [12, 14, 16, 18, 20]:
    n_var, As_real, s_disp, n_capas = seleccionar_varillas(As_pos_nec, b_viga, rec, phi_est, phi_mm)
    if As_real >= As_pos_nec and s_disp >= 2.5:
        opciones_inf.append((phi_mm, n_var, As_real, s_disp, n_capas))

if opciones_inf:
    phi_inf, n_inf, As_inf, s_inf, capas_inf = opciones_inf[0]
else:
    phi_inf, n_inf, As_inf, s_inf, capas_inf = 14, 4, 6.16, 2.5, 1

a_sup = (As_sup * fy) / (0.85 * fc * b_viga * 100)
Mn_sup = As_sup * fy * (d * 100 - a_sup/2) / 100000
Mr_sup = 0.90 * Mn_sup

# CORTANTE
Mpr = 1.25 * As_sup * fy * (d * 100 - 1.25 * As_sup * fy / (1.7 * fc * b_viga * 100)) / 100000
Vum = (Mpr + Mpr) / (Lv - b_col)
Vug = (2 * Lv - b_col) * w * Lv / 4
Vu = Vum + Vug
Vc = 0.53 * np.sqrt(fc) * b_viga * 100 * d * 100 / 1000
Vs = (Vu - 0.75 * Vc) / 0.75
s_est = (d * 100 * 0.00785 * phi_est*1000**2 * 2 * fy) / (Vs * 1000)
Z_prot = 2 * h_viga * 100
s_prot = min(d*100/4, 6*phi_sup/10, 10, s_est)
s_cent = min(d*100/2, 8*phi_sup/10, 15)

print("=" * 60)
print("DISENO DE VIGA - ING. GERY LORENZO MARCILLO MERINO")
print("=" * 60)
print(f"Md     = {Md:.2f} t-m | As_req = {As_req:.2f} cm2")
print(f"As(-)  = {n_sup} varillas de {phi_sup} mm")
print(f"As(+)  = {n_inf} varillas de {phi_inf} mm")
print(f"Mr     = {Mr_sup:.2f} t-m")
print(f"Vu     = {Vu:.2f} t | s_prot = {s_prot:.1f} cm | s_cent = {s_cent:.1f} cm")
print("=" * 60)

# ======================================================================
# VENTANA 1: SOLO GRAFICAS (3 PANELES)
# ======================================================================
fig1 = plt.figure(figsize=(18, 10), num='Ventana 1: Diseno de Viga')
fig1.suptitle(
    "DISENO DE VIGA - FLEXION + CORTANTE + ARMADURA\n"
    "AUTOR: ING. GERY LORENZO MARCILLO MERINO | UNESUM-REZ-2026-JIPIJAPA-001",
    fontsize=14, fontweight='bold'
)

gs1 = GridSpec(2, 2, figure=fig1, width_ratios=[1, 2], height_ratios=[1, 1],
               hspace=0.35, wspace=0.25)

# (a) SECCION TRANSVERSAL
ax1 = fig1.add_subplot(gs1[0, 0])
ax1.set_xlim(-10, b_viga*100 + 10)
ax1.set_ylim(-10, h_viga*100 + 10)
ax1.set_aspect('equal')
ax1.add_patch(Rectangle((0, 0), b_viga*100, h_viga*100, linewidth=3, edgecolor='black', facecolor='#e8e8e8'))
ax1.add_patch(Rectangle((rec*100, rec*100), b_viga*100 - 2*rec*100, h_viga*100 - 2*rec*100,
                         linewidth=2, edgecolor='blue', facecolor='none'))

y_sup = h_viga*100 - rec*100 - phi_est*100 - phi_sup/2
if capas_sup == 1:
    espacio = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_sup*phi_sup) / (n_sup - 1) if n_sup > 1 else 0
    for i in range(n_sup):
        x_var = rec*100 + phi_est*100 + phi_sup/2 + i * (phi_sup + espacio)
        ax1.add_patch(Circle((x_var, y_sup), phi_sup/2, color='red', zorder=10))
else:
    n_capa = n_sup // 2
    espacio = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_capa*phi_sup) / (n_capa - 1) if n_capa > 1 else 0
    for capa in range(2):
        y_capa = y_sup - capa * (phi_sup + 2.5)
        for i in range(n_capa):
            x_var = rec*100 + phi_est*100 + phi_sup/2 + i * (phi_sup + espacio)
            ax1.add_patch(Circle((x_var, y_capa), phi_sup/2, color='red', zorder=10))

y_inf = rec*100 + phi_est*100 + phi_inf/2
espacio_i = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_inf*phi_inf) / (n_inf - 1) if n_inf > 1 else 0
for i in range(n_inf):
    x_var = rec*100 + phi_est*100 + phi_inf/2 + i * (phi_inf + espacio_i)
    ax1.add_patch(Circle((x_var, y_inf), phi_inf/2, color='blue', zorder=10))

ax1.text(b_viga*100/2, h_viga*100 + 5, f'As(-) {n_sup} phi {phi_sup} mm', ha='center', fontsize=10, fontweight='bold', color='red')
ax1.text(b_viga*100/2, -7, f'As(+) {n_inf} phi {phi_inf} mm', ha='center', fontsize=10, fontweight='bold', color='blue')
ax1.set_title('(a) Seccion transversal', fontsize=12, fontweight='bold')
ax1.set_xlabel('b (cm)')
ax1.set_ylabel('h (cm)')
ax1.grid(True, alpha=0.3)

# (b) DETALLE LONGITUDINAL
ax2 = fig1.add_subplot(gs1[0, 1])
ax2.set_xlim(-0.5, Lv + 0.5)
ax2.set_ylim(-1.5, 2.5)
ax2.add_patch(Rectangle((0, 0), Lv, 0.5, facecolor='#e8e8e8', edgecolor='black', linewidth=2))
ax2.plot(0, 0, marker='^', markersize=20, color='blue', zorder=10)
ax2.plot(Lv, 0, marker='o', markersize=16, color='green', zorder=10)

ax2.plot([0, Z_prot/100], [0.5, 0.5], color='red', lw=6, solid_capstyle='round')
ax2.plot([Lv - Z_prot/100, Lv], [0.5, 0.5], color='red', lw=6, solid_capstyle='round')
ax2.text(Z_prot/200, 0.65, f'As(-) {n_sup} phi {phi_sup}', ha='center', fontsize=10, color='red', fontweight='bold')
ax2.text(Lv - Z_prot/200, 0.65, f'As(-) {n_sup} phi {phi_sup}', ha='center', fontsize=10, color='red', fontweight='bold')

ax2.plot([Lv*0.35, Lv*0.65], [0.15, 0.15], color='blue', lw=6, solid_capstyle='round')
ax2.text(Lv/2, 0.3, f'As(+) {n_inf} phi {phi_inf}', ha='center', fontsize=10, color='blue', fontweight='bold')

ax2.axvspan(Lv*0.35, Lv*0.65, alpha=0.15, color='green')
ax2.axvspan(0, Z_prot/100, alpha=0.15, color='orange')
ax2.axvspan(Lv - Z_prot/100, Lv, alpha=0.15, color='orange')

ax2.text(Lv/2, 1.8, 'ZONA DE TRASLAPE', ha='center', fontsize=11, color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', edgecolor='green'))

ax2.set_title('(b) Detalle longitudinal - Armadura', fontsize=12, fontweight='bold')
ax2.set_xlabel('x (m)')
ax2.set_yticks([])
ax2.grid(True, alpha=0.3)

# (c) DISTRIBUCION DE ESTRIBOS
ax3 = fig1.add_subplot(gs1[1, :])
ax3.set_xlim(0, Lv)
ax3.set_ylim(-0.5, 1.5)
ax3.add_patch(Rectangle((0, 0), Lv, 0.5, facecolor='#e8e8e8', edgecolor='black', linewidth=2))

ax3.axvspan(0, Z_prot/100, alpha=0.2, color='red')
ax3.axvspan(Lv - Z_prot/100, Lv, alpha=0.2, color='red')

n_est_p = int(Z_prot/100 / (s_prot/100)) + 1
for i in range(n_est_p):
    x_est = i * s_prot/100
    ax3.plot([x_est, x_est], [0, 0.5], color='red', lw=2.5)
for i in range(n_est_p):
    x_est = Lv - i * s_prot/100
    ax3.plot([x_est, x_est], [0, 0.5], color='red', lw=2.5)

n_est_c = int((Lv - 2*Z_prot/100) / (s_cent/100))
for i in range(n_est_c):
    x_est = Z_prot/100 + i * s_cent/100
    ax3.plot([x_est, x_est], [0, 0.5], color='blue', lw=1.5)

ax3.text(Z_prot/200, 0.7, f's = {s_prot:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')
ax3.text(Lv/2, 0.7, f's = {s_cent:.1f} cm', ha='center', fontsize=10, color='blue', fontweight='bold')
ax3.text(Lv - Z_prot/200, 0.7, f's = {s_prot:.1f} cm', ha='center', fontsize=10, color='red', fontweight='bold')

ax3.set_title('(c) Distribucion de estribos', fontsize=12, fontweight='bold')
ax3.set_xlabel('x (m)')
ax3.set_yticks([])
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('diseno_viga_ventana1.png', dpi=150, bbox_inches='tight')
plt.show(block=False)

# ======================================================================
# VENTANA 2: MODELO 3D
# ======================================================================
fig2 = plt.figure(figsize=(16, 10), num='Ventana 2: Modelo 3D')
ax = fig2.add_subplot(111, projection='3d')

fig2.suptitle(
    f"MODELO 3D - As(-) {n_sup} phi {phi_sup} | As(+) {n_inf} phi {phi_inf}",
    fontsize=13, fontweight='bold'
)

L = Lv
b = b_viga
h = h_viga

vertices = [[0,0,0],[L,0,0],[L,b,0],[0,b,0],[0,0,h],[L,0,h],[L,b,h],[0,b,h]]
caras_idx = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
caras = [[vertices[i] for i in cara] for cara in caras_idx]

ax.add_collection3d(Poly3DCollection(caras, facecolors='#d0d0d0', linewidths=1.5, edgecolors='black', alpha=0.4))

z_sup = h - rec - phi_est - phi_sup/200
for i in range(n_sup):
    if n_sup > 1:
        y_var = rec + phi_est + phi_sup/200 + i * (b - 2*rec - 2*phi_est - phi_sup/100) / (n_sup - 1)
    else:
        y_var = b/2
    ax.plot([0, L/4], [y_var, y_var], [z_sup, z_sup], color='red', lw=5, solid_capstyle='round')
    ax.plot([3*L/4, L], [y_var, y_var], [z_sup, z_sup], color='red', lw=5, solid_capstyle='round')

z_inf = rec + phi_est + phi_inf/200
for i in range(n_inf):
    if n_inf > 1:
        y_var = rec + phi_est + phi_inf/200 + i * (b - 2*rec - 2*phi_est - phi_inf/100) / (n_inf - 1)
    else:
        y_var = b/2
    ax.plot([L/4, 3*L/4], [y_var, y_var], [z_inf, z_inf], color='blue', lw=4, solid_capstyle='round')

for i in range(30):
    x_est = i * L / 29
    y_est = [rec, b - rec, b - rec, rec, rec]
    z_est = [rec, rec, h - rec, h - rec, rec]
    ax.plot([x_est]*5, y_est, z_est, color='gray', lw=1, alpha=0.5)

ax.bar3d(0, 0, 0, 2*h, b, h, color='red', alpha=0.1)
ax.bar3d(L - 2*h, 0, 0, 2*h, b, h, color='red', alpha=0.1)

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_xlim(0, L)
ax.set_ylim(0, b*1.5)
ax.set_zlim(0, h*1.5)
ax.set_title('Modelo 3D - Diseno de Viga', fontsize=13, fontweight='bold')
ax.view_init(elev=25, azim=-50)

plt.tight_layout()
plt.savefig('diseno_viga_ventana2.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nArchivos: diseno_viga_ventana1.png | diseno_viga_ventana2.png")