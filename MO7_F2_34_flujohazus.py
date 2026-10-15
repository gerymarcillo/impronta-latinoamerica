# -*- coding: utf-8 -*-
"""
================================================================================
M07.39 — CLASIFICACIÓN HAZUZ ADAPTADA AL DISEÑO PRINCIPAL
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.39 — Clasificación HAZUZ

OBJETIVO: Integrar la clasificación HAZUZ 1999 en el diseño
          principal del proyecto, con:
          - Cálculo automático de deriva
          - Clasificación por tipo (PLATINUM, GOLD, SILVER, COMPLETO)
          - Cálculo de X objetivo
          - Verificación de cumplimiento

FÓRMULA EXCEL EQUIVALENTE:
    =+SI(F21="PLATINUM";0,0033;
        SI(F21="GOLD";0,0058;
        SI(F21="SYLVER";0,0156;0,04)))

ADAPTACIÓN PYTHON:
    Función clasificar_hazuz(der) que devuelve (tipo, der_obj)
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch, Patch

# ============================================================================
# PALETA NIVEL TOP (DISEÑO PRINCIPAL)
# ============================================================================

COLORES = {
    'fondo': '#f8f9fa',
    'fondo_panel': '#ffffff',
    'titulo': '#0d1b2a',
    'subtitulo': '#415a77',
    'linea': '#778da9',
    'ok': '#2d6a4f',
    'ok_bg': '#d8f3dc',
    'advertencia': '#e07a00',
    'advertencia_bg': '#fff3cd',
    'critica': '#9d0208',
    'critica_bg': '#f8d7da',
    'info': '#1d3557',
    'info_bg': '#d6e4f0',
    'acento': '#f77f00',
    'acento2': '#fcbf49',
    'resultado': '#2d6a4f',
    'platinum': '#6c757d',
    'gold': '#e07a00',
    'silver': '#495057',
    'completo': '#9d0208',
    'box_datos': '#ffffff',
    'box_datos_borde': '#0d1b2a',
    'box_resultado': '#d8f3dc',
    'box_resultado_borde': '#2d6a4f',
    'box_alerta': '#f8d7da',
    'box_alerta_borde': '#9d0208',
    'box_info': '#d6e4f0',
    'box_info_borde': '#1d3557',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."
TITULO = "CLASIFICACIÓN HAZUZ 1999 — ADAPTADA AL DISEÑO PRINCIPAL"

# Datos del proyecto
He = 3.00           # m
X_inel = 2.36       # cm
der = X_inel / He / 100

# ============================================================================
# 2. FUNCIONES HAZUZ
# ============================================================================

def clasificar_hazuz(der):
    """
    Clasifica la deriva según HAZUZ 1999.
    
    Rangos:
        PLATINUM: der < 0.0033
        GOLD:     0.0033 <= der < 0.0058
        SILVER:   0.0058 <= der < 0.0156
        COMPLETO: der >= 0.0156
    """
    if der < 0.0033:
        return "PLATINUM", 0.0033
    elif der < 0.0058:
        return "GOLD", 0.0058
    elif der < 0.0156:
        return "SILVER", 0.0156
    else:
        return "COMPLETO", 0.0400


def der_objetivo(tipo):
    """
    Devuelve la deriva objetivo según el tipo.
    Equivalente a la fórmula Excel.
    """
    if tipo == "PLATINUM":
        return 0.0033
    elif tipo == "GOLD":
        return 0.0058
    elif tipo == "SILVER":
        return 0.0156
    else:
        return 0.0400


def x_objetivo(der_obj, He):
    """
    Calcula X objetivo.
    X obj = der obj × He × 100
    """
    return der_obj * He * 100


# ============================================================================
# 3. CÁLCULOS
# ============================================================================

tipo, der_obj = clasificar_hazuz(der)
X_obj = x_objetivo(der_obj, He)

# Colores por tipo
colores_tipo = {
    "PLATINUM": COLORES['platinum'],
    "GOLD": COLORES['gold'],
    "SILVER": COLORES['silver'],
    "COMPLETO": COLORES['completo'],
}
color_tipo = colores_tipo[tipo]

# ============================================================================
# 4. FIGURA — DISEÑO PRINCIPAL
# ============================================================================

fig = plt.figure(figsize=(28, 20))
fig.patch.set_facecolor(COLORES['fondo'])

# ============================================================================
# ENCABEZADO PROFESIONAL
# ============================================================================

ax_header = fig.add_axes([0, 0.94, 1, 0.06])
ax_header.set_facecolor(COLORES['titulo'])
ax_header.axis('off')

ax_header.text(0.02, 0.5, '🏗️', fontsize=30, va='center')
ax_header.text(0.06, 0.5, 'UNESUM · REZ-2026 · JIPIJAPA-001',
               fontsize=16, fontweight='bold', color='white', va='center')
ax_header.text(0.98, 0.5, 'M07.39 — CLASIFICACIÓN HAZUZ',
               fontsize=16, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.915,
         'CLASIFICACIÓN HAZUZ 1999 — ADAPTADA AL DISEÑO PRINCIPAL',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.892,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): FÓRMULA EXCEL → PYTHON
# ============================================================================

ax1 = fig.add_axes([0.04, 0.68, 0.44, 0.18])
ax1.set_facecolor(COLORES['fondo_panel'])
ax1.axis('off')

ax1.set_title('(a) FÓRMULA EXCEL → PYTHON',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt1 = (
    "FÓRMULA EXCEL:\n"
    "═══════════════════════════════════════════\n"
    "=+SI(F21=\"PLATINUM\";0,0033;\n"
    "    SI(F21=\"GOLD\";0,0058;\n"
    "    SI(F21=\"SYLVER\";0,0156;0,04)))\n\n"
    "ADAPTACIÓN PYTHON:\n"
    "═══════════════════════════════════════════\n"
    "def clasificar_hazuz(der):\n"
    "    if der < 0.0033: return 'PLATINUM', 0.0033\n"
    "    elif der < 0.0058: return 'GOLD', 0.0058\n"
    "    elif der < 0.0156: return 'SILVER', 0.0156\n"
    "    else: return 'COMPLETO', 0.0400"
)

ax1.text(0.5, 0.5, txt1, transform=ax1.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_info'],
                   edgecolor=COLORES['box_info_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (b): DATOS DEL PROYECTO
# ============================================================================

ax2 = fig.add_axes([0.52, 0.68, 0.44, 0.18])
ax2.set_facecolor(COLORES['fondo_panel'])
ax2.axis('off')

ax2.set_title('(b) DATOS DEL PROYECTO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

txt2 = (
    "DATOS DE ENTRADA:\n"
    "═══════════════════════════════════════════\n"
    f"  He       = {He:.2f} m\n"
    f"  X inel   = {X_inel:.2f} cm\n\n"
    "CÁLCULOS:\n"
    "═══════════════════════════════════════════\n"
    f"  der      = X inel / He / 100\n"
    f"  der      = {X_inel:.2f} / {He:.2f} / 100\n"
    f"  der      = {der:.5f}\n\n"
    "CLASIFICACIÓN HAZUZ:\n"
    "═══════════════════════════════════════════\n"
    f"  tipo     = {tipo}\n"
    f"  der obj  = {der_obj:.4f}\n"
    f"  X obj    = {X_obj:.2f} cm"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): TABLA HAZUZ COMPLETA
# ============================================================================

ax3 = fig.add_axes([0.04, 0.38, 0.60, 0.25])
ax3.set_facecolor(COLORES['fondo_panel'])
ax3.axis('off')

ax3.set_title('(c) TABLA HAZUZ 1999 — CLASIFICACIÓN COMPLETA',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# Datos de la tabla
tabla_hazuz = [
    ("PLATINUM", 0.0033, "< 0.33%", "Leve", COLORES['platinum']),
    ("GOLD", 0.0058, "0.33% - 0.58%", "Moderado", COLORES['gold']),
    ("SILVER", 0.0156, "0.58% - 1.56%", "Extenso", COLORES['silver']),
    ("COMPLETO", 0.0400, "> 1.56%", "Completo", COLORES['completo']),
]

# Dibujar tabla
n_rows = len(tabla_hazuz) + 1
row_height = 0.20
y_start = 0.75

# Headers
headers = ["Tipo", "Deriva", "Rango", "Descripción"]
x_cols = [0.05, 0.25, 0.50, 0.75]

for i, (header, x) in enumerate(zip(headers, x_cols)):
    ax3.text(x, y_start, header,
             fontsize=11, fontweight='bold', color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')

# Línea
ax3.plot([0.03, 0.97], [y_start - 0.08, y_start - 0.08],
         color=COLORES['linea'], linewidth=1.5,
         transform=ax3.transAxes, clip_on=False)

# Filas
for i, (tipo_row, der_row, rango, desc, color) in enumerate(tabla_hazuz):
    y = y_start - 0.16 - i * row_height
    
    # Highlight si es el tipo del proyecto
    if tipo_row == tipo:
        rect = FancyBboxPatch((0.02, y - 0.07), 0.96, 0.14,
                               boxstyle="round,pad=0.01",
                               facecolor=color + '30',
                               edgecolor=color, linewidth=2,
                               transform=ax3.transAxes)
        ax3.add_patch(rect)
    
    ax3.text(x_cols[0], y, tipo_row,
             fontsize=10, fontweight='bold', color=color,
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[1], y, f"{der_row:.4f}",
             fontsize=10, color=COLORES['titulo'],
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[2], y, rango,
             fontsize=10, color=COLORES['subtitulo'],
             transform=ax3.transAxes, va='center')
    ax3.text(x_cols[3], y, desc,
             fontsize=10, color=COLORES['subtitulo'],
             transform=ax3.transAxes, va='center')

# ============================================================================
# PANEL (d): RESULTADO DE LA CLASIFICACIÓN
# ============================================================================

ax4 = fig.add_axes([0.68, 0.38, 0.28, 0.25])
ax4.set_facecolor(COLORES['fondo_panel'])
ax4.axis('off')

ax4.set_title('(d) RESULTADO',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# Cuadro grande con el tipo
rect = FancyBboxPatch((0.1, 0.55), 0.8, 0.35,
                       boxstyle="round,pad=0.03",
                       facecolor=color_tipo + '20',
                       edgecolor=color_tipo, linewidth=3,
                       transform=ax4.transAxes)
ax4.add_patch(rect)

ax4.text(0.5, 0.72, tipo,
         fontsize=28, fontweight='bold', color=color_tipo,
         ha='center', va='center', transform=ax4.transAxes)

ax4.text(0.5, 0.58, f"der = {der:.5f}",
         fontsize=14, fontweight='bold', color=COLORES['titulo'],
         ha='center', va='center', transform=ax4.transAxes)

# Valores
txt4 = (
    f"der obj = {der_obj:.4f}\n"
    f"X obj   = {X_obj:.2f} cm\n\n"
    f"He      = {He:.2f} m\n"
    f"X inel  = {X_inel:.2f} cm"
)

ax4.text(0.5, 0.25, txt4,
         fontsize=11, family='monospace',
         ha='center', va='center', transform=ax4.transAxes,
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2))

# ============================================================================
# PANEL (e): GRÁFICA DE BARRAS HAZUZ
# ============================================================================

ax5 = fig.add_axes([0.04, 0.05, 0.92, 0.28])
ax5.set_facecolor(COLORES['fondo_panel'])

# Datos
tipos = ["PLATINUM", "GOLD", "SILVER", "COMPLETO"]
derivas = [0.0033, 0.0058, 0.0156, 0.0400]
colores_barras = [COLORES['platinum'], COLORES['gold'],
                  COLORES['silver'], COLORES['completo']]

# Barras
x_pos = np.arange(len(tipos))
bars = ax5.bar(x_pos, derivas, color=colores_barras,
               edgecolor='#333333', linewidth=2, width=0.6, alpha=0.85)

# Etiquetas
for bar, val in zip(bars, derivas):
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
             f'{val:.4f}', ha='center', va='bottom',
             fontweight='bold', fontsize=11, color=COLORES['titulo'])

# Línea del proyecto
ax5.axhline(y=der, color=COLORES['critica'], linestyle='-',
            linewidth=3, label=f'Proyecto: der = {der:.5f}')
ax5.axhline(y=0.02, color=COLORES['advertencia'], linestyle='--',
            linewidth=2.5, label='Límite NEC-15 = 0.0200')

# Anotación del proyecto
ax5.annotate(f'PROYECTO\n{tipo}',
             xy=(1, der),
             xytext=(1.5, der + 0.015),
             fontsize=13, fontweight='bold',
             color=color_tipo,
             arrowprops=dict(arrowstyle='->',
                             color=color_tipo, lw=3),
             bbox=dict(boxstyle='round,pad=0.4',
                       facecolor='white',
                       edgecolor=color_tipo,
                       linewidth=2.5),
             zorder=15)

ax5.set_xticks(x_pos)
ax5.set_xticklabels(tipos, fontsize=12, fontweight='bold')
ax5.set_ylabel('Deriva de entrepiso', fontsize=13, fontweight='bold')
ax5.set_title('(e) CLASIFICACIÓN HAZUZ — PROYECTO UBICADO',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax5.legend(fontsize=11, loc='upper right')
ax5.grid(True, axis='y', linestyle='--', alpha=0.4)
ax5.set_ylim(0, 0.05)

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

fig.text(0.5, 0.02,
         '"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."',
         ha='center', va='bottom', fontsize=10,
         color=COLORES['subtitulo'], style='italic',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white',
                   edgecolor=COLORES['acento'],
                   linewidth=1.5))

fig.text(0.5, 0.005,
         f'{PROYECTO} · {datetime.now().strftime("%Y-%m-%d %H:%M")}',
         ha='center', va='bottom', fontsize=8,
         color=COLORES['linea'])

# ============================================================================
# 5. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_39"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_39_clasificacion_hazuz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 6. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.39 — CLASIFICACIÓN HAZUZ 1999")
print("=" * 80)
print(f"\n  DATOS DEL PROYECTO:")
print(f"    He       = {He:.2f} m")
print(f"    X inel   = {X_inel:.2f} cm")
print(f"    der      = {der:.5f}")
print(f"\n  CLASIFICACIÓN:")
print(f"    tipo     = {tipo}")
print(f"    der obj  = {der_obj:.4f}")
print(f"    X obj    = {X_obj:.2f} cm")
print(f"\n  TABLA HAZUZ:")
print(f"    {'Tipo':<12} {'Deriva':<10} {'Rango':<20}")
print(f"    {'-'*45}")
for tipo_row, der_row, rango, desc, color in tabla_hazuz:
    marca = " ← PROYECTO" if tipo_row == tipo else ""
    print(f"    {tipo_row:<12} {der_row:<10.4f} {rango:<20}{marca}")
print("=" * 80)