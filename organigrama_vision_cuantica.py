# -*- coding: utf-8 -*-
"""
ORGANIGRAMA DEL OBJETIVO Y VISIÓN A 4 AÑOS (VERSIÓN INTEGRADORA)
Proyecto: ECT-UNESUM-2026 / Laboratorio Vivo
Incluye: Mecánica Cuántica, Métodos Predictivos y Transversalidad
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def dibujar_organigrama():
    fig, ax = plt.subplots(figsize=(14, 11)) # Un poco más ancho para que respire
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_facecolor('#0a0e1a') # Fondo oscuro como la plataforma
    fig.patch.set_facecolor('#0a0e1a')

    # Función auxiliar para crear cajas
    def caja(x, y, texto, color, ancho=2.8, alto=1.0):
        rect = patches.FancyBboxPatch((x - ancho/2, y - alto/2), ancho, alto, 
                                      boxstyle="round,pad=0.1", 
                                      edgecolor=color, facecolor='#141a2e', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, texto, ha='center', va='center', color='white', fontsize=8.5, fontweight='bold')

    # --- NIVEL 0: MACRO OBJETIVO ---
    caja(5, 12.2, "MACRO OBJETIVO:\nRediseño Educativo Predictivo (IA + Estocástico)\nUNESUM-REZ-2026-JIPIJAPA-001", '#16a085', ancho=7, alto=1.2)
    
    # --- NIVEL 1: TRES PILARES CON ENFOQUE CUÁNTICO ---
    caja(1.8, 10, "DOCENCIA\n(Aula Invertida + ABP)\nIncertidumbre Estructural", '#3498db', ancho=3, alto=1.1)
    caja(5, 10, "INVESTIGACIÓN\n(72 Algoritmos + Visión Cuántica)\nModelado Estocástico", '#9b59b6', ancho=3, alto=1.1)
    caja(8.2, 10, "VINCULACIÓN\n(Laboratorio Vivo)\nEntrelazamiento Territorial", '#f39c12', ancho=3, alto=1.1)

    # --- NIVEL 2: APLICACIÓN POR NIVELES ---
    caja(1.8, 7.8, "Sexto Nivel: Estructura I\n(Genera Insumos Base)", '#2980b9', ancho=3, alto=0.9)
    caja(5, 7.8, "Séptimo Nivel: Grandes Edificaciones\n(Diseño + M08 DMTP)", '#8e44ad', ancho=3.5, alto=0.9)
    caja(8.2, 7.8, "Red Interinstitucional\n(GAD, Empresas, SENESCYT)", '#d35400', ancho=3, alto=0.9)

    # --- NIVEL 3: EL ESLABÓN (PROYECTOS) ---
    caja(5, 5.2, "PROYECTOS INTER/MULTIDISCIPLINARIOS\nEntrelazamiento de Saberes (Hidráulica + Estructura + IA)", '#c0392b', ancho=8, alto=1.2)

    # --- NIVEL 4: ENFOQUE PREDICTIVO / MÉTODOS ---
    caja(5, 2.8, "MÉTODOS PREDICTIVOS (El 'Colapso' Cuántico)\nMonte Carlo | Markov | RNA | XGBoost | Análisis de Patologías", '#e67e22', ancho=8, alto=1.2)

    # --- NIVEL 5: META FINAL ---
    caja(5, 0.8, "META A 4 AÑOS:\nInserción Laboral Directa (>90%) y Resiliencia Territorial", '#2ecc71', ancho=6.5, alto=1.2)

    # --- FLECHAS DE CONEXIÓN (El flujo del conocimiento) ---
    flechas = [
        # Macro a Pilares
        ((5, 11.6), (1.8, 10.5)), ((5, 11.6), (5, 10.5)), ((5, 11.6), (8.2, 10.5)),
        # Pilares a Niveles
        ((1.8, 9.5), (1.8, 8.2)), ((5, 9.5), (5, 8.2)), ((8.2, 9.5), (8.2, 8.2)),
        # Niveles a Eslabón
        ((1.8, 7.4), (3.5, 5.8)), ((5, 7.4), (5, 5.8)), ((8.2, 7.4), (6.5, 5.8)),
        # Eslabón a Métodos
        ((5, 4.6), (5, 3.4)),
        # Métodos a Meta
        ((5, 2.2), (5, 1.4))
    ]
    
    for (x1, y1), (x2, y2) in flechas:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#f39c12", lw=2, shrinkA=5, shrinkB=5))

    # Título
    plt.title("ORGANIGRAMA DEL OBJETIVO: DEL AULA AL MERCADO LABORAL\n(Con Visión Cuántica y Predictiva)", color='#5dade2', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Guardar
    plt.savefig('organigrama_ect_2026_cuantico.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✅ Organigrama generado con éxito: organigrama_ect_2026_cuantico.png")

if __name__ == "__main__":
    dibujar_organigrama()