# -*- coding: utf-8 -*-
"""
ORGANIGRAMA DE ENLACE - ANDAMIAJE EN CRECIMIENTO (V2 CORREGIDO)
Proyecto: ECT-UNESUM-2026
Secuencia: Ecosistema -> Sexto -> Séptimo -> Evidencia Científica -> Mercado
"""

import os
import graphviz

# Ruta de Graphviz
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_organigrama_enlace():
    # Gráfico de abajo hacia arriba (BT) con fondo oscuro
    dot = graphviz.Digraph(comment='Andamiaje ECT', format='png')
    dot.attr(rankdir='BT', size='12,12', nodesep='0.6', ranksep='0.7', bgcolor='#0a0e1a') 
    
    # Estilos generales (Fondo de cajas oscuro, texto blanco, borde neón)
    dot.attr('node', shape='box', style='filled, rounded', fontname='Segoe UI', fontcolor='white', margin='0.25', fillcolor='#141a2e')
    dot.attr('edge', color='#f39c12', penwidth='2.5', fontname='Segoe UI', fontsize='11', fontcolor='#ecf0f1')

    # --- NIVEL 1: LA BASE (El Ecosistema) ---
    dot.node('BASE', 'ECOSISTEMA ECT-UNESUM-2026\nPlataforma Digital + 23 Estructuras Especiales\nLaboratorio Vivo: Agua Dulce', 
             color='#16a085', shape='cylinder', fontsize='12', width='6')

    # --- NIVEL 2: SEXTO NIVEL (Diagnóstico) ---
    dot.node('S1', 'SEXTO NIVEL: Estructura I\nFase: Diagnóstico Forense y Cargas', color='#3498db', fontsize='12')
    dot.node('S2', 'Insumos Base Generados:\n- Análisis de Cargas\n- Modelos Matemáticos\n- Algoritmos en Python/GeoGebra', color='#3498db', fontsize='11')
    
    # --- NIVEL 3: SÉPTIMO NIVEL (Validación) ---
    dot.node('S3', 'SÉPTIMO NIVEL: Estructura II\nFase: Diseño, IA y Validación', color='#9b59b6', fontsize='12')
    dot.node('S4', 'Validación Predictiva:\n- Modelado ETABS/SAP2000\n- Prototipo DMTP (Phyphox)\n- Análisis de Patologías (IA)', color='#9b59b6', fontsize='11')

    # --- NIVEL 4: LA EVIDENCIA CIENTÍFICA (El puente al exterior) ---
    dot.node('EVIDENCIA', 'EVIDENCIAS DEL PROCESO\nCertificado de Inducción + Artículo Científico\n(Responsorio del Tutor Socrático)', 
             color='#e67e22', shape='note', fontsize='11', width='5')

    # --- NIVEL 5: ECOSISTEMA EXTERNO (El Crecimiento) ---
    dot.node('EXT', 'ECOSISTEMA EXTERNO Y EMPLEABILIDAD\nEmpresas | GAD | SENESCYT\nProyectos Integradores (PIS) y Tesis', color='#d35400', fontsize='12', width='6')

    # --- CONEXIONES DEL ANDAMIAJE (La secuencia lógica) ---
    # 1. El estudiante se alimenta del ecosistema
    dot.edge('BASE', 'S1', label=' Asignación de Proyecto')
    
    # 2. Los insumos suben de Sexto a Séptimo
    dot.edge('S2', 'S3', label=' TRANSFERENCIA DE INSUMOS\n(Carga, geometría, algoritmos)')
    
    # 3. Séptimo genera la evidencia científica
    dot.edge('S4', 'EVIDENCIA', label=' Genera Producto Científico')
    
    # 4. La evidencia valida el paso al exterior
    dot.edge('EVIDENCIA', 'EXT', label=' Vinculación y Empleabilidad')

    # Generar imagen
    nombre_archivo = 'organigrama_andamiaje_ect_v2'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Organigrama de Enlace generado con secuencia lógica: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_organigrama_enlace()