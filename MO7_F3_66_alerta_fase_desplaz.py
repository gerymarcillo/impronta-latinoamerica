# -*- coding: utf-8 -*-
"""
================================================================================
M07.38 — RECORRIDO CON ALERTAS (M01 → M07.37)
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M07 — Análisis Dinámico Modal
SUBSECCIÓN: M07.38 — Recorrido con Alertas
================================================================================
"""

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

# ============================================================================
# PALETA (CORREGIDA)
# ============================================================================

COLORES = {
    'fondo': '#f5f7fa',
    'titulo': '#1a237e',
    'subtitulo': '#5dade2',
    'ok': '#27ae60',
    'advertencia': '#f39c12',
    'critica': '#e74c3c',
    'info': '#3498db',
    'resultado': '#27ae60',
    'box_datos': '#ffffff',
    'box_datos_borde': '#1a237e',
    'box_resultado': '#eafaf1',
    'box_resultado_borde': '#27ae60',
    'box_alerta': '#fadbd8',
    'box_alerta_borde': '#c0392b',
}

# ============================================================================
# 1. DATOS DE LAS ALERTAS
# ============================================================================

alertas = [
    ("M01-M06", "Diseño de elementos", "OK", "Sin alertas"),
    ("M07.1", "Modelo 3D", "OK", "Sin alertas"),
    ("M07.2", "Matriz de masa", "OK", "Sin alertas"),
    ("M07.3", "Peso reactivo", "OK", "Sin alertas"),
    ("M07.4", "Matriz de rigidez", "OK", "Sin alertas"),
    ("M07.5", "Rigidez a cortante", "OK", "Sin alertas"),
    ("M07.6", "Períodos λ₁, λ₂", "OK", "Sin alertas"),
    ("M07.7", "Monte Carlo", "ADVERTENCIA", "CV de T₁"),
    ("M07.8", "Cadenas de Markov", "ADVERTENCIA", "P(colapso)"),
    ("M07.9", "Fibonacci / φ", "OK", "Sin alertas"),
    ("M07.10", "Espectro NEC-15", "ADVERTENCIA", "Sa = 1.7100 g"),
    ("M07.11", "Cortante basal", "ADVERTENCIA", "V = 231.02 t"),
    ("M07.12", "Igual desplazamiento", "ADVERTENCIA", "Se deforma"),
    ("M07.13", "Factor Ω₀", "ADVERTENCIA", "Ω₀ = 2.0"),
    ("M07.14", "Punto de fluencia", "ADVERTENCIA", "Dy = 2.144 cm"),
    ("M07.15", "Factores R, Ω₀, Cd", "ADVERTENCIA", "ASCE 7-10"),
    ("M07.16", "Tablas completas", "ADVERTENCIA", "Acero + Comp."),
    ("M07.17", "Ω₀ = 2.0 hormigón", "ADVERTENCIA", "Criterio autor"),
    ("M07.18", "Punto de fluencia", "ADVERTENCIA", "Vigas fluyen"),
    ("M07.19", "Cd = 0.75·R", "ADVERTENCIA", "Cd = 4.50"),
    ("M07.20", "X inelástica", "ADVERTENCIA", "4.824 cm"),
    ("M07.21", "Curva Pushover", "ADVERTENCIA", "Elastoplástico"),
    ("M07.22", "Deriva", "ADVERTENCIA", "1.608%"),
    ("M07.23", "Organigrama", "ADVERTENCIA", "Flujo"),
    ("M07.24", "Parámetro λ", "ADVERTENCIA", "λ = 3.1"),
    ("M07.25", "Fase 3 cierre", "ADVERTENCIA", "Verificación"),
    ("M07.26", "Fuerza de fluencia", "CRITICA", "Fy = 231.02 t"),
    ("M07.27", "Flujograma", "ADVERTENCIA", "Diapositivas 48-67"),
    ("M07.28", "Explicación científica", "ADVERTENCIA", "Normas"),
    ("M07.29", "Derivas por piso", "ADVERTENCIA", "0.378%/1.608%"),
    ("M07.30", "Pórtico", "ADVERTENCIA", "X₁/X₂"),
    ("M07.31", "Tabla integradora", "ADVERTENCIA", "6 normas"),
    ("M07.32", "Resumen conceptual", "ADVERTENCIA", "Desempeño"),
    ("M07.33", "Resumen explicativo", "ADVERTENCIA", "7 pasos"),
    ("M07.34", "Fusión integral", "ADVERTENCIA", "Impronta"),
    ("M07.35", "REDi™", "ADVERTENCIA", "Base"),
    ("M07.36", "Comparativa", "CRITICA", "A falla"),
    ("M07.37", "Forense", "CRITICA", "Cadena falla"),
]

