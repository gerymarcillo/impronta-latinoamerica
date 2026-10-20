# -*- coding: utf-8 -*-
"""
M07.67 — ORGANIGRAMA METODOLÓGICO DEL SEMILLERO DE INNOVACIÓN
"""
import os
import graphviz

# Ruta de Graphviz (ajusta si es necesario en tu PC)
ruta_graphviz = r'C:\Program Files\Graphviz\bin'
if not os.path.exists(ruta_graphviz):
    ruta_graphviz = r'C:\Users\geryl\AppData\Local\Programs\Graphviz\bin'
os.environ["PATH"] += os.pathsep + ruta_graphviz

def generar_organigrama():
    # Configuración del gráfico (De arriba hacia abajo)
    dot = graphviz.Digraph(comment='Organigrama ECT-UNESUM', format='png')
    dot.attr(rankdir='TB', size='14,18', nodesep='0.5', ranksep='0.8')
    
    # Estilos generales (CORREGIDO: números como strings)
    dot.attr('node', shape='box', style='filled,rounded', fontname='Arial', fontcolor='white', margin='0.3')
    dot.attr('edge', color='#34495e', penwidth='2')

    # --- NIVEL 1: EL ORIGEN ---
    dot.node('N1', 'FASE 1: RECOLECCIÓN E INVESTIGACIÓN\n(Materiales Locales en Manabí)\n• Caucho de neumáticos (NFU)\n• Caucho butílico (cámaras)\n• Látex natural', 
             fillcolor='#16a085', fontsize='14', shape='folder')

    # --- NIVEL 2: LOS DOS CAMINOS ---
    dot.node('N2A', 'FASE 2A: PROTOTIPO DMTP\n(Superestructura)', fillcolor='#e74c3c', fontsize='14')
    dot.node('N2B', 'FASE 2B: AISLADOR DE CAUCHO\n(Cimentación)', fillcolor='#8e44ad', fontsize='14')

    # --- NIVEL 3: DISEÑO Y CÁLCULO ---
    dot.node('N3A', 'Diseño Viscoelástico\n• Tensor-puntal (50 cm)\n• 4 disipadores por esquina\n• Núcleo polimérico', fillcolor='#c0392b', fontsize='12')
    dot.node('N3B', 'Diseño Elastomérico\n• Capas de caucho y acero\n• Diseño aproximado de cargas\n• Rigidez horizontal (K)', fillcolor='#6c3483', fontsize='12')

    # --- NIVEL 4: ENSAYOS DE LABORATORIO ---
    dot.node('N4A', 'Ensayos del DMTP\n• Compresión cíclica (probeta)\n• Histéresis del prototipo 1:5\n• Medición de energía disipada', fillcolor='#e67e22', fontsize='12')
    dot.node('N4B', 'Ensayos del Aislador\n• Compresión vertical (peso)\n• Corte horizontal (sismo)\n• Medición de deformación', fillcolor='#d35400', fontsize='12')

    # --- NIVEL 5: ANÁLISIS COMPUTACIONAL AVANZADO (SOLO PARA EL AISLADOR) ---
    dot.node('N5B_1', 'Monte Carlo\n(Incertidumbre del caucho reciclado)', fillcolor='#2980b9', fontsize='11')
    dot.node('N5B_2', 'Cadenas de Markov\n(Daño progresivo por réplicas)', fillcolor='#2980b9', fontsize='11')
    dot.node('N5B_3', 'Fibonacci\n(Optimización de espesores de capas)', fillcolor='#2980b9', fontsize='11')
    dot.node('N5B_4', 'Machine Learning\n(Red Neuronal para predecir fallas)', fillcolor='#2980b9', fontsize='11')

    # --- NIVEL 6: EL PRODUCTO FINAL ---
    dot.node('N6', 'PLATAFORMA ECT-UNESUM-2026\nIntegración de Resultados\n(Formatos para SENADI y CACES)', 
             fillcolor='#2c3e50', fontsize='15', shape='doubleoctagon')

    # ==========================================
    # CONEXIONES (FLECHAS)
    # ==========================================
    dot.edge('N1', 'N2A')
    dot.edge('N1', 'N2B')

    dot.edge('N2A', 'N3A')
    dot.edge('N2B', 'N3B')

    dot.edge('N3A', 'N4A')
    dot.edge('N3B', 'N4B')

    # Conexiones del Aislador hacia la IA
    dot.edge('N4B', 'N5B_1')
    dot.edge('N4B', 'N5B_2')
    dot.edge('N4B', 'N5B_3')
    dot.edge('N4B', 'N5B_4')

    # Unir todo al final
    dot.edge('N4A', 'N6', label=' Datos DMTP ')
    dot.edge('N5B_1', 'N6')
    dot.edge('N5B_2', 'N6')
    dot.edge('N5B_3', 'N6')
    dot.edge('N5B_4', 'N6', label=' Predicciones IA ')

    # Generar archivo
    nombre_archivo = 'M07_67_organigrama_semillero_ect'
    dot.render(nombre_archivo, view=True, cleanup=True)
    print(f"✅ Organigrama generado con éxito: {nombre_archivo}.png")

if __name__ == "__main__":
    generar_organigrama()