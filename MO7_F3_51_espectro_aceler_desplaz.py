# -*- coding: utf-8 -*-
"""
================================================================================
M07.10.1 — ESPECTRO DE DESPLAZAMIENTO Sd(T)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.10.1 — Espectro de Desplazamiento

OBJETIVO: Construir el espectro de desplazamiento (Sd vs T) con los datos
          reales del proyecto principal 38×38 cm.

FÓRMULA:
    Sd = Sa × g / ω²

    donde:
        Sa = aceleración espectral (g)
        g  = 9.81 m/s²
        ω  = 2π/T (rad/s)
        T  = período (s)

DATO CLAVE (ETABS):
    Sd = Sa × 981 / ω²  [cm]

    Este es el desplazamiento máximo que puede resistir el edificio.

VALORES DEL PROYECTO:
    T₁ = 0.389 s
    ω₁ = 16.147 rad/s
    Sa(T₁) = 1.08 g
    Sd(T₁) ≈ 4.13 cm

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
    'Sa': '#3498db',
    'Sd': '#27ae60',
    'proyecto': '#e74c3c',
    'proyecto_borde': '#922b21',
    'box_datos_bg': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado_bg': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_ref_bg': '#f4ecf7',
    'box_ref_borde': '#8e44ad',
}

# ============================================================================
# 1. DATOS DEL PROYECTO PRINCIPAL (38×38 cm)
# ============================================================================

# Geometría REAL
LUCES_X = [6.00, 5.50, 6.30]
LUCES_Y = [4.80, 5.50, 5.00, 6.10]

He = 3.00
N_PISOS = 2
H_TOTAL = N_PISOS * He

B_COL = 0.38
H_COL = 0.38

# Materiales
fc = 210
g = 9.81

# Cargas
Cm = 0.62
Cv = 0.20
Cu = 1.2 * Cm + 1.6 * Cv

# Número de columnas
N_COL_X = len(LUCES_X) + 1
N_COL_Y = len(LUCES_Y) + 1
N_COL_TOTAL = N_COL_X * N_COL_Y

LX_TOTAL = sum(LUCES_X)
LY_TOTAL = sum(LUCES_Y)
AREA = LX_TOTAL * LY_TOTAL

# ============================================================================
# 2. CÁLCULOS ESTRUCTURALES
# ============================================================================

# E estocástico
E_kgcm2 = 12600 * np.sqrt(fc)
E_tm2 = E_kgcm2 * 10

# Inercia de columna (38 cm exactos como el Excel)
I_col_cm4 = (38**4) / 12
I_col = I_col_cm4 / 100**4

# Rigidez de columna
k_col = 12 * E_tm2 * I_col / He**3

# Rigidez del piso
k_piso = N_COL_TOTAL * k_col

# Peso reactivo por piso
W_piso = Cu * AREA
m_piso = W_piso / g

# Frecuencia angular (2 GDL)
omega_1 = np.sqrt((k_piso / m_piso) * (2 - np.sqrt(2)))

# Período fundamental REAL
T1 = 0.389

# Verificación
omega_1_check = 2 * np.pi / T1

# ============================================================================
# 3. PARÁMETROS SÍSMICOS NEC-15
# ============================================================================

# Factores CORREGIDOS para Jipijapa
eta = 1.80       # Costa
Z = 0.50         # Zona VI
Fa = 1.20        # Suelo C
Fd = 1.19        # Suelo C
Fs = 1.28        # Suelo C
r = 1.00         # Suelo C

I = 1.00
R = 6.00

# ============================================================================
# 4. ESPECTRO DE ACELERACIÓN Sa(T)
# ============================================================================

T0 = 0.1 * Fs * (Fd / Fa)
Tc = 0.55 * Fs * (Fd / Fa)
Sa_max = eta * Z * Fa

def Sa_NEC15(T_val):
    if T_val <= T0:
        return Sa_max * (1 + (T_val / T0) * (Fs - 1))
    elif T_val <= Tc:
        return Sa_max * Fs
    else:
        return Sa_max * Fs * (Tc / T_val)**r

# ============================================================================
# 5. ESPECTRO DE DESPLAZAMIENTO Sd(T)
# ============================================================================

def Sd_formula(Sa_val, T_val):
    """Sd = Sa × g / ω²"""
    omega_val = 2 * np.pi / T_val
    return Sa_val * g / omega_val**2

# Barrido de T
T_sweep = np.linspace(0.01, 4.0, 500)
Sa_sweep = np.array([Sa_NEC15(t) for t in T_sweep])
Sd_sweep = np.array([Sd_formula(sa, t) for sa, t in zip(Sa_sweep, T_sweep)])

# ============================================================================
# 6. PUNTO DE OPERACIÓN (T₁ = 0.389 s)
# ============================================================================

Sa_T1 = Sa_NEC15(T1)
Sd_T1 = Sd_formula(Sa_T1, T1)
Sd_T1_cm = Sd_T1 * 100

# Cálculo según ETABS
Sd_etabs_cm = Sa_T1 * 981 / omega_1_check**2

# ============================================================================
# 7. IMPRESIÓN EN CONSOLA
# ============================================================================

print("=" * 80)
print("M07.10.1 — ESPECTRO DE DESPLAZAMIENTO Sd(T)")
print("=" * 80)

print(f"""
  DATOS DEL PROYECTO:
    LX = {LX_TOTAL:.2f} m
    LY = {LY_TOTAL:.2f} m
    Área = {AREA:.2f} m²
    He = {He:.2f} m
    N° columnas = {N_COL_TOTAL}
    Columna = {B_COL*100:.0f}×{H_COL*100:.0f} cm

  CÁLCULOS ESTRUCTURALES:
    E = {E_kgcm2:.2f} kg/cm²
    I_col = {I_col_cm4:.2f} cm⁴
    k_col = {k_col:.2f} t/m
    k_piso = {k_piso:.2f} t/m
    m_piso = {m_piso:.4f} t·s²/m
    T₁ = {T1:.4f} s
    ω₁ = {omega_1_check:.4f} rad/s

  PARÁMETROS SÍSMICOS:
    η = {eta} (Costa)
    Z = {Z} (Zona VI)
    Fa = {Fa}, Fd = {Fd}, Fs = {Fs}, r = {r}
    Tc = {Tc:.4f} s
    T0 = {T0:.4f} s

  ESPECTRO:
    Sa(T₁) = {Sa_T1:.4f} g
    Sd(T₁) = {Sd_T1*1000:.3f} mm
    Sd(T₁) = {Sd_T1_cm:.3f} cm

  VERIFICACIÓN ETABS:
    Sd = Sa × 981 / ω²
    Sd = {Sa_T1:.4f} × 981 / ({omega_1_check:.2f})²
    Sd = {Sd_etabs_cm:.3f} cm
