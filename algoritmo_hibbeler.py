"""
================================================================================
📐 SCRIPT: CÁLCULO DE CARGAS ESTRUCTURALES SOBRE VIGA DE ENTREPISO
================================================================================
👤 AUTOR: Lorenzo Marcillo Merino
🏛️ APLICACIÓN: Proyecto multidisciplinario UNESUM - Jipijapa
📖 BASADO EN: NEC - Cargas (Ecuador), Hibbeler (Tabla 1.3)
================================================================================
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================================
# 1. DEFINICIÓN DE DATOS DE ENTRADA (según proyecto real UNESUM)
# ============================================================================

# DATOS DE LA LOSA
ancho_losa_pies = 6.0          # Ancho tributario de la losa (pies)
espesor_losa_pulg = 4.0        # Espesor de la losa de concreto (pulgadas)
densidad_concreto = 8.0        # Densidad concreto ligero (lb/(pie²·pulg))

# ACABADOS Y MUROS
carga_yeso_psf = 5.0           # Yeso inferior (lb/pie²)
peso_muro_psf = 45.0           # Muro de bloque hueco (lb/pie²)
altura_muro_pies = 8.0         # Altura del muro (pies)

# PESO PROPIO ESTIMADO DE LA VIGA
peso_viga_pp_pie = 50.0        # Estimación inicial (lb/pie)

# CARGA VIVA SEGÚN USO DEL EDIFICIO (aulas - NEC)
carga_viva_psf = 250.0         # Carga viva superficial (lb/pie²)

# ============================================================================
# 2. CÁLCULO DE CARGAS MUERTAS (DEAD LOADS - D)
# ============================================================================

# 2.1 Peso de la losa de concreto
peso_losa = densidad_concreto * ancho_losa_pies * espesor_losa_pulg

# 2.2 Peso del yeso inferior
peso_yeso = carga_yeso_psf * ancho_losa_pies

# 2.3 Peso del muro (considerado como carga lineal uniforme)
peso_muro = peso_muro_psf * altura_muro_pies

# 2.4 Carga muerta total (incluye peso propio de viga)
D_total = peso_losa + peso_yeso + peso_muro + peso_viga_pp_pie

# ============================================================================
# 3. CÁLCULO DE CARGA VIVA TOTAL (LIVE LOADS - L)
# ============================================================================

# La carga viva superficial se convierte a carga lineal (lb/pie)
L_total = carga_viva_psf * ancho_losa_pies

# ============================================================================
# 4. COMBINACIÓN MAYORADA (Wu) según NEC / ACI
# ============================================================================

# Combinación crítica para edificaciones comunes: 1.2D + 1.6L
Wu = 1.2 * D_total + 1.6 * L_total

# ============================================================================
# 5. IMPRESIÓN DE RESULTADOS
# ============================================================================

print("=" * 70)
print("📐 CÁLCULO DE CARGAS ESTRUCTURALES SOBRE VIGA DE ENTREPISO")
print("=" * 70)
print(f"\n📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🏛️ Proyecto: UNESUM - Jipijapa - Proyecto Multidisciplinario")

print("\n📊 1. CARGAS MUERTAS (DEAD LOADS - D)")
print("-" * 50)
print(f"   Losa de concreto ligero:     {peso_losa:>10.2f} lb/ft")
print(f"   Yeso inferior:               {peso_yeso:>10.2f} lb/ft")
print(f"   Muro de bloque hueco:        {peso_muro:>10.2f} lb/ft")
print(f"   Peso propio de viga:         {peso_viga_pp_pie:>10.2f} lb/ft")
print("-" * 50)
print(f"   TOTAL CARGA MUERTA (D):      {D_total:>10.2f} lb/ft")

print("\n📊 2. CARGA VIVA (LIVE LOADS - L)")
print("-" * 50)
print(f"   Carga viva (aulas):          {L_total:>10.2f} lb/ft")

print("\n📊 3. CARGA MAYORADA (Wu)")
print("-" * 50)
print(f"   Combinación: 1.2D + 1.6L")
print(f"   Wu = 1.2({D_total:.2f}) + 1.6({L_total:.2f})")
print(f"   Wu =                          {Wu:>10.2f} lb/ft")

print("\n📊 4. RESUMEN DE CARGAS")
print("-" * 50)
print(f"   Carga Muerta (D):   {D_total:>10.2f} lb/ft  ({D_total/(D_total+L_total)*100:>5.1f}%)")
print(f"   Carga Viva (L):     {L_total:>10.2f} lb/ft  ({L_total/(D_total+L_total)*100:>5.1f}%)")
print("-" * 50)
print(f"   Carga Total (D+L):  {D_total + L_total:>10.2f} lb/ft  (100.0%)")
print(f"   Carga Mayorada (Wu):{Wu:>10.2f} lb/ft")

print("\n" + "=" * 70)
print("✅ CÁLCULO COMPLETADO")
print("=" * 70)

# ============================================================================
# 6. GRÁFICO DE BARRAS
# ============================================================================

# Crear figura
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('📊 ANÁLISIS DE CARGAS SOBRE VIGA DE ENTREPISO', 
             fontsize=14, fontweight='bold')

# 6.1 Gráfico de barras de cargas individuales
categorias = ['Losa', 'Yeso', 'Muro', 'Viga', 'Carga\nViva']
valores = [peso_losa, peso_yeso, peso_muro, peso_viga_pp_pie, L_total]
colores = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']

bars = axes[0].bar(categorias, valores, color=colores, 
                   edgecolor='black', linewidth=1.2, alpha=0.85)
axes[0].set_ylabel('Carga (lb/ft)', fontsize=12)
axes[0].set_title('Distribución de Cargas Individuales', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', linestyle='--', alpha=0.3)

# Añadir valores sobre las barras
for bar, val in zip(bars, valores):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f'{val:.1f}', ha='center', va='bottom', fontweight='bold')

# 6.2 Gráfico de torta (contribución a carga muerta)
etiquetas_D = ['Losa', 'Yeso', 'Muro', 'Viga']
valores_D = [peso_losa, peso_yeso, peso_muro, peso_viga_pp_pie]
colores_D = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
explode = (0.05, 0.05, 0.05, 0.05)

axes[1].pie(valores_D, labels=etiquetas_D, autopct='%1.1f%%', 
            colors=colores_D, explode=explode, shadow=True,
            startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[1].set_title('Composición de Carga Muerta (D)', fontsize=12, fontweight='bold')

plt.tight_layout()

# Guardar gráfico
carpeta = Path.cwd() / 'Resultados_Cargas'
carpeta.mkdir(parents=True, exist_ok=True)
nombre_archivo = f"cargas_viga_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
plt.savefig(carpeta / nombre_archivo, dpi=300, bbox_inches='tight')
print(f"\n✅ Gráfico guardado: {carpeta / nombre_archivo}")

plt.show()

print("\n" + "=" * 70)
print("🏁 SCRIPT FINALIZADO")
print("=" * 70)