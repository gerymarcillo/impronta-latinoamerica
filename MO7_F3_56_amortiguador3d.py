# -*- coding: utf-8 -*-
"""
================================================================================
M07.49 — AMORTIGUADOR DE FLUIDO VISCOSO EN 3D
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.49 — Amortiguador 3D

OBJETIVO: Visualización 3D del amortiguador de fluido viscoso (FVD)
          con sus componentes y dimensiones.

CARACTERÍSTICAS:
    - Fuerza: 231.02 t
    - C = 2.378 t·s/m
    - β_V = 10%
    - Stroke: ±150 mm
    - Dimensiones: 460 mm × 2,500 mm
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch

# ============================================================================
# PALETA
# ============================================================================

COLORES = {
    'fondo': '#f8f9fa',
    'titulo': '#0d1b2a',
    'subtitulo': '#415a77',
    'acero': '#495057',
    'acero_oscuro': '#212529',
    'acero_claro': '#6c757d',
    'aceite': '#f39c12',
    'piston': '#7f8c8d',
    'sello': '#e74c3c',
    'conexion': '#2c3e50',
    'ok': '#2d6a4f',
    'info': '#1d3557',
    'acento': '#f77f00',
}

# ============================================================================
# 1. DATOS DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
AUTOR = "Ing. Gery Lorenzo Marcillo Merino, Msc."

# Datos
C_total = 2.378     # t·s/m
F_max = 231.02      # t
beta_V = 0.10       # 10%

# Dimensiones (en mm, escala a metros para 3D)
D_ext = 460 / 1000      # 0.460 m
L_total = 2500 / 1000   # 2.500 m
stroke = 150 / 1000     # 0.150 m
D_piston = 150 / 1000   # 0.150 m
D_vastago = 80 / 1000   # 0.080 m

# ============================================================================
# 2. FIGURA 3D
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.97,
         'M07.49 — AMORTIGUADOR DE FLUIDO VISCOSO EN 3D',
         ha='center', va='top', fontsize=22, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.945,
         f'{AUTOR} · {PROYECTO}',
         ha='center', va='top', fontsize=12,
         color=COLORES['subtitulo'], style='italic')

# ============================================================================
# EJE 3D
# ============================================================================

ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#ffffff')

# ============================================================================
# FUNCIONES PARA DIBUJAR CILINDROS Y TUBOS
# ============================================================================

def dibujar_cilindro(ax, x_centro, y_centro, z_centro, radio, longitud,
                     eje='x', color='#495057', alpha=0.8, linewidth=0.5,
                     n_theta=40, n_z=20):
    """
    Dibuja un cilindro 3D.
    """
    theta = np.linspace(0, 2*np.pi, n_theta)
    z = np.linspace(-longitud/2, longitud/2, n_z)
    theta_grid, z_grid = np.meshgrid(theta, z)
    
    if eje == 'x':
        X = x_centro + z_grid
        Y = y_centro + radio * np.cos(theta_grid)
        Z = z_centro + radio * np.sin(theta_grid)
    elif eje == 'y':
        X = x_centro + radio * np.cos(theta_grid)
        Y = y_centro + z_grid
        Z = z_centro + radio * np.sin(theta_grid)
    else:  # z
        X = x_centro + radio * np.cos(theta_grid)
        Y = y_centro + radio * np.sin(theta_grid)
        Z = z_centro + z_grid
    
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha,
                    linewidth=linewidth, edgecolor='none', shade=True)


def dibujar_tapa_cilindro(ax, x_centro, y_centro, z_centro, radio,
                          eje='x', color='#495057', alpha=0.9, lado='+'):
    """Dibuja una tapa plana de cilindro."""
    theta = np.linspace(0, 2*np.pi, 50)
    r = np.linspace(0, radio, 20)
    theta_grid, r_grid = np.meshgrid(theta, r)
    
    if eje == 'x':
        X = x_centro + np.zeros_like(r_grid)
        Y = y_centro + r_grid * np.cos(theta_grid)
        Z = z_centro + r_grid * np.sin(theta_grid)
    elif eje == 'y':
        X = x_centro + r_grid * np.cos(theta_grid)
        Y = y_centro + np.zeros_like(r_grid)
        Z = z_centro + r_grid * np.sin(theta_grid)
    else:
        X = x_centro + r_grid * np.cos(theta_grid)
        Y = y_centro + r_grid * np.sin(theta_grid)
        Z = z_centro + np.zeros_like(r_grid)
    
    ax.plot_surface(X, Y, Z, color=color, alpha=alpha, linewidth=0)


# ============================================================================
# 3. DIBUJAR EL AMORTIGUADOR
# ============================================================================

# --- CILINDRO PRINCIPAL ---
dibujar_cilindro(ax, 0, 0, 0, D_ext/2, L_total,
                 eje='x', color=COLORES['acero'], alpha=0.85)

# --- TAPAS DEL CILINDRO ---
dibujar_tapa_cilindro(ax, -L_total/2, 0, 0, D_ext/2,
                      eje='x', color=COLORES['acero_oscuro'], alpha=0.95)
dibujar_tapa_cilindro(ax, L_total/2, 0, 0, D_ext/2,
                      eje='x', color=COLORES['acero_oscuro'], alpha=0.95)

# --- ACEITE HIDRÁULICO (cilindro interior) ---
dibujar_cilindro(ax, 0, 0, 0, D_ext/2 - 0.02, L_total - 0.1,
                 eje='x', color=COLORES['aceite'], alpha=0.4)

# --- PISTÓN ---
dibujar_cilindro(ax, 0, 0, 0, D_piston/2, 0.08,
                 eje='x', color=COLORES['piston'], alpha=0.95)

# --- VÁSTAGO (derecha) ---
dibujar_cilindro(ax, L_total/2 + 0.15, 0, 0, D_vastago/2, 0.30,
                 eje='x', color=COLORES['piston'], alpha=0.95)

# --- VÁSTAGO (izquierda) ---
dibujar_cilindro(ax, -L_total/2 - 0.15, 0, 0, D_vastago/2, 0.30,
                 eje='x', color=COLORES['piston'], alpha=0.95)

# --- SELLOS ---
dibujar_cilindro(ax, -L_total/2, 0, 0, D_ext/2 + 0.01, 0.04,
                 eje='x', color=COLORES['sello'], alpha=0.9)
dibujar_cilindro(ax, L_total/2, 0, 0, D_ext/2 + 0.01, 0.04,
                 eje='x', color=COLORES['sello'], alpha=0.9)

# --- CONEXIONES (esferas) ---
u = np.linspace(0, 2*np.pi, 30)
v = np.linspace(0, np.pi, 30)
u, v = np.meshgrid(u, v)

# Conexión izquierda
x_izq = -L_total/2 - 0.35
X_izq = x_izq + 0.08 * np.cos(u) * np.sin(v)
Y_izq = 0.08 * np.sin(u) * np.sin(v)
Z_izq = 0.08 * np.cos(v)
ax.plot_surface(X_izq, Y_izq, Z_izq, color=COLORES['conexion'],
                alpha=0.95, linewidth=0)

# Conexión derecha
x_der = L_total/2 + 0.35
X_der = x_der + 0.08 * np.cos(u) * np.sin(v)
Y_der = 0.08 * np.sin(u) * np.sin(v)
Z_der = 0.08 * np.cos(v)
ax.plot_surface(X_der, Y_der, Z_der, color=COLORES['conexion'],
                alpha=0.95, linewidth=0)

# ============================================================================
# 4. FLECHAS DE MOVIMIENTO
# ============================================================================

# Flecha izquierda
ax.quiver(-L_total/2 - 0.55, 0, 0, -0.15, 0, 0,
          color=COLORES['sello'], arrow_length_ratio=0.3, linewidth=3)

# Flecha derecha
ax.quiver(L_total/2 + 0.55, 0, 0, 0.15, 0, 0,
          color=COLORES['sello'], arrow_length_ratio=0.3, linewidth=3)

# Etiquetas F
ax.text(-L_total/2 - 0.75, 0.1, 0, 'F', fontsize=16, fontweight='bold',
        color=COLORES['sello'])
ax.text(L_total/2 + 0.65, 0.1, 0, 'F', fontsize=16, fontweight='bold',
        color=COLORES['sello'])

# ============================================================================
# 5. COTAS Y DIMENSIONES
# ============================================================================

# Cota L_total
ax.plot([-L_total/2, L_total/2], [-D_ext/2 - 0.15, -D_ext/2 - 0.15], [0, 0],
        'k-', linewidth=1.5)
ax.plot([-L_total/2, -L_total/2], [-D_ext/2 - 0.15, -D_ext/2 - 0.10], [0, 0],
        'k-', linewidth=1.5)
ax.plot([L_total/2, L_total/2], [-D_ext/2 - 0.15, -D_ext/2 - 0.10], [0, 0],
        'k-', linewidth=1.5)
ax.text(0, -D_ext/2 - 0.25, 0, f'L = {L_total*1000:.0f} mm',
        fontsize=11, fontweight='bold', ha='center', color='black')

# Cota D_ext
ax.plot([-L_total/2 - 0.15, -L_total/2 - 0.15], [-D_ext/2, D_ext/2], [0, 0],
        'k-', linewidth=1.5)
ax.plot([-L_total/2 - 0.20, -L_total/2 - 0.15], [-D_ext/2, -D_ext/2], [0, 0],
        'k-', linewidth=1.5)
ax.plot([-L_total/2 - 0.20, -L_total/2 - 0.15], [D_ext/2, D_ext/2], [0, 0],
        'k-', linewidth=1.5)
ax.text(-L_total/2 - 0.35, 0, 0, f'D = {D_ext*1000:.0f} mm',
        fontsize=11, fontweight='bold', ha='center', color='black',
        rotation=90)

# ============================================================================
# 6. CONFIGURACIÓN DE EJES 3D
# ============================================================================

ax.set_xlim(-L_total/2 - 1.0, L_total/2 + 1.0)
ax.set_ylim(-D_ext, D_ext)
ax.set_zlim(-D_ext, D_ext)

ax.set_xlabel('Longitud X (m)', fontsize=11, fontweight='bold')
ax.set_ylabel('Y (m)', fontsize=11, fontweight='bold')
ax.set_zlabel('Z (m)', fontsize=11, fontweight='bold')

ax.set_box_aspect([L_total + 2, 2*D_ext, 2*D_ext])

ax.view_init(elev=20, azim=-45)

# Grid
ax.grid(True, linestyle='--', alpha=0.3)

# Título
ax.set_title('VISTA 3D DEL AMORTIGUADOR DE FLUIDO VISCOSO',
             fontsize=15, fontweight='bold', color=COLORES['titulo'], pad=20)

# ============================================================================
# 7. CUADRO DE CARACTERÍSTICAS
# ============================================================================

txt_caract = (
    "CARACTERÍSTICAS TÉCNICAS\n"
    "═══════════════════════════════\n"
    f"  Fuerza (F)      = {F_max:.2f} t\n"
    f"  C               = {C_total:.4f} t·s/m\n"
    f"  β_V             = {beta_V*100:.1f} %\n"
    "  α               = 0.40\n"
    f"  Stroke          = ±{stroke*1000:.0f} mm\n\n"
    f"  D_exterior      = {D_ext*1000:.0f} mm\n"
    f"  L_total         = {L_total*1000:.0f} mm\n"
    f"  D_pistón        = {D_piston*1000:.0f} mm\n"
    f"  D_vástago       = {D_vastago*1000:.0f} mm\n\n"
    "COMPONENTES:\n"
    "  1. Cilindro\n"
    "  2. Aceite hidráulico\n"
    "  3. Pistón\n"
    "  4. Vástago\n"
    "  5. Sellos\n"
    "  6. Conexiones"
)

fig.text(0.02, 0.15, txt_caract,
         transform=fig.transFigure,
         fontsize=9, family='monospace',
         ha='left', va='bottom',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor='#d6e4f0',
                   edgecolor=COLORES['info'],
                   linewidth=2))

# ============================================================================
# 8. PIE DE PÁGINA
# ============================================================================

fig.text(0.5, 0.02,
         '"Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."',
         ha='center', va='bottom', fontsize=10,
         color=COLORES['subtitulo'], style='italic',
         bbox=dict(boxstyle='round,pad=0.3',
                   facecolor='white',
                   edgecolor=COLORES['acento'],
                   linewidth=1.5))

# ============================================================================
# 9. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_49"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_49_amortiguador_3D_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=200, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 10. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.49 — AMORTIGUADOR DE FLUIDO VISCOSO EN 3D")
print("=" * 80)
print(f"\n  CARACTERÍSTICAS TÉCNICAS:")
print(f"    Fuerza (F)      = {F_max:.2f} t")
print(f"    C               = {C_total:.4f} t·s/m")
print(f"    β_V             = {beta_V*100:.1f} %")
print(f"    α               = 0.40")
print(f"    Stroke          = ±{stroke*1000:.0f} mm")
print(f"\n  DIMENSIONES:")
print(f"    D_exterior      = {D_ext*1000:.0f} mm")
print(f"    L_total         = {L_total*1000:.0f} mm")
print(f"    D_pistón        = {D_piston*1000:.0f} mm")
print(f"    D_vástago       = {D_vastago*1000:.0f} mm")
print("=" * 80)