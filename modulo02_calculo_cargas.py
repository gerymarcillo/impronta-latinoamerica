# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 02 — ANÁLISIS DE CARGAS SEGÚN USO (DASHBOARD MEJORADO)
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
🎯 OBJETIVO: Dashboard con resumen gráfico indexado + comparación de usos
            CORREGIDO: Muestra la gráfica en pantalla al correr
================================================================================
"""

import os
import sys
from datetime import datetime

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("⚠️ matplotlib no está instalado. Ejecute: pip install matplotlib")

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "ANÁLISIS DE CARGAS SEGÚN USO (NEC-15)"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los números son solo el vehículo. El verdadero ingeniero interpreta, decide, contextualiza, se responsabiliza."

# ============================================================================
# 2. DATOS DEL MODELO BASE (PPT — 2 PISOS)
# ============================================================================

DATOS_MODELO = {
    "Lv1": 6.00, "Lv2": 5.50, "Lv3": 6.30,
    "Lt1": 4.80, "Lt2": 5.50, "Lt3": 5.00, "Lt4": 6.10,
    "pisos": 2,
    "H_losa": 25, "bn": 10, "bb": 40, "tc": 5,
    "Fm": 1.2, "b_col": 0.38,
    "fc": 210, "fy": 4200
}

# ============================================================================
# 3. EJEMPLO OFICIAL DEL PROYECTO
# ============================================================================

EJEMPLO_PROYECTO = {
    "uso": "Vivienda",
    "mamposteria": "Pesada",
    "Cm": 0.64,
    "Cv": 0.20,
    "Cu": 1.088,
    "W": 6.256,
    "At": 35.39,
    "Pu": 90.44
}

# ============================================================================
# 4. CRITERIOS DE PREDIMENSIONAMIENTO DE LOSA (NEC-15)
# ============================================================================

CRITERIOS_LOSA = [
    {"luz_max": 3.60, "espesor_cm": 15, "peso_t_m2": 0.25},
    {"luz_max": 4.80, "espesor_cm": 20, "peso_t_m2": 0.30},
    {"luz_max": 6.00, "espesor_cm": 25, "peso_t_m2": 0.36},
    {"luz_max": float('inf'), "espesor_cm": None, "peso_t_m2": None}
]

# ============================================================================
# 5. TIPOS DE USO SEGÚN NEC-15 (TABLA 9)
# ============================================================================

USOS_NEC15 = [
    {"codigo": 1,  "nombre": "Vivienda", "Cv": 0.20, "es_ejemplo": True},
    {"codigo": 2,  "nombre": "Oficinas", "Cv": 0.24, "es_ejemplo": False},
    {"codigo": 3,  "nombre": "Aulas", "Cv": 0.29, "es_ejemplo": False},
    {"codigo": 4,  "nombre": "Bodega liviana", "Cv": 0.60, "es_ejemplo": False},
    {"codigo": 5,  "nombre": "Bodega pesada", "Cv": 1.20, "es_ejemplo": False},
    {"codigo": 6,  "nombre": "Pasillos", "Cv": 0.48, "es_ejemplo": False},
    {"codigo": 7,  "nombre": "Cubierta inaccesible", "Cv": 0.07, "es_ejemplo": False},
    {"codigo": 8,  "nombre": "Terraza", "Cv": 0.30, "es_ejemplo": False},
    {"codigo": 9,  "nombre": "Áreas de reunión", "Cv": 0.29, "es_ejemplo": False},
    {"codigo": 10, "nombre": "Comedores", "Cv": 0.48, "es_ejemplo": False}
]

# ============================================================================
# 6. COMPONENTES DE CARGA MUERTA
# ============================================================================

COMPONENTES_CM = {
    "acabado_superior": 0.04,
    "acabado_inferior": 0.04,
    "instalaciones": 0.02,
    "mamposteria_pesada": 0.18,
    "mamposteria_liviana": 0.09
}

# ============================================================================
# 7. FUNCIONES
# ============================================================================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_header():
    print("=" * 70)
    print(f"[M02] {TITULO}")
    print(f"[PROYECTO] {PROYECTO}")
    print(f"[DOCENTE] {DOCENTE}")
    print("=" * 70)

def predimensionar_losa(luz):
    for criterio in CRITERIOS_LOSA:
        if luz <= criterio["luz_max"]:
            if criterio["espesor_cm"] is None:
                return {"tipo": "Prefabricada / Viga secundaria", "espesor_cm": None, "peso_t_m2": None}
            return {"tipo": "Alivianada", "espesor_cm": criterio["espesor_cm"], "peso_t_m2": criterio["peso_t_m2"]}
    return None

def seleccionar_uso():
    print("\n[SELECCIONE EL TIPO DE USO (NEC-15, Tabla 9)]")
    print("-" * 65)
    print(f"  {'COD':<5} {'USO':<40} {'Cv (t/m2)':<10} {'ESTADO':<10}")
    print("-" * 65)
    for uso in USOS_NEC15:
        estado = "EJEMPLO" if uso["es_ejemplo"] else "Calcular"
        print(f"  [{uso['codigo']:2d}] {uso['nombre']:<40} {uso['Cv']:<10.2f} {estado:<10}")
    print("-" * 65)
    print("El ejemplo del proyecto es VIVIENDA (opcion 1)")
    print("Si elige otro uso, debera calcular con la guia M02")
    print("-" * 65)
    while True:
        try:
            opcion = int(input("\nOpcion (1-10): ").strip())
            for uso in USOS_NEC15:
                if uso["codigo"] == opcion:
                    return uso
            print("Opcion invalida.")
        except ValueError:
            print("Ingrese un numero valido.")

def seleccionar_mamposteria():
    print("\n[SELECCIONE EL TIPO DE MAMPOSTERIA]")
    print("-" * 60)
    print("  [1] Pesada (bloque/ladrillo)  -> 0.18 t/m2  EJEMPLO")
    print("  [2] Liviana (gypsum/steel)    -> 0.09 t/m2  Calcular")
    print("-" * 60)
    while True:
        try:
            opcion = int(input("\nOpcion (1-2): ").strip())
            if opcion == 1:
                return {"tipo": "Pesada (bloque/ladrillo)", "peso": 0.18, "es_ejemplo": True}
            elif opcion == 2:
                return {"tipo": "Liviana (gypsum/steel)", "peso": 0.09, "es_ejemplo": False}
            print("Opcion invalida.")
        except ValueError:
            print("Ingrese un numero valido.")

def calcular_cargas(luz, uso, mamposteria):
    losa = predimensionar_losa(luz)
    if losa["peso_t_m2"] is None:
        return None
    Cm = losa["peso_t_m2"] + COMPONENTES_CM["acabado_superior"] + \
         COMPONENTES_CM["acabado_inferior"] + COMPONENTES_CM["instalaciones"] + \
         mamposteria["peso"]
    Cv = uso["Cv"]
    Cu = 1.2 * Cm + 1.6 * Cv
    b_trib = DATOS_MODELO["Lt2"]
    W = Cu * b_trib
    At = (DATOS_MODELO["Lv1"]/2 + DATOS_MODELO["Lv2"]/2) * \
         (DATOS_MODELO["Lt1"]/2 + DATOS_MODELO["Lt2"]/2)
    Pu = At * Cu * DATOS_MODELO["Fm"]
    return {"losa": losa, "Cm": Cm, "Cv": Cv, "Cu": Cu,
            "W": W, "At": At, "Pu": Pu, "b_trib": b_trib}

def verificar_coincidencia(uso, mamposteria, resultados):
    coincide_uso = uso["es_ejemplo"]
    coincide_mamp = mamposteria["es_ejemplo"]
    if coincide_uso and coincide_mamp:
        if abs(resultados["Cm"] - EJEMPLO_PROYECTO["Cm"]) < 0.001 and \
           abs(resultados["Cu"] - EJEMPLO_PROYECTO["Cu"]) < 0.001:
            return {"coincide": True, "mensaje": "COINCIDE CON EL EJEMPLO DEL PROYECTO"}
        else:
            return {"coincide": False, "mensaje": "Los valores no coinciden exactamente"}
    else:
        return {
            "coincide": False,
            "mensaje": "USTED ELIGIO UN USO DIFERENTE AL EJEMPLO.\n"
                       "   Debe calcular con la guia M02 y verificar los resultados.\n"
                       "   El ejemplo del proyecto es: VIVIENDA + MAMPOSTERIA PESADA"
        }

def mostrar_resultados(uso, mamposteria, resultados, verificacion):
    print("\n" + "=" * 70)
    print("[RESULTADOS DEL ANALISIS DE CARGAS]")
    print("=" * 70)
    print(f"\n[DATOS DEL PROYECTO]")
    print(f"   Proyecto     : {PROYECTO}")
    print(f"   Modelo       : Edificacion de {DATOS_MODELO['pisos']} pisos")
    print(f"   Lv1 = {DATOS_MODELO['Lv1']:.2f} m | Lv2 = {DATOS_MODELO['Lv2']:.2f} m | Lv3 = {DATOS_MODELO['Lv3']:.2f} m")
    print(f"   Lt1 = {DATOS_MODELO['Lt1']:.2f} m | Lt2 = {DATOS_MODELO['Lt2']:.2f} m | Lt3 = {DATOS_MODELO['Lt3']:.2f} m | Lt4 = {DATOS_MODELO['Lt4']:.2f} m")
    print(f"\n[USO SELECCIONADO]")
    print(f"   {uso['nombre']} | Cv = {uso['Cv']:.2f} t/m2")
    print(f"\n[MAMPOSTERIA]")
    print(f"   {mamposteria['tipo']} | Peso = {mamposteria['peso']:.2f} t/m2")
    print(f"\n[PREDIMENSIONAMIENTO DE LOSA]")
    print(f"   Luz de calculo : {DATOS_MODELO['Lv2']:.2f} m")
    print(f"   Tipo           : {resultados['losa']['tipo']}")
    print(f"   Espesor        : {resultados['losa']['espesor_cm']} cm")
    print(f"   Peso           : {resultados['losa']['peso_t_m2']:.2f} t/m2")
    print(f"\n[CARGA MUERTA (Cm)]")
    print(f"   Losa           : {resultados['losa']['peso_t_m2']:.2f} t/m2")
    print(f"   Acab. superior : {COMPONENTES_CM['acabado_superior']:.2f} t/m2")
    print(f"   Acab. inferior : {COMPONENTES_CM['acabado_inferior']:.2f} t/m2")
    print(f"   Instalaciones  : {COMPONENTES_CM['instalaciones']:.2f} t/m2")
    print(f"   Mamposteria    : {mamposteria['peso']:.2f} t/m2")
    print(f"   -----------------------------")
    print(f"   Cm TOTAL       : {resultados['Cm']:.3f} t/m2")
    print(f"\n[CARGA VIVA (Cv)]")
    print(f"   {uso['nombre']} : {resultados['Cv']:.2f} t/m2")
    print(f"\n[CARGA ULTIMA (Cu)]")
    print(f"   Cu = 1.2*Cm + 1.6*Cv")
    print(f"   Cu = 1.2*{resultados['Cm']:.3f} + 1.6*{resultados['Cv']:.2f}")
    print(f"   Cu = {1.2*resultados['Cm']:.3f} + {1.6*resultados['Cv']:.3f}")
    print(f"   Cu = {resultados['Cu']:.3f} t/m2")
    print(f"\n[CARGAS PARA LA SIGUIENTE FASE (M03)]")
    print(f"   W  = {resultados['W']:.3f} t/m")
    print(f"   At = {resultados['At']:.3f} m2")
    print(f"   Pu = {resultados['Pu']:.3f} t")
    print(f"   Cu = {resultados['Cu']:.3f} t/m2")
    print("\n" + "=" * 70)
    print(f"[VERIFICACION]")
    print(f"   {verificacion['mensaje']}")
    print("=" * 70)
    if verificacion["coincide"]:
        print("\n[COMPARACION CON EL EJEMPLO DEL PROYECTO]")
        print(f"   {'Variable':<10} {'Ejemplo':<15} {'Calculado':<15} {'Estado':<10}")
        print(f"   {'-'*50}")
        print(f"   {'Cm':<10} {EJEMPLO_PROYECTO['Cm']:<15.3f} {resultados['Cm']:<15.3f} {'OK' if abs(resultados['Cm']-EJEMPLO_PROYECTO['Cm'])<0.001 else 'X':<10}")
        print(f"   {'Cv':<10} {EJEMPLO_PROYECTO['Cv']:<15.3f} {resultados['Cv']:<15.3f} {'OK' if abs(resultados['Cv']-EJEMPLO_PROYECTO['Cv'])<0.001 else 'X':<10}")
        print(f"   {'Cu':<10} {EJEMPLO_PROYECTO['Cu']:<15.3f} {resultados['Cu']:<15.3f} {'OK' if abs(resultados['Cu']-EJEMPLO_PROYECTO['Cu'])<0.001 else 'X':<10}")
    print("\n" + "=" * 70)
    print(f"Frase: {FRASE}")
    print("=" * 70)

def guardar_reporte(uso, mamposteria, resultados, verificacion):
    carpeta = "Resultados_M02"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre = f"reporte_M02_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"[M02] {TITULO}\n")
        f.write(f"[PROYECTO] {PROYECTO}\n")
        f.write(f"[DOCENTE] {DOCENTE}\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"USO: {uso['nombre']} (Cv = {uso['Cv']:.2f} t/m2)\n")
        f.write(f"MAMPOSTERIA: {mamposteria['tipo']} ({mamposteria['peso']:.2f} t/m2)\n\n")
        f.write(f"CARGA MUERTA (Cm) = {resultados['Cm']:.3f} t/m2\n")
        f.write(f"CARGA VIVA (Cv)   = {resultados['Cv']:.3f} t/m2\n")
        f.write(f"CARGA ULTIMA (Cu) = {resultados['Cu']:.3f} t/m2\n\n")
        f.write(f"CARGAS PARA M03:\n")
        f.write(f"   W  = {resultados['W']:.3f} t/m\n")
        f.write(f"   At = {resultados['At']:.3f} m2\n")
        f.write(f"   Pu = {resultados['Pu']:.3f} t\n\n")
        f.write(f"VERIFICACION: {verificacion['mensaje']}\n\n")
        f.write("=" * 70 + "\n")
        f.write(f"Frase: {FRASE}\n")
        f.write("=" * 70 + "\n")
    print(f"\nReporte guardado: {ruta}")

def generar_dashboard(uso, mamposteria, resultados, verificacion):
    """Genera el dashboard con resumen grafico indexado."""
    if not MATPLOTLIB_OK:
        print("No se puede generar el dashboard.")
        return
    carpeta = "Resultados_M02"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Calcular Cu para todos los usos (con la misma mamposteria)
    usos_nombres = [u["nombre"] for u in USOS_NEC15]
    usos_cu = []
    for u in USOS_NEC15:
        cm_temp = resultados['losa']['peso_t_m2'] + COMPONENTES_CM["acabado_superior"] + \
                  COMPONENTES_CM["acabado_inferior"] + COMPONENTES_CM["instalaciones"] + \
                  mamposteria['peso']
        usos_cu.append(1.2 * cm_temp + 1.6 * u["Cv"])
    
    # Colores: verde para el ejemplo, azul para los demás
    colores_usos = ['#2ecc71' if u["es_ejemplo"] else '#3498db' for u in USOS_NEC15]
    
    # Crear figura con grid 2x3
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle(f'DASHBOARD M02 - ANALISIS DE CARGAS\n{PROYECTO}', 
                 fontsize=18, fontweight='bold', color='#2c3e50')
    
    # ============================================================
    # SUBGRÁFICO 1: Torta de composición de Cm
    # ============================================================
    ax1 = fig.add_subplot(2, 3, 1)
    labels_cm = ['Losa', 'Acab. sup.', 'Acab. inf.', 'Instal.', 'Mamposteria']
    sizes_cm = [resultados['losa']['peso_t_m2'], COMPONENTES_CM['acabado_superior'],
                COMPONENTES_CM['acabado_inferior'], COMPONENTES_CM['instalaciones'],
                mamposteria['peso']]
    colors_cm = ['#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#e74c3c']
    wedges, texts, autotexts = ax1.pie(sizes_cm, labels=labels_cm, autopct='%1.1f%%', 
                                        colors=colors_cm, startangle=90, 
                                        textprops={'fontsize': 9})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    ax1.set_title(f'Composicion de Cm = {resultados["Cm"]:.3f} t/m2', 
                  fontsize=12, fontweight='bold')
    
    # ============================================================
    # SUBGRÁFICO 2: Barras Cm vs Cv vs Cu
    # ============================================================
    ax2 = fig.add_subplot(2, 3, 2)
    categorias = ['Cm', 'Cv', 'Cu']
    valores = [resultados['Cm'], resultados['Cv'], resultados['Cu']]
    colores = ['#3498db', '#2ecc71', '#e74c3c']
    bars = ax2.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5)
    for bar, val in zip(bars, valores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Carga (t/m2)', fontsize=11)
    ax2.set_title('Comparacion Cm vs Cv vs Cu', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_ylim(0, max(valores) * 1.3)
    
    # ============================================================
    # SUBGRÁFICO 3: Desglose de Cu
    # ============================================================
    ax3 = fig.add_subplot(2, 3, 3)
    labels_cu = ['1.2*Cm', '1.6*Cv']
    sizes_cu = [1.2 * resultados['Cm'], 1.6 * resultados['Cv']]
    colors_cu = ['#3498db', '#2ecc71']
    bars3 = ax3.barh(labels_cu, sizes_cu, color=colors_cu, edgecolor='black', linewidth=1.5)
    for bar, val in zip(bars3, sizes_cu):
        ax3.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.3f} t/m2', ha='left', va='center', fontweight='bold', fontsize=11)
    ax3.set_xlabel('Carga (t/m2)', fontsize=11)
    ax3.set_title(f'Desglose de Cu = {resultados["Cu"]:.3f} t/m2', 
                  fontsize=12, fontweight='bold')
    ax3.grid(axis='x', linestyle='--', alpha=0.3)
    ax3.set_xlim(0, max(sizes_cu) * 1.3)
    
    # ============================================================
    # SUBGRÁFICO 4: Comparación de los 10 usos
    # ============================================================
    ax4 = fig.add_subplot(2, 3, 4)
    x_pos = np.arange(len(usos_nombres))
    bars4 = ax4.bar(x_pos, usos_cu, color=colores_usos, edgecolor='black', linewidth=1)
    for bar, val in zip(bars4, usos_cu):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(usos_nombres, rotation=45, ha='right', fontsize=8)
    ax4.set_ylabel('Cu (t/m2)', fontsize=11)
    ax4.set_title('Comparacion de Cu para los 10 Usos (NEC-15)', 
                  fontsize=12, fontweight='bold')
    ax4.grid(axis='y', linestyle='--', alpha=0.3)
    ax4.axhline(y=resultados['Cu'], color='red', linestyle='--', 
                linewidth=2, label=f'Uso seleccionado: {resultados["Cu"]:.3f}')
    ax4.axhline(y=EJEMPLO_PROYECTO['Cu'], color='green', linestyle=':', 
                linewidth=2, label=f'Ejemplo: {EJEMPLO_PROYECTO["Cu"]:.3f}')
    ax4.legend(fontsize=9)
    
    # ============================================================
    # SUBGRÁFICO 5: Semáforo de decisión
    # ============================================================
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.axis('off')
    
    if verificacion["coincide"]:
        color_semaforo = '#2ecc71'
        texto_semaforo = 'COINCIDE\nCON EL EJEMPLO'
        icono = 'OK'
    else:
        color_semaforo = '#e74c3c'
        texto_semaforo = 'CALCULAR CON\nLA GUIA M02'
        icono = '!'
    
    circulo = plt.Circle((0.5, 0.55), 0.28, color=color_semaforo, 
                          transform=ax5.transAxes, zorder=5)
    ax5.add_patch(circulo)
    ax5.text(0.5, 0.55, icono, transform=ax5.transAxes,
             fontsize=36, fontweight='bold', color='white',
             ha='center', va='center', zorder=6)
    ax5.text(0.5, 0.1, texto_semaforo, transform=ax5.transAxes,
             fontsize=13, fontweight='bold', color=color_semaforo,
             ha='center', va='center')
    ax5.set_title('Semaforo de Decision', fontsize=12, fontweight='bold')
    
    # ============================================================
    # SUBGRÁFICO 6: Ficha técnica + Valores para M03
    # ============================================================
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.axis('off')
    
    ficha = (
        f"FICHA TECNICA DEL PROYECTO\n"
        f"{'-' * 45}\n"
        f"Proyecto    : {PROYECTO}\n"
        f"Modelo      : {DATOS_MODELO['pisos']} pisos\n"
        f"Lv1={DATOS_MODELO['Lv1']:.2f}  Lv2={DATOS_MODELO['Lv2']:.2f}  Lv3={DATOS_MODELO['Lv3']:.2f} m\n"
        f"Lt1={DATOS_MODELO['Lt1']:.2f}  Lt2={DATOS_MODELO['Lt2']:.2f}  Lt3={DATOS_MODELO['Lt3']:.2f}  Lt4={DATOS_MODELO['Lt4']:.2f} m\n"
        f"{'-' * 45}\n"
        f"Uso         : {uso['nombre']}\n"
        f"Cv          : {uso['Cv']:.2f} t/m2\n"
        f"Mamposteria : {mamposteria['tipo']}\n"
        f"Losa        : {resultados['losa']['espesor_cm']} cm\n"
        f"{'-' * 45}\n"
        f"Cm          : {resultados['Cm']:.3f} t/m2\n"
        f"Cv          : {resultados['Cv']:.3f} t/m2\n"
        f"Cu          : {resultados['Cu']:.3f} t/m2\n"
        f"{'-' * 45}\n"
        f"VALORES PARA M03 (VIGA + SISMO):\n"
        f"   W  = {resultados['W']:.3f} t/m\n"
        f"   At = {resultados['At']:.3f} m2\n"
        f"   Pu = {resultados['Pu']:.3f} t\n"
        f"   Cu = {resultados['Cu']:.3f} t/m2\n"
        f"{'-' * 45}\n"
        f"{'COINCIDE CON EL EJEMPLO' if verificacion['coincide'] else 'REVISAR CON LA GUIA M02'}"
    )
    ax6.text(0.02, 0.98, ficha, transform=ax6.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#2c3e50', linewidth=2))
    
    plt.tight_layout()
    nombre_img = f"dashboard_M02_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    ruta_img = os.path.join(carpeta, nombre_img)
    plt.savefig(ruta_img, dpi=150, bbox_inches='tight')
    print(f"\nDashboard guardado: {ruta_img}")
    
    # MOSTRAR LA GRÁFICA EN PANTALLA
    print("\nMostrando grafica en pantalla...")
    print("(Cierre la ventana para continuar)")
    plt.show()

# ============================================================================
# 8. FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    limpiar_pantalla()
    imprimir_header()
    
    print("\n[DATOS DEL MODELO BASE (2 PISOS)]")
    print(f"   Lv1 = {DATOS_MODELO['Lv1']:.2f} m")
    print(f"   Lv2 = {DATOS_MODELO['Lv2']:.2f} m")
    print(f"   Lv3 = {DATOS_MODELO['Lv3']:.2f} m")
    print(f"   Lt1 = {DATOS_MODELO['Lt1']:.2f} m")
    print(f"   Lt2 = {DATOS_MODELO['Lt2']:.2f} m")
    print(f"   Lt3 = {DATOS_MODELO['Lt3']:.2f} m")
    print(f"   Lt4 = {DATOS_MODELO['Lt4']:.2f} m")
    
    uso = seleccionar_uso()
    mamposteria = seleccionar_mamposteria()
    
    luz = DATOS_MODELO["Lv2"]
    resultados = calcular_cargas(luz, uso, mamposteria)
    
    if resultados is None:
        print("\nNo se pudo calcular. Revise la luz.")
        return
    
    verificacion = verificar_coincidencia(uso, mamposteria, resultados)
    
    mostrar_resultados(uso, mamposteria, resultados, verificacion)
    guardar_reporte(uso, mamposteria, resultados, verificacion)
    generar_dashboard(uso, mamposteria, resultados, verificacion)
    
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)

if __name__ == "__main__":
    main()