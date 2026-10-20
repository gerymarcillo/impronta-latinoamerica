# -*- coding: utf-8 -*-
"""
PIRÁMIDE DEL MODELO ECT-UNESUM: LA JUSTIFICACIÓN DEL CAMBIO SOCIAL
Proyecto: Rediseño Curricular Dinámico 2020-2026
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_piramide_cambio_social():
    # Gráfico vertical (Bottom to Top)
    dot = graphviz.Digraph(comment='Pirámide ECT-UNESUM', format='png')
    dot.attr(rankdir='BT', size='10,12', nodesep='0.3', ranksep='0.8')
    
    # Estilos generales
    dot.attr('node', shape='box', style='filled, rounded', fontname='Arial', fontcolor='white', margin='0.2')
    dot.attr('edge', color='#f39c12', penwidth='3', style='dashed')

    # --- CÚSPIDE (Nivel 4: El Cambio de Vida y el Rechazo al Q4) ---
    dot.node('N4', 'LA JUSTIFICACIÓN: EL CAMBIO SOCIAL\n"Un Q4 no mejora la calidad de vida"\nEvaluación Cualitativa (CACES) → Impacto real en la Zona 4', 
             fillcolor='#e74c3c', shape='doubleoctagon', width='6', fontsize='12')
    
    # --- CUERPO ALTO (Nivel 3: Prototipado y Validación) ---
    dot.node('N3', 'FASE DE VALIDACIÓN (SÉPTIMO NIVEL)\nModelado ETABS / Análisis Matricial 3D\nPrototipado DMTP y Sensores Phyphox', 
             fillcolor='#9b59b6', width='7', fontsize='11')
    
    # --- CUERPO MEDIO (Nivel 2: Diagnóstico e Insumos) ---
    dot.node('N2', 'FASE DE DIAGNÓSTICO (SEXTO NIVEL)\nCargas, Armaduras y Algoritmos Base\nLaboratorio Vivo: Agua Dulce', 
             fillcolor='#3498db', width='8', fontsize='11')

    # --- BASE (Nivel 1: El Modelo Educativo) ---
    dot.node('N1', 'MODELO EDUCATIVO Y GÉNESIS (2020-2026)\nConstructivismo + ABP + Aula Invertida + TAC\nPlataforma ECT-UNESUM y Bóveda de Recursos (M08)', 
             fillcolor='#16a085', width='9', fontsize='11')

    # --- CONEXIONES (Flechas que suben) ---
    dot.edge('N1', 'N2', label=' Genera Insumos ')
    dot.edge('N2', 'N3', label=' Transfiere Insumos ')
    dot.edge('N3', 'N4', label=' Eslabón Universitario:\nTransferencia a la Comunidad ')

    # --- IMPRONTA (Al costado) ---
    dot.node('AUTOR', 'Autor e Investigador Principal:\nIng. Gery Lorenzo Marcillo Merino, Msc.\n\n"Desde cero. Juntos. Con propósito."', 
             shape='plaintext', fontcolor='#f39c12', fontname='Arial bold', fontsize='13')

    # Alinear el autor con la base
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('N1')
        s.node('AUTOR')

    # Generar imagen
    nombre_archivo = 'piramide_cambio_social_ect'
    dot.render(nombre_archivo, view=True)
    print(f"✅ Pirámide del Cambio Social generada: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_piramide_cambio_social()