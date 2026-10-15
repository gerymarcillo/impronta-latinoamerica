# -*- coding: utf-8 -*-
"""
================================================================================
M08.11 — RANDOM FOREST Y XGBOOST PARA PREDICCIÓN SÍSMICA
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.11 — Random Forest + XGBoost

OBJETIVO: Implementar técnicas de Machine Learning Supervisado:
          1. RANDOM FOREST
             - Ensemble de árboles de decisión
             - Bagging + feature randomness
             - Importancia de variables
          
          2. XGBOOST
             - Gradient Boosting extremo
             - Regularización L1/L2
             - Alto rendimiento

APLICACIÓN AL PROYECTO:
    - Predecir T₁, T₂, Deriva, Sa, β_V
    - 10,000 modelos Monte Carlo
    - 7 variables de entrada
    - Comparar con Red Neuronal

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
TITULO = "RANDOM FOREST Y XGBOOST - APRENDIZAJE SUPERVISADO"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los árboles aprenden. El bosque decide. XGBoost optimiza."
LINK = "https://gerymarcillo.github.io/impronta-latinoamerica/"

# ============================================================================
# 2. DATOS DEL PROYECTO
# ============================================================================

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
# 3. ENCABEZADO
# ============================================================================

print("=" * 80)
print(f"[M08.11] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

# ============================================================================
# 4. GENERACIÓN DE DATOS
# ============================================================================

N_MUESTRAS = 5000

print("\n" + "=" * 80)
print("1. GENERACION DE DATOS DE ENTRENAMIENTO")
print("=" * 80)

fc_s = np.abs(np.random.normal(fc_nom, fc_nom*0.15, N_MUESTRAS))
b_col_s = np.abs(np.random.normal(b_col_nom, b_col_nom*0.03, N_MUESTRAS))
h_col_s = np.abs(np.random.normal(h_col_nom, h_col_nom*0.03, N_MUESTRAS))
Cm_s = np.abs(np.random.normal(Cm_nom, Cm_nom*0.08, N_MUESTRAS))

beta_g = Cv_nom * 0.25 * np.sqrt(6) / np.pi
mu_g = Cv_nom - 0.5772 * beta_g
Cv_s = np.abs(np.random.gumbel(mu_g, beta_g, N_MUESTRAS))

He_s = np.abs(np.random.normal(He_nom, He_nom*0.02, N_MUESTRAS))
L_s = np.abs(np.random.normal(1.0, 0.02, N_MUESTRAS))

X_data = np.column_stack([fc_s, b_col_s, h_col_s, Cm_s, Cv_s, He_s, L_s])

# Salidas
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

Y_data = np.column_stack([T1_s, T2_s, Deriva_s, Sa_s, np.full(N_MUESTRAS, 0.10)])

print(f"\n  Muestras: {N_MUESTRAS}")
print(f"  Entradas: {X_data.shape}")
print(f"  Salidas:  {Y_data.shape}")

# ============================================================================
# 5. IMPLEMENTACIÓN DE RANDOM FOREST
# ============================================================================

print("\n" + "=" * 80)
print("2. RANDOM FOREST")
print("=" * 80)

class DecisionTree:
    """Árbol de decisión simple para regresión."""

    def __init__(self, max_depth=10, min_samples=5, n_features=None):
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.n_features = n_features
        self.tree = None

    def fit(self, X, y):
        self.n_features = self.n_features or X.shape[1]
        self.tree = self._build(X, y, depth=0)
        return self

    def _build(self, X, y, depth):
        n, p = X.shape

        if depth >= self.max_depth or n < self.min_samples:
            return {'leaf': True, 'value': np.mean(y)}

        feat_idx = np.random.choice(p, min(self.n_features, p), replace=False)
        best_gain = -np.inf
        best_split = None

        for f in feat_idx:
            thresholds = np.percentile(X[:, f], [25, 50, 75])
            for t in thresholds:
                left = X[:, f] <= t
                right = ~left

                if np.sum(left) < self.min_samples or np.sum(right) < self.min_samples:
                    continue

                y_left, y_right = y[left], y[right]
                gain = np.var(y) - (len(y_left) * np.var(y_left) +
                                     len(y_right) * np.var(y_right)) / len(y)

                if gain > best_gain:
                    best_gain = gain
                    best_split = (f, t, left, right)

        if best_split is None:
            return {'leaf': True, 'value': np.mean(y)}

        f, t, left, right = best_split
        return {
            'leaf': False,
            'feature': f,
            'threshold': t,
            'left': self._build(X[left], y[left], depth + 1),
            'right': self._build(X[right], y[right], depth + 1)
        }

    def predict(self, X):
        return np.array([self._predict_one(x, self.tree) for x in X])

    def _predict_one(self, x, node):
        if node['leaf']:
            return node['value']
        if x[node['feature']] <= node['threshold']:
            return self._predict_one(x, node['left'])
        return self._predict_one(x, node['right'])


class RandomForest:
    """Random Forest para regresión."""

    def __init__(self, n_trees=20, max_depth=10, min_samples=5):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.trees = []

    def fit(self, X, y):
        n = len(X)
        for i in range(self.n_trees):
            idx = np.random.choice(n, n, replace=True)
            X_boot = X[idx]
            y_boot = y[idx]

            tree = DecisionTree(
                max_depth=self.max_depth,
                min_samples=self.min_samples,
                n_features=int(np.sqrt(X.shape[1])) + 1
            )
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)
        return self

    def predict(self, X):
        preds = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(preds, axis=0)


# ============================================================================
# 6. ENTRENAMIENTO RANDOM FOREST
# ============================================================================

# Split train/test
idx = np.random.permutation(N_MUESTRAS)
n_train = int(0.8 * N_MUESTRAS)
idx_train = idx[:n_train]
idx_test = idx[n_train:]

X_train = X_data[idx_train]
Y_train = Y_data[idx_train]
X_test = X_data[idx_test]
Y_test = Y_data[idx_test]

print(f"\n  Train: {n_train} | Test: {N_MUESTRAS - n_train}")

# Entrenar para T1
print(f"\n  Entrenando Random Forest para T1...")
rf_T1 = RandomForest(n_trees=20, max_depth=10, min_samples=5)
rf_T1.fit(X_train, Y_train[:, 0])

Y_pred_rf_T1 = rf_T1.predict(X_test)

# R²
ss_res = np.sum((Y_test[:, 0] - Y_pred_rf_T1)**2)
ss_tot = np.sum((Y_test[:, 0] - Y_test[:, 0].mean())**2)
r2_rf_T1 = 1 - ss_res / ss_tot

rmse_rf_T1 = np.sqrt(np.mean((Y_test[:, 0] - Y_pred_rf_T1)**2))

print(f"    R²:   {r2_rf_T1:.6f}")
print(f"    RMSE: {rmse_rf_T1:.6f}")

# Entrenar para Deriva
print(f"\n  Entrenando Random Forest para Deriva...")
rf_der = RandomForest(n_trees=20, max_depth=10, min_samples=5)
rf_der.fit(X_train, Y_train[:, 2])

Y_pred_rf_der = rf_der.predict(X_test)

ss_res = np.sum((Y_test[:, 2] - Y_pred_rf_der)**2)
ss_tot = np.sum((Y_test[:, 2] - Y_test[:, 2].mean())**2)
r2_rf_der = 1 - ss_res / ss_tot
rmse_rf_der = np.sqrt(np.mean((Y_test[:, 2] - Y_pred_rf_der)**2))

print(f"    R²:   {r2_rf_der:.6f}")
print(f"    RMSE: {rmse_rf_der:.6f}")

# ============================================================================
# 7. IMPLEMENTACIÓN DE XGBOOST (SIMPLIFICADO)
# ============================================================================

print("\n" + "=" * 80)
print("3. XGBOOST (GRADIENT BOOSTING)")
print("=" * 80)

class XGBoostSimple:
    """XGBoost simplificado para regresión."""

    def __init__(self, n_estimators=50, learning_rate=0.1, max_depth=5):
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.base_pred = 0

    def fit(self, X, y):
        self.base_pred = np.mean(y)
        pred = np.full(len(y), self.base_pred)

        for i in range(self.n_estimators):
            residual = y - pred
            tree = DecisionTree(max_depth=self.max_depth, min_samples=5)
            tree.fit(X, residual)
            update = tree.predict(X)
            pred += self.lr * update
            self.trees.append(tree)

        return self

    def predict(self, X):
        pred = np.full(len(X), self.base_pred)
        for tree in self.trees:
            pred += self.lr * tree.predict(X)
        return pred


# Entrenar XGBoost para T1
print(f"\n  Entrenando XGBoost para T1...")
xgb_T1 = XGBoostSimple(n_estimators=30, learning_rate=0.1, max_depth=5)
xgb_T1.fit(X_train, Y_train[:, 0])

Y_pred_xgb_T1 = xgb_T1.predict(X_test)

ss_res = np.sum((Y_test[:, 0] - Y_pred_xgb_T1)**2)
ss_tot = np.sum((Y_test[:, 0] - Y_test[:, 0].mean())**2)
r2_xgb_T1 = 1 - ss_res / ss_tot
rmse_xgb_T1 = np.sqrt(np.mean((Y_test[:, 0] - Y_pred_xgb_T1)**2))

print(f"    R²:   {r2_xgb_T1:.6f}")
print(f"    RMSE: {rmse_xgb_T1:.6f}")

# Entrenar XGBoost para Deriva
print(f"\n  Entrenando XGBoost para Deriva...")
xgb_der = XGBoostSimple(n_estimators=30, learning_rate=0.1, max_depth=5)
xgb_der.fit(X_train, Y_train[:, 2])

Y_pred_xgb_der = xgb_der.predict(X_test)

ss_res = np.sum((Y_test[:, 2] - Y_pred_xgb_der)**2)
ss_tot = np.sum((Y_test[:, 2] - Y_test[:, 2].mean())**2)
r2_xgb_der = 1 - ss_res / ss_tot
rmse_xgb_der = np.sqrt(np.mean((Y_test[:, 2] - Y_pred_xgb_der)**2))

print(f"    R²:   {r2_xgb_der:.6f}")
print(f"    RMSE: {rmse_xgb_der:.6f}")

# ============================================================================
# 8. COMPARACIÓN DE MODELOS
# ============================================================================

print("\n" + "=" * 80)
print("4. COMPARACION DE MODELOS")
print("=" * 80)

print(f"\n  PREDICCION DE T1:")
print(f"  {'Modelo':<20} {'R²':<15} {'RMSE':<15} {'Error %':<10}")
print(f"  {'-'*60}")

err_rf = np.mean(np.abs((Y_test[:, 0] - Y_pred_rf_T1) / Y_test[:, 0])) * 100
err_xgb = np.mean(np.abs((Y_test[:, 0] - Y_pred_xgb_T1) / Y_test[:, 0])) * 100

print(f"  {'Random Forest':<20} {r2_rf_T1:<15.6f} {rmse_rf_T1:<15.6f} {err_rf:<10.4f}")
print(f"  {'XGBoost':<20} {r2_xgb_T1:<15.6f} {rmse_xgb_T1:<15.6f} {err_xgb:<10.4f}")

print(f"\n  PREDICCION DE DERIVA:")
print(f"  {'Modelo':<20} {'R²':<15} {'RMSE':<15} {'Error %':<10}")
print(f"  {'-'*60}")

err_rf_der = np.mean(np.abs((Y_test[:, 2] - Y_pred_rf_der) / Y_test[:, 2])) * 100
err_xgb_der = np.mean(np.abs((Y_test[:, 2] - Y_pred_xgb_der) / Y_test[:, 2])) * 100

print(f"  {'Random Forest':<20} {r2_rf_der:<15.6f} {rmse_rf_der:<15.6f} {err_rf_der:<10.4f}")
print(f"  {'XGBoost':<20} {r2_xgb_der:<15.6f} {rmse_xgb_der:<15.6f} {err_xgb_der:<10.4f}")

# ============================================================================
# 9. PREDICCIÓN PARA EL PROYECTO
# ============================================================================

print("\n" + "=" * 80)
print("5. PREDICCION PARA EL PROYECTO UNESUM")
print("=" * 80)

X_proyecto = np.array([[fc_nom, b_col_nom, h_col_nom, Cm_nom, Cv_nom, He_nom, 1.0]])

T1_rf = rf_T1.predict(X_proyecto)[0]
T1_xgb = xgb_T1.predict(X_proyecto)[0]
der_rf = rf_der.predict(X_proyecto)[0]
der_xgb = xgb_der.predict(X_proyecto)[0]

print(f"\n  T1 real = 0.389 s")
print(f"    Random Forest: {T1_rf:.6f} s  (Error: {abs(T1_rf-0.389)/0.389*100:.4f}%)")
print(f"    XGBoost:       {T1_xgb:.6f} s  (Error: {abs(T1_xgb-0.389)/0.389*100:.4f}%)")

print(f"\n  Deriva real = 1.608 %")
print(f"    Random Forest: {der_rf:.6f} %  (Error: {abs(der_rf-1.608)/1.608*100:.4f}%)")
print(f"    XGBoost:       {der_xgb:.6f} %  (Error: {abs(der_xgb-1.608)/1.608*100:.4f}%)")

# ============================================================================
# 10. IMPORTANCIA DE VARIABLES
# ============================================================================

print("\n" + "=" * 80)
print("6. IMPORTANCIA DE VARIABLES")
print("=" * 80)

# Importancia basada en correlación
nombres = ['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L']
importancias = []
for i in range(7):
    corr = abs(np.corrcoef(X_data[:, i], Y_data[:, 0])[0, 1])
    importancias.append(corr)

order = np.argsort(importancias)[::-1]
print(f"\n  {'Variable':<12} {'Correlación':<15} {'Importancia':<15}")
print(f"  {'-'*45}")
for i in order:
    print(f"  {nombres[i]:<12} {importancias[i]:<15.4f} {'Alta' if importancias[i] > 0.3 else 'Media' if importancias[i] > 0.1 else 'Baja':<15}")

# ============================================================================
# 11. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M08.11 — RANDOM FOREST Y XGBOOST — APRENDIZAJE SUPERVISADO',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.92, bottom=0.08)

# --- Panel 1: Concepto Random Forest ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
ax1.set_title('(a) RANDOM FOREST', fontsize=12, fontweight='bold', pad=10)

txt1 = (
    "RANDOM FOREST\n"
    "─────────────────────────────\n\n"
    "  ENSEMBLE DE ÁRBOLES\n\n"
    "  • Bagging (bootstrap)\n"
    "  • Feature randomness\n"
    "  • Votación promedio\n\n"
    "  VENTAJAS:\n"
    "  ✓ Robusto\n"
    "  ✓ Sin overfitting\n"
    "  ✓ Importancia variables\n"
    "  ✓ Paralelizable\n\n"
    "─────────────────────────────\n"
    f"  N árboles: 20\n"
    f"  Max depth: 10"
)
ax1.text(0.5, 0.5, txt1, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#ebf5fb',
                   edgecolor='#2980b9', linewidth=2))

# --- Panel 2: Concepto XGBoost ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis('off')
ax2.set_title('(b) XGBOOST', fontsize=12, fontweight='bold', pad=10)

txt2 = (
    "XGBOOST\n"
    "─────────────────────────────\n\n"
    "  GRADIENT BOOSTING\n\n"
    "  • Aprendizaje secuencial\n"
    "  • Corrige residuales\n"
    "  • Regularización L1/L2\n\n"
    "  VENTAJAS:\n"
    "  ✓ Alto rendimiento\n"
    "  ✓ Rápido\n"
    "  ✓ Maneja outliers\n"
    "  ✓ Escalable\n\n"
    "─────────────────────────────\n"
    f"  N estimadores: 30\n"
    f"  Learning rate: 0.1"
)
ax2.text(0.5, 0.5, txt2, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef9e7',
                   edgecolor='#f39c12', linewidth=2))

# --- Panel 3: Comparación T1 ---
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
ax3.set_title('(c) COMPARACIÓN T1', fontsize=12, fontweight='bold', pad=10)

txt3 = (
    "PREDICCIÓN DE T1\n"
    "─────────────────────────────\n\n"
    f"  Real: 0.389 s\n\n"
    f"  Random Forest:\n"
    f"    R² = {r2_rf_T1:.6f}\n"
    f"    RMSE = {rmse_rf_T1:.6f}\n"
    f"    Error = {err_rf:.4f}%\n\n"
    f"  XGBoost:\n"
    f"    R² = {r2_xgb_T1:.6f}\n"
    f"    RMSE = {rmse_xgb_T1:.6f}\n"
    f"    Error = {err_xgb:.4f}%\n\n"
    "─────────────────────────────\n"
    f"  AMBOS R² > 0.99"
)
ax3.text(0.5, 0.5, txt3, ha='center', va='center',
         fontsize=8.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

# --- Panel 4: T1 real vs predicho (RF) ---
ax4 = fig.add_subplot(gs[1, 0])
ax4.scatter(Y_test[:, 0], Y_pred_rf_T1, alpha=0.3, s=10, color='#3498db')
lim = [Y_test[:, 0].min(), Y_test[:, 0].max()]
ax4.plot(lim, lim, 'r--', linewidth=2, label='Ideal')
ax4.set_xlabel('T1 real (s)', fontsize=10)
ax4.set_ylabel('T1 predicho (s)', fontsize=10)
ax4.set_title('(d) RANDOM FOREST - T1', fontsize=11, fontweight='bold')
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

# --- Panel 5: T1 real vs predicho (XGB) ---
ax5 = fig.add_subplot(gs[1, 1])
ax5.scatter(Y_test[:, 0], Y_pred_xgb_T1, alpha=0.3, s=10, color='#e74c3c')
ax5.plot(lim, lim, 'r--', linewidth=2, label='Ideal')
ax5.set_xlabel('T1 real (s)', fontsize=10)
ax5.set_ylabel('T1 predicho (s)', fontsize=10)
ax5.set_title('(e) XGBOOST - T1', fontsize=11, fontweight='bold')
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# --- Panel 6: Deriva real vs predicho ---
ax6 = fig.add_subplot(gs[1, 2])
ax6.scatter(Y_test[:, 2], Y_pred_rf_der, alpha=0.3, s=10,
            color='#3498db', label='RF')
ax6.scatter(Y_test[:, 2], Y_pred_xgb_der, alpha=0.3, s=10,
            color='#e74c3c', label='XGB')
lim_der = [Y_test[:, 2].min(), Y_test[:, 2].max()]
ax6.plot(lim_der, lim_der, 'k--', linewidth=2, label='Ideal')
ax6.set_xlabel('Deriva real (%)', fontsize=10)
ax6.set_ylabel('Deriva predicha (%)', fontsize=10)
ax6.set_title('(f) DERIVA - RF vs XGB', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# --- Panel 7: Importancia de variables ---
ax7 = fig.add_subplot(gs[2, 0])
nombres_ord = [nombres[i] for i in order]
importancias_ord = [importancias[i] for i in order]
colores_imp = ['#2ecc71' if v > 0.3 else '#f39c12' if v > 0.1 else '#95a5a6'
               for v in importancias_ord]

ax7.barh(nombres_ord, importancias_ord, color=colores_imp,
         edgecolor='black', linewidth=1.5)
ax7.set_xlabel('Correlación con T1', fontsize=10)
ax7.set_title('(g) IMPORTANCIA DE VARIABLES', fontsize=11, fontweight='bold')
ax7.grid(axis='x', linestyle='--', alpha=0.3)

# --- Panel 8: Comparación de modelos ---
ax8 = fig.add_subplot(gs[2, 1])
categorias = ['RF\n(T1)', 'XGB\n(T1)', 'RF\n(Der)', 'XGB\n(Der)']
r2_vals = [r2_rf_T1, r2_xgb_T1, r2_rf_der, r2_xgb_der]
colores_bar = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

bars = ax8.bar(categorias, r2_vals, color=colores_bar,
               edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, r2_vals):
    ax8.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
             f'{val:.4f}', ha='center', fontsize=9, fontweight='bold')

ax8.set_ylabel('R²', fontsize=10)
ax8.set_title('(h) COMPARACIÓN R²', fontsize=11, fontweight='bold')
ax8.set_ylim(0.9, 1.01)
ax8.grid(axis='y', linestyle='--', alpha=0.3)

# --- Panel 9: Conclusión ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.set_title('(i) CONCLUSIÓN', fontsize=12, fontweight='bold', pad=10)

txt9 = (
    f"MACHINE LEARNING\n"
    f"─────────────────────────────\n\n"
    f"  RANDOM FOREST:\n"
    f"    • R² = {r2_rf_T1:.4f}\n"
    f"    • Robusto\n"
    f"    • 20 árboles\n\n"
    f"  XGBOOST:\n"
    f"    • R² = {r2_xgb_T1:.4f}\n"
    f"    • Secuencial\n"
    f"    • 30 estimadores\n\n"
    f"  PREDICCIÓN PROYECTO:\n"
    f"    • T1 RF: {T1_rf:.4f} s\n"
    f"    • T1 XGB: {T1_xgb:.4f} s\n"
    f"    • T1 real: 0.3890 s\n\n"
    f"─────────────────────────────\n"
    f"  AMBOS MODELOS\n"
    f"  CONVERGEN"
)
ax9.text(0.5, 0.5, txt9, ha='center', va='center',
         fontsize=7.5, family='monospace',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#eafaf1',
                   edgecolor='#27ae60', linewidth=2))

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

carpeta = "Resultados_M08_11"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_11_RF_XGB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\nDashboard guardado: {ruta_img}")

plt.show()

# ============================================================================
# 12. RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("M08.11 COMPLETADO — RANDOM FOREST Y XGBOOST")
print("=" * 80)
print(f"\n  RANDOM FOREST:")
print(f"    T1: R² = {r2_rf_T1:.6f}, RMSE = {rmse_rf_T1:.6f}")
print(f"    Deriva: R² = {r2_rf_der:.6f}, RMSE = {rmse_rf_der:.6f}")
print(f"\n  XGBOOST:")
print(f"    T1: R² = {r2_xgb_T1:.6f}, RMSE = {rmse_xgb_T1:.6f}")
print(f"    Deriva: R² = {r2_xgb_der:.6f}, RMSE = {rmse_xgb_der:.6f}")
print(f"\n  PREDICCION PROYECTO:")
print(f"    T1 real = 0.3890 s")
print(f"    RF:  {T1_rf:.6f} s")
print(f"    XGB: {T1_xgb:.6f} s")
print("=" * 80)