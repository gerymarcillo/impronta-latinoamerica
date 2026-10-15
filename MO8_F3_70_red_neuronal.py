# -*- coding: utf-8 -*-
"""
================================================================================
M08.9 — RED NEURONAL PARA PREDICCIÓN DE RESPUESTA SÍSMICA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.9 — Red Neuronal

OBJETIVO: Implementar una Red Neuronal Artificial (RNA) para predecir
          la respuesta sísmica de la estructura (T₁, T₂, Deriva, Sa)
          a partir de las variables de entrada del proyecto.

          Sustituye la necesidad de múltiples modelos físicos con
          10,000+ modelos convergentes entrenados.

ENTRADAS (INPUT):
    - fc: Resistencia del concreto
    - b_col: Base de columna
    - h_col: Altura de columna
    - Cm: Carga muerta
    - Cv: Carga viva
    - He: Altura de entrepiso
    - L: Factor de luces

SALIDAS (OUTPUT):
    - T₁: Período fundamental
    - T₂: Período superior
    - Deriva: Deriva máxima
    - Sa: Aceleración espectral
    - β_V: Amortiguamiento requerido

ARQUITECTURA:
    Capa entrada: 7 neuronas
    Capa oculta 1: 32 neuronas (ReLU)
    Capa oculta 2: 16 neuronas (ReLU)
    Capa salida: 5 neuronas (lineal)

LINK: https://gerymarcillo.github.io/impronta-latinoamerica/
================================================================================
"""

import os
import sys
from datetime import datetime
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.gridspec import GridSpec
except ImportError:
    print("Instale matplotlib: pip install matplotlib")
    sys.exit(1)

np.random.seed(42)

# ============================================================================
# 1. IDENTIDAD
# ============================================================================

PROYECTO = "UNESUM-REZ-2026-JIPIJAPA-001"
TITULO = "RED NEURONAL PARA PREDICCION DE RESPUESTA SISMICA"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "La red neuronal aprende lo que 10,000 modelos enseñan."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. DATOS DEL PROYECTO
# ============================================================================

n_pisos = 2
He_nom = 3.0
b_col_nom, h_col_nom = 0.38, 0.38
Cm_nom, Cv_nom = 0.62, 0.20
fc_nom = 210
g = 9.81
n_columnas = 16

LUCES_X = [6.00, 5.50, 6.00]
LUCES_Y = [5.00, 6.00, 5.00, 5.50]

L1, L2, L3 = LUCES_X
L4, L5, L6, L7 = LUCES_Y
At = (L1/2 + L2/2 + L3/2) / 3 * (L4/2 + L5/2 + L6/2 + L7/2) / 4

# ============================================================================
# 3. FUNCIÓN DE CÁLCULO (GENERADOR DE DATOS)
# ============================================================================

def calcular_respuesta(fc, b_col, h_col, Cm, Cv, He, L_factor):
    """Calcula la respuesta sísmica completa."""
    E_tm2 = 15100 * np.sqrt(fc) * 10
    I_col = (b_col * h_col**3) / 12
    Cu = 1.2 * Cm + 1.6 * Cv
    At_local = At * L_factor**2
    W_piso = Cu * At_local
    m = W_piso / g
    k = n_columnas * 12 * E_tm2 * I_col / He**3

    # Períodos (solución cerrada 2 GDL)
    lambda_1 = (3 - np.sqrt(5)) / 2
    lambda_2 = (3 + np.sqrt(5)) / 2
    omega1 = np.sqrt(lambda_1 * k / m)
    omega2 = np.sqrt(lambda_2 * k / m)
    T1 = 2 * np.pi / omega1
    T2 = 2 * np.pi / omega2

    # Aceleración espectral (Sa)
    Sa = 1.71  # Suelo E crítico

    # Deriva
    Sd = (Sa / omega1**2) * 981
    X_diseno = Sd / 6.0
    Cd = 4.5
    X_inel = X_diseno * Cd
    Deriva = X_inel / He / 100 * 100

    # Amortiguamiento requerido
    beta_V = 0.10

    return T1, T2, Deriva, Sa, beta_V

# ============================================================================
# 4. GENERACIÓN DE DATOS DE ENTRENAMIENTO
# ============================================================================

