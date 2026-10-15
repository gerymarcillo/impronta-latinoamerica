# -*- coding: utf-8 -*-
"""
================================================================================
M07.10 — ESPECTRO DE RESPUESTA NEC-15 (CORREGIDO CON η)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.10 — Espectro NEC-15

CORRECCIÓN APLICADA:
    ✅ Fórmula: Sa = η × Z × Fa × (Tc/T)^r
    ✅ Factor η = 1.80 (Costa)
    ✅ Factor r = 1.0 (suelos A-D) / 1.5 (suelo E)
    ✅ SIN dividir por R (espectro elástico)

REFERENCIA EXCEL: PERIODO ESPECTRO.xlsx (hoja LORENZO)
================================================================================
"""

import os
import sys
from datetime import datetime
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

# ============================================================================
# PALETA DEL PROYECTO
# ============================================================================

COLORES = {
    'fondo_fig': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'suelo_C': '#3498db',
    'suelo_D': '#e74c3c',
    'suelo_E': '#27ae60',
    'proyecto': '#f39c12',
    'box_datos_bg': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado_bg': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_ref_bg': '#f4ecf7',
    'box_ref_borde': '#8e44ad',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

# Parámetros sísmicos (Excel LORENZO)
I_sismico = 1.0
fi_p = 1.0
fi_e = 1.0
R = 6.0
Z = 0.5
g = 9.81

# ✅ FACTOR η (razón Sa/PGA) - CORREGIDO
eta = 1.80  # Costa (excepto Esmeraldas)

# ✅ Factores de suelo con r
suelos = {
    'C': {'Fa': 1.2, 'Fd': 1.11, 'Fs': 1.11, 'r': 1.0, 'color': COLORES['suelo_C']},
    'D': {'Fa': 1.2, 'Fd': 1.19, 'Fs': 1.28, 'r': 1.0, 'color': COLORES['suelo_D']},
    'E': {'Fa': 1.0, 'Fd': 1.60, 'Fs': 1.90, 'r': 1.5, 'color': COLORES['suelo_E']},
}

# Parámetros del proyecto
He = 3.00
N_PISOS = 2
B_COL = 0.38
H_COL = 0.38
fc = 210
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]
N_COL_TOTAL = (len(LUCES_X) + 1) * (len(LUCES_Y) + 1)

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL

# E estocástico
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10
I_col_cm4 = (38**4) / 12
I_col = I_col_cm4 / 100**4

# k_piso
k_col = 12 * E_tm2 * I_col / He**3
k_piso = N_COL_TOTAL * k_col

# Masa
W_piso = Cu * AREA
m_piso = W_piso / g

# Período REAL del Excel
T1 = 0.389
omega1 = 2 * np.pi / T1

# ============================================================================
# 2. FUNCIÓN CORREGIDA DEL ESPECTRO
# ============================================================================

def calcular_espectro(suelo, T_array):
    """
    Calcula el espectro de respuesta NEC-15 CORREGIDO.
    
    FÓRMULA CORRECTA:
        Sa = η × Z × Fa × (Tc/T)^r
    """
    Fa = suelo['Fa']
    Fd = suelo['Fd']
    Fs = suelo['Fs']
    r = suelo['r']
    
    # Períodos característicos (NEC-15)
    Tc = 0.55 * Fs * Fd / Fa
    T0 = 0.1 * Fs * Fd / Fa
    
    # ✅ ACELERACIÓN MÁXIMA CORREGIDA (con η)
    Sa_max = eta * Z * Fa
    
    Sa = np.zeros_like(T_array)
    
    for i, T in enumerate(T_array):
        if T < T0:
            # Rama ascendente
            Sa[i] = Sa_max * (1 + (T / T0) * (Fs - 1))
        elif T < Tc:
            # Meseta
            Sa[i] = Sa_max * Fs
        else:
            # Rama descendente
            Sa[i] = Sa_max * Fs * (Tc / T)**r
    
    return Sa, Tc, T0, Sa_max

# ============================================================================
# 3. CÁLCULO DE LOS 3 ESPECTROS
# ============================================================================

T_array = np.linspace(0.01, 4.0, 500)

espectros = {}
for nombre, suelo in suelos.items():
    Sa, Tc, T0, Sa_max = calcular_espectro(suelo, T_array)
    espectros[nombre] = {
        'Sa': Sa,
        'Tc': Tc,
        'T0': T0,
        'Sa_max': Sa_max,
    }

# ============================================================================
# 4. PUNTO DE OPERACIÓN (T₁ = 0.389 s)
# ============================================================================

puntos_operacion = {}
for nombre in suelos.keys():
    Sa_T1 = np.interp(T1, T_array, espectros[nombre]['Sa'])
    puntos_operacion[nombre] = {'Sa': Sa_T1}

