# packages/modules/methode_umap.py

import umap
import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

class UMAPVisualizer:
    """
    Classe pour la visualisation de données à l'aide de UMAP.
    """
    def __init__(self, df: pd.DataFrame):
        """
        Initialise la classe avec un DataFrame.
        Vérifie la présence de données numériques et les standardise.
        """
        self.df = df
        self.numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not self.numeric_cols:
            raise ValueError("Le DataFrame ne contient aucune colonne numérique pour la réduction de dimension.")
        
        # Standardisation des données numériques pour la réduction de dimension
        self.X_scaled = StandardScaler().fit_transform(self.df[self.numeric_cols])

    def visualize(self, n_components: int, n_neighbors: int = 15, min_dist: float = 0.1, color_by_col: str = None):
        """
        Applique UMAP et génère un graphique Plotly.
        
        Args:
            n_components (int): Nombre de dimensions à réduire (2 ou 3).
            n_neighbors (int): Nombre de voisins proches à considérer pour la structure locale.
            min_dist (float): Distance minimale entre les points réduits.
            color_by_col (str): Nom de la colonne à utiliser pour la coloration des points.

        Returns:
            tuple[plotly.graph_objects.Figure, pd.DataFrame]: La figure Plotly et le DataFrame des données réduites.
        """
        reducer = umap.UMAP(
            n_components=n_components, 
            n_neighbors=n_neighbors, 
            min_dist=min_dist, 
            random_state=42
        )
        X_embedded = reducer.fit_transform(self.X_scaled)
        
        umap_cols = [f"UMAP-{i+1}" for i in range(n_components)]
        reduced_df = pd.DataFrame(X_embedded, columns=umap_cols)

        # Gestion de la coloration
        color_data = self.df[color_by_col] if color_by_col and color_by_col in self.df.columns else None

        if n_components == 2:
            fig = px.scatter(
                reduced_df, x="UMAP-1", y="UMAP-2", color=color_data,
                title=f"UMAP en 2D (n_neighbors={n_neighbors}, min_dist={min_dist})",
                labels={"color": color_by_col}
            )
        elif n_components == 3:
            fig = px.scatter_3d(
                reduced_df, x="UMAP-1", y="UMAP-2", z="UMAP-3", color=color_data,
                title=f"UMAP en 3D (n_neighbors={n_neighbors}, min_dist={min_dist})",
                labels={"color": color_by_col}
            )
        else:
            raise ValueError("n_components doit être 2 ou 3 pour la visualisation.")
        
        return fig, reduced_df