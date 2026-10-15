# -*- coding: utf-8 -*-
"""
================================================================================
M07.48 — DISEÑO DEL AMORTIGUADOR DE FLUIDO VISCOSO (FVD)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.48 — Diseño del Amortiguador

OBJETIVO: Generar ficha técnica visual del amortiguador de fluido
          viscoso requerido para el proyecto.

CARACTERÍSTICAS:
    - Fuerza: 231.02 t (2,270 kN)
    - C = 2.378 t·s/m
    - β_V = 10%
    - Carrera: ±150 mm
    - Dimensiones: 460 mm × 2,500 mm

TABLAS DE REFERENCIA:
    - Yokogawa Bridge
    - Taylor Devices
    - ASCE 7-16 (Cap. 18)
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon
from matplotlib.gridspec import GridSpec

# ============================================================================
# PALETA
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
    'acero': '#495057',
    'acero_oscuro': '#212529',
    'aceite': '#f39c12',
    'aceite_bg': '#fdebd0',
    'piston': '#7f8c8d',
    'sello': '#e74c3c',
    'box_datos': '#ffffff',
    'box_datos_borde': '#0d1b2a',
    'box_resultado': '#d8f3dc',
    'box_resultado_borde': '#2d6a4f',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Datos del amortiguador
C_total = 2.378     # t·s/m
F_max = 231.02      # t
beta_V = 0.10       # 10%
alpha = 0.40        # exponente de velocidad

# Dimensiones (referenciales)
D_exterior = 460    # mm
L_total = 2500      # mm
stroke = 150        # mm (±)
D_piston = 150      # mm
D_vastago = 80      # mm

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(28, 22))
fig.patch.set_facecolor(COLORES['fondo'])

# Encabezado
ax_header = fig.add_axes([0, 0.95, 1, 0.05])
ax_header.set_facecolor(COLORES['titulo'])
ax_header.axis('off')
ax_header.text(0.02, 0.5, '🏗️', fontsize=28, va='center')
ax_header.text(0.05, 0.5, 'UNESUM · REZ-2026 · JIPIJAPA-001',
               fontsize=15, fontweight='bold', color='white', va='center')
ax_header.text(0.98, 0.5, 'M07.48 — DISEÑO DEL AMORTIGUADOR',
               fontsize=15, fontweight='bold', color=COLORES['acento'],
               va='center', ha='right')

fig.text(0.5, 0.925,
         'FICHA TÉCNICA — AMORTIGUADOR DE FLUIDO VISCOSO (FVD)',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.905,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=11,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# PANEL (a): ESQUEMA DEL AMORTIGUADOR (vista lateral - sección)
# ============================================================================

ax1 = fig.add_axes([0.04, 0.48, 0.44, 0.38])
ax1.set_facecolor('#ffffff')
ax1.set_xlim(-100, L_total + 300)
ax1.set_ylim(-D_exterior*0.9, D_exterior*0.9)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('(a) ESQUEMA DEL AMORTIGUADOR (CORTE LATERAL)',
              fontsize=13, fontweight='bold', color=COLORES['titulo'], pad=10)

# --- CILINDRO PRINCIPAL ---
cilindro = Rectangle((0, -D_exterior/2), L_total, D_exterior,
                      facecolor=COLORES['acero'], edgecolor=COLORES['acero_oscuro'],
                      linewidth=3, alpha=0.7, zorder=2)
ax1.add_patch(cilindro)

# --- ACEITE HIDRÁULICO ---
aceite = Rectangle((50, -D_exterior/2 + 20), L_total - 100, D_exterior - 40,
                    facecolor=COLORES['aceite'], edgecolor='#b9770e',
                    linewidth=2, alpha=0.6, zorder=3)
ax1.add_patch(aceite)

# Etiqueta aceite
ax1.text(L_total/2, 0, 'ACEITE\nHIDRÁULICO', ha='center', va='center',
         fontsize=11, fontweight='bold', color='#7e5109', zorder=5)

# --- PISTÓN ---
piston = Rectangle((L_total*0.45, -D_exterior/2 + 40), 80, D_exterior - 80,
                    facecolor=COLORES['piston'], edgecolor='#2c3e50',
                    linewidth=2.5, zorder=4)
ax1.add_patch(piston)

# --- VÁSTAGO (a la derecha) ---
vastago = Rectangle((L_total*0.45 + 80, -D_vastago/2), 200, D_vastago,
                     facecolor=COLORES['piston'], edgecolor='#2c3e50',
                     linewidth=2.5, zorder=4)
ax1.add_patch(vastago)

# --- VÁSTAGO (a la izquierda) ---
vastago_izq = Rectangle((L_total*0.45 - 200, -D_vastago/2), 200, D_vastago,
                         facecolor=COLORES['piston'], edgecolor='#2c3e50',
                         linewidth=2.5, zorder=4)
ax1.add_patch(vastago_izq)

# --- ORIFICIOS (válvula) ---
for i in range(3):
    y_orif = -40 + i * 40
    orificio = Rectangle((L_total*0.45 + 20, y_orif), 15, 20,
                          facecolor='white', edgecolor=COLORES['sello'],
                          linewidth=1.5, zorder=5)
    ax1.add_patch(orificio)

# --- SELLOS ---
# Sello izquierdo
sello_izq = Rectangle((-20, -D_exterior/2 - 10), 40, D_exterior + 20,
                       facecolor=COLORES['sello'], edgecolor='#922b21',
                       linewidth=2, zorder=5)
ax1.add_patch(sello_izq)

# Sello derecho
sello_der = Rectangle((L_total - 20, -D_exterior/2 - 10), 40, D_exterior + 20,
                       facecolor=COLORES['sello'], edgecolor='#922b21',
                       linewidth=2, zorder=5)
ax1.add_patch(sello_der)

# --- CONEXIONES (extremos) ---
# Conexión izquierda
conexion_izq = Circle((-80, 0), 40, facecolor=COLORES['acero_oscuro'],
                       edgecolor='black', linewidth=2, zorder=6)
ax1.add_patch(conexion_izq)

# Conexión derecha
conexion_der = Circle((L_total + 80, 0), 40, facecolor=COLORES['acero_oscuro'],
                       edgecolor='black', linewidth=2, zorder=6)
ax1.add_patch(conexion_der)

# --- FLECHAS DE MOVIMIENTO ---
# Flecha izquierda
ax1.annotate('', xy=(-150, D_exterior*0.7), xytext=(-80, D_exterior*0.7),
             arrowprops=dict(arrowstyle='->', color=COLORES['critica'],
                             lw=3, mutation_scale=20))
ax1.text(-180, D_exterior*0.7, 'F', fontsize=14, fontweight='bold',
         color=COLORES['critica'], ha='center')

# Flecha derecha
ax1.annotate('', xy=(L_total + 150, D_exterior*0.7),
             xytext=(L_total + 80, D_exterior*0.7),
             arrowprops=dict(arrowstyle='->', color=COLORES['critica'],
                             lw=3, mutation_scale=20))
ax1.text(L_total + 180, D_exterior*0.7, 'F', fontsize=14, fontweight='bold',
         color=COLORES['critica'], ha='center')

# --- ETIQUETAS ---
# D_exterior
ax1.annotate('', xy=(-30, -D_exterior/2), xytext=(-30, D_exterior/2),
             arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax1.text(-60, 0, f'D = {D_exterior} mm', fontsize=10, fontweight='bold',
         rotation=90, va='center', ha='center')

# L_total
ax1.annotate('', xy=(0, -D_exterior*0.8), xytext=(L_total, -D_exterior*0.8),
             arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax1.text(L_total/2, -D_exterior*0.85, f'L = {L_total} mm',
         fontsize=10, fontweight='bold', ha='center', va='top')

# Stroke
ax1.annotate('', xy=(L_total + 150, -D_exterior*0.5),
             xytext=(L_total + 150, -D_exterior*0.5 + stroke*2),
             arrowprops=dict(arrowstyle='<->', color=COLORES['info'], lw=2))
ax1.text(L_total + 170, -D_exterior*0.5 + stroke,
         f'Stroke\n±{stroke} mm', fontsize=9, fontweight='bold',
         color=COLORES['info'], va='center')

# ============================================================================
# PANEL (b): VISTA FRONTAL
# ============================================================================

ax2 = fig.add_axes([0.52, 0.68, 0.20, 0.18])
ax2.set_facecolor('#ffffff')
ax2.set_xlim(-D_exterior*0.6, D_exterior*0.6)
ax2.set_ylim(-D_exterior*0.6, D_exterior*0.6)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('(b) VISTA FRONTAL',
              fontsize=12, fontweight='bold', color=COLORES['titulo'], pad=10)

# Círculo exterior
circulo_ext = Circle((0, 0), D_exterior/2, facecolor=COLORES['acero'],
                     edgecolor=COLORES['acero_oscuro'], linewidth=3, alpha=0.7)
ax2.add_patch(circulo_ext)

# Círculo del pistón
circulo_piston = Circle((0, 0), D_piston/2, facecolor=COLORES['piston'],
                        edgecolor='#2c3e50', linewidth=2)
ax2.add_patch(circulo_piston)

# Círculo del vástago
circulo_vastago = Circle((0, 0), D_vastago/2, facecolor=COLORES['aceite'],
                         edgecolor='#b9770e', linewidth=2)
ax2.add_patch(circulo_vastago)

# Orificios
for angle in [0, 90, 180, 270]:
    rad = np.radians(angle)
    x_orif = (D_piston/2 - 15) * np.cos(rad)
    y_orif = (D_piston/2 - 15) * np.sin(rad)
    orificio = Circle((x_orif, y_orif), 8, facecolor='white',
                      edgecolor=COLORES['sello'], linewidth=1.5)
    ax2.add_patch(orificio)

# Etiquetas
ax2.text(0, D_exterior/2 + 15, f'D = {D_exterior} mm',
         fontsize=9, fontweight='bold', ha='center')
ax2.text(0, -D_piston/2 - 10, f'Pistón: {D_piston} mm',
         fontsize=8, color=COLORES['piston'], ha='center')
ax2.text(0, -D_vastago/2 - 10, f'Vástago: {D_vastago} mm',
         fontsize=7, color=COLORES['aceite'], ha='center')

# ============================================================================
# PANEL (c): CARACTERÍSTICAS TÉCNICAS
# ============================================================================

ax3 = fig.add_axes([0.76, 0.68, 0.20, 0.18])
ax3.set_facecolor('#ffffff')
ax3.axis('off')
ax3.set_title('(c) CARACTERÍSTICAS',
              fontsize=12, fontweight='bold', color=COLORES['titulo'], pad=10)

txt3 = (
    "CARACTERÍSTICAS\n"
    "═══════════════════════════\n\n"
    f"  Fuerza (F)      = {F_max:.2f} t\n"
    f"  C               = {C_total:.4f} t·s/m\n"
    f"  β_V             = {beta_V*100:.1f}%\n"
    f"  α               = {alpha:.2f}\n"
    f"  Stroke          = ±{stroke} mm\n\n"
    f"  D_exterior      = {D_exterior} mm\n"
    f"  L_total         = {L_total} mm\n"
    f"  D_pistón        = {D_piston} mm\n"
    f"  D_vástago       = {D_vastago} mm"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.5',
                   facecolor=COLORES['info_bg'],
                   edgecolor=COLORES['info'],
                   linewidth=2, alpha=0.95))

# ============================================================================
# PANEL (d): DESPIECE (EXPLODED VIEW)
# ============================================================================

ax4 = fig.add_axes([0.04, 0.05, 0.92, 0.38])
ax4.set_facecolor('#ffffff')
ax4.set_xlim(-100, L_total + 500)
ax4.set_ylim(-400, 400)
ax4.set_aspect('equal')
ax4.axis('off')
ax4.set_title('(d) DESPIECE DEL AMORTIGUADOR — COMPONENTES',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=10)

# --- 1. CILINDRO ---
cil = Rectangle((0, 100), L_total, D_exterior,
                 facecolor=COLORES['acero'], edgecolor=COLORES['acero_oscuro'],
                 linewidth=3, alpha=0.7)
ax4.add_patch(cil)
ax4.text(L_total/2, 100 + D_exterior/2, '1. CILINDRO',
         ha='center', va='center', fontsize=11, fontweight='bold',
         color='white', zorder=5)

# --- 2. ACEITE ---
ace = Rectangle((50, 100 + 20), L_total - 100, D_exterior - 40,
                 facecolor=COLORES['aceite'], edgecolor='#b9770e',
                 linewidth=2, alpha=0.6)
ax4.add_patch(ace)
ax4.text(L_total/2, 100 + D_exterior/2, '2. ACEITE',
         ha='center', va='center', fontsize=10, fontweight='bold',
         color='#7e5109', zorder=6)

# --- 3. PISTÓN ---
pis = Rectangle((L_total*0.45, 100 + 40), 80, D_exterior - 80,
                 facecolor=COLORES['piston'], edgecolor='#2c3e50',
                 linewidth=2.5)
ax4.add_patch(pis)

# --- 4. VÁSTAGO ---
vas = Rectangle((L_total*0.45 + 80, 100 + D_exterior/2 - D_vastago/2),
                 250, D_vastago,
                 facecolor=COLORES['piston'], edgecolor='#2c3e50',
                 linewidth=2.5)
ax4.add_patch(vas)

# --- 5. SELLOS ---
sello1 = Rectangle((-20, 100 - 10), 40, D_exterior + 20,
                    facecolor=COLORES['sello'], edgecolor='#922b21',
                    linewidth=2)
ax4.add_patch(sello1)

sello2 = Rectangle((L_total - 20, 100 - 10), 40, D_exterior + 20,
                    facecolor=COLORES['sello'], edgecolor='#922b21',
                    linewidth=2)
ax4.add_patch(sello2)

# --- CONEXIONES ---
con1 = Circle((-80, 100 + D_exterior/2), 40,
               facecolor=COLORES['acero_oscuro'], edgecolor='black', linewidth=2)
ax4.add_patch(con1)

con2 = Circle((L_total + 80, 100 + D_exterior/2), 40,
               facecolor=COLORES['acero_oscuro'], edgecolor='black', linewidth=2)
ax4.add_patch(con2)

# --- ETIQUETAS DE COMPONENTES ---
componentes = [
    (L_total/2, 100 + D_exterior + 50, '3. ORIFICIOS', COLORES['sello']),
    (L_total*0.45, 50, '4. PISTÓN', COLORES['piston']),
    (L_total*0.45 + 200, 30, '5. VÁSTAGO', COLORES['piston']),
    (-80, 50, '6. CONEXIÓN', COLORES['acero_oscuro']),
    (L_total - 20, 50, '7. SELLO', COLORES['sello']),
]

for x, y, texto, color in componentes:
    ax4.text(x, y, texto, ha='center', va='top',
             fontsize=10, fontweight='bold', color=color,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=color, linewidth=1.5))

# --- TÍTULO DE LA SECCIÓN ---
ax4.text(-100, 380, 'COMPONENTES DEL AMORTIGUADOR DE FLUIDO VISCOSO',
         ha='left', va='top', fontsize=12, fontweight='bold',
         color=COLORES['titulo'])

# ============================================================================
# PIE DE PÁGINA
# ============================================================================

fig.text(0.5, 0.015,
         '"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."',
         ha='center', va='bottom', fontsize=10,
         color=COLORES['subtitulo'], style='italic',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white',
                   edgecolor=COLORES['acento'],
                   linewidth=1.5))

fig.text(0.5, 0.002,
         f'{PROYECTO} · {datetime.now().strftime("%Y-%m-%d %H:%M")}',
         ha='center', va='bottom', fontsize=8,
         color=COLORES['linea'])

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_48"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_48_amortiguador_esquema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.48 — DISEÑO DEL AMORTIGUADOR DE FLUIDO VISCOSO")
print("=" * 80)
print(f"\n  CARACTERÍSTICAS TÉCNICAS:")
print(f"    Fuerza (F)      = {F_max:.2f} t")
print(f"    C               = {C_total:.4f} t·s/m")
print(f"    β_V             = {beta_V*100:.1f}%")
print(f"    α               = {alpha:.2f}")
print(f"    Stroke          = ±{stroke} mm")
print(f"\n  DIMENSIONES:")
print(f"    D_exterior      = {D_exterior} mm")
print(f"    L_total         = {L_total} mm")
print(f"    D_pistón        = {D_piston} mm")
print(f"    D_vástago       = {D_vastago} mm")
print(f"\n  COMPONENTES:")
print(f"    1. Cilindro")
print(f"    2. Aceite hidráulico")
print(f"    3. Orificios (válvula)")
print(f"    4. Pistón")
print(f"    5. Vástago")
print(f"    6. Conexiones")
print(f"    7. Sellos")
print("=" * 80)