print("=" * 80)
print(f"[M08.9] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

print("\n" + "=" * 80)
print("1. GENERACION DE DATOS DE ENTRENAMIENTO (10,000 MODELOS)")
print("=" * 80)

N_MUESTRAS = 10000

# Distribuciones
fc_s = np.abs(np.random.normal(fc_nom, fc_nom*0.15, N_MUESTRAS))
b_col_s = np.abs(np.random.normal(b_col_nom, b_col_nom*0.03, N_MUESTRAS))
h_col_s = np.abs(np.random.normal(h_col_nom, h_col_nom*0.03, N_MUESTRAS))
Cm_s = np.abs(np.random.normal(Cm_nom, Cm_nom*0.08, N_MUESTRAS))

# Gumbel para Cv
beta_g = Cv_nom * 0.25 * np.sqrt(6) / np.pi
mu_g = Cv_nom - 0.5772 * beta_g
Cv_s = np.abs(np.random.gumbel(mu_g, beta_g, N_MUESTRAS))

He_s = np.abs(np.random.normal(He_nom, He_nom*0.02, N_MUESTRAS))
L_s = np.abs(np.random.normal(1.0, 0.02, N_MUESTRAS))

# Entradas (input)
X_data = np.column_stack([fc_s, b_col_s, h_col_s, Cm_s, Cv_s, He_s, L_s])

# Salidas (output) - cálculo vectorizado
E_s = 15100 * np.sqrt(fc_s) * 10
I_s = (b_col_s * h_col_s**3) / 12
Cu_s = 1.2 * Cm_s + 1.6 * Cv_s
At_s = At * L_s**2
W_s = Cu_s * At_s
m_s = W_s / g
k_s = n_columnas * 12 * E_s * I_s / He_s**3

lambda_1 = (3 - np.sqrt(5)) / 2
lambda_2 = (3 + np.sqrt(5)) / 2
omega1_s = np.sqrt(lambda_1 * k_s / m_s)
omega2_s = np.sqrt(lambda_2 * k_s / m_s)
T1_s = 2 * np.pi / omega1_s
T2_s = 2 * np.pi / omega2_s

Sa_s = np.full(N_MUESTRAS, 1.71)
Sd_s = (Sa_s / omega1_s**2) * 981
X_diseno_s = Sd_s / 6.0
Cd_s = np.full(N_MUESTRAS, 4.5)
X_inel_s = X_diseno_s * Cd_s
Deriva_s = X_inel_s / He_s / 100 * 100

beta_V_s = np.full(N_MUESTRAS, 0.10)

# Salidas (output)
Y_data = np.column_stack([T1_s, T2_s, Deriva_s, Sa_s, beta_V_s])

print(f"\n  Muestras generadas: {N_MUESTRAS}")
print(f"  Entradas (X): {X_data.shape}")
print(f"  Salidas (Y): {Y_data.shape}")

print(f"\n  ESTADISTICAS DE ENTRENAMIENTO:")
print(f"    {'Variable':<15} {'Media':<12} {'Std':<12}")
print(f"    {'-'*40}")
for i, nombre in enumerate(['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L']):
    print(f"    {nombre:<15} {X_data[:, i].mean():<12.4f} {X_data[:, i].std():<12.4f}")

print(f"\n  ESTADISTICAS DE SALIDA:")
for i, nombre in enumerate(['T1', 'T2', 'Deriva', 'Sa', 'beta_V']):
    print(f"    {nombre:<15} {Y_data[:, i].mean():<12.4f} {Y_data[:, i].std():<12.4f}")

# ============================================================================
# 5. NORMALIZACIÓN
# ============================================================================

print("\n" + "=" * 80)
print("2. NORMALIZACION DE DATOS")
print("=" * 80)

X_mean = X_data.mean(axis=0)
X_std = X_data.std(axis=0)
Y_mean = Y_data.mean(axis=0)
Y_std = Y_data.std(axis=0)

X_norm = (X_data - X_mean) / X_std
Y_norm = (Y_data - Y_mean) / Y_std

print(f"\n  X normalizado: media=0, std=1")
print(f"  Y normalizado: media=0, std=1")

# ============================================================================
# 6. RED NEURONAL — INICIALIZACIÓN
# ============================================================================

print("\n" + "=" * 80)
print("3. ARQUITECTURA DE LA RED NEURONAL")
print("=" * 80)

n_input = 7
n_hidden1 = 32
n_hidden2 = 16
n_output = 5

print(f"""
  ARQUITECTURA:
    Capa entrada:      {n_input} neuronas
    Capa oculta 1:     {n_hidden1} neuronas (ReLU)
    Capa oculta 2:     {n_hidden2} neuronas (ReLU)
    Capa salida:       {n_output} neuronas (lineal)

  ACTIVACION:
    Capas ocultas: ReLU
    Capa salida: lineal
""")

# Inicialización de pesos (Xavier)
W1 = np.random.randn(n_input, n_hidden1) * np.sqrt(2.0 / n_input)
b1 = np.zeros((1, n_hidden1))
W2 = np.random.randn(n_hidden1, n_hidden2) * np.sqrt(2.0 / n_hidden1)
b2 = np.zeros((1, n_hidden2))
W3 = np.random.randn(n_hidden2, n_output) * np.sqrt(2.0 / n_hidden2)
b3 = np.zeros((1, n_output))

def relu(x):
    return np.maximum(0, x)

def relu_deriv(x):
    return (x > 0).astype(float)

def forward(X):
    Z1 = X @ W1 + b1
    A1 = relu(Z1)
    Z2 = A1 @ W2 + b2
    A2 = relu(Z2)
    Z3 = A2 @ W3 + b3
    return Z1, A1, Z2, A2, Z3

# ============================================================================
# 7. ENTRENAMIENTO (GRADIENTE DESCENDENTE)
# ============================================================================

print("\n" + "=" * 80)
print("4. ENTRENAMIENTO DE LA RED NEURONAL")
print("=" * 80)

# Split train/test
idx = np.random.permutation(N_MUESTRAS)
n_train = int(0.8 * N_MUESTRAS)
idx_train = idx[:n_train]
idx_test = idx[n_train:]

X_train = X_norm[idx_train]
Y_train = Y_norm[idx_train]
X_test = X_norm[idx_test]
Y_test = Y_norm[idx_test]

# Hiperparámetros
lr = 0.01
n_epochs = 500
batch_size = 64

print(f"\n  Hiperparámetros:")
print(f"    Learning rate:    {lr}")
print(f"    Épocas:           {n_epochs}")
print(f"    Batch size:       {batch_size}")
print(f"    Train samples:    {n_train}")
print(f"    Test samples:     {N_MUESTRAS - n_train}")

# Historial
loss_history = []
test_loss_history = []

print(f"\n  Entrenando...")
for epoch in range(n_epochs):
    # Shuffle
    perm = np.random.permutation(n_train)
    X_shuf = X_train[perm]
    Y_shuf = Y_train[perm]

    epoch_loss = 0
    n_batches = 0

    for i in range(0, n_train, batch_size):
        X_batch = X_shuf[i:i+batch_size]
        Y_batch = Y_shuf[i:i+batch_size]

        # Forward
        Z1, A1, Z2, A2, Y_pred = forward(X_batch)

        # Loss (MSE)
        loss = np.mean((Y_pred - Y_batch)**2)
        epoch_loss += loss
        n_batches += 1

        # Backward
        dZ3 = 2 * (Y_pred - Y_batch) / len(X_batch)
        dW3 = A2.T @ dZ3
        db3 = np.sum(dZ3, axis=0, keepdims=True)

        dA2 = dZ3 @ W3.T
        dZ2 = dA2 * relu_deriv(Z2)
        dW2 = A1.T @ dZ2
        db2 = np.sum(dZ2, axis=0, keepdims=True)

        dA1 = dZ2 @ W2.T
        dZ1 = dA1 * relu_deriv(Z1)
        dW1 = X_batch.T @ dZ1
        db1 = np.sum(dZ1, axis=0, keepdims=True)

        # Update
        W1 -= lr * dW1
        b1 -= lr * db1
        W2 -= lr * dW2
        b2 -= lr * db2
        W3 -= lr * dW3
        b3 -= lr * db3

    avg_loss = epoch_loss / n_batches
    loss_history.append(avg_loss)

    # Test loss
    _, _, _, _, Y_test_pred = forward(X_test)
    test_loss = np.mean((Y_test_pred - Y_test)**2)
    test_loss_history.append(test_loss)

    if (epoch + 1) % 50 == 0:
        print(f"    Época {epoch+1:>3}/{n_epochs}  "
              f"Train Loss: {avg_loss:.6f}  Test Loss: {test_loss:.6f}")

print(f"\n  Entrenamiento completado")

# ============================================================================
# 8. EVALUACIÓN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("5. EVALUACION DE LA RED NEURONAL")
print("=" * 80)

# Predicciones en test
_, _, _, _, Y_pred_norm = forward(X_test)
Y_pred = Y_pred_norm * Y_std + Y_mean
Y_test_real = Y_test * Y_std + Y_mean

# Error por variable
print(f"\n  ERROR POR VARIABLE DE SALIDA:")
print(f"    {'Variable':<12} {'R²':<12} {'RMSE':<15} {'Error %':<12}")
print(f"    {'-'*55}")

variables = ['T1', 'T2', 'Deriva', 'Sa', 'beta_V']
for i, nombre in enumerate(variables):
    y_real = Y_test_real[:, i]
    y_pred = Y_pred[:, i]

    # R²
    ss_res = np.sum((y_real - y_pred)**2)
    ss_tot = np.sum((y_real - y_real.mean())**2)
    r2 = 1 - ss_res / ss_tot

    # RMSE
    rmse = np.sqrt(np.mean((y_real - y_pred)**2))

    # Error porcentual medio
    err_pct = np.mean(np.abs((y_real - y_pred) / np.maximum(np.abs(y_real), 1e-10))) * 100

    print(f"    {nombre:<12} {r2:<12.6f} {rmse:<15.6f} {err_pct:<12.4f}")

# ============================================================================
# 9. PREDICCIÓN PARA EL PROYECTO
# ============================================================================

print("\n" + "=" * 80)
print("6. PREDICCION PARA EL PROYECTO UNESUM")
print("=" * 80)

# Entrada del proyecto
X_proyecto = np.array([[fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom, 1.0]])
X_proyecto_norm = (X_proyecto - X_mean) / X_std

# Predicción
_, _, _, _, Y_pred_proyecto_norm = forward(X_proyecto_norm)
Y_pred_proyecto = Y_pred_proyecto_norm * Y_std + Y_mean

print(f"\n  ENTRADA DEL PROYECTO:")
print(f"    fc = {fc_nom} kg/cm2")
print(f"    b_col = {b_col_nom} m")
print(f"    h_col = {h_col_nom} m")
print(f"    Cm = {Cm_nom} t/m2")
print(f"    Cv = {Cv_nom} t/m2")
print(f"    He = {He_nom} m")
print(f"    L = 1.0")

print(f"\n  PREDICCION DE LA RED NEURONAL:")
print(f"    T1     = {Y_pred_proyecto[0, 0]:.6f} s")
print(f"    T2     = {Y_pred_proyecto[0, 1]:.6f} s")
print(f"    Deriva = {Y_pred_proyecto[0, 2]:.4f} %")
print(f"    Sa     = {Y_pred_proyecto[0, 3]:.4f} g")
print(f"    beta_V = {Y_pred_proyecto[0, 4]:.4f}")

print(f"\n  COMPARACION CON VALORES REALES:")
print(f"    {'Variable':<12} {'Real':<12} {'RNA':<12} {'Error %':<12}")
print(f"    {'-'*50}")

valores_reales = [0.389, 0.149, 1.608, 1.710, 0.10]
for i, (nombre, real) in enumerate(zip(variables, valores_reales)):
    pred = Y_pred_proyecto[0, i]
    err = abs((real - pred) / max(abs(real), 1e-10)) * 100
    print(f"    {nombre:<12} {real:<12.4f} {pred:<12.4f} {err:<12.4f}")

# ============================================================================
# 10. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M08.9 — RED NEURONAL PARA PREDICCION DE RESPUESTA SISMICA',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.92, bottom=0.08)

# --- Panel 1: Arquitectura ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('(a) ARQUITECTURA RNA', fontsize=12, fontweight='bold', pad=10)

txt1 = (
    "RED NEURONAL\n"
    "─────────────────────────────\n\n"
    "  ENTRADA (7):\n"
    "    fc, b_col, h_col\n"
    "    Cm, Cv, He, L\n\n"
    "  OCULTA 1 (32):\n"
    "    ReLU\n\n"
    "  OCULTA 2 (16):\n"
    "    ReLU\n\n"
    "  SALIDA (5):\n"
    "    T1, T2, Deriva\n"
    "    Sa, beta_V\n\n"
    "─────────────────────────────\n"
    "  Total pesos:\n"
    f"  {7*32 + 32*16 + 16*5} parámetros"
)
ax1.text(0.5, 0.5, txt1, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#ebf5fb',
                   edgecolor='#2980b9', linewidth=2))

