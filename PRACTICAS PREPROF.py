# -*- coding: utf-8 -*-
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle, FancyBboxPatch
import warnings

# Ocultar advertencias
warnings.filterwarnings("ignore", category=UserWarning)

# ============================================================================
# 🛠️ RUTA A SU CARPETA
# ============================================================================
carpeta_trabajo = r"C:\Users\geryl\OneDrive\Escritorio\CONVOCATORIA PRACTICAS PREPROF"
if not os.path.exists(carpeta_trabajo):
    carpeta_trabajo = os.getcwd()

def buscar_por_prefijo(prefijo):
    for archivo in os.listdir(carpeta_trabajo):
        if archivo.startswith(prefijo) and archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            return mpimg.imread(os.path.join(carpeta_trabajo, archivo))
    return None

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
COLORES = {
    'fondo': '#0a0e1a', 'titulo': '#ecf0f1', 'acento_naranja': '#f39c12',
    'acento_rojo': '#e74c3c', 'texto_gris': '#bdc3c7', 'verde_validacion': '#2ecc71',
    'azul_link': '#5dade2', 'dorado_senecyt': '#E0A800'
}

fig = plt.figure(figsize=(10, 15))
fig.patch.set_facecolor(COLORES['fondo'])
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)
ax.axis('off')

# ============================================================================
# CARGAR IMÁGENES
# ============================================================================
foto_izq = buscar_por_prefijo('foto_3')
if foto_izq is None:
    foto_izq = buscar_por_prefijo('foto_1')

foto_der = buscar_por_prefijo('foto_2')

mapa_fondo = buscar_por_prefijo('mapa_sismos')
if mapa_fondo is not None:
    ax.imshow(mapa_fondo, extent=(0, 10, 0, 15), aspect='auto', zorder=0, alpha=0.3)
    ax.add_patch(Rectangle((0, 0), 10, 15, facecolor=(0, 0, 0, 0.85), zorder=1))

# ============================================================================
# LOGO UNESUM (AHORA MÁS VERTICAL)
# ============================================================================
logo_img = buscar_por_prefijo('logo_unesum')
if logo_img is not None:
    # Ajustado a (0.8 de ancho, 1.8 de alto) para que se estire hacia abajo y no se aplaste
    ax.imshow(logo_img, extent=(0.2, 1.0, 13.4, 14.9), aspect='auto', zorder=4, interpolation='bilinear')

# ============================================================================
# TEXTOS SUPERIORES
# ============================================================================
ax.text(5, 14.5, 'UNIVERSIDAD ESTATAL DEL SUR DE MANABÍ', ha='center', va='center', fontsize=12, fontweight='bold', color=COLORES['texto_gris'], zorder=3)
ax.text(5, 14.1, 'Facultad de Ciencias Técnicas — Carrera de Ingeniería Civil', ha='center', va='center', fontsize=10, color=COLORES['acento_naranja'], zorder=3)
ax.text(5, 13.0, 'CONVOCATORIA DE PRÁCTICAS\nPREPROFESIONALES', ha='center', va='center', fontsize=24, fontweight='bold', color=COLORES['titulo'], linespacing=1.2, zorder=3)
ax.text(5, 11.9, 'CERTIFICACIÓN OFICIAL + EXPOSICIÓN ABIERTA', ha='center', va='center', fontsize=10, fontweight='bold', color=COLORES['fondo'], bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORES['verde_validacion'], edgecolor='none'), zorder=3)
ax.text(5, 11.2, 'DMTP: 50 cm · Ganancia 52.7% · Deriva 0.76% (NEC-15 OK)', ha='center', va='center', fontsize=10, fontweight='bold', color=COLORES['fondo'], bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORES['acento_naranja'], edgecolor='none'), zorder=3)

# ============================================================================
# SECCIÓN VISUAL: DOS COLUMNAS
# ============================================================================
rect_izq = FancyBboxPatch((1.0, 7.2), 3.5, 3.5, boxstyle="round,pad=0.1", facecolor='#152238', edgecolor=COLORES['acento_rojo'], linewidth=3, zorder=2)
ax.add_patch(rect_izq)

rect_der = FancyBboxPatch((5.5, 7.2), 3.5, 3.5, boxstyle="round,pad=0.1", facecolor='#152238', edgecolor=COLORES['acento_naranja'], linewidth=3, zorder=2)
ax.add_patch(rect_der)

if foto_izq is not None:
    ax.imshow(foto_izq, extent=(1.1, 4.4, 7.3, 10.6), aspect='auto', zorder=3)
