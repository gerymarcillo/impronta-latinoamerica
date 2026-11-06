# -*- coding: utf-8 -*-
"""
======================================================================
M03: MODELO 3D DEL ACERO EN EL NUDO (RÓTULA PLÁSTICA)
Proyecto: ECT-UNESUM-2026
======================================================================
Este script genera una visualización 3D de la viga, mostrando el
acero longitudinal continuo (la "pinza"), el acero positivo anclado
en el nudo y los resultados de Md y As.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def generar_modelo_3d_nudo():
    # ======================================================================
    # 1. DATOS DEL MODELO Y RESULTADOS
    # ======================================================================
    Lv = 6.00           # Luz de la viga (m)
    b_viga = 0.30       # Base (m)
    h_viga = 0.45       # Peralte (m)
    rec = 0.025         # Recubrimiento (m)
    phi_sup = 0.016     # Diámetro varilla superior (m)
    phi_inf = 0.014     # Diámetro varilla inferior (m)
    
    n_sup = 4           # Número de varillas superiores (As-)
    n_inf = 2           # Número de varillas inferiores (As+)

    # Resultados del cálculo (del script del acero)
    Md_val = 18.02      # t·m
    As_val = 10.00      # cm² (As-)
    As_pos_val = 5.00   # cm² (As+ estimado)
    rho_val = 0.82      # %

    # ======================================================================
    # 2. CONFIGURACIÓN GRÁFICA
    # ======================================================================
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor('#1e1e2e')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#1e1e2e')

    # ======================================================================
    # 3. DIBUJAR EL CONCRETO (TRANSPARENTE)
    # ======================================================================
    vertices = [
        [0, 0, 0], [Lv, 0, 0], [Lv, b_viga, 0], [0, b_viga, 0],
        [0, 0, h_viga], [Lv, 0, h_viga], [Lv, b_viga, h_viga], [0, b_viga, h_viga]
    ]
    caras_idx = [
        [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]
    ]
    caras = [[vertices[i] for i in cara] for cara in caras_idx]
    
    ax.add_collection3d(Poly3DCollection(caras, facecolors='#5dade2', linewidths=1, edgecolors='#ecf0f1', alpha=0.05))

    # ======================================================================
    # 4. DIBUJAR ACERO LONGITUDINAL (LA PINZA Y EL AS+)
    # ======================================================================
    # --- Acero superior (Negativo - La Pinza Continua) ---
    y_sup = np.linspace(rec + phi_sup/2, b_viga - rec - phi_sup/2, n_sup)
    z_sup = h_viga - rec - phi_sup/2
    for y in y_sup:
        # La pinza roja continua de lado a lado
        ax.plot([0, Lv], [y, y], [z_sup, z_sup], color='#e74c3c', linewidth=5, solid_capstyle='round', zorder=10)
        # Ganchos en los extremos (anclaje en el nudo)
        ax.plot([0, 0.2], [y, y], [z_sup, z_sup - 0.15], color='#e74c3c', linewidth=5, zorder=10)
        ax.plot([Lv, Lv - 0.2], [y, y], [z_sup, z_sup - 0.15], color='#e74c3c', linewidth=5, zorder=10)

    # --- Acero inferior (Positivo - Azul) ---
    y_inf = np.linspace(rec + phi_inf/2, b_viga - rec - phi_inf/2, n_inf)
    z_inf = rec + phi_inf/2
    for y in y_inf:
        # El acero positivo también se ancla en los nudos
        ax.plot([0, Lv], [y, y], [z_inf, z_inf], color='#3498db', linewidth=4, solid_capstyle='round', zorder=9)
        # Ganchos en los extremos
        ax.plot([0, 0.2], [y, y], [z_inf, z_inf + 0.15], color='#3498db', linewidth=4, zorder=9)
        ax.plot([Lv, Lv - 0.2], [y, y], [z_inf, z_inf + 0.15], color='#3498db', linewidth=4, zorder=9)

    # ======================================================================
    # 5. DIBUJAR ESTRIBOS (CONFINAMIENTO SUTIL)
    # ======================================================================
    n_estribos = 8
    x_estribos = np.linspace(0.2, Lv - 0.2, n_estribos)
    
    for x in x_estribos:
        y_est = [rec, b_viga - rec, b_viga - rec, rec, rec]
        z_est = [rec, rec, h_viga - rec, h_viga - rec, rec]
        ax.plot([x]*5, y_est, z_est, color='#7f8c8d', linewidth=1, alpha=0.3, zorder=5)

    # ======================================================================
    # 6. EL NUDO (ZONA DE RÓTULA PLÁSTICA) Y TEXTOS
    # ======================================================================
    # Marcar el nudo con un cubo semitransparente en el extremo izquierdo
    cubo_nudo = [[0, 0, 0], [0.4, 0, 0], [0.4, b_viga, 0], [0, b_viga, 0], 
                 [0, 0, h_viga], [0.4, 0, h_viga], [0.4, b_viga, h_viga], [0, b_viga, h_viga]]
    caras_nudo = [[cubo_nudo[i] for i in cara] for cara in caras_idx]
    ax.add_collection3d(Poly3DCollection(caras_nudo, facecolors='#f1c40f', linewidths=1, edgecolors='#f1c40f', alpha=0.15))

    # Textos informativos en el nudo
    texto_nudo = (
        f"RÓTULA PLÁSTICA\n"
        f"Md = {Md_val:.1f} t·m\n"
        f"As(-) = {As_val:.1f} cm²\n"
        f"As(+) = {As_pos_val:.1f} cm²\n"
        f"ρ = {rho_val:.2f}% (DÚCTIL)"
    )
    
    # Colocamos el texto flotando en el extremo izquierdo de la viga
    ax.text(0.1, b_viga/2, h_viga + 0.15, texto_nudo, 
            color='#f1c40f', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#2c3e50', edgecolor='#f1c40f', alpha=0.9))

    # ======================================================================
    # 7. CONFIGURACIÓN FINAL
    # ======================================================================
    ax.set_xlabel('Longitud (m)', color='#ecf0f1', fontsize=10)
    ax.set_ylabel('Ancho (m)', color='#ecf0f1', fontsize=10)
    ax.set_zlabel('Peralte (m)', color='#ecf0f1', fontsize=10)
    
    ax.set_xlim(0, Lv)
    ax.set_ylim(0, b_viga)
    ax.set_zlim(0, h_viga + 0.2)
    
    ax.view_init(elev=20, azim=-45)
    
    # Ocultar paneles de fondo
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#1e1e2e')
    ax.yaxis.pane.set_edgecolor('#1e1e2e')
    ax.zaxis.pane.set_edgecolor('#1e1e2e')
    
    ax.tick_params(colors='#ecf0f1')

    ax.set_title("M03: MODELO 3D DEL NUDO - ACERO POSITIVO Y NEGATIVO ANCLADO\n(La Rótula Plástica se forma en el cubo amarillo)", 
                 color='#ecf0f1', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('m03_modelo_3d_nudo_completo.png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()
    print("✅ Imagen 3D generada: m03_modelo_3d_nudo_completo.png")

if __name__ == "__main__":
    generar_modelo_3d_nudo()