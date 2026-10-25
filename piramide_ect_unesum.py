# -*- coding: utf-8 -*-
"""
PIRÁMIDE DEL MODELO ECT-UNESUM (VISIÓN ESTRATÉGICA 2026)
Estilo adaptado a la plataforma web (Fondo oscuro / Neón)
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_piramide_modelo():
    # Configuración del gráfico: Fondo oscuro
    dot = graphviz.Digraph(comment='Pirámide ECT-UNESUM', format='png')
    dot.attr(rankdir='BT', size='10,12', nodesep='0.4', ranksep='0.8', bgcolor='#0a0e1a')
    
    # Estilos generales de los nodos (Fondo transparente, borde grueso, texto blanco)
    dot.attr('node', shape='box', style='rounded,filled', fontname='Segoe UI', fontcolor='white', 
             fillcolor='#141a2e', color='#f39c12', penwidth='2', margin='0.3')
    
    # Estilos de las flechas (Dorado/Neón)
    dot.attr('edge', color='#f39c12', penwidth='3', style='dashed')

    # --- BASE (Nivel 1: Verde Neón) ---
    dot.node('N1', 'NIVEL 1: MODELO EDUCATIVO Y PLATAFORMA (2020-2026)\nConstructivismo + ABP + IA + Laboratorio Vivo (Agua Dulce)\nPlataforma ECT-UNESUM (Módulos M01-M08)', 
             color='#16a085', width='8', fontsize='11')
    
    # --- CUERPO MEDIO (Nivel 2: Azul Neón) ---
    dot.node('N2', 'NIVEL 2: SEXTO (Estructura I)\nDiagnóstico de Cargas y Armaduras (GeoGebra)\nInsumos Base del Territorio', 
             color='#3498db', width='7', fontsize='11')
    
    # --- CUERPO ALTO (Nivel 3: Morado Neón) ---
    dot.node('N3', 'NIVEL 3: SÉPTIMO (Estructura II)\nAnálisis Matricial 3D y Validación (Phyphox)\nPrototipo DMTP + Modelos Predictivos', 
             color='#9b59b6', width='6', fontsize='11')

    # --- CÚSPIDE (Nivel 4: Rojo Neón) ---
    dot.node('N4', 'NIVEL 4: CÚSPIDE (Ecosistema Externo)\nCertificado de Inducción + Artículo Científico\nResiliencia Territorial + Acreditación CACES', 
             color='#c0392b', width='5', fontsize='12')

    # --- CONEXIONES (Flechas que suben mostrando el flujo de insumos) ---
    dot.edge('N1', 'N2', label=' Asignación de Proyecto ', fontcolor='#ecf0f1')
    dot.edge('N2', 'N3', label=' Trazabilidad de Insumos ', fontcolor='#ecf0f1')
    dot.edge('N3', 'N4', label=' Evidencias y Validación ', fontcolor='#ecf0f1')

    # --- IMPRONTA DEL AUTOR ---
    dot.node('AUTOR', 'Autor e Investigador Principal:\nIng. Gery Lorenzo Marcillo Merino, M.Sc.\n\n"Desde cero. Juntos. Con propósito."\n\n✅ MODELO DINÁMICO (CACES)', 
             shape='plaintext', fontcolor='#f39c12', fontname='Arial bold', fontsize='12')

    # Alinear el autor con la base
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('N1')
        s.node('AUTOR')

    # Generar imagen
    nombre_archivo = 'piramide_ect_modelo_2026_oscuro'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Pirámide generada con éxito: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_piramide_modelo()