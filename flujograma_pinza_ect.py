# -*- coding: utf-8 -*-
"""
FLUJOGRAMA DE LA ESTRUCTURA "PINZA" (SEXTO Y SÉPTIMO) - ESTILO PLATAFORMA ECT
Impacto: Trazabilidad Curricular y Transferencia de Insumos
"""

import os
import graphviz

# 1. CONFIGURACIÓN DE RUTA PARA GRAPHVIZ
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_flujograma_pinza():
    # Gráfico vertical (TB) con fondo oscuro
    dot = graphviz.Digraph(comment='Estructura Pinza', format='png')
    dot.attr(rankdir='TB', size='10,14', nodesep='0.5', ranksep='0.7', bgcolor='#0a0e1a')
    
    # Estilos generales (Fondo de cajas oscuro, texto blanco, bordes neón)
    dot.attr('node', shape='box', style='filled, rounded', fontname='Segoe UI', fontcolor='white', margin='0.2', fillcolor='#141a2e')
    dot.attr('edge', color='#f39c12', penwidth='2.5', fontname='Segoe UI bold', fontsize='11', fontcolor='#ecf0f1')

    # --- TÍTULO ---
    dot.node('TITULO', 'ESTRUCTURA "PINZA": ARTICULACIÓN 1 A 1\n(El fin del borrón y cuenta nueva)', 
             shape='plaintext', fontcolor='#f39c12', fontname='Segoe UI bold', fontsize='16')

    # --- BLOQUE SEXTO NIVEL ---
    with dot.subgraph(name='cluster_sexto') as c:
        c.attr(label='SEXTO NIVEL (Estructura I) - DIAGNÓSTICO', color='#3498db', fontcolor='#3498db', style='dashed', fontname='Segoe UI bold', penwidth='2')
        c.node('S1', 'UT1: Cargas y Áreas Tributarias\n(Agua Dulce / Colegios)', color='#3498db')
        c.node('S2', 'UT2: Armaduras y Pórticos\n(Análisis Hiperestático)', color='#3498db')
        c.node('S3', 'UT3: Líneas de Influencia\n(Trenes de Carga)', color='#3498db')
        c.node('S4', 'UT4: Principios Energéticos\n(Introducción a Matrices)', color='#3498db')

    # --- EL TESTIGO (INSUMOS) ---
    dot.node('I1', '📦 INSUMO: Vector de Cargas', color='#e67e22', shape='note')
    dot.node('I2', '📦 INSUMO: Matriz Base', color='#e67e22', shape='note')
    dot.node('I3', '📦 INSUMO: Solicitaciones Críticas', color='#e67e22', shape='note')
    dot.node('I4', '📦 INSUMO: Algoritmo Base', color='#e67e22', shape='note')

    # --- BLOQUE SÉPTIMO NIVEL ---
    with dot.subgraph(name='cluster_septimo') as c:
        c.attr(label='SÉPTIMO NIVEL (Estructura II) - DISEÑO Y VALIDACIÓN', color='#9b59b6', fontcolor='#9b59b6', style='dashed', fontname='Segoe UI bold', penwidth='2')
        c.node('P1', 'UT1: Coordenadas y G.D.L.\n(Modelado en ETABS)', color='#9b59b6')
        c.node('P2', 'UT2: Matriz de Rigidez 1D\n(Programación en Python)', color='#9b59b6')
        c.node('P3', 'UT3: Matriz de Columnas\n(Diseño de Muros de Corte)', color='#9b59b6')
        c.node('P4', 'UT4: Matriz 3D y DMTP\n(Prototipado y Phyphox)', color='#9b59b6')

    # --- CONEXIONES DE LA PINZA (1 a 1) ---
    dot.edge('S1', 'I1')
    dot.edge('S2', 'I2')
    dot.edge('S3', 'I3')
    dot.edge('S4', 'I4')

    dot.edge('I1', 'P1')
    dot.edge('I2', 'P2')
    dot.edge('I3', 'P3')
    dot.edge('I4', 'P4')

    # Conectar visualmente el título
    dot.edge('TITULO', 'S1', style='invis')
    
    # Alinear las unidades
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('S1'); s.node('S2'); s.node('S3'); s.node('S4')
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('I1'); s.node('I2'); s.node('I3'); s.node('I4')
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('P1'); s.node('P2'); s.node('P3'); s.node('P4')

    # Generar imagen
    nombre_archivo = 'flujograma_pinza_ect'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Flujograma 'Pinza' generado con impacto curricular: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_flujograma_pinza()