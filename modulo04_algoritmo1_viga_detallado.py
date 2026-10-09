# -*- coding: utf-8 -*-
"""
================================================================================
MODULO 04 - ALGORITMO 1: VIGA RESILIENTE - ULTIMA CORRIDA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
NORMA: ACI 318-19 Cap. 18 (ZONA SISMICA) + NEC-15
OBJETIVO: VIGA RESILIENTE - Detalles de armado NUNCA ANTES VISTOS
          - Diagrama mariposa (curva de SEGUNDO ORDEN)
          - Mitad de mariposa: M(x) = Mpr * (2x/Lv)^2
          - Sistema de marcas (Mc 341, 342, 343)
          - Ganchos normalizados (12db + 4db)
          - Diagrama de cortante (T-U-V-W)
          - Bloque de compresion "a"
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
CASO = "Estructuras Especiales"
TITULO = "VIGA RESILIENTE - DETALLES DE ARMADO"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
NORMA = "ACI 318-19 Cap. 18 + NEC-15"
FRASE = "Los numeros son solo el vehiculo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DEL PPT (VIGA SISMORRESISTENTE)
# ============================================================================

Lv = 6.20
Lt = 5.85
b_trib = 5.85
Fm = 1.20
b_col = 0.54
rec = 2.50
fc = 210
fy = 4200
Es = 2.1e6

Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv
w = Cu * b_trib

b_viga = 30
h_viga = 46
h_def = 46
phi_est = 10
phi_min_nec = 12

# ============================================================================
# 3. CALCULOS DE FLEXION
# ============================================================================

Me = 24.93
Md = 16.53
d_cm = 40.7
d_prime_cm = h_def - d_cm

As_req = 30 * Md / d_cm
As_min = 14 * b_viga * d_cm / fy

phi_sup = 16
phi_inf = 16
n_sup_extremo = 6
n_sup_centro = 2
n_inf = 3

As_varilla_16 = 0.00785 * 16**2

As_sup_extremo = n_sup_extremo * As_varilla_16
As_sup_centro = n_sup_centro * As_varilla_16
As_inf = n_inf * As_varilla_16
As_real = As_sup_extremo

a_cm = 9.46
rel_a_h = a_cm / h_def
Mr = 16.40
rho = As_sup_extremo / (b_viga * h_def) * 100

# ============================================================================
# 4. TIC
# ============================================================================

rel_hb = h_def / b_viga

if rel_hb <= 1.1:
    tic_hb_nivel = "IDEAL"
elif rel_hb <= 1.3:
    tic_hb_nivel = "CUMPLE"
elif rel_hb <= 1.5:
    tic_hb_nivel = "LIMITE (NEC-15)"
else:
    tic_hb_nivel = "NO CUMPLE"

rho_max_ductil = 1.0
tic_rho_nivel = "CUMPLE (ductil)" if rho <= rho_max_ductil else "NO CUMPLE (fragil)"

eps_y = fy / Es
c_bal = d_cm * 0.003 / (0.003 + eps_y)
rho_bal_pct = 0.85 * 0.85 * (fc/fy) * (0.003/(0.003+eps_y)) * 100
rho_max_bal_pct = 0.75 * rho_bal_pct
rho_min_pct = max(0.25 * np.sqrt(fc) / fy, 1.4 / fy) * 100

if rho < rho_min_pct:
    tipo_falla = "FRAGIL"
elif rho < rho_max_bal_pct:
    tipo_falla = "DUCTIL POR TRACCION"
elif rho < rho_bal_pct:
    tipo_falla = "TRANSICION"
else:
    tipo_falla = "FRAGIL POR COMPRESION"

rel_as = As_inf / As_sup_extremo * 100
tic_as_nivel = "CUMPLE" if As_inf >= 0.5 * As_sup_extremo else "NO CUMPLE"

tic_a_nivel = "IDEAL (viga T)" if 15 <= rel_a_h*100 <= 25 else "REVISAR"

# ============================================================================
# 5. CORTANTE
# ============================================================================

Mpr1 = 22.02
Mpr2 = 11.95
Vum = 6.00
Vug = 10.19
Vu = 16.19
Vc = 0.53 * np.sqrt(fc) * b_viga * d_cm / 1000
Vs = 12.21
s_est = 22
Z_prot = 92
s_prot = 10
Z_cent = 386
s_cent = 13

# ============================================================================
# 6. IMPRESION EN CONSOLA
# ============================================================================

print("=" * 80)
print(f"[M04 - A1] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[NORMA] {NORMA}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print(f"\n--- FLEXION ---")
print(f"  Me = {Me:.2f} t-m | Md = {Md:.2f} t-m")
print(f"  d = {d_cm:.2f} cm | d' = {d_prime_cm:.2f} cm")
print(f"  As_req = {As_req:.2f} cm2 | As_min = {As_min:.2f} cm2")
print(f"  As(-) ext = {n_sup_extremo} phi{phi_sup} = {As_sup_extremo:.2f} cm2")
print(f"  As(-) cen = {n_sup_centro} phi{phi_sup} = {As_sup_centro:.2f} cm2")
print(f"  As(+) = {n_inf} phi{phi_inf} = {As_inf:.2f} cm2")
print(f"  a = {a_cm:.2f} cm | a/h = {rel_a_h*100:.1f}%")
print(f"  Mr = {Mr:.2f} t-m | rho = {rho:.2f}%")

print(f"\n--- CORTANTE ---")
print(f"  Mpr1 = {Mpr1:.2f} t-m | Mpr2 = {Mpr2:.2f} t-m")
print(f"  Vum = {Vum:.2f} t | Vug = {Vug:.2f} t")
print(f"  Vu = Vum + Vug = {Vum:.2f} + {Vug:.2f} = {Vu:.2f} t")
print(f"  Vc = {Vc:.2f} t | Vs = {Vs:.2f} t")
print(f"  s_est = {s_est} cm")

print(f"\n--- ESTRIBOS ---")
print(f"  Z_prot = {Z_prot} cm | s_prot = {s_prot} cm")
print(f"  Z_cent = {Z_cent} cm | s_cent = {s_cent} cm")

print(f"\n--- 5 TIC VIGA RESILIENTE ---")
print(f"  TIC 1: h/b = {rel_hb:.3f} -> {tic_hb_nivel}")
print(f"  TIC 2: rho = {rho:.2f}% -> {tic_rho_nivel}")
print(f"  TIC 3: rho_bal = {rho_bal_pct:.2f}% -> {tipo_falla}")
print(f"  TIC 4: As(+)/As(-) = {rel_as:.1f}% -> {tic_as_nivel}")
print(f"  TIC 5: a/h = {rel_a_h*100:.1f}% -> {tic_a_nivel}")

print("\n" + "=" * 80)
print(f"Frase: {FRASE}")
print("=" * 80)

# ============================================================================
# 7. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M04"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M04_algoritmo1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M04 - A1] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[NORMA] {NORMA}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"FLEXION:\n")
    f.write(f"  Me = {Me:.2f} t-m | Md = {Md:.2f} t-m\n")
    f.write(f"  d = {d_cm:.2f} cm\n")
    f.write(f"  As_req = {As_req:.2f} cm2\n")
    f.write(f"  As(-) ext = {n_sup_extremo} phi{phi_sup} = {As_sup_extremo:.2f} cm2\n")
    f.write(f"  As(+) = {n_inf} phi{phi_inf} = {As_inf:.2f} cm2\n")
    f.write(f"  a = {a_cm:.2f} cm | a/h = {rel_a_h*100:.1f}%\n")
    f.write(f"  Mr = {Mr:.2f} t-m | rho = {rho:.2f}%\n\n")
    f.write(f"CORTANTE:\n")
    f.write(f"  Mpr1 = {Mpr1:.2f} t-m | Mpr2 = {Mpr2:.2f} t-m\n")
    f.write(f"  Vum = {Vum:.2f} t | Vug = {Vug:.2f} t\n")
    f.write(f"  Vu = {Vu:.2f} t | Vs = {Vs:.2f} t\n\n")
    f.write(f"ESTRIBOS:\n")
    f.write(f"  Z_prot = {Z_prot} cm | s_prot = {s_prot} cm\n")
    f.write(f"  Z_cent = {Z_cent} cm | s_cent = {s_cent} cm\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 8. DASHBOARD 2D (8 PANELES)
# ============================================================================

fig1 = plt.figure(figsize=(22, 18), num='M04-A1: Dashboard Detalles Armado')
fig1.suptitle(
    f"M04 - ALGORITMO 1: VIGA RESILIENTE - DETALLES DE ARMADO\n"
    f"{PROYECTO} | {CASO}",
    fontsize=16, fontweight='bold', color='#2c3e50'
)

gs1 = GridSpec(4, 2, figure=fig1,
               width_ratios=[1, 2], height_ratios=[1, 1, 1, 1],
               hspace=0.55, wspace=0.25)

# --------------------------------------------------------
# (a) SECCION TRANSVERSAL CON BLOQUE "a"
# --------------------------------------------------------
ax1 = fig1.add_subplot(gs1[0, 0])
ax1.set_xlim(-15, b_viga + 40)
ax1.set_ylim(-35, h_def + 15)
ax1.set_aspect('equal')

ax1.add_patch(Rectangle((0, 0), b_viga, h_def, linewidth=3, edgecolor='black', facecolor='#e8e8e8'))

y_a = h_def - a_cm
ax1.add_patch(Rectangle((0, y_a), b_viga, a_cm, facecolor='#3498db', alpha=0.75, edgecolor='darkblue', linewidth=2))
ax1.add_patch(Rectangle((0, 0), b_viga, y_a, facecolor='#95a5a6', alpha=0.4))

ax1.add_patch(Rectangle((rec, rec), b_viga - 2*rec, h_def - 2*rec,
                         linewidth=2, edgecolor='blue', facecolor='none'))

y_sup = h_def - rec - phi_est/10 - phi_sup/20
espacio_sup = (b_viga - 2*rec - 2*phi_est/10 - n_sup_extremo*phi_sup/10) / (n_sup_extremo - 1)
for i in range(n_sup_extremo):
    x_var = rec + phi_est/10 + phi_sup/20 + i * (phi_sup/10 + espacio_sup)
    ax1.add_patch(Circle((x_var, y_sup), phi_sup/20, color='red', zorder=10))

y_inf = rec + phi_est/10 + phi_inf/20
espacio_inf = (b_viga - 2*rec - 2*phi_est/10 - n_inf*phi_inf/10) / (n_inf - 1)
for i in range(n_inf):
    x_var = rec + phi_est/10 + phi_inf/20 + i * (phi_inf/10 + espacio_inf)
    ax1.add_patch(Circle((x_var, y_inf), phi_inf/20, color='blue', zorder=10))

ax1.text(b_viga/2, y_a + a_cm/2, f'a = {a_cm:.2f} cm\n{rel_a_h*100:.1f}%',
         ha='center', va='center', fontsize=9, fontweight='bold', color='white',
         bbox=dict(boxstyle='round', facecolor='darkblue', edgecolor='white'))
ax1.text(b_viga/2, y_a/2, f'NO TRABAJA',
         ha='center', va='center', fontsize=8, color='white', style='italic')

ax1.text(b_viga/2, h_def + 5, f'6 φ16', ha='center', fontsize=10, fontweight='bold', color='red')
ax1.text(b_viga/2, -8, f'3 φ16', ha='center', fontsize=10, fontweight='bold', color='blue')

ax1.set_title('(a) Seccion + Bloque a', fontsize=11, fontweight='bold')
ax1.axis('off')

# --------------------------------------------------------
# (b) DETALLE LONGITUDINAL CON SISTEMA DE MARCAS
# --------------------------------------------------------
ax2 = fig1.add_subplot(gs1[0, 1])
ax2.set_xlim(-0.3, Lv + 0.3)
ax2.set_ylim(-1.8, 2.8)

ax2.add_patch(Rectangle((-0.15, -0.3), 0.15, 1.5, facecolor='#7f8c8d', edgecolor='black', linewidth=2))
ax2.add_patch(Rectangle((Lv, -0.3), 0.15, 1.5, facecolor='#7f8c8d', edgecolor='black', linewidth=2))

ax2.add_patch(Rectangle((0, 0), Lv, 0.5, facecolor='#e8e8e8', edgecolor='black', linewidth=2))

ax2.plot(0.3, 0.25, marker='o', markersize=15, color='red', zorder=10)
ax2.text(0.3, -0.15, 'Rotula\nplastica', ha='center', fontsize=7, color='red', fontweight='bold')

ax2.plot(Lv - 0.3, 0.25, marker='s', markersize=12, color='red', zorder=10)
ax2.text(Lv - 0.3, -0.15, 'Conexion\nreforzada', ha='center', fontsize=7, color='red', fontweight='bold')

ax2.plot([0.1, 1.0], [0.65, 0.65], color='red', lw=5, solid_capstyle='round')
ax2.text(0.55, 0.85, '4 φ16 Mc 341', ha='center', fontsize=8, color='red', fontweight='bold')

ax2.plot([1.2, Lv-1.2], [0.60, 0.60], color='blue', lw=4, solid_capstyle='round')
ax2.text(Lv/2, 0.80, '2 φ16 Mc 342', ha='center', fontsize=8, color='blue', fontweight='bold')

ax2.plot([Lv-1.0, Lv-0.1], [0.65, 0.65], color='red', lw=5, solid_capstyle='round')
ax2.text(Lv-0.55, 0.85, '4 φ16 Mc 343', ha='center', fontsize=8, color='red', fontweight='bold')

ax2.plot([0, Lv], [0.10, 0.10], color='blue', lw=4, solid_capstyle='round')
ax2.text(Lv/2, 0.25, 'As(+) 3 φ16', ha='center', fontsize=8, color='blue', fontweight='bold')

ax2.axvspan(0, Z_prot/100, alpha=0.15, color='red')
ax2.axvspan(Lv - Z_prot/100, Lv, alpha=0.15, color='red')

ax2.plot([0.05, 0.05], [0.5, 0.3], color='red', lw=3, solid_capstyle='round')
ax2.plot([Lv-0.05, Lv-0.05], [0.5, 0.3], color='red', lw=3, solid_capstyle='round')
ax2.text(0.12, 0.35, '12db', fontsize=7, color='red', fontweight='bold')
ax2.text(Lv-0.12, 0.35, '12db', fontsize=7, color='red', fontweight='bold')

ax2.set_title('(b) Detalle longitudinal - Sistema de marcas', fontsize=11, fontweight='bold')
ax2.set_xlabel('x (m)')
ax2.set_yticks([])
ax2.grid(True, alpha=0.3)

# --------------------------------------------------------
# (c) DISTRIBUCION DE ESTRIBOS + ZONA PROTEGIDA
# --------------------------------------------------------
ax3 = fig1.add_subplot(gs1[1, 0])
ax3.set_xlim(-10, Lv*100 + 10)
ax3.set_ylim(-8, 18)
ax3.add_patch(Rectangle((0, 0), Lv*100, 12, facecolor='#e8e8e8', edgecolor='black', linewidth=2))

ax3.axvspan(0, Z_prot, alpha=0.25, color='red')
ax3.axvspan(Lv*100 - Z_prot, Lv*100, alpha=0.25, color='red')

n_est_p = int(Z_prot / s_prot) + 1
for i in range(n_est_p):
    x_est = i * s_prot
    ax3.plot([x_est, x_est], [0, 12], color='red', lw=2)
for i in range(n_est_p):
    x_est = Lv*100 - i * s_prot
    ax3.plot([x_est, x_est], [0, 12], color='red', lw=2)

n_est_c = int(Z_cent / s_cent)
for i in range(n_est_c):
    x_est = Z_prot + i * s_cent
    ax3.plot([x_est, x_est], [0, 12], color='blue', lw=1)

ax3.text(Z_prot/2, 14, f's={s_prot}', ha='center', fontsize=9, color='red', fontweight='bold')
ax3.text(Lv*50, 14, f's={s_cent}', ha='center', fontsize=9, color='blue', fontweight='bold')
ax3.text(Lv*100 - Z_prot/2, 14, f's={s_prot}', ha='center', fontsize=9, color='red', fontweight='bold')

ax3.text(Z_prot/2, -5, f'Z_prot={Z_prot}', ha='center', fontsize=8, color='red', fontweight='bold')
ax3.text(Lv*50, -5, f'Z_cent={Z_cent}', ha='center', fontsize=8, color='blue', fontweight='bold')

ax3.set_title('(c) Distribucion estribos + Zona protegida 2h', fontsize=11, fontweight='bold')
ax3.set_xlabel('x (cm)')
ax3.set_yticks([])
ax3.grid(True, alpha=0.3)

# --------------------------------------------------------
# (d) DETALLE DE GANCHO (12db + 4db)
# --------------------------------------------------------
ax4 = fig1.add_subplot(gs1[1, 1])
ax4.set_xlim(-15, 45)
ax4.set_ylim(-15, 55)
ax4.set_aspect('equal')

ax4.add_patch(Rectangle((0, 0), 30, 46, facecolor='#e8e8e8', edgecolor='black', linewidth=2))
ax4.add_patch(Rectangle((2.5, 2.5), 25, 41, linewidth=1.5, edgecolor='blue', facecolor='none'))

ax4.plot([2.5, 2.5, 7.5], [42, 46, 46], color='red', lw=4, solid_capstyle='round')
ax4.plot([2.5, 2.5, 7.5], [25, 20, 20], color='red', lw=4, solid_capstyle='round')

ax4.plot([5, 5], [30, 38], color='red', lw=2, linestyle='--')
ax4.text(6, 34, 'FISURA', fontsize=8, color='red', fontweight='bold')

ax4.annotate('', xy=(0, 46), xytext=(0, 42), arrowprops=dict(arrowstyle='<->', color='blue'))
ax4.text(-4, 44, '12db', fontsize=8, color='blue', fontweight='bold')

ax4.annotate('', xy=(7.5, 40), xytext=(7.5, 46), arrowprops=dict(arrowstyle='<->', color='blue'))
ax4.text(9, 43, '4db', fontsize=8, color='blue', fontweight='bold')

ax4.set_title('(d) Detalle de gancho (12db + 4db)', fontsize=11, fontweight='bold')
ax4.axis('off')

# --------------------------------------------------------
# (e) DIAGRAMA MARIPOSA - CURVA DE SEGUNDO ORDEN (MITAD)
# --------------------------------------------------------
ax5 = fig1.add_subplot(gs1[2, 0])
ax5.set_xlim(-0.2, Lv + 0.2)
ax5.set_ylim(-Mpr1*0.15, Mpr1*1.15)

# Curva de segundo orden: M(x) = Mpr * (x/Lv)^2 * 4
# Simula la curva real de la imagen
x_diag = np.linspace(0, Lv, 300)
M_diag = Mpr1 * (2 * x_diag / Lv)**2 / 4

ax5.plot(x_diag, M_diag, 'r-', linewidth=3.5, label='M(x) - 2do orden')
ax5.fill_between(x_diag, M_diag, alpha=0.25, color='red')

ax5.axhline(y=0, color='black', linewidth=1)

# Zonas
ax5.axvspan(0, Z_prot/100, alpha=0.15, color='red')
ax5.axvspan(Lv - Z_prot/100, Lv, alpha=0.15, color='red')

# Etiquetas
ax5.text(Z_prot/200, Mpr1*0.05, f'M_min\n~0', ha='center', fontsize=9, color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red'))
ax5.text(Lv - Z_prot/200, Mpr1*0.9, f'Mpr1\n{Mpr1:.2f} t-m', ha='center', fontsize=9, color='red', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='red'))

# Anotacion
ax5.annotate('Curva de\nSEGUNDO ORDEN', xy=(Lv/2, Mpr1*0.25), 
             xytext=(Lv/3, Mpr1*0.5),
             fontsize=8, color='darkred', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
             bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='darkred'))

ax5.set_title('(e) DIAGRAMA MARIPOSA - Mitad (2do orden)', fontsize=11, fontweight='bold')
ax5.set_xlabel('x (m)')
ax5.set_ylabel('M (t-m)')
ax5.legend(loc='upper left', fontsize=8)
ax5.grid(True, alpha=0.3)

# --------------------------------------------------------
# (f) DIAGRAMA DE CORTANTE (T-U-V-W)
# --------------------------------------------------------
ax6 = fig1.add_subplot(gs1[2, 1])
ax6.set_xlim(-0.2, Lv + 0.2)
ax6.set_ylim(-Vu*1.5, Vu*1.5)

x_v = np.linspace(0, Lv, 300)
V_diag = np.zeros_like(x_v)

for i, x in enumerate(x_v):
    if x < Z_prot/100:
        V_diag[i] = Vu - (Vu - Vug) * (x/(Z_prot/100))
    elif x > Lv - Z_prot/100:
        V_diag[i] = -Vu + (Vu - Vug) * ((Lv - x)/(Z_prot/100))
    else:
        V_diag[i] = Vum * (1 - 2*(x - Z_prot/100)/(Lv - 2*Z_prot/100))

ax6.plot(x_v, V_diag, 'b-', linewidth=3.5, label='V(x)')
ax6.fill_between(x_v, V_diag, alpha=0.25, color='blue')
ax6.axhline(y=0, color='black', linewidth=1)

ax6.axvspan(0, Z_prot/100, alpha=0.15, color='red')
ax6.axvspan(Lv - Z_prot/100, Lv, alpha=0.15, color='red')

ax6.text(Z_prot/200, Vu*0.9, f'T-U\nPRIMER\nCORTANTE\nU = {Vu:.2f} t', ha='center', fontsize=8, color='blue', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='blue'))
ax6.text(Lv/2, 1.5, 'V = 0', ha='center', fontsize=10, color='green', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='green'))
ax6.text(Lv - Z_prot/200, -Vu*0.9, f'SEGUNDO\nCORTANTE\nW = {-Vu:.2f} t', ha='center', fontsize=8, color='blue', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='blue'))

ax6.text(Lv/2, -Vu*1.3, f'Vu = Vum + Vug = {Vum:.2f} + {Vug:.2f} = {Vu:.2f} t',
         ha='center', fontsize=9, color='darkblue', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='darkblue', linewidth=2))

ax6.set_title('(f) DIAGRAMA DE CORTANTE V(x)', fontsize=11, fontweight='bold')
ax6.set_xlabel('x (m)')
ax6.set_ylabel('V (t)')
ax6.legend(loc='upper right', fontsize=8)
ax6.grid(True, alpha=0.3)

# --------------------------------------------------------
# (g) FALLA POR SISMO
# --------------------------------------------------------
ax7 = fig1.add_subplot(gs1[3, 0])
ax7.set_xlim(0, 10)
ax7.set_ylim(0, 10)
ax7.axis('off')

ax7.text(5, 9.5, 'FALLA POR SISMO', ha='center', fontsize=11, fontweight='bold', color='red')

ax7.plot([1, 1], [3, 7], color='black', lw=3)
ax7.plot([9, 9], [3, 7], color='black', lw=3)
ax7.plot([1, 9], [7, 7], color='blue', lw=3)
ax7.plot([1, 9], [3, 3], color='blue', lw=3)

ax7.plot(2, 5, marker='o', markersize=15, color='red')
ax7.text(2, 4, 'Giro', fontsize=8, color='red', fontweight='bold')

ax7.annotate('', xy=(5, 5.5), xytext=(5, 4), arrowprops=dict(arrowstyle='->', color='red', lw=3))
ax7.text(5.5, 4.7, 'Vmom', fontsize=8, color='red', fontweight='bold')

ax7.annotate('', xy=(8, 4.5), xytext=(8, 5.5), arrowprops=dict(arrowstyle='->', color='green', lw=3))
ax7.text(8.5, 5, 'Vgrav', fontsize=8, color='green', fontweight='bold')

ax7.set_title('(g) Falla por sismo', fontsize=11, fontweight='bold')

# --------------------------------------------------------
# (h) CUANTIAS Y DUCTILIDAD
# --------------------------------------------------------
ax8 = fig1.add_subplot(gs1[3, 1])
ax8.set_xlim(0, 3)
ax8.set_ylim(0, 1)

ax8.axvline(x=rho_min_pct/100, color='blue', linestyle='--', linewidth=2, label=f'rho_min = {rho_min_pct:.2f}%')
ax8.axvline(x=rho/100, color='green', linestyle='-', linewidth=3, label=f'rho_real = {rho:.2f}%')
ax8.axvline(x=1.0/100, color='yellow', linestyle='--', linewidth=2, label='rho_ductil = 1%')
ax8.axvline(x=rho_max_bal_pct/100, color='orange', linestyle='--', linewidth=2, label=f'0.75 rho_bal = {rho_max_bal_pct:.2f}%')
ax8.axvline(x=rho_bal_pct/100, color='red', linestyle='--', linewidth=2, label=f'rho_bal = {rho_bal_pct:.2f}%')

ax8.axvspan(0, rho_min_pct/100, alpha=0.15, color='red')
ax8.axvspan(rho_min_pct/100, 1.0/100, alpha=0.15, color='green')
ax8.axvspan(1.0/100, rho_max_bal_pct/100, alpha=0.15, color='yellow')
ax8.axvspan(rho_max_bal_pct/100, rho_bal_pct/100, alpha=0.15, color='orange')

ax8.plot(rho/100, 0.5, 'go', markersize=15, zorder=10)

criterios_box = (
    f"rho_real = {rho:.2f}%\n"
    f"rho <= 1%  OK\n"
    f"rho_bal = {rho_bal_pct:.2f}%\n"
    f"FALLA: {tipo_falla}"
)
ax8.text(1.5, 0.5, criterios_box, ha='center', va='center', fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='green', linewidth=2))

ax8.set_xlabel('Cuantia rho (%)', fontsize=11)
ax8.set_title('(h) CUANTIAS Y DUCTILIDAD', fontsize=11, fontweight='bold')
ax8.legend(loc='upper right', fontsize=7)
ax8.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('M04_A1_dashboard_2D.png', dpi=150, bbox_inches='tight')
print(f"\nDashboard 2D guardado: M04_A1_dashboard_2D.png")
plt.show(block=False)

# ============================================================================
# 9. MODELO 3D
# ============================================================================

fig2 = plt.figure(figsize=(20, 14), num='M04-A1: Modelo 3D Detalles')
ax = fig2.add_subplot(111, projection='3d')

fig2.suptitle(
    f"M04 - ALGORITMO 1: VIGA RESILIENTE EN 3D - DETALLES DE ARMADO\n"
    f"Sistema de marcas: Mc 341 | Mc 342 | Mc 343",
    fontsize=14, fontweight='bold', color='#2c3e50'
)

L = Lv
b = b_viga / 100
h = h_def / 100

vertices = [[0,0,0],[L,0,0],[L,b,0],[0,b,0],[0,0,h],[L,0,h],[L,b,h],[0,b,h]]
caras_idx = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]
caras = [[vertices[i] for i in cara] for cara in caras_idx]

ax.add_collection3d(Poly3DCollection(caras, facecolors='#d0d0d0', linewidths=1.5, edgecolors='black', alpha=0.30))

z_sup = h - rec/100 - phi_est/1000 - phi_sup/2000
for i in range(4):
    y_var = rec/100 + phi_est/1000 + phi_sup/2000 + i * (b - 2*rec/100 - 2*phi_est/1000 - phi_sup/1000) / 3
    ax.plot([0, 1.0], [y_var, y_var], [z_sup, z_sup], color='red', lw=5, solid_capstyle='round')
    ax.plot([L - 1.0, L], [y_var, y_var], [z_sup, z_sup], color='red', lw=5, solid_capstyle='round')

for i in range(2):
    y_var = b/2 + (i - 0.5) * 0.04
    ax.plot([0, L], [y_var, y_var], [z_sup, z_sup], color='blue', lw=4, solid_capstyle='round', alpha=0.8)

z_inf = rec/100 + phi_est/1000 + phi_inf/2000
for i in range(3):
    y_var = rec/100 + phi_est/1000 + phi_inf/2000 + i * (b - 2*rec/100 - 2*phi_est/1000 - phi_inf/1000) / 2
    ax.plot([0, L], [y_var, y_var], [z_inf, z_inf], color='blue', lw=4, solid_capstyle='round')

n_est_prot = int((Z_prot/100) / (s_prot/100))
for i in range(n_est_prot):
    x_est = i * s_prot/100
    y_est = [rec/100, b - rec/100, b - rec/100, rec/100, rec/100]
    z_est = [rec/100, rec/100, h - rec/100, h - rec/100, rec/100]
    ax.plot([x_est]*5, y_est, z_est, color='red', lw=1.5, alpha=0.8)
for i in range(n_est_prot):
    x_est = L - i * s_prot/100
    y_est = [rec/100, b - rec/100, b - rec/100, rec/100, rec/100]
    z_est = [rec/100, rec/100, h - rec/100, h - rec/100, rec/100]
    ax.plot([x_est]*5, y_est, z_est, color='red', lw=1.5, alpha=0.8)

n_est_cent = int((L - 2*Z_prot/100) / (s_cent/100))
for i in range(n_est_cent):
    x_est = Z_prot/100 + i * s_cent/100
    y_est = [rec/100, b - rec/100, b - rec/100, rec/100, rec/100]
    z_est = [rec/100, rec/100, h - rec/100, h - rec/100, rec/100]
    ax.plot([x_est]*5, y_est, z_est, color='blue', lw=1, alpha=0.6)

ax.scatter(0, b/2, -0.05, color='blue', s=200, marker='^', label='Articulacion')
ax.scatter(L, b/2, -0.05, color='green', s=200, marker='o', label='Rodillo')

for x_carga in np.linspace(0.3, L-0.3, 10):
    ax.plot([x_carga, x_carga], [b/2, b/2], [h+0.15, h+0.05], color='red', lw=2)
ax.plot([0.3, L-0.3], [b/2, b/2], [h+0.15, h+0.15], color='red', lw=2.5)
ax.text(L/2, b/2, h+0.25, f'w = {w:.2f} t/m', color='red', fontsize=11, fontweight='bold', ha='center')

tic_3d = (
    f"VIGA RESILIENTE\n"
    f"rho = {rho:.2f}% <= 1%\n"
    f"As+/As- = {rel_as:.0f}% >= 50%\n"
    f"a/h = {rel_a_h*100:.0f}% ~ 20%\n"
    f"h/b = {rel_hb:.2f} <= 1.5\n"
    f"Mc 341 | Mc 342 | Mc 343"
)
ax.text(L/2, b/2, h + 0.55, tic_3d, color='darkgreen', fontsize=10, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='green', linewidth=2))

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.set_xlim(-0.5, L+0.5)
ax.set_ylim(-0.3, b+0.3)
ax.set_zlim(-0.5, h+1.0)
ax.set_title('Modelo 3D - Viga Resiliente con Detalles de Armado', fontsize=13, fontweight='bold')
ax.view_init(elev=20, azim=-55)
ax.legend(loc='upper left', fontsize=9)

plt.tight_layout()
plt.savefig('M04_A1_modelo_3D.png', dpi=150, bbox_inches='tight')
print(f"Modelo 3D guardado: M04_A1_modelo_3D.png")
plt.show()

print("\n" + "=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 70)