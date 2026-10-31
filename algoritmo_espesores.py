"""
================================================================================
📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN
================================================================================
👤 AUTOR: Lorenzo Marcillo Merino
🏛️ APLICACIÓN: Proyecto multidisciplinario UNESUM - Jipijapa
📖 BASADO EN: Criterios de diseño estructural
================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================================
# 1. DEFINICIÓN DE CRITERIOS DE DISEÑO
# ============================================================================

CRITERIOS_LOSAS = [
    {'luz_max': 3.60, 'tipo': 'Alivianada', 'espesor_cm': 15, 'color': '#3498db'},
    {'luz_max': 4.80, 'tipo': 'Alivianada', 'espesor_cm': 20, 'color': '#2ecc71'},
    {'luz_max': 6.00, 'tipo': 'Alivianada', 'espesor_cm': 25, 'color': '#f39c12'},
    {'luz_max': float('inf'), 'tipo': 'Prefabricada / Viga secundaria', 'espesor_cm': None, 'color': '#e74c3c'}
]

# ============================================================================
# 2. FUNCIÓN PARA DETERMINAR EL TIPO DE LOSA
# ============================================================================

def determinar_tipo_losa(luz):
    """
    Determina el tipo de losa y espesor según la luz ingresada.
    
    Parámetros:
    - luz (float): Luz de la losa en metros
    
    Retorna:
    - dict: Diccionario con tipo, espesor y color
    """
    for criterio in CRITERIOS_LOSAS:
        if luz <= criterio['luz_max']:
            return {
                'tipo': criterio['tipo'],
                'espesor_cm': criterio['espesor_cm'],
                'color': criterio['color'],
                'luz_max': criterio['luz_max']
            }
    return None

# ============================================================================
# 3. FUNCIÓN PARA INGRESO DE DATOS
# ============================================================================

def ingresar_datos():
    """
    Permite al usuario ingresar una o más luces para analizar.
    """
    print("\n" + "=" * 60)
    print("📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN")
    print("=" * 60)
    print("\n📋 CRITERIOS DE DISEÑO:")
    print("-" * 50)
    print(f"{'Luz máxima (m)':<20} {'Tipo de losa':<25} {'Espesor (cm)':<15}")
    print("-" * 50)
    for c in CRITERIOS_LOSAS:
        if c['luz_max'] == float('inf'):
            print(f">{'6.00':<19} {c['tipo']:<25} {'---':<15}")
        else:
            print(f"≤ {c['luz_max']:<18.2f} {c['tipo']:<25} {c['espesor_cm']:<15}")
    print("-" * 50)
    
    print("\n📌 OPCIONES:")
    print("   1. Ingresar una sola luz")
    print("   2. Ingresar múltiples luces (separadas por comas)")
    print("   3. Ejemplo: 2.50, 3.60, 4.50, 5.20, 6.50")
    print("   4. Generar rango automático (2.0 a 7.0 m)")
    
    opcion = input("\nSeleccione una opción (1/2/3/4): ").strip()
    
    if opcion == '1':
        luz = float(input("Ingrese la luz de la losa (m): "))
        return [luz]
    
    elif opcion == '2':
        entrada = input("Ingrese las luces (separadas por comas): ")
        luces = [float(x.strip()) for x in entrada.split(',')]
        return luces
    
    elif opcion == '3':
        return [2.50, 3.60, 4.50, 5.20, 6.50]
    
    elif opcion == '4':
        inicio = float(input("Luz mínima (m): ") or "2.0")
        fin = float(input("Luz máxima (m): ") or "7.0")
        paso = float(input("Paso (m): ") or "0.5")
        return list(np.arange(inicio, fin + paso, paso))
    
    else:
        print("❌ Opción inválida. Usando valores de ejemplo.")
        return [2.50, 3.60, 4.50, 5.20, 6.50]

# ============================================================================
# 4. FUNCIÓN PARA MOSTRAR RESULTADOS
# ============================================================================

def mostrar_resultados(luces):
    """
    Muestra los resultados del predimensionamiento en formato tabla.
    """
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DEL PREDIMENSIONAMIENTO")
    print("=" * 70)
    print(f"{'Luz (m)':<12} {'Tipo de losa':<30} {'Espesor (cm)':<15} {'Recomendación':<25}")
    print("-" * 70)
    
    resultados = []
    for luz in luces:
        info = determinar_tipo_losa(luz)
        if info:
            if info['espesor_cm'] is None:
                espesor = '---'
                recomendacion = 'Usar prefabricada o viga secundaria'
            else:
                espesor = info['espesor_cm']
                recomendacion = f'Losa alivianada de {espesor} cm'
            
            resultados.append({
                'luz': luz,
                'tipo': info['tipo'],
                'espesor_cm': espesor,
                'recomendacion': recomendacion,
                'color': info['color']
            })
            
            print(f"{luz:<12.2f} {info['tipo']:<30} {espesor:<15} {recomendacion:<25}")
    
    print("=" * 70)
    return resultados

# ============================================================================
# 5. FUNCIÓN PARA GENERAR GRÁFICOS
# ============================================================================

def generar_graficos(resultados):
    """
    Genera gráficos de barras y de relación luz-espesor.
    """
    if not resultados:
        print("❌ No hay datos para graficar.")
        return
    
    # Preparar datos
    luces = [r['luz'] for r in resultados]
    espesores = [r['espesor_cm'] if r['espesor_cm'] != '---' else 0 for r in resultados]
    colores = [r['color'] for r in resultados]
    etiquetas = [f"{r['luz']:.2f}m\n{r['recomendacion'][:15]}..." if len(r['recomendacion']) > 15 else f"{r['luz']:.2f}m\n{r['recomendacion']}" for r in resultados]
    
    # Crear figura con dos subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('📊 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN', 
                 fontsize=16, fontweight='bold')
    
    # 6.1 Gráfico de barras: Espesor según luz
    bars = ax1.bar(range(len(luces)), espesores, color=colores, 
                   edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Añadir valores y etiquetas
    for i, (bar, esp, luz) in enumerate(zip(bars, espesores, luces)):
        if esp > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{esp} cm', ha='center', va='bottom', fontweight='bold', fontsize=10)
        else:
            ax1.text(bar.get_x() + bar.get_width()/2, 0.5,
                    'Prefabricada\nViga secundaria', ha='center', va='bottom', 
                    fontweight='bold', fontsize=8, color='red')
        
        ax1.text(bar.get_x() + bar.get_width()/2, -0.5,
                f'{luz:.2f} m', ha='center', va='top', fontsize=9)
    
    # Configuración del gráfico de barras
    ax1.set_ylabel('Espesor de losa (cm)', fontsize=12)
    ax1.set_xlabel('Luz de losa (m)', fontsize=12)
    ax1.set_title('Espesor Recomendado según Luz', fontsize=13, fontweight='bold')
    ax1.set_xticks([])  # Ocultar ticks de x
    ax1.set_ylim(0, max(espesores) * 1.3 + 5 if max(espesores) > 0 else 30)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Añadir líneas de referencia para los criterios
    for c in CRITERIOS_LOSAS[:-1]:  # Excluir el último (infinito)
        if c['espesor_cm']:
            ax1.axhline(y=c['espesor_cm'], color=c['color'], linestyle='--', 
                       alpha=0.5, linewidth=1, 
                       label=f"≤ {c['luz_max']:.2f}m → {c['espesor_cm']} cm")
    
    ax1.legend(loc='upper left', fontsize=9)
    
    # 6.2 Gráfico de relación Luz vs Espesor (curva escalonada)
    # Crear datos para la curva
    x_curva = [0, 3.60, 3.60, 4.80, 4.80, 6.00, 6.00, 7.50]
    y_curva = [15, 15, 20, 20, 25, 25, 0, 0]  # 0 representa prefabricada
    
    ax2.step(x_curva, y_curva, where='post', linewidth=3, color='purple', 
             label='Criterio de diseño')
    
    # Puntos de los resultados
    for r in resultados:
        esp = r['espesor_cm'] if r['espesor_cm'] != '---' else 0
        ax2.scatter(r['luz'], esp, color='red', s=100, zorder=5, 
                   edgecolor='black', linewidth=1.5)
        if esp > 0:
            ax2.annotate(f'{esp} cm', (r['luz'], esp), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold')
    
    # Configuración del gráfico de relación
    ax2.set_xlabel('Luz de losa (m)', fontsize=12)
    ax2.set_ylabel('Espesor de losa (cm)', fontsize=12)
    ax2.set_title('Relación Luz - Espesor', fontsize=13, fontweight='bold')
    ax2.set_xlim(1.5, 7.5)
    ax2.set_ylim(0, 35)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.legend(loc='upper left', fontsize=10)
    
    # Añadir zonas de diseño
    ax2.axvspan(0, 3.60, alpha=0.1, color='#3498db', label='Zona: 15 cm')
    ax2.axvspan(3.60, 4.80, alpha=0.1, color='#2ecc71', label='Zona: 20 cm')
    ax2.axvspan(4.80, 6.00, alpha=0.1, color='#f39c12', label='Zona: 25 cm')
    ax2.axvspan(6.00, 7.50, alpha=0.1, color='#e74c3c', label='Prefabricada / Viga')
    
    # Guardar gráfico
    carpeta = Path.cwd() / 'Resultados_Losas'
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"predimensionamiento_losas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(carpeta / nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico guardado: {carpeta / nombre_archivo}")
    
    plt.tight_layout()
    plt.show()
    
    return fig

# ============================================================================
# 6. FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal del programa.
    """
    print("=" * 70)
    print("🏗️ PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN")
    print("   PROYECTO MULTIDISCIPLINARIO UNESUM - JIPIJAPA")
    print("=" * 70)
    
    # Ingresar datos
    luces = ingresar_datos()
    
    # Mostrar resultados
    resultados = mostrar_resultados(luces)
    
    # Generar gráficos
    if resultados:
        generar_graficos(resultados)
    
    # Guardar reporte
    guardar_reporte(resultados)
    
    print("\n" + "=" * 70)
    print("✅ PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)

# ============================================================================
# 7. FUNCIÓN PARA GUARDAR REPORTE
# ============================================================================

def guardar_reporte(resultados):
    """
    Guarda los resultados en un archivo de texto.
    """
    carpeta = Path.cwd() / 'Resultados_Losas'
    carpeta.mkdir(parents=True, exist_ok=True)
    
    nombre_archivo = f"reporte_losas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    ruta = carpeta / nombre_archivo
    
    with open(ruta, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN\n")
        f.write("=" * 70 + "\n")
        f.write(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🏛️ Proyecto: UNESUM - Jipijapa\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("📊 RESULTADOS:\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'Luz (m)':<12} {'Tipo de losa':<30} {'Espesor (cm)':<15} {'Recomendación':<25}\n")
        f.write("-" * 70 + "\n")
        
        for r in resultados:
            esp = r['espesor_cm'] if r['espesor_cm'] != '---' else '---'
            f.write(f"{r['luz']:<12.2f} {r['tipo']:<30} {esp:<15} {r['recomendacion']:<25}\n")
        
        f.write("=" * 70 + "\n")
    
    print(f"\n✅ Reporte guardado: {ruta}")

# ============================================================================
# 8. EJECUCIÓN DEL SCRIPT
# ============================================================================

if __name__ == "__main__":
    main()