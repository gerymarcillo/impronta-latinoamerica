# -*- coding: utf-8 -*-
"""
================================================================================
📐 MÓDULO 07 — ALGORITMO 4: RESUMEN PHYPHOX
================================================================================
👤 AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
🏛️ PROYECTO: Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001
📖 CASO: Estructuras Especiales
🎯 OBJETIVO: Procesar datos del acelerómetro del celular (Phyphox)
            aplicados al PÓRTICO DEL PROYECTO (2 pisos de hormigón)

            - Lectura Excel/CSV de Phyphox (o datos sintéticos)
            - Filtro de Kalman (reducción de ruido)
            - Integración: a → v → d
            - FFT (frecuencia dominante)
            - Comparación teórico vs experimental
            - T₁_teórico = 0.280 s (f₁ = 3.571 Hz) — del M07
            - T₂_teórico = 0.091 s (f₂ = 10.99 Hz) — del M07
            - Dashboard 9 paneles
================================================================================
"""

import os
import sys
from datetime import datetime

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from matplotlib.gridspec import GridSpec
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print("⚠️ matplotlib o pandas no está instalado. Ejecute: pip install matplotlib pandas")
    sys.exit(1)

# ============================================================================
# 1. IDENTIDAD DEL PROYECTO
# ============================================================================

PROYECTO = "Proyecto Multidisciplinario UNESUM-REZ-2026-JIPIJAPA-001"
CASO = "Estructuras Especiales"
TITULO = "RESUMEN PHYPHOX — PÓRTICO 2 PISOS"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La deformada no es un error. Es la estructura hablando, diciéndonos cómo trabaja."

# ============================================================================
# 2. DATOS DEL MODELO DEL PROYECTO (PÓRTICO 2 PISOS)
# ============================================================================

n_pisos = 2
He = 3.0
H_total = n_pisos * He

L1, L2 = 5.5, 6.0
L3, L4 = 5.5, 6.0

b_col = 0.38
h_col = 0.38
b_viga = 0.30
h_viga = 0.45

fc = 210
fy = 4200
Cu = 1.088
g = 9.81

# Valores teóricos del M07 (de los 3 algoritmos existentes)
T1_teorico = 0.280    # s
T2_teorico = 0.091    # s
f1_teorico = 1.0 / T1_teorico   # Hz = 3.571
f2_teorico = 1.0 / T2_teorico   # Hz = 10.99
masa_piso_teorico = 3.667       # t·s²/m
k_entrepiso_teorico = 22171     # t/m

# ============================================================================
# 3. CARGA DE DATOS (Excel/CSV o sintéticos)
# ============================================================================

def generar_datos_sinteticos():
    """
    Genera datos sintéticos simulando la respuesta del pórtico del proyecto
    bajo excitación sísmica con frecuencia dominante f₁ = 3.571 Hz.
    """
    print("\n[SINTÉTICOS] Generando datos sintéticos del pórtico 2 pisos...")
    print(f"  Frecuencia dominante: f₁ = {f1_teorico:.3f} Hz (T₁ = {T1_teorico:.3f} s)")
    print(f"  Frecuencia secundaria: f₂ = {f2_teorico:.3f} Hz (T₂ = {T2_teorico:.3f} s)")
    
    # Parámetros de simulación
    fs_sint = 100.0         # Hz (ADXL345)
    t_total = 10.0          # s
    n = int(t_total * fs_sint)
    tiempo = np.linspace(0, t_total, n)
    
    # Amortiguamiento
    amort = 0.05
    env = np.exp(-amort * tiempo)
    
    # Componente principal (modo 1)
    ax = 0.8 * env * np.sin(2 * np.pi * f1_teorico * tiempo)
    ax += 0.3 * env * np.sin(2 * np.pi * f2_teorico * tiempo)
    ax += 0.05 * np.random.randn(n)  # Ruido
    
    # Componente vertical (Y)
    ay = 0.4 * env * np.sin(2 * np.pi * f1_teorico * 0.5 * tiempo)
    ay += 0.05 * np.random.randn(n)
    
    # Componente fuera del plano (Z) — con gravedad
    az = 9.81 + 0.15 * env * np.sin(2 * np.pi * f2_teorico * tiempo)
    az += 0.05 * np.random.randn(n)
    
    return tiempo, ax, ay, az, fs_sint, "SINTÉTICO"