# ============================================================================
# 2. FIGURA
# ============================================================================

fig = plt.figure(figsize=(26, 20))
fig.patch.set_facecolor(COLORES['fondo'])

fig.text(0.5, 0.985,
         'M07.38 — RECORRIDO CON ALERTAS (M01 → M07.37)',
         ha='center', va='top', fontsize=24, fontweight='bold',
         color=COLORES['titulo'])

fig.text(0.5, 0.962,
         'UNESUM-REZ-2026-JIPIJAPA-001 | 30 alertas identificadas',
         ha='center', va='top', fontsize=14,
         color=COLORES['subtitulo'], style='italic')

gs = GridSpec(2, 3, figure=fig,
              hspace=0.30, wspace=0.25,
              left=0.04, right=0.97,
              top=0.92, bottom=0.04,
              height_ratios=[1.3, 1.0])

# ============================================================================
# PANEL (a): LÍNEA DE TIEMPO CON ALERTAS
# ============================================================================

ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor('#ffffff')

modulos_m07 = [a for a in alertas if a[0].startswith('M07')]

x_pos = np.arange(len(modulos_m07))
colores_alerta = []
for a in modulos_m07:
    if a[2] == 'CRITICA':
        colores_alerta.append(COLORES['critica'])
    elif a[2] == 'ADVERTENCIA':
        colores_alerta.append(COLORES['advertencia'])
    else:
        colores_alerta.append(COLORES['ok'])

bars = ax1.bar(x_pos, [1]*len(modulos_m07), color=colores_alerta,
               edgecolor='black', linewidth=1.5, width=0.8)

for i, (bar, a) in enumerate(zip(bars, modulos_m07)):
    modulo = a[0].replace('M07.', '')
    ax1.text(bar.get_x() + bar.get_width()/2, 1.1,
             modulo, ha='center', va='bottom',
             fontsize=9, fontweight='bold', rotation=45)

    if a[2] == 'CRITICA':
        emoji = '🔴'
    elif a[2] == 'ADVERTENCIA':
        emoji = '⚠️'
    else:
        emoji = '✅'

    ax1.text(bar.get_x() + bar.get_width()/2, 0.5,
             emoji, ha='center', va='center', fontsize=14)

ax1.set_xlim(-0.5, len(modulos_m07) - 0.5)
ax1.set_ylim(0, 1.5)
ax1.set_yticks([])
ax1.set_title('(a) LÍNEA DE TIEMPO — ALERTAS POR MÓDULO',
              fontsize=14, fontweight='bold', color=COLORES['titulo'], pad=15)
ax1.set_xlabel('Módulos M07', fontsize=12, fontweight='bold')

legend_elements = [
    Patch(facecolor=COLORES['ok'], edgecolor='black', label='✅ Sin alertas'),
    Patch(facecolor=COLORES['advertencia'], edgecolor='black', label='⚠️ Advertencia'),
    Patch(facecolor=COLORES['critica'], edgecolor='black', label='🔴 Crítica'),
]
ax1.legend(handles=legend_elements, fontsize=10, loc='upper right')

# ============================================================================
# PANEL (b): RESUMEN DE ALERTAS
# ============================================================================

ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')
ax2.set_title('(b) RESUMEN DE ALERTAS',
              fontsize=12, fontweight='bold', color=COLORES['titulo'], pad=15)

n_ok = sum(1 for a in alertas if a[2] == 'OK')
n_adv = sum(1 for a in alertas if a[2] == 'ADVERTENCIA')
n_crit = sum(1 for a in alertas if a[2] == 'CRITICA')

txt2 = (
    "RESUMEN DE ALERTAS\n"
    "═══════════════════════════════\n\n"
    f"  ✅ Sin alertas:    {n_ok}\n"
    f"  ⚠️ Advertencias:   {n_adv}\n"
    f"  🔴 Críticas:       {n_crit}\n\n"
    f"  TOTAL:             {len(alertas)}\n\n"
    "═══════════════════════════════\n\n"
    "  ALERTAS CRÍTICAS:\n"
    "  • M07.26: Fy = 231.02 t\n"
    "  • M07.36: A falla (2.233%)\n"
    "  • M07.37: Cadena de falla\n\n"
    "═══════════════════════════════\n"
    "  El Proyecto A falla\n"
    "  por sección insuficiente"
)