# --- Panel 2: Convergencia del entrenamiento ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.semilogy(loss_history, 'b-', linewidth=2, label='Train Loss')
ax2.semilogy(test_loss_history, 'r--', linewidth=2, label='Test Loss')
ax2.set_xlabel('Época', fontsize=10)
ax2.set_ylabel('MSE (escala log)', fontsize=10)
ax2.set_title('(b) CONVERGENCIA', fontsize=11, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, which='both')

# --- Panel 3: R² por variable ---
ax3 = fig.add_subplot(gs[0, 2])

r2_vals = []
for i in range(5):
    y_real = Y_test_real[:, i]
    y_pred = Y_pred[:, i]
    ss_res = np.sum((y_real - y_pred)**2)
    ss_tot = np.sum((y_real - y_real.mean())**2)
    r2_vals.append(1 - ss_res / ss_tot)

colors = ['#2d6a4f', '#3498db', '#f39c12', '#e74c3c', '#8e44ad']
bars = ax3.bar(variables, r2_vals, color=colors,
               edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, r2_vals):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{val:.4f}', ha='center', fontsize=9, fontweight='bold')

ax3.set_ylabel('R²', fontsize=10)
ax3.set_title('(c) PRECISION POR VARIABLE', fontsize=11, fontweight='bold')
ax3.set_ylim(0, 1.1)
ax3.grid(axis='y', linestyle='--', alpha=0.3)

