import numpy as np
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

# Chargement du dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

def apply_pca():
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)
    return {
        "x": X_pca[:, 0].tolist(),
        "y": X_pca[:, 1].tolist(),
        "z": X_pca[:, 2].tolist(),
        "labels": y.tolist()
    }

def apply_tsne():
    tsne = TSNE(n_components=2, random_state=42, init="random")
    X_tsne = tsne.fit_transform(X)
    return {
        "x": X_tsne[:, 0].tolist(),
        "y": X_tsne[:, 1].tolist(),
        "labels": y.tolist()
    }

def apply_umap():
    reducer = umap.UMAP(n_components=2, random_state=42)
    X_umap = reducer.fit_transform(X)
    return {
        "x": X_umap[:, 0].tolist(),
        "y": X_umap[:, 1].tolist(),
        "labels": y.tolist()
    }