ax2.text(0.5, 0.5, txt2, transform=ax2.transAxes,
         ha='center', va='center', fontsize=9, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_alerta'],
                   edgecolor=COLORES['box_alerta_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (c): ALERTAS POR TIPO
# ============================================================================

ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')
ax3.set_title('(c) ALERTAS POR TIPO',
              fontsize=12, fontweight='bold', color=COLORES['titulo'], pad=15)

txt3 = (
    "TIPOS DE ALERTAS\n"
    "═══════════════════════════════\n\n"
    "  ⚠️ ADVERTENCIA:\n"
    "  • Incertidumbre (M07.7)\n"
    "  • Degradación (M07.8)\n"
    "  • Espectro crítico (M07.10)\n"
    "  • Cortante basal (M07.11)\n"
    "  • Igual desplazamiento (M07.12)\n"
    "  • Ω₀ = 2.0 (M07.13, M07.17)\n"
    "  • Fluencia (M07.14, M07.18)\n"
    "  • Cd = 4.50 (M07.19)\n"
    "  • X inelástica (M07.20)\n"
    "  • Pushover (M07.21)\n"
    "  • Deriva (M07.22, M07.29)\n"
    "  • Normas (M07.24, M07.31)\n"
    "  • REDi (M07.35)\n\n"
    "  🔴 CRÍTICA:\n"
    "  • Fy = 231.02 t (M07.26)\n"
    "  • A falla (M07.36)\n"
    "  • Forense (M07.37)"
)

ax3.text(0.5, 0.5, txt3, transform=ax3.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_datos'],
                   edgecolor=COLORES['box_datos_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# PANEL (d): CONCLUSIONES
# ============================================================================

ax4 = fig.add_subplot(gs[1, 2])
ax4.axis('off')
ax4.set_title('(d) CONCLUSIONES',
              fontsize=12, fontweight='bold', color=COLORES['resultado'], pad=15)

txt4 = (
    "CONCLUSIONES DEL RECORRIDO\n"
    "═══════════════════════════════\n\n"
    "  ✅ M01-M06: Sin alertas\n"
    "     (Diseño de elementos)\n\n"
    "  ✅ M07.1-M07.6: Sin alertas\n"
    "     (Análisis modal)\n\n"
    "  ⚠️ M07.7-M07.35: Advertencias\n"
    "     (Pushover, derivas, normas)\n\n"
    "  🔴 M07.26, M07.36, M07.37:\n"
    "     Críticas (Fy, A falla, forense)\n\n"
    "═══════════════════════════════\n\n"
    "  LECCIÓN PRINCIPAL:\n"
    "  La sección de columna es\n"
    "  CRÍTICA para la resiliencia\n\n"
    "═══════════════════════════════\n"
    "  ✅ Proyecto C (38×38) cumple\n"
    "  ❌ Proyecto A (25×25) falla"
)

ax4.text(0.5, 0.5, txt4, transform=ax4.transAxes,
         ha='center', va='center', fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6',
                   facecolor=COLORES['box_resultado'],
                   edgecolor=COLORES['box_resultado_borde'],
                   linewidth=2.5, alpha=0.98))

# ============================================================================
# 3. GUARDAR
# ============================================================================

carpeta = "Resultados_M07_38"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M07_38_recorrido_alertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)

plt.savefig(ruta_img, dpi=150, bbox_inches='tight',
            facecolor=COLORES['fondo'])
print(f"\n✅ Imagen guardada: {ruta_img}")

plt.show()

# ============================================================================
# 4. VERIFICACIÓN EN CONSOLA
# ============================================================================

print("\n" + "=" * 80)
print("M07.38 — RECORRIDO CON ALERTAS")
print("=" * 80)
print(f"\n  RESUMEN DE ALERTAS:")
print(f"    ✅ Sin alertas:  {n_ok}")
print(f"    ⚠️ Advertencias: {n_adv}")
print(f"    🔴 Críticas:     {n_crit}")
print(f"    TOTAL:           {len(alertas)}")
print(f"\n  ALERTAS CRÍTICAS:")
print(f"    • M07.26: Fy = 231.02 t")
print(f"    • M07.36: A falla (2.233%)")
print(f"    • M07.37: Cadena de falla")
print(f"\n  LECCIÓN PRINCIPAL:")
print(f"    La sección de columna es CRÍTICA")
print(f"    Proyecto C (38×38) cumple")
print(f"    Proyecto A (25×25) falla")
print("=" * 80)