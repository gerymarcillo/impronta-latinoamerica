"""
================================================================================
📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN
================================================================================
👤 AUTOR: Lorenzo Marcillo Merino
🏛️ APLICACIÓN: Proyecto multidisciplinario UNESUM - Jipijapa
📖 BASADO EN: Criterios de diseño estructural y NEC-15
================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================================
# 1. DEFINICIÓN DE CRITERIOS DE DISEÑO (SEGÚN M01 Y NEC-15)
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
# 3. FUNCIÓN PARA INGRESO DE DATOS (CON ARTICULACIÓN AL M02)
# ============================================================================

def ingresar_datos():
    """
    Permite al usuario ingresar la luz y el tipo de uso del territorio.
    """
    print("\n" + "=" * 60)
    print("📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN")
    print("   PROYECTO UNESUM - JIPIJAPA")
    print("=" * 60)
    print("\n📋 CRITERIOS DE DISEÑO (M01):")
    print("-" * 50)
    print(f"{'Luz máxima (m)':<20} {'Tipo de losa':<25} {'Espesor (cm)':<15}")
    print("-" * 50)
    for c in CRITERIOS_LOSAS:
        if c['luz_max'] == float('inf'):
            print(f">{'6.00':<19} {c['tipo']:<25} {'---':<15}")
        else:
            print(f"≤ {c['luz_max']:<18.2f} {c['tipo']:<25} {c['espesor_cm']:<15}")
    print("-" * 50)
    
    print("\n📌 TIPO DE USO (Articulación con M02):")
    print("   1. Aulas / Escuela (Cv = 0.29 t/m²)")
    print("   2. Hospital / Centro de Salud (Cv = 0.50 t/m²)")
    print("   3. Vivienda / Oficina (Cv = 0.25 t/m²)")
    opcion_uso = input("\nSeleccione el uso (1/2/3): ").strip()
    
    cv = 0.29 # Default Aulas
    if opcion_uso == '2':
        cv = 0.50
    elif opcion_uso == '3':
        cv = 0.25

    luces = []
    print("\n📌 OPCIONES DE LUZ:")
    print("   1. Ingresar una sola luz")
    print("   2. Ingresar múltiples luces (separadas por comas)")
    print("   3. Ejemplo: 2.50, 3.60, 4.50, 5.20, 6.50")
    print("   4. Generar rango automático (2.0 a 7.0 m)")
    
    opcion_luz = input("\nSeleccione una opción (1/2/3/4): ").strip()
    
    if opcion_luz == '1':
        luz = float(input("Ingrese la luz de la losa (m): "))
        luces = [luz]
    elif opcion_luz == '2':
        entrada = input("Ingrese las luces (separadas por comas): ")
        luces = [float(x.strip()) for x in entrada.split(',')]
    elif opcion_luz == '3':
        luces = [2.50, 3.60, 4.50, 5.20, 6.50]
    elif opcion_luz == '4':
        inicio = float(input("Luz mínima (m): ") or "2.0")
        fin = float(input("Luz máxima (m): ") or "7.0")
        paso = float(input("Paso (m): ") or "0.5")
        luces = list(np.arange(inicio, fin + paso, paso))
    else:
        print("❌ Opción inválida. Usando valores de ejemplo.")
        luces = [2.50, 3.60, 4.50, 5.20, 6.50]
        
    return luces, cv

# ============================================================================
# 4. FUNCIÓN PARA MOSTRAR RESULTADOS (CON CÁLCULO DE CARGAS)
# ============================================================================

def mostrar_resultados(luces, cv):
    """
    Muestra los resultados del predimensionamiento en formato tabla y calcula cargas.
    """
    print("\n" + "=" * 80)
    print("📊 RESULTADOS DEL PREDIMENSIONAMIENTO Y CARGAS (NEC-15)")
    print("=" * 80)
    print(f"{'Luz (m)':<10} {'Tipo de losa':<25} {'Espesor (cm)':<15} {'Cm (t/m²)':<12} {'Cv (t/m²)':<12} {'Cu (t/m²)':<12}")
    print("-" * 80)
    
    resultados = []
    for luz in luces:
        info = determinar_tipo_losa(luz)
        if info:
            if info['espesor_cm'] is None:
                espesor = '---'
                cm = 0
                cu = 0
                recomendacion = 'Usar prefabricada o viga secundaria'
            else:
                espesor = info['espesor_cm']
                # Cálculo de Carga Muerta (Cm) aproximada: Peso propio + Acabados
                peso_propio = (espesor * 15) / 1000 # Aproximación
                cm = peso_propio + 0.26 # Acabados 0.26 t/m²
                # Cálculo de Carga Última (Cu): 1.4*Cm + 1.7*Cv
                cu = (1.4 * cm) + (1.7 * cv)
                recomendacion = f'Losa alivianada de {espesor} cm'
            
            resultados.append({
                'luz': luz,
                'tipo': info['tipo'],
                'espesor_cm': espesor,
                'cm': cm,
                'cv': cv,
                'cu': cu,
                'recomendacion': recomendacion,
                'color': info['color']
            })
            
            print(f"{luz:<10.2f} {info['tipo']:<25} {str(espesor):<15} {cm:<12.2f} {cv:<12.2f} {cu:<12.2f}")
    
    print("=" * 80)
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
    
    luces = [r['luz'] for r in resultados]
    espesores = [r['espesor_cm'] if r['espesor_cm'] != '---' else 0 for r in resultados]
    colores = [r['color'] for r in resultados]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('📊 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN', fontsize=16, fontweight='bold')
    
    # Gráfico de barras
    bars = ax1.bar(range(len(luces)), espesores, color=colores, edgecolor='black', linewidth=1.5, alpha=0.85)
    for i, (bar, esp, luz) in enumerate(zip(bars, espesores, luces)):
        if esp > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{esp} cm', ha='center', va='bottom', fontweight='bold', fontsize=10)
        else:
            ax1.text(bar.get_x() + bar.get_width()/2, 0.5, 'Prefabricada\nViga secundaria', ha='center', va='bottom', fontweight='bold', fontsize=8, color='red')
        ax1.text(bar.get_x() + bar.get_width()/2, -0.5, f'{luz:.2f} m', ha='center', va='top', fontsize=9)
    
    ax1.set_ylabel('Espesor de losa (cm)', fontsize=12)
    ax1.set_xlabel('Luz de losa (m)', fontsize=12)
    ax1.set_title('Espesor Recomendado según Luz', fontsize=13, fontweight='bold')
    ax1.set_xticks([])
    ax1.set_ylim(0, max(espesores) * 1.3 + 5 if max(espesores) > 0 else 30)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)
    
    for c in CRITERIOS_LOSAS[:-1]:
        if c['espesor_cm']:
            ax1.axhline(y=c['espesor_cm'], color=c['color'], linestyle='--', alpha=0.5, linewidth=1, label=f"≤ {c['luz_max']:.2f}m → {c['espesor_cm']} cm")
    ax1.legend(loc='upper left', fontsize=9)
    
    # Gráfico de relación
    x_curva = [0, 3.60, 3.60, 4.80, 4.80, 6.00, 6.00, 7.50]
    y_curva = [15, 15, 20, 20, 25, 25, 0, 0]
    ax2.step(x_curva, y_curva, where='post', linewidth=3, color='purple', label='Criterio de diseño')
    
    for r in resultados:
        esp = r['espesor_cm'] if r['espesor_cm'] != '---' else 0
        ax2.scatter(r['luz'], esp, color='red', s=100, zorder=5, edgecolor='black', linewidth=1.5)
        if esp > 0:
            ax2.annotate(f'{esp} cm', (r['luz'], esp), xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('Luz de losa (m)', fontsize=12)
    ax2.set_ylabel('Espesor de losa (cm)', fontsize=12)
    ax2.set_title('Relación Luz - Espesor', fontsize=13, fontweight='bold')
    ax2.set_xlim(1.5, 7.5)
    ax2.set_ylim(0, 35)
    ax2.grid(True, linestyle='--', alpha=0.3)
    ax2.legend(loc='upper left', fontsize=10)
    ax2.axvspan(0, 3.60, alpha=0.1, color='#3498db', label='Zona: 15 cm')
    ax2.axvspan(3.60, 4.80, alpha=0.1, color='#2ecc71', label='Zona: 20 cm')
    ax2.axvspan(4.80, 6.00, alpha=0.1, color='#f39c12', label='Zona: 25 cm')
    ax2.axvspan(6.00, 7.50, alpha=0.1, color='#e74c3c', label='Prefabricada / Viga')
    
    carpeta = Path.cwd() / 'Resultados_Losas'
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"predimensionamiento_losas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(carpeta / nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico guardado: {carpeta / nombre_archivo}")
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# 6. FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print("=" * 70)
    print("🏗️ PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN")
    print("   PROYECTO MULTIDISCIPLINARIO UNESUM - JIPIJAPA")
    print("=" * 70)
    
    luces, cv = ingresar_datos()
    resultados = mostrar_resultados(luces, cv)
    
    if resultados:
        generar_graficos(resultados)
    
    guardar_reporte(resultados)

# ============================================================================
# 7. FUNCIÓN PARA GUARDAR REPORTE
# ============================================================================

def guardar_reporte(resultados):
    carpeta = Path.cwd() / 'Resultados_Losas'
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"reporte_losas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    ruta = carpeta / nombre_archivo
    
    with open(ruta, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("📐 PREDIMENSIONAMIENTO DE LOSAS DE HORMIGÓN Y CARGAS\n")
        f.write("=" * 80 + "\n")
        f.write(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🏛️ Proyecto: UNESUM - Jipijapa\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("📊 RESULTADOS:\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Luz (m)':<10} {'Tipo de losa':<25} {'Espesor (cm)':<15} {'Cm (t/m²)':<12} {'Cv (t/m²)':<12} {'Cu (t/m²)':<12}\n")
        f.write("-" * 80 + "\n")
        
        for r in resultados:
            esp = r['espesor_cm'] if r['espesor_cm'] != '---' else '---'
            f.write(f"{r['luz']:<10.2f} {r['tipo']:<25} {str(esp):<15} {r['cm']:<12.2f} {r['cv']:<12.2f} {r['cu']:<12.2f}\n")
        
        f.write("=" * 80 + "\n")
    
    print(f"\n✅ Reporte guardado: {ruta}")

# ============================================================================
# 8. EJECUCIÓN DEL SCRIPT
# ============================================================================

if __name__ == "__main__":
    main()
