import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# ============================================================
# GRÁFICA DEL CICLO NONAKA-TAKEUCHI
# Aplicado al análisis de la viga del Colegio Alejo Lascano
# Proyecto UNESUM-REZ-2026-JIPIJAPA-001
# ============================================================

fig, ax = plt.subplots(figsize=(14, 11))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('#F5F5F5')

# ------------------------------------------------------------
# COLORES
# ------------------------------------------------------------
COL = {
    'social':  '#B71C1C',   # rojo
    'extern':  '#E65100',   # naranja
    'combin':  '#F9A825',   # amarillo
    'intern':  '#00695C',   # verde petróleo
    'centro':  '#1A1A2E',   # azul oscuro
    'flecha':  '#333333',
}

# ------------------------------------------------------------
# FUNCIÓN PARA DIBUJAR BLOQUE
# ------------------------------------------------------------
def bloque(x, y, w, h, titulo, contenido, color):
    caja = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.1,rounding_size=0.25",
                          linewidth=2.5, edgecolor='black',
                          facecolor=color, alpha=1.0)
    ax.add_patch(caja)
    ax.text(x + w/2, y + h - 0.3, titulo,
            ha='center', va='top', fontsize=12,
            fontweight='bold', color='white')
    ax.text(x + w/2, y + h - 0.7, contenido,
            ha='center', va='top', fontsize=9,
            color='white', linespacing=1.4)

# ------------------------------------------------------------
# FUNCIÓN PARA FLECHA CURVA
# ------------------------------------------------------------
def flecha(x1, y1, x2, y2, rad=0.0, color='#333333', lw=2.5):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                 connectionstyle=f"arc3,rad={rad}",
                 arrowstyle='-|>', mutation_scale=22,
                 linewidth=lw, color=color))

# ============================================================
# CENTRO — GESTIÓN DEL CONOCIMIENTO
# ============================================================
centro = Circle((5.0, 5.0), radius=1.8,
                facecolor=COL['centro'], edgecolor='black',
                linewidth=2.5, alpha=1.0)
ax.add_patch(centro)

ax.text(5.0, 5.6, "GESTIÓN DEL",
        ha='center', va='center', fontsize=13,
        fontweight='bold', color='white')
ax.text(5.0, 5.1, "CONOCIMIENTO",
        ha='center', va='center', fontsize=13,
        fontweight='bold', color='white')
ax.text(5.0, 4.4, "Nonaka & Takeuchi",
        ha='center', va='center', fontsize=9,
        color='white', style='italic')
ax.text(5.0, 4.1, "(1995)",
        ha='center', va='center', fontsize=9,
        color='white', style='italic')

# ============================================================
# 4 BLOQUES — MODOS DEL CICLO
# ============================================================

# 1. SOCIALIZACIÓN (arriba izquierda)
bloque(0.3, 7.5, 3.8, 1.9,
       "1. SOCIALIZACIÓN",
       "Tácito → Tácito\n\n"
       "• Visita al Colegio Alejo Lascano\n"
       "• Observación directa de la viga\n"
       "• Medición inicial con Phyphox\n"
       "• Compartir experiencias",
       COL['social'])

# 2. EXTERNALIZACIÓN (arriba derecha)
bloque(5.9, 7.5, 3.8, 1.9,
       "2. EXTERNALIZACIÓN",
       "Tácito → Explícito\n\n"
       "• Cálculo en Excel (matriz [K])\n"
       "• Código Python (gráficas M–θ)\n"
       "• Fórmulas: K = 4EI/L\n"
       "• θ = q·L³/(24EI)",
       COL['extern'])

# 3. COMBINACIÓN (abajo derecha)
bloque(5.9, 0.6, 3.8, 1.9,
       "3. COMBINACIÓN",
       "Explícito → Explícito\n\n"
       "• Integración con NEC-15\n"
       "• Comparación con ACI 318\n"
       "• Verificación normativa\n"
       "• Modelo normativo",
       COL['combin'])

# 4. INTERNALIZACIÓN (abajo izquierda)
bloque(0.3, 0.6, 3.8, 1.9,
       "4. INTERNALIZACIÓN",
       "Explícito → Tácito\n\n"
       "• Maqueta a escala (1:10)\n"
       "• Ensayo de flexión\n"
       "• Aplicación en campo\n"
       "• Nuevo conocimiento tácito",
       COL['intern'])

# ============================================================
# FLECHAS DEL CICLO (sentido horario)
# ============================================================
# Socialización → Externalización
flecha(4.1, 8.5, 5.9, 8.5, rad=-0.3)

# Externalización → Combinación
flecha(7.8, 7.4, 7.8, 2.6, rad=-0.3)

# Combinación → Internalización
flecha(5.9, 1.5, 4.1, 1.5, rad=-0.3)

# Internalización → Socialización
flecha(2.2, 2.6, 2.2, 7.4, rad=-0.3)

# ============================================================
# ETIQUETAS DE LOS MODOS
# ============================================================
ax.text(2.2, 9.7, "TÁCITO → TÁCITO",
        ha='center', va='top', fontsize=10,
        fontweight='bold', color=COL['social'])
ax.text(7.8, 9.7, "TÁCITO → EXPLÍCITO",
        ha='center', va='top', fontsize=10,
        fontweight='bold', color=COL['extern'])
ax.text(7.8, 0.3, "EXPLÍCITO → EXPLÍCITO",
        ha='center', va='bottom', fontsize=10,
        fontweight='bold', color=COL['combin'])
ax.text(2.2, 0.3, "EXPLÍCITO → TÁCITO",
        ha='center', va='bottom', fontsize=10,
        fontweight='bold', color=COL['intern'])

# ============================================================
# TÍTULO GENERAL
# ============================================================
ax.text(5.0, 10.5,
        "CICLO NONAKA-TAKEUCHI APLICADO AL ANÁLISIS DE VIGA\n"
        "Colegio Alejo Lascano — Proyecto UNESUM-REZ-2026-JIPIJAPA-001",
        ha='center', va='top', fontsize=14, fontweight='bold',
        color='#1A1A2E')

# ============================================================
# FLECHA DE RETROALIMENTACIÓN (ciclo virtuoso)
# ============================================================
ax.text(5.0, 5.0, "", ha='center', va='center')

# ============================================================
# GUARDAR Y MOSTRAR
# ============================================================
plt.tight_layout()
plt.savefig('ciclo_nonaka_viga.png', dpi=200,
            bbox_inches='tight', facecolor='#F5F5F5')
plt.show()
print("✅ Imagen guardada: ciclo_nonaka_viga.png")
print("📂 Ubicación: misma carpeta del script")