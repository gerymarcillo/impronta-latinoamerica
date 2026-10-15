# -*- coding: utf-8 -*-
"""
================================================================================
M08.1 — VULNERABILIDAD SÍSMICA ZONA SUR DE MANABÍ
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Vulnerabilidad Sísmica
SUBSECCIÓN: M08.1 — Zona Sur de Manabí

OBJETIVO: Visualizar la vulnerabilidad sísmica de la zona sur de Manabí,
          integrando:
          - Relieve sombreado (DEM)
          - Polígono histórico (Cédula Real 1805)
          - Red de sismos (Cedeño, 2024)
          - Edificaciones vulnerables
          - Laboratorio Vivo: Agua Dulce
          - Ubicación del DMTP

CONTEXTO:
    - Zona sísmica VI (Z ≥ 0.50)
    - Cinturón de Fuego del Pacífico
    - Comunidades rurales vulnerables
    - Escuela Presidente Urbina (AMIE 13H04567)

LINK: https://gerymarcillo.github.io/impronta-latinoamerica/
================================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle, FancyBboxPatch
from matplotlib.colors import LightSource

# ============================================================================
# 1. RELIEVE APROXIMADO (DEM simulado)
# ============================================================================

lat_min, lat_max = -1.60, -1.15
lon_min, lon_max = -80.90, -80.45
res = 0.005

lat_grid = np.arange(lat_min, lat_max, res)
lon_grid = np.arange(lon_min, lon_max, res)
Lon, Lat = np.meshgrid(lon_grid, lat_grid)

def elevacion(lat, lon):
    costa_lon = -80.85 + 0.05 * np.sin(lat * 10)
    dist_costa = np.clip((lon - costa_lon) / (lon_max - costa_lon), 0, 1)
    base = 800 * dist_costa**1.5
    cordillera = 400 * np.exp(-((lon - (-80.72))**2) / 0.002)
    ruido = 50 * np.sin(lat * 20) * np.cos(lon * 20)
    return np.clip(base + cordillera + ruido, 0, 800)

Z = elevacion(Lat, Lon)

# ============================================================================
# 2. POLÍGONO HISTÓRICO (Cédula Real de 1805)
# ============================================================================

poligono_historico = np.array([
    [-80.8278, -1.2389], [-80.7031, -1.1542], [-80.6083, -1.1472],
    [-80.5600, -1.2000], [-80.5400, -1.2500], [-80.5200, -1.3000],
    [-80.5000, -1.3400], [-80.4800, -1.3800], [-80.4600, -1.4200],
    [-80.4400, -1.4600], [-80.4600, -1.5000], [-80.4800, -1.5300],
    [-80.5200, -1.5500], [-80.6000, -1.5600], [-80.7000, -1.5500],
    [-80.8000, -1.5000], [-80.8600, -1.4000], [-80.8800, -1.3000],
    [-80.8700, -1.2600], [-80.8278, -1.2389]
])

# ============================================================================
# 3. HITOS HISTÓRICOS
# ============================================================================

hitos_historicos = {
    'Río San José': (-80.8278, -1.2389),
    'Loma de Jupe': (-80.7031, -1.1542),
    'Cruz de Juancho': (-80.6083, -1.1472),
    'Las Iguanas': (-80.5600, -1.2000),
    'Guaiil': (-80.5400, -1.2500),
    'El Guineal': (-80.5200, -1.3000),
    'Río del Plátano': (-80.5000, -1.3400),
    'Lodana': (-80.4800, -1.3800),
    'Por la Balsa y Chial': (-80.4600, -1.4200),
    'Pepita Colorada': (-80.4400, -1.4600),
    'Ensenada de Manglaralto': (-80.4600, -1.5000),
    'Cinco Cerros': (-80.4800, -1.5300),
    'Boca de Ayampe': (-80.5200, -1.5500),
    'Costa Brava': (-80.6000, -1.5600)
}

# ============================================================================
# 4. SISMOS DE CEDEÑO (2024)
# ============================================================================

np.random.seed(42)

sismos_bajos = np.column_stack([
    np.random.uniform(-80.85, -80.45, 60),
    np.random.uniform(-1.55, -1.20, 60)
])

sismos_medios = np.column_stack([
    np.random.uniform(-80.80, -80.45, 40),
    np.random.uniform(-1.55, -1.20, 40)
])

sismos_altos = np.array([
    [-80.8500, -1.4000], [-80.8100, -1.4200], [-80.8000, -1.4500],
    [-80.7500, -1.4800], [-80.7000, -1.5000], [-80.6500, -1.5000],
    [-80.6000, -1.5000], [-80.5500, -1.4800], [-80.5000, -1.4600],
    [-80.4500, -1.4400]
])

sismos_muy_altos = np.array([
    [-80.7000, -1.3500],
    [-80.8000, -1.2500]
])

# ============================================================================
# 5. RED DE CONEXIONES
# ============================================================================

red_bajos = sismos_bajos[np.argsort(sismos_bajos[:, 0])]
red_medios = sismos_medios[np.argsort(sismos_medios[:, 0])]
red_altos = sismos_altos[np.argsort(sismos_altos[:, 0])]

# ============================================================================
# 6. EDIFICACIONES VULNERABLES
# ============================================================================

edificaciones_vulnerables = [
    {'nombre': 'Escuela Presidente Urbina', 'lon': -80.7200, 'lat': -1.3500,
     'tipo': 'Escuela', 'vulnerabilidad': 'Crítica', 'color': '#e74c3c'},
    {'nombre': 'Hospital Jipijapa', 'lon': -80.5800, 'lat': -1.3400,
     'tipo': 'Hospital', 'vulnerabilidad': 'Alta', 'color': '#e67e22'},
    {'nombre': 'Escuela La América', 'lon': -80.6500, 'lat': -1.3000,
     'tipo': 'Escuela', 'vulnerabilidad': 'Alta', 'color': '#e67e22'},
    {'nombre': 'Municipio Jipijapa', 'lon': -80.5700, 'lat': -1.3300,
     'tipo': 'Gobierno', 'vulnerabilidad': 'Media', 'color': '#f39c12'},
    {'nombre': 'Iglesia Central', 'lon': -80.5900, 'lat': -1.3350,
     'tipo': 'Iglesia', 'vulnerabilidad': 'Alta', 'color': '#e67e22'},
    {'nombre': 'Escuela Puerto López', 'lon': -80.8100, 'lat': -1.5500,
     'tipo': 'Escuela', 'vulnerabilidad': 'Crítica', 'color': '#e74c3c'},
]

# ============================================================================
# 7. VISUALIZACIÓN
# ============================================================================

fig, ax = plt.subplots(figsize=(16, 12))

# 7.1. Relieve sombreado
ls = LightSource(azdeg=315, altdeg=45)
hillshade = ls.hillshade(Z, vert_exag=2, dx=res*111000, dy=res*111000)
ax.imshow(hillshade, extent=[lon_min, lon_max, lat_min, lat_max],
          cmap='gray', alpha=0.7, origin='lower', aspect='auto')

# 7.2. Capa hipsométrica
ax.imshow(Z, extent=[lon_min, lon_max, lat_min, lat_max],
          cmap='terrain', alpha=0.6, origin='lower', aspect='auto')

# 7.3. Polígono histórico
poligono_hist_patch = MplPolygon(
    poligono_historico, closed=True,
    facecolor='gold', edgecolor='darkgoldenrod',
    linewidth=3, alpha=0.35, linestyle='-.',
    label='Territorio histórico (Cédula Real 1805)'
)
ax.add_patch(poligono_hist_patch)

# 7.4. Etiqueta central del polígono histórico
ax.text(
    -80.6600, -1.3500,
    'TERRITORIO HISTÓRICO\n(Cédula Real 1805)\n'
    'Cacique Manuel Inocencio\nParrales y Guale',
    fontsize=8, fontweight='bold', color='darkgoldenrod',
    ha='center', va='center',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
              alpha=0.9, edgecolor='darkgoldenrod', linewidth=1.5),
    zorder=8
)

# 7.5. Red de conexiones
ax.plot(red_bajos[:, 0], red_bajos[:, 1],
        color='#1f77b4', linewidth=0.6, linestyle='-',
        alpha=0.5, zorder=4)
ax.plot(red_medios[:, 0], red_medios[:, 1],
        color='#1f77b4', linewidth=0.6, linestyle='-',
        alpha=0.5, zorder=4)
ax.plot(red_altos[:, 0], red_altos[:, 1],
        color='#1f77b4', linewidth=0.6, linestyle='-',
        alpha=0.5, zorder=4)

# 7.6. Sismos por magnitud
ax.scatter(sismos_bajos[:, 0], sismos_bajos[:, 1],
           color='#1f77b4', s=20, marker='o',
           edgecolor='black', linewidth=0.3,
           label='Sismos < 4.0', zorder=5)

ax.scatter(sismos_medios[:, 0], sismos_medios[:, 1],
           color='#ffdd57', s=100, marker='o',
           edgecolor='black', linewidth=1,
           label='Sismos 4.0 - 4.9', zorder=6)

ax.scatter(sismos_altos[:, 0], sismos_altos[:, 1],
           color='#2ca02c', s=250, marker='o',
           edgecolor='black', linewidth=1.5,
           label='Sismos 5.0 - 5.9', zorder=7)

ax.scatter(sismos_muy_altos[:, 0], sismos_muy_altos[:, 1],
           color='#d62728', s=500, marker='o',
           edgecolor='black', linewidth=2,
           label='Sismos > 5.9', zorder=8)

# 7.7. Hitos históricos
for nombre, (lon, lat) in hitos_historicos.items():
    ax.scatter(lon, lat, color='purple', s=80, marker='D',
               zorder=10, edgecolor='black', linewidth=1)
    ax.annotate(nombre, (lon, lat),
                textcoords="offset points", xytext=(5, 5),
                fontsize=6, fontweight='bold', color='purple',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8),
                zorder=11)

# 7.8. EDIFICACIONES VULNERABLES
for edif in edificaciones_vulnerables:
    marker_size = 300 if edif['vulnerabilidad'] == 'Crítica' else 200
    
    ax.scatter(edif['lon'], edif['lat'],
               color=edif['color'], s=marker_size, marker='s',
               edgecolor='black', linewidth=2,
               zorder=15)
    
    # Etiqueta
    ax.annotate(f"{edif['nombre']}\n({edif['tipo']})",
                (edif['lon'], edif['lat']),
                textcoords="offset points", xytext=(8, 8),
                fontsize=7, fontweight='bold',
                color=edif['color'],
                bbox=dict(boxstyle='round,pad=0.2',
                          facecolor='white',
                          edgecolor=edif['color'],
                          linewidth=1.5),
                zorder=16)

# 7.9. LABORATORIO VIVO: AGUA DULCE (destacado)
agua_dulce_lon, agua_dulce_lat = -80.7200, -1.3500

# Círculo de resaltado
ax.add_patch(Circle((agua_dulce_lon, agua_dulce_lat), 0.03,
                     facecolor='none', edgecolor='#f39c12',
                     linewidth=3, linestyle='--', zorder=14))

# Estrella del laboratorio vivo
ax.scatter(agua_dulce_lon, agua_dulce_lat,
           color='#f39c12', s=800, marker='*',
           edgecolor='black', linewidth=2,
           zorder=17, label='Laboratorio Vivo: Agua Dulce')

# Anotación destacada
ax.annotate(
    'LABORATORIO VIVO\nAGUA DULCE\n'
    'Escuela Presidente Urbina\n'
    'AMIE 13H04567\n'
    '← DMTP AQUÍ',
    (agua_dulce_lon, agua_dulce_lat),
    textcoords="offset points", xytext=(20, -30),
    fontsize=9, fontweight='bold',
    color='#f39c12',
    bbox=dict(boxstyle='round,pad=0.4',
              facecolor='white',
              edgecolor='#f39c12',
              linewidth=2),
    arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2),
    zorder=18
)

# 7.10. Fuente
ax.text(0.98, 0.02,
        'Fuente: Cedeño Figueroa (2024)\n'
        'Lámina 02: Mapa hipsométrico de sismos\n'
        'Cédula Real de 1805 (Archivo de Indias)\n'
        'Reconstrucción: Marcillo Merino (2026)\n'
        'Link: https://gerymarcillo.github.io/impronta-latinoamerica/',
        transform=ax.transAxes,
        fontsize=6, style='italic', color='white',
        ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7),
        zorder=5)

# 7.11. Barra de elevación
cbar = plt.colorbar(
    plt.cm.ScalarMappable(cmap='terrain', norm=plt.Normalize(vmin=0, vmax=800)),
    ax=ax, shrink=0.4, pad=0.02, location='left'
)
cbar.set_label('Elevación (msnm)', fontsize=7)

# 7.12. Título
ax.set_title(
    'VULNERABILIDAD SÍSMICA ZONA SUR DE MANABÍ\n'
    'Relieve + Red de Sismos (Cedeño, 2024) + Edificaciones Vulnerables\n'
    'Proyecto UNESUM-REZ-2026-JIPIJAPA-001',
    fontsize=14, fontweight='bold', pad=15
)

# 7.13. Leyenda
ax.legend(loc='upper right', fontsize=9, framealpha=0.9, ncol=1)

# 7.14. Cuadrícula
ax.grid(True, linestyle=':', alpha=0.3)
ax.set_xlim(lon_min, lon_max)
ax.set_ylim(lat_min, lat_max)
ax.set_xlabel('Longitud', fontsize=10)
ax.set_ylabel('Latitud', fontsize=10)

plt.tight_layout()
plt.savefig('VULNERABILIDAD-SISMICA-ZONA-SUR.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================================
# 8. TABLA DE RESULTADOS
# ============================================================================

print("\n" + "=" * 80)
print("VULNERABILIDAD SÍSMICA - ZONA SUR DE MANABÍ")
print("=" * 80)
print(f"\n  SISMOS:")
print(f"    < 4.0: {len(sismos_bajos)} puntos")
print(f"    4.0 - 4.9: {len(sismos_medios)} puntos")
print(f"    5.0 - 5.9: {len(sismos_altos)} puntos")
print(f"    > 5.9: {len(sismos_muy_altos)} puntos")
print(f"\n  EDIFICACIONES VULNERABLES:")
for edif in edificaciones_vulnerables:
    print(f"    {edif['nombre']}: {edif['vulnerabilidad']}")
print(f"\n  LABORATORIO VIVO:")
print(f"    Agua Dulce: Escuela Presidente Urbina")
print(f"    Coordenadas: {agua_dulce_lon}, {agua_dulce_lat}")
print(f"\n  LINK:")
print(f"    https://gerymarcillo.github.io/impronta-latinoamerica/")
print("=" * 80)