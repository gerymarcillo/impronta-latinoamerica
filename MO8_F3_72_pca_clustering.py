# -*- coding: utf-8 -*-
"""
================================================================================
M08.10 — ANÁLISIS DE COMPONENTES PRINCIPALES (PCA) Y CLUSTERING
================================================================================
AUTOR: Ing. Gery Lorenzo Marcillo Merino, Msc.
PROYECTO: UNESUM-REZ-2026-JIPIJAPA-001
MÓDULO: M08 — Análisis Estocástico
SUBSECCIÓN: M08.10 — PCA + Clustering

OBJETIVO: Aplicar técnicas de aprendizaje no supervisado al proyecto:
          1. PCA (Análisis de Componentes Principales)
             - Reducción de dimensionalidad
             - Identificar variables dominantes
             - Visualizar estructura de datos
          
          2. CLUSTERING (Agrupamiento)
             - K-means
             - DBSCAN
             - Clustering Jerárquico
             - Identificar grupos de estructuras similares

APLICACIÓN AL PROYECTO:
    - 10,000 modelos Monte Carlo
    - 7 variables de entrada
    - 5 variables de salida
    - Identificar patrones ocultos
    - Agrupar por comportamiento sísmico

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
TITULO = "PCA Y CLUSTERING - APRENDIZAJE NO SUPERVISADO"
DOCENTE = "Ing. Gery Lorenzo Marcillo Merino, Msc."
FRASE = "Los datos hablan por sí solos. Solo hay que escucharlos."
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
# 3. GENERACIÓN DE DATOS
# ============================================================================

print("=" * 80)
print(f"[M08.10] {TITULO}")
print(f"[PROYECTO] {PROYECTO}")
print(f"[DOCENTE] {DOCENTE}")
print("=" * 80)

N_MUESTRAS = 5000

# Distribuciones de entrada
fc_s = np.abs(np.random.normal(fc_nom, fc_nom*0.15, N_MUESTRAS))
b_col_s = np.abs(np.random.normal(b_col_nom, b_col_nom*0.03, N_MUESTRAS))
h_col_s = np.abs(np.random.normal(h_col_nom, h_col_nom*0.03, N_MUESTRAS))
Cm_s = np.abs(np.random.normal(Cm_nom, Cm_nom*0.08, N_MUESTRAS))

beta_g = Cv_nom * 0.25 * np.sqrt(6) / np.pi
mu_g = Cv_nom - 0.5772 * beta_g
Cv_s = np.abs(np.random.gumbel(mu_g, beta_g, N_MUESTRAS))

He_s = np.abs(np.random.normal(He_nom, He_nom*0.02, N_MUESTRAS))
L_s = np.abs(np.random.normal(1.0, 0.02, N_MUESTRAS))

# Matriz de entrada
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

# ============================================================================
# 4. PCA — ANÁLISIS DE COMPONENTES PRINCIPALES
# ============================================================================

print("\n" + "=" * 80)
print("1. PCA - ANALISIS DE COMPONENTES PRINCIPALES")
print("=" * 80)

# Combinar entradas y salidas
X_completo = np.column_stack([X_data, Y_data])
nombres = ['fc', 'b_col', 'h_col', 'Cm', 'Cv', 'He', 'L',
           'T1', 'T2', 'Deriva', 'Sa', 'beta_V']

# Normalizar
X_mean = X_completo.mean(axis=0)
X_std = X_completo.std(axis=0)
X_norm = (X_completo - X_mean) / X_std

# Matriz de covarianza
Cov = np.cov(X_norm.T)

# Eigenvalores y eigenvectores
eigvals, eigvecs = np.linalg.eigh(Cov)
idx = np.argsort(eigvals)[::-1]
eigvals = eigvals[idx]
eigvecs = eigvecs[:, idx]

# Varianza explicada
var_explicada = eigvals / eigvals.sum() * 100
var_acumulada = np.cumsum(var_explicada)

print(f"\n  VARIANZA EXPLICADA:")
print(f"  {'Componente':<12} {'Eigenvalor':<12} {'Var (%)':<10} {'Acum (%)':<10}")
print(f"  {'-'*50}")
for i in range(6):
    print(f"  PC{i+1:<10} {eigvals[i]:<12.4f} {var_explicada[i]:<10.2f} {var_acumulada[i]:<10.2f}")

# Proyección en 2D
X_pca = X_norm @ eigvecs[:, :2]

# Componentes principales (cargas)
print(f"\n  CARGAS DE PC1 y PC2:")
print(f"  {'Variable':<12} {'PC1':<12} {'PC2':<12}")
print(f"  {'-'*40}")
for i, nombre in enumerate(nombres):
    print(f"  {nombre:<12} {eigvecs[i, 0]:<12.4f} {eigvecs[i, 1]:<12.4f}")

# ============================================================================
# 5. K-MEANS
# ============================================================================

print("\n" + "=" * 80)
print("2. K-MEANS CLUSTERING")
print("=" * 80)

def kmeans(X, k, max_iter=100):
    n = len(X)
    idx = np.random.choice(n, k, replace=False)
    centroides = X[idx].copy()

    for _ in range(max_iter):
        distancias = np.linalg.norm(X[:, None] - centroides[None, :], axis=2)
        etiquetas = np.argmin(distancias, axis=1)

        nuevos_centroides = np.array([X[etiquetas == j].mean(axis=0)
                                       if np.sum(etiquetas == j) > 0
                                       else centroides[j]
                                       for j in range(k)])

        if np.allclose(centroides, nuevos_centroides):
            break
        centroides = nuevos_centroides

    return etiquetas, centroides

# Usar PCA 2D para clustering
K = 4
etiquetas_km, centroides_km = kmeans(X_pca, K)

# Tamaño de cada cluster
print(f"\n  K-MEANS (K={K}):")
print(f"  {'Cluster':<12} {'N':<10} {'%':<10}")
print(f"  {'-'*32}")
for j in range(K):
    n_j = np.sum(etiquetas_km == j)
    print(f"  {j:<12} {n_j:<10} {n_j/N_MUESTRAS*100:<10.2f}")

# ============================================================================
# 6. DBSCAN
# ============================================================================

print("\n" + "=" * 80)
print("3. DBSCAN CLUSTERING")
print("=" * 80)

def dbscan(X, eps, min_pts):
    n = len(X)
    etiquetas = -np.ones(n, dtype=int)
    cluster_id = 0

    for i in range(n):
        if etiquetas[i] != -1:
            continue

        vecinos = np.where(np.linalg.norm(X - X[i], axis=1) < eps)[0]

        if len(vecinos) < min_pts:
            etiquetas[i] = -2  # Ruido
            continue

        etiquetas[i] = cluster_id
        semilla = list(vecinos)

        while semilla:
            j = semilla.pop()
            if etiquetas[j] == -2:
                etiquetas[j] = cluster_id
            if etiquetas[j] != -1:
                continue

            etiquetas[j] = cluster_id
            vecinos_j = np.where(np.linalg.norm(X - X[j], axis=1) < eps)[0]
            if len(vecinos_j) >= min_pts:
                semilla.extend(vecinos_j)

        cluster_id += 1

    return etiquetas

# Usar subconjunto para DBSCAN (más rápido)
N_DBSCAN = 1000
X_dbscan = X_pca[:N_DBSCAN]
etiquetas_db = dbscan(X_dbscan, eps=0.5, min_pts=5)

n_clusters_db = len(set(etiquetas_db)) - (1 if -2 in etiquetas_db else 0)
n_ruido = np.sum(etiquetas_db == -2)

print(f"\n  DBSCAN (eps=0.5, min_pts=5):")
print(f"    Clusters encontrados: {n_clusters_db}")
print(f"    Puntos de ruido: {n_ruido}")
print(f"    Puntos en clusters: {N_DBSCAN - n_ruido}")

# ============================================================================
# 7. CLUSTERING JERÁRQUICO
# ============================================================================

print("\n" + "=" * 80)
print("4. CLUSTERING JERARQUICO")
print("=" * 80)

# Usar subconjunto
N_JER = 200
X_jer = X_pca[:N_JER]

# Distancias
distancias = np.linalg.norm(X_jer[:, None] - X_jer[None, :], axis=2)

# Linkage simple
clusters = [[i] for i in range(N_JER)]
merge_history = []

while len(clusters) > 1:
    min_dist = np.inf
    par_min = None

    for i in range(len(clusters)):
        for j in range(i+1, len(clusters)):
            for a in clusters[i]:
                for b in clusters[j]:
                    if distancias[a, b] < min_dist:
                        min_dist = distancias[a, b]
                        par_min = (i, j)

    i, j = par_min
    merge_history.append((clusters[i], clusters[j], min_dist))
    clusters[i] = clusters[i] + clusters[j]
    del clusters[j]

print(f"\n  JERARQUICO (N={N_JER}):")
print(f"    Fusiones: {len(merge_history)}")
print(f"    Ultima distancia: {merge_history[-1][2]:.4f}")

# ============================================================================
# 8. DASHBOARD
# ============================================================================

fig = plt.figure(figsize=(24, 16))
fig.patch.set_facecolor('#f5f7fa')

fig.text(0.5, 0.980,
         'M08.10 — PCA Y CLUSTERING — APRENDIZAJE NO SUPERVISADO',
         ha='center', va='top', fontsize=18, fontweight='bold',
         color='#1a237e')
fig.text(0.5, 0.955, PROYECTO,
         ha='center', va='top', fontsize=11,
         color='#5dade2', style='italic')

gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.32,
              left=0.05, right=0.98, top=0.92, bottom=0.08)

# --- Panel 1: Varianza explicada ---
ax1 = fig.add_subplot(gs[0, 0])
n_pcs = min(8, len(var_explicada))
ax1.bar(range(1, n_pcs+1), var_explicada[:n_pcs],
        color='#3498db', edgecolor='black', linewidth=1.5)
ax1.plot(range(1, n_pcs+1), var_acumulada[:n_pcs],
         'ro-', linewidth=2, markersize=8, label='Acumulada')
ax1.axhline(90, color='green', linestyle='--', linewidth=2, label='90%')
ax1.set_xlabel('Componente Principal', fontsize=10)
ax1.set_ylabel('Varianza explicada (%)', fontsize=10)
ax1.set_title('(a) VARIANZA EXPLICADA', fontsize=11, fontweight='bold')
ax1.legend(fontsize=8)
ax1.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 2: Cargas de PC1 y PC2 ---
ax2 = fig.add_subplot(gs[0, 1])
x_pos = np.arange(len(nombres))
width = 0.35

ax2.barh(x_pos - width/2, eigvecs[:, 0], width, color='#3498db',
         edgecolor='black', linewidth=1, label='PC1')
ax2.barh(x_pos + width/2, eigvecs[:, 1], width, color='#e74c3c',
         edgecolor='black', linewidth=1, label='PC2')
ax2.set_yticks(x_pos)
ax2.set_yticklabels(nombres, fontsize=9)
ax2.set_xlabel('Carga', fontsize=10)
ax2.set_title('(b) CARGAS DE PC1 y PC2', fontsize=11, fontweight='bold')
ax2.legend(fontsize=8)
ax2.grid(True, axis='x', linestyle='--', alpha=0.3)

# --- Panel 3: Proyección PCA con K-means ---
ax3 = fig.add_subplot(gs[0, 2])
colores_cluster = ['#2d6a4f', '#3498db', '#f39c12', '#e74c3c', '#8e44ad']
for j in range(K):
    mask = etiquetas_km == j
    ax3.scatter(X_pca[mask, 0], X_pca[mask, 1],
                c=colores_cluster[j], s=10, alpha=0.5,
                label=f'Cluster {j}')
for j in range(K):
    ax3.scatter(centroides_km[j, 0], centroides_km[j, 1],
                c=colores_cluster[j], s=200, marker='X',
                edgecolor='black', linewidth=2, zorder=5)
ax3.set_xlabel('PC1', fontsize=10)
ax3.set_ylabel('PC2', fontsize=10)
ax3.set_title('(c) PCA + K-MEANS', fontsize=11, fontweight='bold')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)

# --- Panel 4: Distribución de clusters ---
ax4 = fig.add_subplot(gs[1, 0])
tamanos = [np.sum(etiquetas_km == j) for j in range(K)]
bars = ax4.bar(range(K), tamanos, color=colores_cluster[:K],
               edgecolor='black', linewidth=1.5)
for bar, val in zip(bars, tamanos):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
             f'{val}', ha='center', fontsize=10, fontweight='bold')
ax4.set_xlabel('Cluster', fontsize=10)
ax4.set_ylabel('Número de modelos', fontsize=10)
ax4.set_title('(d) TAMAÑO DE CLUSTERS', fontsize=11, fontweight='bold')
ax4.grid(True, axis='y', linestyle='--', alpha=0.3)

# --- Panel 5: T1 por cluster ---
ax5 = fig.add_subplot(gs[1, 1])
for j in range(K):
    mask = etiquetas_km == j
    ax5.scatter(X_pca[mask, 0], T1_s[:len(X_pca)][mask],
                c=colores_cluster[j], s=8, alpha=0.5)
ax5.set_xlabel('PC1', fontsize=10)
ax5.set_ylabel('T1 (s)', fontsize=10)
ax5.set_title('(e) T1 POR CLUSTER', fontsize=11, fontweight='bold')
ax5.grid(True, alpha=0.3)

# --- Panel 6: Deriva por cluster ---
ax6 = fig.add_subplot(gs[1, 2])
for j in range(K):
    mask = etiquetas_km == j
    ax6.scatter(X_pca[mask, 0], Deriva_s[:len(X_pca)][mask],
                c=colores_cluster[j], s=8, alpha=0.5)
ax6.axhline(2.0, color='red', linestyle='--', linewidth=2, label='NEC-15')
ax6.set_xlabel('PC1', fontsize=10)
ax6.set_ylabel('Deriva (%)', fontsize=10)
ax6.set_title('(f) DERIVA POR CLUSTER', fontsize=11, fontweight='bold')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)

# --- Panel 7: DBSCAN ---
ax7 = fig.add_subplot(gs[2, 0])
for j in range(n_clusters_db):
    mask = etiquetas_db == j
    ax7.scatter(X_dbscan[mask, 0], X_dbscan[mask, 1],
                s=15, alpha=0.6, label=f'Cluster {j}')
mask_ruido = etiquetas_db == -2
ax7.scatter(X_dbscan[mask_ruido, 0], X_dbscan[mask_ruido, 1],
            c='black', s=15, alpha=0.5, label='Ruido')
ax7.set_xlabel('PC1', fontsize=10)
ax7.set_ylabel('PC2', fontsize=10)
ax7.set_title('(g) DBSCAN', fontsize=11, fontweight='bold')
ax7.legend(fontsize=7)
ax7.grid(True, alpha=0.3)

# --- Panel 8: Dendrograma simplificado ---
ax8 = fig.add_subplot(gs[2, 1])
distancias_fusion = [m[2] for m in merge_history]
ax8.plot(range(len(distancias_fusion)), distancias_fusion,
         'b-', linewidth=1.5)
ax8.set_xlabel('Fusión', fontsize=10)
ax8.set_ylabel('Distancia', fontsize=10)
ax8.set_title('(h) DENDROGRAMA JERARQUICO', fontsize=11, fontweight='bold')
ax8.grid(True, alpha=0.3)

# --- Panel 9: Conclusión ---
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')
ax9.set_title('(i) CONCLUSION', fontsize=12, fontweight='bold', pad=10)

txt9 = (
    f"APRENDIZAJE NO SUPERVISADO\n"
    f"─────────────────────────────\n\n"
    f"  PCA:\n"
    f"    • PC1 explica {var_explicada[0]:.1f}%\n"
    f"    • PC2 explica {var_explicada[1]:.1f}%\n"
    f"    • 2 PCs explican {var_acumulada[1]:.1f}%\n\n"
    f"  K-MEANS (K={K}):\n"
    f"    • Agrupa {N_MUESTRAS} modelos\n"
    f"    • Identifica {K} grupos\n"
    f"    • T1 medio por cluster\n\n"
    f"  DBSCAN:\n"
    f"    • {n_clusters_db} clusters\n"
    f"    • {n_ruido} puntos de ruido\n\n"
    f"  APLICACIÓN:\n"
    f"    • Clasificar estructuras\n"
    f"    • Detectar outliers\n"
    f"    • Optimizar diseño\n\n"
    f"─────────────────────────────\n"
    f"  {FRASE}"
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

carpeta = "Resultados_M08_10"
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

nombre_img = f"M08_10_PCA_clustering_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
ruta_img = os.path.join(carpeta, nombre_img)
plt.savefig(ruta_img, dpi=150, bbox_inches='tight', facecolor='#f5f7fa')
print(f"\nDashboard guardado: {ruta_img}")

plt.show()

# ============================================================================
# 9. RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 80)
print("M08.10 COMPLETADO — PCA Y CLUSTERING")
print("=" * 80)
print(f"\n  PCA:")
print(f"    PC1 explica: {var_explicada[0]:.2f}%")
print(f"    PC2 explica: {var_explicada[1]:.2f}%")
print(f"    2 PCs:       {var_acumulada[1]:.2f}%")
print(f"\n  K-MEANS (K={K}):")
for j in range(K):
    print(f"    Cluster {j}: {np.sum(etiquetas_km == j)} modelos")
print(f"\n  DBSCAN:")
print(f"    Clusters: {n_clusters_db}")
print(f"    Ruido:    {n_ruido}")
print("=" * 80)