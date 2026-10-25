# -*- coding: utf-8 -*-
"""
FLUJOGRAMA VERTICAL A4 - ARTICULACIÓN UT4 (MÉTODO DE RIGIDEZ)
Proyecto: ECT-UNESUM-2026 (Sexto y Séptimo) - Estilo Oscuro
Secuencia: Métodos Energéticos y G.D.L. Espaciales (Sexto) -> Pórtico 3D (Séptimo)
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_flujograma_ut4_portico_3d():
    dot = graphviz.Digraph(comment='Flujo A4 UT4 Portico 3D', format='png')
    dot.attr(rankdir='TB', size='8,11', nodesep='0.4', ranksep='0.6', bgcolor='#0a0e1a') 
    
    dot.attr('node', shape='box', style='filled, rounded', fontname='Segoe UI', fontcolor='white', margin='0.15', fillcolor='#141a2e')
    dot.attr('edge', color='#f39c12', penwidth='2', fontname='Segoe UI bold', fontsize='11', fontcolor='#ecf0f1')

    # --- BLOQUE SEXTO (UT4) ---
    with dot.subgraph(name='cluster_sexto') as c:
        c.attr(label='FASE 1: SEXTO - UT4 (Introducción al Método de Rigidez)', color='#3498db', fontcolor='#3498db', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('S1', 'SEMANA 17: MÉTODOS ENERGÉTICOS\n(Maxwell-Betti y Trabajo Virtual)', color='#3498db', width='4')
        c.node('S2', 'SEMANA 18: GRADOS DE LIBERTAD ESPACIALES\n(Pre-dimensionamiento de Nodos 3D)', color='#3498db', width='4')
        c.node('S3', 'SEMANA 19: ENTREGA DEL INSUMO\n(Matriz de Flexibilidad Espacial y G.D.L.)', color='#2980b9', width='4')

    # --- HITO DE CONTROL ---
    dot.node('T1', 'HITO DE CONTROL (Semana 19)\nValidación de Métodos Energéticos\n(Entrega de G.D.L. Espaciales)', 
             color='#f39c12', shape='hexagon', fontcolor='white', width='4')

    # --- BLOQUE SÉPTIMO (UT4) ---
    with dot.subgraph(name='cluster_septimo') as c:
        c.attr(label='FASE 2: SÉPTIMO - UT4 (Matriz de Rigidez y Pórtico 3D)', color='#9b59b6', fontcolor='#9b59b6', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('P1', 'SEMANA 20: MATRIZ DE RIGIDEZ DE VIGAS\n(Análisis de Elementos Individuales)', color='#9b59b6', width='4')
        c.node('P2', 'SEMANA 21: MATRIZ DE RIGIDEZ DE COLUMNAS\n(Análisis de Elementos Individuales)', color='#8e44ad', width='4')
        c.node('P3', 'SEMANA 22: ENSAMBLAJE DE PÓRTICO PLANO\n(Unión de Vigas + Columnas)', color='#9b59b6', width='4')
        c.node('P4', 'SEMANA 23: MATRIZ DE RIGIDEZ 3D\n(Pórtico Tridimensional - 6 G.D.L. por Nodo)', color='#d35400', width='4', penwidth='3')

    # --- HITO DE CONTROL FINAL ---
    dot.node('T2', 'HITO DE DEFENSA (Semana 23)\nExamen Integrador de Capítulo\n(Defensa del Pórtico 3D)', 
             color='#2ecc71', shape='hexagon', fontcolor='white', width='4')

    # --- CONEXIONES (La secuencia estricta) ---
    dot.edge('S1', 'S2', label=' Energía a G.D.L.')
    dot.edge('S2', 'S3', label=' Matriz de Flexibilidad')
    dot.edge('S3', 'T1', label=' Cierre de Sexto')
    
    # El insumo pasa a Séptimo (El puente de conexión)
    dot.edge('T1', 'P1', label=' TRANSFERENCIA: G.D.L. Espaciales')
    
    dot.edge('P1', 'P2', label=' Análisis Individual')
    dot.edge('P2', 'P3', label=' Ensamblaje 2D')
    dot.edge('P3', 'P4', label=' Salto a 3D')
    dot.edge('P4', 'T2', label=' Cierre de Séptimo')

    nombre_archivo = 'flujograma_ut4_portico_3d'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Flujograma UT4 (Pórtico 3D) generado: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_flujograma_ut4_portico_3d()