# ============================================================================
# 5. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.10 — ESPECTRO DE RESPUESTA NEC-15 (CORREGIDO CON η)")
print("=" * 80)
print(f"""
  ✅ FÓRMULA CORREGIDA:
    Sa = η × Z × Fa × (Tc/T)^r

  PARÁMETROS SÍSMICOS (NEC-15):
    η = {eta} (Costa)
    Z = {Z} (Zona VI)
    I = {I_sismico}
    R = {R} (NO se aplica al espectro elástico)

  FACTORES DE SUELO:
    C: Fa={suelos['C']['Fa']}, Fd={suelos['C']['Fd']}, Fs={suelos['C']['Fs']}, r={suelos['C']['r']}
    D: Fa={suelos['D']['Fa']}, Fd={suelos['D']['Fd']}, Fs={suelos['D']['Fs']}, r={suelos['D']['r']}
    E: Fa={suelos['E']['Fa']}, Fd={suelos['E']['Fd']}, Fs={suelos['E']['Fs']}, r={suelos['E']['r']}

  SA_MAX (CORREGIDO):
""")

for nombre in ['C', 'D', 'E']:
    esp = espectros[nombre]
    print(f"    Suelo {nombre}: Sa_max = η × Z × Fa = {eta} × {Z} × {suelos[nombre]['Fa']} = {esp['Sa_max']:.4f} g")

print(f"""
  PUNTO DE OPERACIÓN (T₁ = {T1:.4f} s):
""")

for nombre in ['C', 'D', 'E']:
    Sa = puntos_operacion[nombre]['Sa']
    print(f"    Suelo {nombre}: Sa(T₁) = {Sa:.4f} g")

print("=" * 80)

# ============================================================================
# 6. FIGURA
# ============================================================================

fig = plt.figure(figsize=(24, 14))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.10 — ESPECTRO DE RESPUESTA NEC-15 (CORREGIDO)',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | T₁ = {T1:.4f} s | Sa = η × Z × Fa | η = {eta}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.5, 1.0])

# ============================================================================
# PANEL (a): 3 CURVAS DE CAPACIDAD
# ============================================================================

ax1 = fig.add_subplot(gs[0, :])

for nombre in ['C', 'D', 'E']:
    ax1.plot(T_array, espectros[nombre]['Sa'], '-',
             color=suelos[nombre]['color'], linewidth=3,
             label=f"Suelo {nombre} (Fa={suelos[nombre]['Fa']}, Fd={suelos[nombre]['Fd']}, Fs={suelos[nombre]['Fs']}, r={suelos[nombre]['r']})")

ax1.axvline(x=T1, color=COLORES['proyecto'],
            linestyle='--', linewidth=3,
            label=f'T₁ = {T1:.4f} s')

for nombre in ['C', 'D', 'E']:
    Sa = puntos_operacion[nombre]['Sa']
    ax1.plot(T1, Sa, 'o', color=suelos[nombre]['color'],
             markersize=18, markeredgecolor='black',
             markeredgewidth=2, zorder=10)

for i, nombre in enumerate(['C', 'D', 'E']):
    Sa = puntos_operacion[nombre]['Sa']
    offset_y = 0.15 + i * 0.10
    ax1.annotate(f'Sa({nombre}) = {Sa:.3f} g',
                 xy=(T1, Sa),
                 xytext=(T1 + 0.3, Sa + offset_y),
                 fontsize=11, fontweight='bold',
                 color=suelos[nombre]['color'],
                 arrowprops=dict(arrowstyle='->',
                                 color=suelos[nombre]['color'], lw=2),
                 bbox=dict(boxstyle='round,pad=0.3',
                           facecolor='white',
                           edgecolor=suelos[nombre]['color'],
                           linewidth=2))

ax1.axvspan(0, 0.13, alpha=0.08, color='green')
ax1.axvspan(0.13, 0.70, alpha=0.08, color='yellow')
ax1.axvspan(0.70, 4.5, alpha=0.08, color='red')

ax1.text(0.06, 1.6, 'Rama\nascendente', ha='center', fontsize=9,
         color='green', fontweight='bold')
ax1.text(0.4, 1.6, 'Meseta', ha='center', fontsize=9,
         color='#d68910', fontweight='bold')
ax1.text(2.5, 1.6, 'Rama descendente', ha='center', fontsize=9,
         color='red', fontweight='bold')

