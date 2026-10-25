# -*- coding: utf-8 -*-
"""
FLUJOGRAMA VERTICAL A4 - ARTICULACIÓN UT2 (HIPERESTÁTICOS -> COORDENADAS)
Proyecto: ECT-UNESUM-2026 (Sexto y Séptimo) - Estilo Oscuro
Secuencia: UT2 Sexto -> Insumo -> UT2 Séptimo
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_flujograma_a4_ut2():
    dot = graphviz.Digraph(comment='Flujo A4 UT2', format='png')
    # Configuración A4 vertical con fondo oscuro
    dot.attr(rankdir='TB', size='7.5,10', nodesep='0.4', ranksep='0.6', bgcolor='#0a0e1a') 
    
    # Estilos generales
    dot.attr('node', shape='box', style='filled, rounded', fontname='Segoe UI', fontcolor='white', margin='0.15', fillcolor='#141a2e')
    dot.attr('edge', color='#f39c12', penwidth='2', fontname='Segoe UI bold', fontsize='11', fontcolor='#ecf0f1')

    # --- BLOQUE SEXTO (UT2) ---
    with dot.subgraph(name='cluster_sexto') as c:
        c.attr(label='FASE 1: SEXTO - UT2 (Análisis Hiperestático)', color='#3498db', fontcolor='#3498db', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('S1', 'SEMANA 7-8: ANÁLISIS DE ARMADURAS\n(Método de nodos y secciones)', color='#3498db', width='4')
        c.node('S2', 'SEMANA 9-10: VIGAS GERBER Y PÓRTICOS\n(Cálculo de reacciones)', color='#3498db', width='4')
        c.node('S3', 'SEMANA 11-12: ENTREGA DEL MODELO\n(Fuerzas internas y prototipo)', color='#2980b9', width='4')

    # --- HITO DE CONTROL ---
    dot.node('T1', 'HITO DE CONTROL (Semana 12)\nEvaluación de Gestión del Tiempo\n(Entrega del Insumo Estructural)', 
             color='#f39c12', shape='hexagon', fontcolor='white', width='4')

    # --- BLOQUE SÉPTIMO (UT2) ---
    with dot.subgraph(name='cluster_septimo') as c:
        c.attr(label='FASE 2: SÉPTIMO - UT2 (Coordenadas y GDL)', color='#9b59b6', fontcolor='#9b59b6', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('P1', 'SEMANA 13: COORDENADAS GLOBALES\n(Ubicación de la estructura)', color='#9b59b6', width='4')
        c.node('P2', 'SEMANA 14: COORDENADAS LOCALES Y NODALES\n(Definición de Grados de Libertad)', color='#8e44ad', width='4')
        c.node('P3', 'SEMANA 15-16: EJERCICIOS DE APLICACIÓN\n(Matriz de Transformación)', color='#9b59b6', width='4')

    # --- HITO DE CONTROL FINAL ---
    dot.node('T2', 'HITO DE DEFENSA (Semana 16)\nExamen Integrador de Capítulo\n(Ensamblaje de Coordenadas)', 
             color='#2ecc71', shape='hexagon', fontcolor='white', width='4')

    # --- CONEXIONES (La secuencia estricta) ---
    dot.edge('S1', 'S2', label=' 2 semanas')
    dot.edge('S2', 'S3', label=' 2 semanas')
    dot.edge('S3', 'T1', label=' Cierre de Sexto')
    
    # El insumo pasa a Séptimo
    dot.edge('T1', 'P1', label=' TRANSFERENCIA: Fuerzas y Geometría')
    
    dot.edge('P1', 'P2', label=' 1 semana')
    dot.edge('P2', 'P3', label=' 2 semanas')
    dot.edge('P3', 'T2', label=' Cierre de Séptimo')

    # Generar imagen
    nombre_archivo = 'flujograma_UT2_articulacion'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Flujograma UT2 generado con secuencia estricta: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_flujograma_a4_ut2()