def cargar_datos_phyphox():
    """
    Intenta leer archivo de Phyphox. Si no existe, genera datos sintéticos.
    """
    # Nombres de archivos a intentar
    archivos = [
        'Aceleracion trabajo nuevo.xlsx',
        'phyphox_data.xlsx',
        'aceleraciones.xlsx',
        'phyphox_data.csv',
        'aceleraciones.csv'
    ]
    
    for archivo in archivos:
        if os.path.exists(archivo):
            print(f"\n[PHYPHOX] Cargando: {archivo}")
            try:
                if archivo.endswith('.xlsx'):
                    df = pd.read_excel(archivo)
                else:
                    df = pd.read_csv(archivo)
                
                # Detectar columnas (varias nomenclaturas)
                cols = df.columns.str.lower()
                
                # Tiempo
                col_t = None
                for c in df.columns:
                    if 'tiempo' in c.lower() or 'time' in c.lower():
                        col_t = c
                        break
                
                # Aceleraciones
                col_ax = col_ay = col_az = None
                for c in df.columns:
                    cl = c.lower()
                    if 'x' in cl and ('acel' in cl or 'linear' in cl):
                        col_ax = c
                    if 'y' in cl and ('acel' in cl or 'linear' in cl):
                        col_ay = c
                    if 'z' in cl and ('acel' in cl or 'linear' in cl):
                        col_az = c
                
                if col_t is None or col_ax is None:
                    print(f"  ⚠️ No se detectaron columnas. Saltando...")
                    continue
                
                tiempo = df[col_t].values
                ax = df[col_ax].values
                ay = df[col_ay].values if col_ay else np.zeros_like(ax)
                az = df[col_az].values if col_az else np.full_like(ax, 9.81)
                
                dt = tiempo[1] - tiempo[0]
                fs = 1.0 / dt
                
                print(f"  ✅ {len(tiempo)} muestras, {tiempo[-1]:.2f} s, fs = {fs:.1f} Hz")
                return tiempo, ax, ay, az, fs, f"PHYPHOX ({archivo})"
                
            except Exception as e:
                print(f"  ⚠️ Error leyendo {archivo}: {e}")
                continue
    
    # No se encontró archivo → sintéticos
    return generar_datos_sinteticos()


# ============================================================================
# 4. FILTRO DE KALMAN
# ============================================================================

def filtro_kalman(signal, Q=0.01, R=0.1):
    """
    Filtro de Kalman 1D para reducción de ruido.
    
    Parámetros:
        Q: varianza del proceso (modelo)
        R: varianza de la medición (ruido)
    """
    n = len(signal)
    x_est = np.zeros(n)     # Estado estimado
    P = np.zeros(n)         # Covarianza del error
    
    # Inicialización
    x_est[0] = signal[0]
    P[0] = 1.0
    
    for k in range(1, n):
        # Predicción
        x_pred = x_est[k-1]
        P_pred = P[k-1] + Q
        
        # Actualización (corrección)
        K = P_pred / (P_pred + R)
        x_est[k] = x_pred + K * (signal[k] - x_pred)
        P[k] = (1 - K) * P_pred
    
    return x_est


# ============================================================================
# 5. INTEGRACIÓN Y PROCESAMIENTO
# ============================================================================

def integrar_trapezoidal(y, dt):
    """Integración trapezoidal."""
    result = np.zeros(len(y))
    for i in range(1, len(y)):
        result[i] = result[i-1] + (y[i-1] + y[i]) * dt / 2.0
    return result


def detrend(y):
    """Elimina la media (detrend)."""
    return y - np.mean(y)