else:
    ax.text(2.75, 8.95, 'Falta foto 1', ha='center', va='center', fontsize=10, color='white', zorder=4)

if foto_der is not None:
    ax.imshow(foto_der, extent=(5.6, 8.9, 7.3, 10.6), aspect='auto', zorder=3)
else:
    ax.text(7.25, 8.95, 'Falta foto 2', ha='center', va='center', fontsize=10, color='white', zorder=4)

ax.text(2.75, 7.4, 'EVALUACIÓN\nPOST-SISMO', ha='center', va='center', fontsize=9, fontweight='bold', color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORES['acento_rojo'], edgecolor='none'), zorder=4)
ax.text(7.25, 7.4, 'REHABILITACIÓN\nCON DMTP', ha='center', va='center', fontsize=9, fontweight='bold', color='white', bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORES['acento_naranja'], edgecolor='none'), zorder=4)

# ============================================================================
# MENSAJE CENTRAL
# ============================================================================
texto_contexto = (
    "Proceso combinado de intervención:\n"
    "Diagnóstico Forense  ->  Rehabilitación Estructural\n\n"
    "Únete al equipo que evalúa los daños post-sismo y\n"
    "diseña el Disipador Marcillo Tensor-Puntal (DMTP)."
)
ax.text(5, 5.8, texto_contexto, ha='center', va='center', fontsize=11, color=COLORES['titulo'], linespacing=1.4, 
        bbox=dict(boxstyle='round,pad=0.8', facecolor=(0.05, 0.1, 0.15, 0.95), edgecolor=COLORES['acento_naranja'], linewidth=2), zorder=3)

# ============================================================================
# TEXTOS INFERIORES
# ============================================================================
ax.text(5, 4.2, 'Laboratorio Vivo: Agua Dulce — Escuela Presidente Urbina', ha='center', va='center', fontsize=9, fontweight='bold', color=COLORES['azul_link'], style='italic', zorder=3)
ax.text(5, 3.6, 'SOLO 5 CUPOS DISPONIBLES', ha='center', va='center', fontsize=14, fontweight='bold', color='white', bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORES['acento_rojo'], edgecolor='none'), zorder=3)
ax.text(5, 3.0, 'Apoyo del Tutor Socrático (IA)  |  Aprobación por Examen Complexivo', ha='center', va='center', fontsize=9, color=COLORES['texto_gris'], style='italic', zorder=3)
ax.text(5, 2.5, 'SENESCYT REG-INV-25-08261  ·  ORCID: 0009-0000-5583-0042', ha='center', va='center', fontsize=8, color=COLORES['dorado_senecyt'], fontweight='bold', zorder=3)
ax.text(5, 2.0, '"Hemos aportado a la resiliencia de la vida."', ha='center', va='center', fontsize=9, color=COLORES['texto_gris'], style='italic', zorder=3)

# ============================================================================
# QR MÁS PEQUEÑO Y SUBIDO
# ============================================================================
qr_img = buscar_por_prefijo('qr-code')
if qr_img is not None:
    # Hacemos el recuadro más pequeño (0.9 x 0.9) y lo subimos a Y=0.6
    rect_qr = Rectangle((4.55, 0.6), 0.9, 0.9, facecolor='white', edgecolor=COLORES['acento_naranja'], linewidth=2, zorder=4)
    ax.add_patch(rect_qr)
    ax.imshow(qr_img, extent=(4.6, 5.4, 0.65, 1.45), aspect='auto', zorder=5, interpolation='nearest')
    ax.text(5, 0.3, 'Escanea para postularte', ha='center', va='center', fontsize=9, fontweight='bold', color=COLORES['titulo'], zorder=5)

# LINK DEL PROYECTO (El que chocaba, ahora está libre)
fig.text(0.5, 0.005, 'Más información: https://gerymarcillo.github.io/impronta-latinoamerica/', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#2980b9', bbox=dict(boxstyle='round,pad=0.4', facecolor='#ebf5fb', edgecolor='#2980b9', linewidth=2))

# ============================================================================
# GUARDAR Y MOSTRAR
# ============================================================================
nombre_archivo = f"Flyer_Final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta_trabajo, nombre_archivo)
plt.savefig(ruta_img, dpi=300, bbox_inches='tight', facecolor=COLORES['fondo'])

print(f"\n✅ ¡LISTO! El flyer se ha guardado en: {ruta_img}")
plt.show(block=True) 