ax1.set_xlabel('Período T (s)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Aceleración Espectral Sa (g)', fontsize=13, fontweight='bold')
ax1.set_title('(a) 3 CURVAS DE CAPACIDAD - ESPECTRO NEC-15 (Sa = η × Z × Fa)',
              fontsize=14, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.set_xlim(0, 4.5)
ax1.set_ylim(0, 2.0)

# ============================================================================
# PANEL (b): PARÁMETROS SÍSMICOS
# ============================================================================

ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')
ax2.set_title('(b) PARÁMETROS SÍSMICOS NEC-15',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)

txt2 = (
    "PARÁMETROS NEC-15\n"
    "═══════════════════════════════\n\n"
    f"  η  = {eta}  (Costa)\n"
    f"  Z  = {Z}  (Zona VI)\n"
    f"  I  = {I_sismico}\n"
    f"  R  = {R}  (NO aplica a Sa)\n"
    f"  φP = {fi_p}\n"
    f"  φE = {fi_e}\n\n"
    "═══════════════════════════════\n"
    "FÓRMULA:\n"
    "  Sa = η × Z × Fa\n\n"
    "═══════════════════════════════\n"
    "SA_MAX:\n"
    f"  Suelo C: {espectros['C']['Sa_max']:.4f} g\n"
    f"  Suelo D: {espectros['D']['Sa_max']:.4f} g\n"
    f"  Suelo E: {espectros['E']['Sa_max']:.4f} g"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): PUNTO DE OPERACIÓN
# ============================================================================

ax3 = fig.add_subplot(gs[1, 1])

categorias = ['Suelo C', 'Suelo D', 'Suelo E']
valores = [
    puntos_operacion['C']['Sa'],
    puntos_operacion['D']['Sa'],
    puntos_operacion['E']['Sa'],
]
colores_bar = [
    COLORES['suelo_C'],
    COLORES['suelo_D'],
    COLORES['suelo_E'],
]

bars = ax3.bar(categorias, valores, color=colores_bar,
               edgecolor='black', linewidth=2, width=0.6)

for bar, val in zip(bars, valores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.4f} g', ha='center', va='bottom',
             fontweight='bold', fontsize=11)

ax3.set_ylabel('Sa(T₁) (g)', fontsize=11, fontweight='bold')
ax3.set_title(f'(c) PUNTO DE OPERACIÓN - T₁ = {T1:.4f} s',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.set_ylim(0, max(valores) * 1.3)

# ============================================================================
# PANEL (d): PERÍODOS CARACTERÍSTICOS
# ============================================================================

ax4 = fig.add_subplot(gs[1, 2])

Tc_vals = [espectros['C']['Tc'], espectros['D']['Tc'], espectros['E']['Tc']]
T0_vals = [espectros['C']['T0'], espectros['D']['T0'], espectros['E']['T0']]

x_pos = np.arange(len(categorias))
width = 0.35

bars1 = ax4.bar(x_pos - width/2, Tc_vals, width,
                label='Tc (s)', color='#3498db',
                edgecolor='black', linewidth=1.5)
bars2 = ax4.bar(x_pos + width/2, T0_vals, width,
                label='T0 (s)', color='#e74c3c',
                edgecolor='black', linewidth=1.5)

for bar, val in zip(bars1, Tc_vals):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.3f}', ha='center', va='bottom',
             fontweight='bold', fontsize=10)
for bar, val in zip(bars2, T0_vals):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.3f}', ha='center', va='bottom',
             fontweight='bold', fontsize=10)

ax4.set_xticks(x_pos)
ax4.set_xticklabels(categorias, fontsize=10)
ax4.set_ylabel('Período (s)', fontsize=11, fontweight='bold')
ax4.set_title('(d) PERÍODOS CARACTERÍSTICOS',
              fontsize=12, fontweight='bold',
              color=COLORES['titulo'], pad=10)
ax4.legend(fontsize=10)
ax4.grid(axis='y', linestyle='--', alpha=0.3)

# ============================================================================
# 7. MENSAJES OPORTUNOS
# ============================================================================

msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Excel PERIODO ESPECTRO\n"
    "  NEC-15 (2015)"
)

fig.text(0.015, 0.925, msg1, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=1.5, alpha=0.95))

msg2 = (
    "CORRECCIÓN\n"
    "═══════════════════════════\n"
    f"  η = {eta} (Costa)\n"
    "  Sa = η × Z × Fa\n"
    "  SIN dividir por R"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fadbd8',
                   edgecolor='#c0392b',
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 8. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_10"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_10_espectro_corregido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"Imagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.10 COMPLETADO — ESPECTRO CORREGIDO CON η")
print("=" * 80)
print(f"  Fórmula: Sa = η × Z × Fa")
print(f"  η = {eta}")
print(f"  Suelo C: Sa_max = {espectros['C']['Sa_max']:.4f} g")
print(f"  Suelo D: Sa_max = {espectros['D']['Sa_max']:.4f} g")
print(f"  Suelo E: Sa_max = {espectros['E']['Sa_max']:.4f} g")
print("=" * 80)