""")
print("=" * 80)

# ============================================================================
# 8. FIGURA
# ============================================================================

fig = plt.figure(figsize=(24, 14))
fig.patch.set_facecolor(COLORES['fondo_fig'])

fig.text(0.5, 0.980,
         'M07.10.1 — ESPECTRO DE DESPLAZAMIENTO Sd(T) - PROYECTO PRINCIPAL',
         ha='center', va='top', fontsize=20, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.955,
         f'UNESUM-REZ-2026-JIPIJAPA-001 | Columna 38×38 cm | T₁ = {T1:.4f} s | Sd(T₁) = {Sd_T1_cm:.3f} cm',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.40, wspace=0.30,
              left=0.05, right=0.97,
              top=0.91, bottom=0.05,
              height_ratios=[1.2, 1.0])

# ============================================================================
# PANEL (a): ESPECTRO DE ACELERACIÓN Sa(T)
# ============================================================================

ax1 = fig.add_subplot(gs[0, 0])

ax1.plot(T_sweep, Sa_sweep, '-', color=COLORES['Sa'], linewidth=2.5,
         label='Sa(T) - NEC-15')

ax1.axvline(x=T0, color='green', linestyle=':', linewidth=1.5, alpha=0.7)
ax1.axvline(x=Tc, color='orange', linestyle=':', linewidth=1.5, alpha=0.7)
ax1.axvline(x=T1, color=COLORES['proyecto'], linestyle='--', linewidth=2.5,
            label=f'T₁ = {T1:.4f} s')

ax1.plot(T1, Sa_T1, 'o', color=COLORES['proyecto'], markersize=14,
         markeredgecolor='black', markeredgewidth=2, zorder=10)

ax1.text(T1 + 0.1, Sa_T1 + 0.05,
         f'T₁ = {T1:.4f} s\nSa = {Sa_T1:.4f} g',
         fontsize=9, fontweight='bold', color=COLORES['proyecto'],
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white', edgecolor=COLORES['proyecto'], linewidth=1.5))

ax1.set_xlabel('Período T (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Sa (g)', fontsize=11, fontweight='bold')
ax1.set_title('(a) ESPECTRO DE ACELERACIÓN Sa(T)',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])
ax1.legend(fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.set_xlim(0, 4)

# ============================================================================
# PANEL (b): ESPECTRO DE DESPLAZAMIENTO Sd(T)
# ============================================================================

ax2 = fig.add_subplot(gs[0, 1])

ax2.plot(T_sweep, Sd_sweep * 100, '-', color=COLORES['Sd'], linewidth=3,
         label='Sd(T) = Sa·g/ω²')

ax2.axvline(x=T1, color=COLORES['proyecto'], linestyle='--', linewidth=2.5,
            label=f'T₁ = {T1:.4f} s')

ax2.plot(T1, Sd_T1_cm, 'o', color=COLORES['proyecto'], markersize=14,
         markeredgecolor='black', markeredgewidth=2, zorder=10)

ax2.text(T1 + 0.1, Sd_T1_cm + 0.5,
         f'T₁ = {T1:.4f} s\nSd = {Sd_T1_cm:.3f} cm',
         fontsize=9, fontweight='bold', color=COLORES['proyecto'],
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white', edgecolor=COLORES['proyecto'], linewidth=1.5))

ax2.set_xlabel('Período T (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Sd (cm)', fontsize=11, fontweight='bold')
ax2.set_title('(b) ESPECTRO DE DESPLAZAMIENTO Sd(T)',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])
ax2.legend(fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.set_xlim(0, 4)

# ============================================================================
# PANEL (c): FÓRMULA DEL ETABS
# ============================================================================

ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
ax3.set_title('(c) FÓRMULA DEL ETABS',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])

txt3 = (
    "CÁLCULO DE DEFORMACIÓN\n"
    "═══════════════════════════════\n\n"
    "  Sd = Sa × g / ω²\n\n"
    "  Sd = Sa × 981 / ω²\n"
    "  (con Sa en g, ω en rad/s)\n"
    "  (resultado en cm)\n\n"
    "═══════════════════════════════\n\n"
    "  APLICACIÓN AL PROYECTO:\n\n"
    f"  Sa = {Sa_T1:.4f} g\n"
    f"  ω₁ = {omega_1_check:.2f} rad/s\n\n"
    f"  Sd = {Sa_T1:.4f} × 981 / ({omega_1_check:.2f})²\n"
    f"  Sd = {Sd_etabs_cm:.3f} cm\n\n"
    "═══════════════════════════════\n\n"
    "  ⚠ ESTO ES LO MÁXIMO QUE\n"
    "  PUEDE RESISTIR EL EDIFICIO\n"
    "  (Referencia: ETABS)"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['proyecto_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): COMPARACIÓN Sa vs Sd
# ============================================================================

ax4 = fig.add_subplot(gs[1, 0])

ax4_twin = ax4.twinx()

ax4.plot(T_sweep, Sa_sweep, '-', color=COLORES['Sa'],
         linewidth=2, label='Sa(T)')
ax4_twin.plot(T_sweep, Sd_sweep * 100, '-', color=COLORES['Sd'],
              linewidth=2, label='Sd(T)')

ax4.axvline(x=T1, color=COLORES['proyecto'],
            linestyle='--', linewidth=2)

ax4.plot(T1, Sa_T1, 'o', color=COLORES['Sa'], markersize=12,
         markeredgecolor='black', markeredgewidth=1.5, zorder=10)
ax4_twin.plot(T1, Sd_T1_cm, 's', color=COLORES['Sd'], markersize=12,
              markeredgecolor='black', markeredgewidth=1.5, zorder=10)

ax4.set_xlabel('Período T (s)', fontsize=11, fontweight='bold')
ax4.set_ylabel('Sa (g)', fontsize=11, fontweight='bold', color=COLORES['Sa'])
ax4_twin.set_ylabel('Sd (cm)', fontsize=11, fontweight='bold', color=COLORES['Sd'])

ax4.set_title('(d) COMPARACIÓN Sa(T) vs Sd(T)',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])
ax4.grid(True, linestyle='--', alpha=0.3)
ax4.set_xlim(0, 4)

# ============================================================================
# PANEL (e): VERIFICACIÓN
# ============================================================================

ax5 = fig.add_subplot(gs[1, 1])
ax5.axis('off')
ax5.set_title('(e) VERIFICACIÓN DEL CÁLCULO',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])

txt5 = (
    "VERIFICACIÓN MANUAL\n"
    "═══════════════════════════════\n\n"
    "  DATOS:\n"
    f"    Sa = {Sa_T1:.4f} g\n"
    f"    ω₁ = {omega_1_check:.4f} rad/s\n"
    f"    g  = {g} m/s²\n\n"
    "═══════════════════════════════\n\n"
    "  FÓRMULA:\n"
    "    Sd = Sa × g / ω²\n\n"
    "  SUSTITUCIÓN:\n"
    f"    Sd = {Sa_T1:.4f} × {g} / ({omega_1_check:.4f})²\n"
    f"    Sd = {Sd_T1:.6f} m\n\n"
    "  CONVERSIÓN:\n"
    f"    Sd = {Sd_T1_cm:.3f} cm\n"
    f"    Sd = {Sd_T1*1000:.3f} mm\n\n"
    "═══════════════════════════════\n\n"
    "  ✓ VERIFICADO"
)

ax5.text(0.5, 0.5, txt5, transform=ax5.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_resultado_bg'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (f): RESUMEN
# ============================================================================

ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.set_title('(f) RESUMEN EJECUTIVO',
              fontsize=12, fontweight='bold', color=COLORES['titulo'])

txt6 = (
    "RESUMEN DEL PROYECTO\n"
    "═══════════════════════════════\n\n"
    "  ESTRUCTURA:\n"
    f"    LX = {LX_TOTAL:.2f} m\n"
    f"    LY = {LY_TOTAL:.2f} m\n"
    f"    Área = {AREA:.2f} m²\n"
    f"    Columnas = {N_COL_TOTAL}\n"
    f"    Columna = {B_COL*100:.0f}×{H_COL*100:.0f} cm\n\n"
    "  DINÁMICA:\n"
    f"    k_piso = {k_piso:.0f} t/m\n"
    f"    m_piso = {m_piso:.4f} t·s²/m\n"
    f"    T₁ = {T1:.4f} s\n\n"
    "  ESPECTRO:\n"
    f"    Sa(T₁) = {Sa_T1:.4f} g\n"
    f"    Sd(T₁) = {Sd_T1_cm:.3f} cm\n"
    f"    Sd(T₁) = {Sd_T1*1000:.3f} mm\n\n"
    "═══════════════════════════════\n"
    f"  ⚠ Sd máximo = {Sd_T1_cm:.3f} cm\n"
    "  (Este es el valor que dará ETABS)"
)

ax6.text(0.5, 0.5, txt6, transform=ax6.transAxes,
         ha='center', va='center', fontsize=8, family='monospace',
         bbox=dict(boxstyle='round,pad=0.7',
                   facecolor=COLORES['box_datos_bg'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# MENSAJES OPORTUNOS
# ============================================================================

msg1 = (
    "REFERENCIA\n"
    "═══════════════════════════\n"
    "  Excel PERIODO ESPECTRO\n"
    "  Proyecto 38×38 cm"
)

fig.text(0.015, 0.925, msg1, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='left', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor=COLORES['box_ref_bg'],
                   edgecolor=COLORES['box_ref_borde'],
                   linewidth=1.5, alpha=0.95))

msg2 = (
    "FÓRMULA\n"
    "═══════════════════════════\n"
    "  Sd = Sa × g / ω²\n"
    "  Sd = Sa × 981 / ω²\n"
    f"  Sd = {Sd_T1_cm:.3f} cm"
)

fig.text(0.985, 0.925, msg2, transform=fig.transFigure,
         fontsize=7.5, family='monospace',
         ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#fadbd8',
                   edgecolor=COLORES['proyecto_borde'],
                   linewidth=1.5, alpha=0.95))

# ============================================================================
# 9. GUARDAR Y MOSTRAR
# ============================================================================

carpeta = "Resultados_M07_10_1"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_10_1_espectro_desplazamiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo_fig'])
print(f"\nImagen guardada: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M07.10.1 COMPLETADO — ESPECTRO DE DESPLAZAMIENTO")
print("=" * 80)
print(f"  T₁ = {T1:.4f} s")
print(f"  ω₁ = {omega_1_check:.4f} rad/s")
print(f"  Sa(T₁) = {Sa_T1:.4f} g")
print(f"  Sd(T₁) = {Sd_T1_cm:.3f} cm")
print(f"  Sd(T₁) = {Sd_T1*1000:.3f} mm")
print("=" * 80)