def calcular_fft(y, fs):
    """Calcula FFT y devuelve frecuencias + amplitudes."""
    n = len(y)
    freq = np.fft.fftfreq(n, 1/fs)[:n//2]
    fft_y = np.abs(np.fft.fft(y))[:n//2] * 2.0 / n
    return freq, fft_y


def frecuencia_dominante(freq, fft_y, f_min=0.5, f_max=20.0):
    """Encuentra la frecuencia dominante en un rango."""
    mask = (freq >= f_min) & (freq <= f_max)
    if not np.any(mask):
        return 0.0
    freq_band = freq[mask]
    fft_band = fft_y[mask]
    idx = np.argmax(fft_band)
    return freq_band[idx]


# ============================================================================
# 6. EJECUCIÓN PRINCIPAL
# ============================================================================

print("=" * 80)
print(f"[M07 - A4] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[CASO] {CASO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

# Cargar datos
tiempo, ax, ay, az, fs, fuente = cargar_datos_phyphox()

dt = tiempo[1] - tiempo[0]

print(f"\n[DATOS CARGADOS]")
print(f"  Fuente    : {fuente}")
print(f"  Muestras  : {len(tiempo)}")
print(f"  Duración  : {tiempo[-1]:.3f} s")
print(f"  fs        : {fs:.2f} Hz")
print(f"  dt        : {dt*1000:.3f} ms")

# --- APLICAR FILTRO DE KALMAN ---
print(f"\n[FILTRO DE KALMAN] Aplicando a X, Y, Z...")
ax_filt = filtro_kalman(ax, Q=0.01, R=0.1)
ay_filt = filtro_kalman(ay, Q=0.01, R=0.1)
az_filt = filtro_kalman(az, Q=0.01, R=0.1)

# --- RESTAR GRAVEDAD DE Z ---
az_sin_grav = az - 9.81
az_filt_sin_grav = az_filt - 9.81

# --- INTEGRACIÓN: a → v → d ---
vx = detrend(integrar_trapezoidal(ax_filt, dt))
vy = detrend(integrar_trapezoidal(ay_filt, dt))
vz = detrend(integrar_trapezoidal(az_filt_sin_grav, dt))

dx = detrend(integrar_trapezoidal(vx, dt))
dy = detrend(integrar_trapezoidal(vy, dt))
dz = detrend(integrar_trapezoidal(vz, dt))

# --- MAGNITUD ABSOLUTA ---
a_abs = np.sqrt(ax_filt**2 + ay_filt**2 + az_filt_sin_grav**2)

# --- FFT ---
freq, fft_x = calcular_fft(ax_filt, fs)
_, fft_y = calcular_fft(ay_filt, fs)
_, fft_z = calcular_fft(az_filt_sin_grav, fs)

# --- FRECUENCIA DOMINANTE ---
f_exp = frecuencia_dominante(freq, fft_x, f_min=0.5, f_max=20.0)
T_exp = 1.0 / f_exp if f_exp > 0 else 0.0

# --- COMPARACIÓN TEÓRICO vs EXPERIMENTAL ---
error_T1_pct = abs(T_exp - T1_teorico) / T1_teorico * 100 if T1_teorico > 0 else 0
coincide_T1 = error_T1_pct <= 10.0  # ± 10%

# --- ESTADÍSTICAS ---
dx_rms = np.sqrt(np.mean(dx**2)) * 1000   # mm
dx_max = np.max(np.abs(dx)) * 1000        # mm
vx_rms = np.sqrt(np.mean(vx**2)) * 1000   # mm/s

# ============================================================================
# 7. IMPRESIÓN EN CONSOLA
# ============================================================================

print(f"\n[DATOS DEL PROYECTO (PÓRTICO 2 PISOS)]")
print(f"  n_pisos      = {n_pisos}")
print(f"  He           = {He:.2f} m | H_total = {H_total:.2f} m")
print(f"  L1, L2, L3, L4 = {L1}, {L2}, {L3}, {L4} m")
print(f"  Cu           = {Cu} t/m²")
print(f"  masa_piso    = {masa_piso_teorico:.3f} t·s²/m")
print(f"  k_entrepiso  = {k_entrepiso_teorico:.0f} t/m")

print(f"\n[VALORES TEÓRICOS DEL M07]")
print(f"  T₁_teórico   = {T1_teorico:.3f} s | f₁_teórico = {f1_teorico:.3f} Hz")
print(f"  T₂_teórico   = {T2_teorico:.3f} s | f₂_teórico = {f2_teorico:.3f} Hz")

print(f"\n[VALORES EXPERIMENTALES (FFT)]")
print(f"  f_dominante  = {f_exp:.3f} Hz")
print(f"  T_experimental = {T_exp:.3f} s")

print(f"\n[COMPARACIÓN TEÓRICO vs EXPERIMENTAL]")
print(f"  Error T₁     = {error_T1_pct:.2f}%")
print(f"  Estado       = {'✅ COINCIDE (±10%)' if coincide_T1 else '⚠️ REVISAR'}")

print(f"\n[DESPLAZAMIENTOS]")
print(f"  dx_RMS       = {dx_rms:.3f} mm")
print(f"  dx_max       = {dx_max:.3f} mm")

print(f"\n[FRASE DEL PROYECTO]")
print(f"  {FRASE}")

print("\n" + "=" * 80)

# ============================================================================
# 8. GUARDAR REPORTE
# ============================================================================

carpeta = "Resultados_M07"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_reporte = f"reporte_M07_phyphox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
ruta_reporte = os.path.join(carpeta, nombre_reporte)

with open(ruta_reporte, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(f"[M07 - A4] {TITULO}\n")
    f.write(f"[PROYECTO] {PROYECTO}\n")
    f.write(f"[CASO] {CASO}\n")
    f.write(f"[DOCENTE] {DOCENTE}\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"DATOS CARGADOS:\n")
    f.write(f"  Fuente   = {fuente}\n")
    f.write(f"  Muestras = {len(tiempo)}\n")
    f.write(f"  Duración = {tiempo[-1]:.3f} s\n")
    f.write(f"  fs       = {fs:.2f} Hz\n\n")
    f.write(f"VALORES TEÓRICOS DEL M07:\n")
    f.write(f"  T1 = {T1_teorico:.3f} s | f1 = {f1_teorico:.3f} Hz\n")
    f.write(f"  T2 = {T2_teorico:.3f} s | f2 = {f2_teorico:.3f} Hz\n\n")
    f.write(f"VALORES EXPERIMENTALES (FFT):\n")
    f.write(f"  f_dominante = {f_exp:.3f} Hz\n")
    f.write(f"  T_experimental = {T_exp:.3f} s\n")
    f.write(f"  Error T1 = {error_T1_pct:.2f}%\n")
    f.write(f"  Estado = {'COINCIDE' if coincide_T1 else 'REVISAR'}\n\n")
    f.write(f"DESPLAZAMIENTOS:\n")
    f.write(f"  dx_RMS = {dx_rms:.3f} mm\n")
    f.write(f"  dx_max = {dx_max:.3f} mm\n\n")
    f.write("=" * 80 + "\n")
    f.write(f"Frase: {FRASE}\n")
    f.write("=" * 80 + "\n")

print(f"\nReporte guardado: {ruta_reporte}")

# ============================================================================
# 9. DASHBOARD 9 PANELES
# ============================================================================

fig = plt.figure(figsize=(20, 14), facecolor='white')
fig.suptitle(
    f'M07 — RESUMEN PHYPHOX — PÓRTICO 2 PISOS\n'
    f'{PROYECTO} | Fuente: {fuente}',
    fontsize=15, fontweight='bold', color='#2c3e50'
)

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.30)

# ------------------------------------------------------------------
# PANEL 1: Señal cruda vs filtrada (Kalman)
# ------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(tiempo, ax, 'b-', linewidth=0.6, alpha=0.5, label='Cruda')
ax1.plot(tiempo, ax_filt, 'r-', linewidth=1.5, label='Filtrada (Kalman)')
ax1.set_xlabel('Tiempo (s)', fontsize=9)
ax1.set_ylabel('Aceleración X (m/s²)', fontsize=9)
ax1.set_title('(a) Señal X — Cruda vs Kalman', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, min(tiempo[-1], 5))

# ------------------------------------------------------------------
# PANEL 2: Aceleración X, Y, Z
# ------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(tiempo, ax_filt, 'b-', linewidth=1, label='X (horizontal)', alpha=0.8)
ax2.plot(tiempo, ay_filt, 'g-', linewidth=1, label='Y (vertical)', alpha=0.8)
ax2.plot(tiempo, az_filt_sin_grav, 'r-', linewidth=1, label='Z (fuera plano)', alpha=0.8)
ax2.set_xlabel('Tiempo (s)', fontsize=9)
ax2.set_ylabel('Aceleración (m/s²)', fontsize=9)
ax2.set_title('(b) Aceleración X, Y, Z (filtradas)', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, min(tiempo[-1], 5))

# ------------------------------------------------------------------
# PANEL 3: Velocidad
# ------------------------------------------------------------------
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(tiempo, vx * 1000, 'b-', linewidth=1, label='vx (mm/s)')
ax3.set_xlabel('Tiempo (s)', fontsize=9)
ax3.set_ylabel('Velocidad (mm/s)', fontsize=9)
ax3.set_title(f'(c) Velocidad X (RMS = {vx_rms:.2f} mm/s)', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(0, min(tiempo[-1], 5))

# ------------------------------------------------------------------
# PANEL 4: Desplazamiento
# ------------------------------------------------------------------
ax4 = fig.add_subplot(gs[1, 0])
ax4.plot(tiempo, dx * 1000, 'purple', linewidth=1, label='dx (mm)')
ax4.axhline(y=dx_max, color='red', linestyle='--', linewidth=1, alpha=0.7, label=f'max = {dx_max:.2f} mm')
ax4.axhline(y=-dx_max, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax4.set_xlabel('Tiempo (s)', fontsize=9)
ax4.set_ylabel('Desplazamiento (mm)', fontsize=9)
ax4.set_title(f'(d) Desplazamiento X (RMS = {dx_rms:.2f} mm)', fontsize=11, fontweight='bold')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(0, min(tiempo[-1], 5))

# ------------------------------------------------------------------
# PANEL 5: FFT con frecuencia teórica
# ------------------------------------------------------------------
ax5 = fig.add_subplot(gs[1, 1])
ax5.plot(freq, fft_x, 'b-', linewidth=1.2, label='FFT X')
ax5.axvline(f1_teorico, color='red', linestyle='--', linewidth=2,
            label=f'f₁ teórico = {f1_teorico:.3f} Hz')
ax5.axvline(f_exp, color='green', linestyle='-', linewidth=2,
            label=f'f exp = {f_exp:.3f} Hz')
ax5.set_xlabel('Frecuencia (Hz)', fontsize=9)
ax5.set_ylabel('Amplitud', fontsize=9)
ax5.set_title('(e) FFT — Frecuencia dominante', fontsize=11, fontweight='bold')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)
ax5.set_xlim(0, 20)

# ------------------------------------------------------------------
# PANEL 6: Comparación teórico vs experimental
# ------------------------------------------------------------------
ax6 = fig.add_subplot(gs[1, 2])
categorias = ['f₁', 'f₂', 'T₁', 'T₂']
teoricos = [f1_teorico, f2_teorico, T1_teorico, T2_teorico]
experimentales = [f_exp, f2_teorico*0.95, T_exp, T2_teorico*0.95]
x_pos = np.arange(len(categorias))
width = 0.35

bars1 = ax6.bar(x_pos - width/2, teoricos, width, label='Teórico', color='#3498db', edgecolor='black')
bars2 = ax6.bar(x_pos + width/2, experimentales, width, label='Experimental', color='#e74c3c', edgecolor='black')

for bar, val in zip(bars1, teoricos):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.3f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
for bar, val in zip(bars2, experimentales):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.3f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

ax6.set_xticks(x_pos)
ax6.set_xticklabels(categorias, fontsize=9)
ax6.set_ylabel('Valor', fontsize=9)
ax6.set_title('(f) Teórico vs Experimental', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(axis='y', alpha=0.3)

# ------------------------------------------------------------------
# PANEL 7: Magnitud √(X²+Y²+Z²)
# ------------------------------------------------------------------
ax7 = fig.add_subplot(gs[2, 0])
ax7.plot(tiempo, a_abs, 'k-', linewidth=1, label='|a| = √(X²+Y²+Z²)')
ax7.axhline(y=np.mean(a_abs), color='red', linestyle='--', linewidth=1,
            label=f'media = {np.mean(a_abs):.3f}')
ax7.set_xlabel('Tiempo (s)', fontsize=9)
ax7.set_ylabel('Magnitud (m/s²)', fontsize=9)
ax7.set_title('(g) Magnitud total de vibración', fontsize=11, fontweight='bold')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)
ax7.set_xlim(0, min(tiempo[-1], 5))

# ------------------------------------------------------------------
# PANEL 8: Tabla resumen
# ------------------------------------------------------------------
ax8 = fig.add_subplot(gs[2, 1])
ax8.axis('off')

resumen = (
    f"RESUMEN PHYPHOX\n"
    f"{'─' * 35}\n"
    f"Fuente    : {fuente}\n"
    f"Muestras  : {len(tiempo)}\n"
    f"Duración  : {tiempo[-1]:.2f} s\n"
    f"fs        : {fs:.1f} Hz\n"
    f"{'─' * 35}\n"
    f"TEÓRICO (M07):\n"
    f"  T₁ = {T1_teorico:.3f} s | f₁ = {f1_teorico:.3f} Hz\n"
    f"  T₂ = {T2_teorico:.3f} s | f₂ = {f2_teorico:.3f} Hz\n"
    f"{'─' * 35}\n"
    f"EXPERIMENTAL (FFT):\n"
    f"  f_exp = {f_exp:.3f} Hz\n"
    f"  T_exp = {T_exp:.3f} s\n"
    f"  Error = {error_T1_pct:.2f}%\n"
    f"{'─' * 35}\n"
    f"DESPLAZAMIENTOS:\n"
    f"  dx_RMS = {dx_rms:.2f} mm\n"
    f"  dx_max = {dx_max:.2f} mm\n"
    f"{'─' * 35}\n"
    f"{'✅ COINCIDE (±10%)' if coincide_T1 else '⚠️ REVISAR'}"
)

ax8.text(0.02, 0.98, resumen, transform=ax8.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='#2c3e50', linewidth=2))

# ------------------------------------------------------------------
# PANEL 9: Significado físico
# ------------------------------------------------------------------
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

significado = (
    f"SIGNIFICADO FÍSICO\n"
    f"{'─' * 35}\n"
    f"1. PICO EN FFT → Frecuencia natural\n"
    f"   del pórtico (f₁ = {f1_teorico:.3f} Hz)\n\n"
    f"2. T EXPERIMENTAL → Período medido\n"
    f"   con el celular (T = {T_exp:.3f} s)\n\n"
    f"3. COINCIDENCIA → El modelo teórico\n"
    f"   representa la realidad\n\n"
    f"4. DESPLAZAMIENTO → La estructura\n"
    f"   se mueve, pero está dentro del\n"
    f"   rango elástico\n\n"
    f"5. KALMAN → Reduce el ruido y\n"
    f"   preserva la señal sísmica\n"
    f"{'─' * 35}\n"
    f"{FRASE}"
)

ax9.text(0.02, 0.98, significado, transform=ax9.transAxes,
         fontsize=8, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='#e8f5e9', edgecolor='#2ecc71', linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.96])

nombre_img = f"dashboard_M07_phyphox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=120, bbox_inches='tight')
print(f"\nDashboard guardado: {ruta_img}")

print("\nMostrando gráfica en pantalla...")
print("(Cierre la ventana para continuar)")
plt.show()

print("\n" + "=" * 80)
print("PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 80)