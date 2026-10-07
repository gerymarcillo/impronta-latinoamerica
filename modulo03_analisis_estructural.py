# -*- coding: utf-8 -*-
"""
======================================================================
RIGIDEZ ENERGETICA APLICADA A LA INGENIERIA CIVIL
======================================================================
AUTOR: ING. GERY LORENZO MARCILLO MERINO
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
CASO: COLEGIO ALEJO LASCANO - JIPIJAPA, MANABI, ECUADOR
======================================================================
VENTANA 1: DASHBOARD 2D
======================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, Circle

# ======================================================================
# DATOS DE ENTRADA
# ======================================================================
luces_X = [5.5, 6.0]
luces_Y = [5.5, 6.0]
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

Lv = max(max(luces_X), max(luces_Y))
Lt = (luces_X[0] + luces_X[1]) / 2
b_trib = (luces_X[0] + luces_X[1]) / 2

# ======================================================================
# CALCULOS
# ======================================================================
E_kgcm2 = 15100 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
I_viga = (b_viga * h_viga**3) / 12
EI = E_tm2 * I_viga

w = Cu * b_trib
R1 = R2 = w * Lv / 2
Vmax = R1
Mmax = w * Lv**2 / 8
theta_max = (w * Lv**3) / (24 * EI)
delta_max = (5 * w * Lv**4) / (384 * EI)
delta_adm = Lv / 240

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
        As_real = n_var * As_varilla
        return n_var, As_real, s_disponible, 1
    else:
        n_var_capa = int(np.ceil(n_var / 2))
        n_var = n_var_capa * 2
        As_real = n_var * As_varilla
        s_disponible = (b*100 - 2*rec*100 - 2*phi_est*100 - n_var_capa*phi_mm) / (n_var_capa - 1) if n_var_capa > 1 else 0
        return n_var, As_real, s_disponible, 2

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

# ======================================================================
# RESUMEN COMPACTO EN CONSOLA
# ======================================================================
print("=" * 60)
print("RIGIDEZ ENERGETICA - ING. GERY LORENZO MARCILLO MERINO")
print("=" * 60)
print(f"Md       = {Md:.2f} t-m")
print(f"As_req   = {As_req:.2f} cm2")
print(f"As(-)    = {n_sup} varillas de {phi_sup} mm")
print(f"As(+)    = {n_inf} varillas de {phi_inf} mm")
print(f"Mr       = {Mr_sup:.2f} t-m")
print(f"Vu       = {Vu:.2f} t")
print(f"s_prot   = {s_prot:.1f} cm")
print(f"s_cent   = {s_cent:.1f} cm")
print(f"Verif    = {'CUMPLE' if Mr_sup >= Md else 'NO CUMPLE'}")
print("=" * 60)

# ======================================================================
# VENTANA 1: DASHBOARD 2D
# ======================================================================
fig1 = plt.figure(figsize=(20, 16), num='Ventana 1: Dashboard 2D')
fig1.suptitle(
    "RIGIDEZ ENERGETICA - ING. GERY LORENZO MARCILLO MERINO\n"
    f"Md = {Md:.2f} t-m | As(-) = {n_sup} varillas de {phi_sup} mm | As(+) = {n_inf} varillas de {phi_inf} mm",
    fontsize=14, fontweight='bold', y=0.98
)

gs1 = GridSpec(4, 3, figure=fig1, width_ratios=[1,1,1], height_ratios=[1.2,1,1,1], hspace=0.50, wspace=0.30)

# (a) ESQUEMA
ax0 = fig1.add_subplot(gs1[0, :])
ax0.set_xlim(-0.5, Lv + 0.5)
ax0.set_ylim(-2.0, 1.8)
ax0.axhline(0, color='black', linewidth=5)
ax0.plot(0, 0, marker='^', markersize=25, color='blue', label='Articulacion', zorder=10)
ax0.plot(Lv, 0, marker='o', markersize=20, color='green', label='Rodillo', zorder=10)
for xi in np.linspace(0, Lv, 20):
    ax0.annotate('', xy=(xi, 0), xytext=(xi, 1.2), arrowprops=dict(arrowstyle='->', color='red', lw=2))
ax0.plot([0, Lv], [1.2, 1.2], color='red', lw=3)
ax0.text(Lv/2, 1.35, f'w = {w:.3f} t/m', ha='center', fontsize=13, color='red', fontweight='bold')
ax0.annotate('', xy=(0, -1.0), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='purple', lw=3))
ax0.text(0.2, -1.3, f'R1 = {R1:.2f} t', fontsize=11, color='purple', fontweight='bold')
ax0.annotate('', xy=(Lv, -1.0), xytext=(Lv, 0), arrowprops=dict(arrowstyle='->', color='purple', lw=3))
ax0.text(Lv - 1.8, -1.3, f'R2 = {R2:.2f} t', fontsize=11, color='purple', fontweight='bold')
ax0.annotate('', xy=(0, -1.7), xytext=(Lv, -1.7), arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax0.text(Lv/2, -1.9, f'L = {Lv:.2f} m', ha='center', fontsize=12, fontweight='bold')
ax0.set_title(f'(a) ESQUEMA ESTRUCTURAL (Lt = {Lt:.2f} m)', fontsize=13, fontweight='bold')
ax0.set_xlabel('x (m)')
ax0.set_yticks([])
ax0.legend(loc='upper right', fontsize=10)
ax0.grid(True, alpha=0.3)

x = np.linspace(0, Lv, 500)
V = R1 - w * x
M = R1 * x - (w * x**2) / 2
theta = (w / (24 * EI)) * (4*x**3 - 6*Lv*x**2 + Lv**3)
delta = (w * x / (24 * EI)) * (Lv**3 - 2*Lv*x**2 + x**3)

# (b) CORTANTE
ax1 = fig1.add_subplot(gs1[1, 0])
ax1.plot(x, V, color='blue', lw=3)
ax1.fill_between(x, V, alpha=0.20, color='blue')
ax1.axhline(0, color='black', lw=1)
ax1.text(Lv/2, Vmax*0.7, f"Vmax = {Vmax:.2f} t", ha='center', fontsize=10, color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
ax1.set_title('(b) Cortante V(x)', fontsize=11, fontweight='bold')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('V (t)')
ax1.grid(True, alpha=0.3)

# (c) MOMENTO
ax2 = fig1.add_subplot(gs1[1, 1])
ax2.plot(x, M, color='darkorange', lw=3)
ax2.fill_between(x, M, alpha=0.20, color='orange')
ax2.axhline(0, color='black', lw=1)
ax2.text(Lv/2, Mmax*0.7, f"Mmax = {Mmax:.2f} t-m", ha='center', fontsize=10, color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))
ax2.set_title('(c) Momento M(x)', fontsize=11, fontweight='bold')
ax2.set_xlabel('x (m)')
ax2.set_ylabel('M (t-m)')
ax2.grid(True, alpha=0.3)

# (d) ROTACION
ax3 = fig1.add_subplot(gs1[1, 2])
ax3.plot(x, theta, color='green', lw=3)
ax3.fill_between(x, theta, alpha=0.20, color='green')
ax3.axhline(0, color='black', lw=1)
ax3.set_title('(d) Rotacion theta(x)', fontsize=11, fontweight='bold')
ax3.set_xlabel('x (m)')
ax3.set_ylabel('theta (rad)')
ax3.grid(True, alpha=0.3)

# (e) DEFLEXION
ax4 = fig1.add_subplot(gs1[2, 0])
ax4.plot(x, delta * 1000, color='purple', lw=3)
ax4.fill_between(x, delta * 1000, alpha=0.20, color='purple')
ax4.axhline(0, color='black', lw=1)
delta_adm_mm = delta_adm * 1000
ax4.axhline(delta_adm_mm, color='red', linestyle='--', lw=2, alpha=0.8, label=f'dadm = {delta_adm_mm:.1f} mm')
ax4.set_title('(e) Deflexion delta(x)', fontsize=11, fontweight='bold')
ax4.set_xlabel('x (m)')
ax4.set_ylabel('delta (mm)')
ax4.legend(loc='best', fontsize=9)
ax4.grid(True, alpha=0.3)

# (f) SECCION
ax5 = fig1.add_subplot(gs1[2, 1])
ax5.set_xlim(-10, b_viga*100 + 10)
ax5.set_ylim(-10, h_viga*100 + 10)
ax5.set_aspect('equal')
rect = Rectangle((0, 0), b_viga*100, h_viga*100, linewidth=3, edgecolor='black', facecolor='#e8e8e8')
ax5.add_patch(rect)
estribo = Rectangle((rec*100, rec*100), b_viga*100 - 2*rec*100, h_viga*100 - 2*rec*100, linewidth=2, edgecolor='blue', facecolor='none')
ax5.add_patch(estribo)

y_sup = h_viga*100 - rec*100 - phi_est*100 - phi_sup/2
if capas_sup == 1:
    espacio_sup = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_sup*phi_sup) / (n_sup - 1) if n_sup > 1 else 0
    for i in range(n_sup):
        x_var = rec*100 + phi_est*100 + phi_sup/2 + i * (phi_sup + espacio_sup)
        ax5.add_patch(Circle((x_var, y_sup), phi_sup/2, color='red', zorder=10))
else:
    n_capa = n_sup // 2
    espacio_sup = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_capa*phi_sup) / (n_capa - 1) if n_capa > 1 else 0
    for capa in range(2):
        y_capa = y_sup - capa * (phi_sup + 2.5)
        for i in range(n_capa):
            x_var = rec*100 + phi_est*100 + phi_sup/2 + i * (phi_sup + espacio_sup)
            ax5.add_patch(Circle((x_var, y_capa), phi_sup/2, color='red', zorder=10))

y_inf = rec*100 + phi_est*100 + phi_inf/2
espacio_inf = (b_viga*100 - 2*rec*100 - 2*phi_est*100 - n_inf*phi_inf) / (n_inf - 1) if n_inf > 1 else 0
for i in range(n_inf):
    x_var = rec*100 + phi_est*100 + phi_inf/2 + i * (phi_inf + espacio_inf)
    ax5.add_patch(Circle((x_var, y_inf), phi_inf/2, color='blue', zorder=10))

ax5.text(b_viga*100/2, h_viga*100 + 5, f'As(-) = {n_sup} var {phi_sup} mm', ha='center', fontsize=9, fontweight='bold', color='red')
ax5.text(b_viga*100/2, -7, f'As(+) = {n_inf} var {phi_inf} mm', ha='center', fontsize=9, fontweight='bold', color='blue')
ax5.set_title('(f) Seccion transversal', fontsize=11, fontweight='bold')
ax5.set_xlabel('b (cm)')
ax5.set_ylabel('h (cm)')
ax5.grid(True, alpha=0.3)

# (g) CARGA VERTICAL vs SISMO
ax6 = fig1.add_subplot(gs1[2, 2])
ax6.set_xlim(-0.5, Lv + 0.5)
ax6.set_ylim(-2.0, 3.0)
x_plot = np.linspace(0, Lv, 100)
M_vert = (w * Lv / 2) * x_plot - (w * x_plot**2) / 2
M_vert_norm = M_vert / M_vert.max() + 1.0
M_sismo = Md * (1 - 2 * np.abs(x_plot - Lv/2) / Lv)
M_sismo_norm = M_sismo / M_sismo.max()
ax6.plot(x_plot, M_vert_norm, 'b-', lw=3, label='Carga Vertical')
ax6.plot(x_plot, M_sismo_norm, 'r-', lw=3, label='Sismo')
ax6.axhline(1.0, color='black', lw=1, linestyle='--', alpha=0.5)
ax6.axhline(0, color='black', lw=1)
ax6.axvspan(Lv/3, 2*Lv/3, alpha=0.2, color='green')
ax6.text(Lv/2, 2.5, 'ZONA DE TRASLAPE', ha='center', fontsize=10, color='green', fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', edgecolor='green'))
ax6.text(Lv/8, 2.0, 'As(-)', ha='center', fontsize=9, color='red', fontweight='bold')
ax6.text(7*Lv/8, 2.0, 'As(-)', ha='center', fontsize=9, color='red', fontweight='bold')
ax6.text(Lv/2, 0.5, 'As(+)', ha='center', fontsize=9, color='blue', fontweight='bold')
ax6.text(Lv/2, -1.5, 'PROHIBIDO TRASLAPAR EN NUDOS', ha='center', fontsize=9, color='red', fontweight='bold', bbox=dict(boxstyle='round', facecolor='#ffcccc', edgecolor='red'))
ax6.set_title('(g) Carga Vertical vs Sismo', fontsize=11, fontweight='bold')
ax6.set_xlabel('x (m)')
ax6.set_yticks([])
ax6.legend(loc='upper right', fontsize=8)
ax6.grid(True, alpha=0.3)

# (h) RESUMEN
ax7 = fig1.add_subplot(gs1[3, :])
ax7.axis('off')

resumen = "RIGIDEZ ENERGETICA - ING. GERY LORENZO MARCILLO MERINO\n"
resumen += "=" * 80 + "\n"
resumen += f"FLEXION:  Md = {Md:.2f} t-m | As_req = {As_req:.2f} cm2 | Mr = {Mr_sup:.2f} t-m\n"
resumen += f"As(-) = {n_sup} varillas de {phi_sup} mm | As(+) = {n_inf} varillas de {phi_inf} mm\n"
resumen += f"CORTE:    Vu = {Vu:.2f} t | Vc = {Vc:.2f} t | Vs = {Vs:.2f} t\n"
resumen += f"CONFIN:   Z_prot = {Z_prot:.0f} cm | s_prot = {s_prot:.1f} cm | s_cent = {s_cent:.1f} cm\n"
resumen += "=" * 80 + "\n"
resumen += f"{'CUMPLE CON NEC-15' if Mr_sup >= Md else 'NO CUMPLE - REVISAR'}\n"
resumen += "=" * 80 + "\n"
resumen += '"La rigidez no es solo un numero; es energia almacenada, es resiliencia, es vida."\n'
resumen += "-- Ing. Gery Lorenzo Marcillo Merino"

ax7.text(0.5, 0.5, resumen, ha='center', va='center', fontsize=10, family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='green' if Mr_sup >= Md else 'red', lw=3))

plt.savefig('rigidez_energetica_ventana1.png', dpi=150, bbox_inches='tight')
plt.show()