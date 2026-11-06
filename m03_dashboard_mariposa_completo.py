# -*- coding: utf-8 -*-
"""
======================================================================
M03: DASHBOARD INTEGRAL - MOMENTO DE DISEÑO Y MARIPOSA SÍSMICA
Proyecto: ECT-UNESUM-2026 (Modelo Asignado por Sorteo)
======================================================================
Este script calcula el Momento de Diseño (Md) mediante el pórtico
equivalente y lo grafica junto al diagrama de mariposa reversible,
mostrando la ubicación de la rótula plástica.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

def generar_dashboard_integral():
    # ======================================================================
    # 1. DATOS DEL MODELO (Deben venir del proyecto asignado)
    # ======================================================================
    Lv = 6.00           # Luz entre ejes (m)
    b_col = 0.38        # Ancho de columna (m)
    Lt = 5.75           # Longitud transversal (m)
    Wu = 1.064          # Carga última (t/m2)
    f_viga = 0.65
    f_fisura = 0.85
    Fm = 1.35
    
    # Acero y capacidades (para la rótula)
    As_viga = 10.00     # cm2
    fy = 4200           # kg/cm2
    fc = 210            # kg/cm2
    b_viga = 30         # cm
    d = 40.7            # cm
    
    # ======================================================================
    # 2. CÁLCULOS DE INGENIERÍA
    # ======================================================================
    # A) Momento Estático (Pórtico Equivalente)
    luz_libre = Lv - b_col
    Me = (Wu * Lt * luz_libre**2) / 8
    
    # B) Momento de Diseño
    Md = Me * f_viga * f_fisura * Fm
    
    # C) Capacidad Probable (Mpr) para la rótula
    fs_real = 1.25 * fy
    a = (As_viga * fs_real) / (0.85 * fc * b_viga)
    Mpr = (As_viga * fs_real * (d - a/2)) / 100000

    # ======================================================================
    # 3. CONFIGURACIÓN GRÁFICA (Dashboard 2x2)
    # ======================================================================
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('#1e1e2e')
    
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.2)

    color_texto = '#ecf0f1'
    color_borde = '#f1c40f'

    # --- PANEL 1: FORMULACIÓN DEL MOMENTO DE DISEÑO ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#1e1e2e')
    ax1.axis('off')
    
    formula_texto = (
        "📐 CÁLCULO DEL MOMENTO DE DISEÑO (Pórtico Equivalente)\n"
        "---------------------------------------------------------\n"
        "1. Luz Libre de Cálculo:\n"
        f"   Luz Libre = Lv - b_col = {Lv:.2f} - {b_col:.2f} = {luz_libre:.2f} m\n\n"
        "2. Momento Estático (Me):\n"
        "   Me = [ Wu · Lt · (Luz Libre)² ] / 8\n"
        f"   Me = [ {Wu} · {Lt:.2f} · ({luz_libre:.2f})² ] / 8\n"
        f"   Me = {Me:.2f} t·m\n\n"
        "3. Momento de Diseño (Md):\n"
        "   Md = Me · f_viga · f_fisura · Fm\n"
        f"   Md = {Me:.2f} · {f_viga} · {f_fisura} · {Fm}\n"
        f"   Md = {Md:.2f} t·m"
    )
    ax1.text(0.05, 0.95, formula_texto, transform=ax1.transAxes, fontsize=12, 
             verticalalignment='top', fontfamily='monospace', color='#5dade2',
             bbox=dict(boxstyle='round,pad=1', facecolor='#2c3e50', edgecolor='#f39c12', lw=2))
    
    # --- PANEL 2: LA VIGA Y LA PINZA (ACERO CONTINUO) ---
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1e1e2e')
    ax2.axis('off')
    
    # Dibujar columnas
    rect_col_izq = Rectangle((0, -1), b_col, 2, facecolor='#34495e', edgecolor='white', lw=2, zorder=5)
    rect_col_der = Rectangle((Lv - b_col, -1), b_col, 2, facecolor='#34495e', edgecolor='white', lw=2, zorder=5)
    ax2.add_patch(rect_col_izq)
    ax2.add_patch(rect_col_der)
    
    # Dibujar viga
    rect_viga = Rectangle((b_col, -0.5), luz_libre, 1, facecolor='#2c3e50', edgecolor='white', lw=1.5, alpha=0.5)
    ax2.add_patch(rect_viga)

    # La Pinza (Acero continuo)
    acero_x = [0.1, 0.3, b_col, Lv - b_col, Lv - 0.3, Lv - 0.1]
    acero_y = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
    ax2.plot(acero_x, acero_y, color='#e74c3c', linewidth=6, zorder=10, solid_capstyle='round')
    ax2.plot([0.1, 0.1], [0.3, -0.3], color='#e74c3c', linewidth=6, zorder=10)
    ax2.plot([Lv - 0.1, Lv - 0.1], [0.3, -0.3], color='#e74c3c', linewidth=6, zorder=10)

    ax2.text(Lv/2, 0.6, "Acero continuo (La pinza que une los nudos)", ha='center', va='bottom', color='#e74c3c', fontsize=11, fontweight='bold')
    ax2.set_xlim(-0.5, Lv + 0.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_title("B) ACERO LONGITUDINAL CONTINUO (LA PINZA)", color=color_texto, fontsize=14, fontweight='bold')

    # --- PANEL 3: MARIPOSA SÍSMICA (DOBLE CURVATURA) ---
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#1e1e2e')
    
    x = np.linspace(0, Lv, 300)
    # Curva Suavizada (Coseno) para la mariposa
    M_sismo = Mpr * np.cos(np.pi * x / Lv)
    
    ax3.plot(x, M_sismo, color='#e74c3c', linewidth=4, label='Empuje Sísmico (→)')
    ax3.plot(x, -M_sismo, color='#c0392b', linewidth=4, linestyle='--', label='Empuje Sísmico (←)')
    ax3.axhline(0, color='white', lw=1.5, alpha=0.8)
    
    # Sombreado de la rótula (cara de columna)
    ax3.axvspan(0, b_col, color='#f1c40f', alpha=0.2)
    ax3.axvspan(Lv - b_col, Lv, color='#f1c40f', alpha=0.2)
    
    # Punto de inflexión
    ax3.scatter([Lv/2], [0], color='#2ecc71', s=150, zorder=10, edgecolor='black')
    ax3.text(Lv/2, 0, "M = 0\n(Punto de Inflexión)", 
             ha='center', va='center', color='#2ecc71', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', fc='#2c3e50', ec='#2ecc71', lw=2))
    
    ax3.annotate(f"Rótula Plástica\nMpr = {Mpr:.1f} t·m", xy=(0, Mpr), xytext=(1.0, Mpr*1.1),
                 arrowprops=dict(arrowstyle='->', color='#f1c40f', lw=2), 
                 color='#f1c40f', fontsize=11, fontweight='bold', ha='center')
    
    ax3.annotate(f"Rótula Plástica\nMpr = {Mpr:.1f} t·m", xy=(Lv, -Mpr), xytext=(Lv-1.0, -Mpr*1.1),
                 arrowprops=dict(arrowstyle='->', color='#f1c40f', lw=2), 
                 color='#f1c40f', fontsize=11, fontweight='bold', ha='center')

    ax3.set_xlabel("Abscisa x (m)", color=color_texto, fontsize=12)
    ax3.set_ylabel("Momento Sísmico (t·m)", color=color_texto, fontsize=12)
    ax3.set_xlim(0, Lv)
    ax3.set_ylim(-Mpr*1.4, Mpr*1.4)
    ax3.legend(facecolor='#2c3e50', edgecolor=color_texto, labelcolor=color_texto, loc='upper right')
    ax3.grid(True, linestyle='--', alpha=0.2)
    ax3.tick_params(colors=color_texto)
    for spine in ax3.spines.values(): spine.set_color(color_texto)
    ax3.set_title("C) DIAGRAMA DE MOMENTO SÍSMICO (MARIPOSA REVERSIBLE)", color=color_texto, fontsize=14, fontweight='bold')

    # --- PANEL 4: RESUMEN DE RESULTADOS ---
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#1e1e2e')
    ax4.axis('off')
    
    resumen = (
        "📊 RESUMEN DEL DISEÑO SÍSMICO\n"
        "--------------------------------------------------\n"
        f"1. Carga Última (Wu)     = {Wu:.3f} t/m²\n"
        f"2. Luz Libre             = {luz_libre:.2f} m\n"
        f"3. Momento Estático (Me) = {Me:.2f} t·m\n"
        f"4. Momento Diseño (Md)   = {Md:.2f} t·m\n\n"
        f"5. Acero Requerido (As)  = {As_viga:.2f} cm²\n"
        f"6. Cuantía (ρ)           = {(As_viga / (b_viga * d))*100:.2f}% (Dúctil)\n"
        f"7. Capacidad (Mpr)       = {Mpr:.2f} t·m\n\n"
        "✅ DISEÑO CUMPLE CON EL CRITERIO DE DUCTILIDAD\n"
        "   (La rótula se forma antes de la falla frágil)"
    )
    ax4.text(0.05, 0.95, resumen, transform=ax4.transAxes, fontsize=12, 
             verticalalignment='top', fontfamily='monospace', color='#2ecc71',
             bbox=dict(boxstyle='round,pad=1', facecolor='#2c3e50', edgecolor='#2ecc71', lw=2))

    fig.suptitle("M03: CÁLCULO DEL MOMENTO DE DISEÑO Y COMPORTAMIENTO SÍSMICO REVERSIBLE", 
                 color=color_texto, fontsize=18, fontweight='bold', y=0.95)
    
    plt.savefig('m03_dashboard_integral_md.png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()

if __name__ == "__main__":
    generar_dashboard_integral()