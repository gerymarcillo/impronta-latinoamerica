# -*- coding: utf-8 -*-
"""
FLUJOGRAMA VERTICAL A4 - ARTICULACIÓN UT3 (PUENTE ATIRANTADO)
Proyecto: ECT-UNESUM-2026 (Sexto y Séptimo) - Estilo Oscuro
Secuencia: Líneas de Influencia (Sexto) -> Matriz de Rigidez (Séptimo)
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_flujograma_ut3_atirado():
    dot = graphviz.Digraph(comment='Flujo A4 UT3 Atirantado', format='png')
    # Configuración A4 vertical con fondo oscuro
    dot.attr(rankdir='TB', size='8,11', nodesep='0.4', ranksep='0.6', bgcolor='#0a0e1a') 
    
    # Estilos generales
    dot.attr('node', shape='box', style='filled, rounded', fontname='Segoe UI', fontcolor='white', margin='0.15', fillcolor='#141a2e')
    dot.attr('edge', color='#f39c12', penwidth='2', fontname='Segoe UI bold', fontsize='11', fontcolor='#ecf0f1')

    # --- BLOQUE SEXTO (UT3) ---
    with dot.subgraph(name='cluster_sexto') as c:
        c.attr(label='FASE 1: SEXTO - UT3 (Líneas de Influencia)', color='#3498db', fontcolor='#3498db', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('S1', 'SEMANA 13-14: VIGAS GERBER Y TRENES DE CARGA\n(Análisis de Solicitaciones)', color='#3498db', width='4')
        c.node('S2', 'SEMANA 15: APLICACIÓN AL PUENTE ATIRANTADO\n(Identificación de Cables Críticos)', color='#3498db', width='4')
        c.node('S3', 'SEMANA 16: ENTREGA DEL INSUMO\n(Solicitaciones Críticas del Tablero)', color='#2980b9', width='4')

    # --- HITO DE CONTROL ---
    dot.node('T1', 'HITO DE CONTROL (Semana 16)\nValidación del Tren de Carga\n(Entrega de Solicitaciones)', 
             color='#f39c12', shape='hexagon', fontcolor='white', width='4')

    # --- BLOQUE SÉPTIMO (UT3) ---
    with dot.subgraph(name='cluster_septimo') as c:
        c.attr(label='FASE 2: SÉPTIMO - UT3 (Matriz de Rigidez 42 Elementos)', color='#9b59b6', fontcolor='#9b59b6', style='dashed', fontname='Segoe UI bold', fontsize='12')
        c.node('P1', 'SEMANA 17: MATRIZ DE RIGIDEZ LOCAL\n(Programación 1D de Cables y Tablero)', color='#9b59b6', width='4')
        c.node('P2', 'SEMANA 18: MATRIZ DE TRANSFORMACIÓN\n(Coordenadas Globales / Locales)', color='#8e44ad', width='4')
        c.node('P3', 'SEMANA 19: ENSAMBLAJE GLOBAL (42 ELEMENTOS)\n(Análisis en Python / SAP2000)', color='#9b59b6', width='4')
        c.node('P4', 'SEMANA 20: ZONAS DE EMPOTRAMIENTO\n(Diseño de Anclajes y Bases de Torres)', color='#d35400', width='4', penwidth='3')

    # --- HITO DE CONTROL FINAL ---
    dot.node('T2', 'HITO DE DEFENSA (Semana 20)\nExamen Integrador de Capítulo\n(Aplicación al Territorio Rural)', 
             color='#2ecc71', shape='hexagon', fontcolor='white', width='4')

    # --- CONEXIONES (La secuencia cuántica) ---
    dot.edge('S1', 'S2', label=' 2 semanas')
    dot.edge('S2', 'S3', label=' 1 semana')
    dot.edge('S3', 'T1', label=' Cierre de Sexto')
    
    # El insumo pasa a Séptimo
    dot.edge('T1', 'P1', label=' TRANSFERENCIA: Solicitaciones y Geometría')
    
    dot.edge('P1', 'P2', label=' Ensamblaje')
    dot.edge('P2', 'P3', label=' Validación')
    dot.edge('P3', 'P4', label=' Diseño Final')
    dot.edge('P4', 'T2', label=' Cierre de Séptimo')

    # Generar imagen
    nombre_archivo = 'flujograma_ut3_atirado'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Flujograma UT3 (Atirantado) generado: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_flujograma_ut3_atirado()