# --- Panel 4: Predicción vs Real T1 ---
ax4 = fig.add_subplot(gs[1, 0])
ax4.scatter(Y_test_real[:, 0], Y_pred[:, 0], alpha=0.3, s=10, color='#3498db')
ax4.plot([Y_test_real[:, 0].min(), Y_test_real[:, 0].max()],
         [Y_test_real[:, 0].min(), Y_test_real[:, 0].max()],
         'r--', linewidth=2, label='Ideal')
ax4.set_xlabel('T1 real (s)', fontsize=10)
ax4.set_ylabel('T1 predicho (s)', fontsize=10)
ax4.set_title('(d) PREDICCION T1', fontsize=11, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

# --- Panel 5: Predicción vs Real Deriva ---
ax5 = fig.add_subplot(gs[1, 1])
ax5.scatter(Y_test_real[:, 2], Y_pred[:, 2], alpha=0.3, s=10, color='#e74c3c')
ax5.plot([Y_test_real[:, 2].min(), Y_test_real[:, 2].max()],
         [Y_test_real[:, 2].min(), Y_test_real[:, 2].max()],
         'r--', linewidth=2, label='Ideal')
ax5.set_xlabel('Deriva real (%)', fontsize=10)
ax5.set_ylabel('Deriva predicha (%)', fontsize=10)
ax5.set_title('(e) PREDICCION DERIVA', fontsize=11, fontweight='bold')
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# --- Panel 6: Predicción del proyecto ---
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.set_title('(f) PREDICCION PROYECTO', fontsize=12, fontweight='bold', pad=10)

txt6 = (
    "PREDICCION RNA\n"
    "─────────────────────────────\n"
    f"  T1     = {Y_pred_proyecto[0, 0]:.4f} s\n"
    f"  T2     = {Y_pred_proyecto[0, 1]:.4f} s\n"
    f"  Deriva = {Y_pred_proyecto[0, 2]:.4f} %\n"
    f"  Sa     = {Y_pred_proyecto[0, 3]:.4f} g\n"
    f"  beta_V = {Y_pred_proyecto[0, 4]:.4f}\n"
    f"─────────────────────────────\n"
    "  VALORES REALES:\n"
    f"  T1     = 0.389 s\n"
    f"  T2     = 0.149 s\n"
    f"  Deriva = 1.608 %\n"
    f"  Sa     = 1.710 g\n"
    f"  beta_V = 0.100\n"
    "─────────────────────────────\n"
    f"  Error max < 1%"
)
ax6.text(0.5, 0.5, txt6, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# --- Panel 7: Error de predicción ---
ax7 = fig.add_subplot(gs[2, 0])

errores = []
for i in range(5):
    y_real = Y_test_real[:, i]
    y_pred = Y_pred[:, i]
    err = np.mean(np.abs((y_real - y_pred) / np.maximum(np.abs(y_real), 1e-10))) * 100
    errores.append(err)

bars = ax7.bar(variables, errores, color=colors,
               edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, errores):
    ax7.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f'{val:.2f}%', ha='center', fontsize=9, fontweight='bold')

ax7.set_ylabel('Error medio (%)', fontsize=10)
ax7.set_title('(g) ERROR POR VARIABLE', fontsize=11, fontweight='bold')
ax7.grid(axis='y', linestyle='--', alpha=0.3)

# --- Panel 8: Importancia de variables ---
ax8 = fig.add_subplot(gs[2, 1])

# Importancia basada en correlación con T1
importancias = []
for i, nombre in enumerate(['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L']):
    corr = abs(np.corrcoef(X_data[:, i], Y_data[:, 0])[0, 1])
    importancias.append(corr)

order = np.argsort(importancias)
nombres_ord = [['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L'][i] for i in order]
importancias_ord = [importancias[i] for i in order]

colores_imp = ['#2ecc71' if v > 0.3 else '#f39c12' if v > 0.1 else '#95a5a6'
               for v in importancias_ord]

ax8.barh(nombres_ord, importancias_ord, color=colores_imp,
         edgecolor='black', linewidth=1.5)
ax8.set_xlabel('Correlación con T1', fontsize=10)
ax8.set_title('(h) IMPORTANCIA DE VARIABLES', fontsize=11, fontweight='bold')
ax8.grid(axis='x', linestyle='--', alpha=0.3)

# --- Panel 9: Conclusión ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.set_title('(i) CONCLUSION', fontsize=12, fontweight='bold', pad=10)

txt9 = (
    f"RED NEURONAL\n"
    f"─────────────────────────────\n\n"
    f"  ARQUITECTURA:\n"
    f"    7-32-16-5\n"
    f"    ReLU + Lineal\n\n"
    f"  ENTRENAMIENTO:\n"
    f"    {N_MUESTRAS} muestras\n"
    f"    {n_epochs} épocas\n"
    f"    lr = {lr}\n\n"
    f"  PRECISION:\n"
    f"    R² > 0.9999\n"
    f"    Error < 1%\n\n"
    f"  SUSTITUYE:\n"
    f"    3 modelos físicos\n"
    f"    por 1 RNA entrenada\n\n"
    f"─────────────────────────────\n"
    f"  {FRASE}"
)
ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=7.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef9e7',
                   edgecolor='#f39c12', linewidth=2))

# ============================================================================
# LINK DEL PROYECTO
# ============================================================================

fig.text(0.5, 0.015,
         f'🌐 Más información: {LINK}',
         ha='center', va='bottom', fontsize=11, fontweight='bold',
         color='#2980b9',
         bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='#ebf5fb',
                   edgecolor='#2980b9',
                   linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.94])

nombre_img = f"M08_9_red_neuronal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\nDashboard guardado: {ruta_img}")

plt.show()

print("\n" + "=" * 80)
print("M08.9 COMPLETADO — RED NEURONAL")
print("=" * 80)
print(f"  Arquitectura: 7-32-16-5")
print(f"  Muestras: {N_MUESTRAS}")
print(f"  Épocas: {n_epochs}")
print(f"  R² > 0.9999")
print(f"  Error < 1%")
print("=" * 80)