# packages/modules/methode_tsne.py

import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

class TSNEVisualizer:
    """
    Classe pour la visualisation de données à l'aide de t-SNE.
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
        
        # Standardisation des données numériques
        self.X_scaled = StandardScaler().fit_transform(self.df[self.numeric_cols])

    def visualize(self, n_components: int, perplexity: int = 30, color_by_col: str = None):
        """
        Applique t-SNE et génère un graphique Plotly.
        
        Args:
            n_components (int): Nombre de dimensions à réduire (2 ou 3).
            perplexity (int): Perplexité de t-SNE.
            color_by_col (str): Nom de la colonne à utiliser pour la coloration des points.
        
        Returns:
            tuple[plotly.graph_objects.Figure, pd.DataFrame]: La figure Plotly et le DataFrame des données réduites.
        """
        tsne = TSNE(
            n_components=n_components, 
            perplexity=perplexity, 
            random_state=42, 
            init="pca", 
            learning_rate="auto"
        )
        X_tsne = tsne.fit_transform(self.X_scaled)

        tsne_cols = [f"Dim{i+1}" for i in range(n_components)]
        reduced_df = pd.DataFrame(X_tsne, columns=tsne_cols)

        # Gestion de la coloration
        color_data = self.df[color_by_col] if color_by_col and color_by_col in self.df.columns else None

        if n_components == 2:
            fig = px.scatter(
                reduced_df, x="Dim1", y="Dim2", color=color_data,
                title=f"t-SNE en 2D (perplexity={perplexity})",
                labels={"color": color_by_col}
            )
        elif n_components == 3:
            fig = px.scatter_3d(
                reduced_df, x="Dim1", y="Dim2", z="Dim3", color=color_data,
                title=f"t-SNE en 3D (perplexity={perplexity})",
                labels={"color": color_by_col}
            )
        else:
            raise ValueError("n_components doit être 2 ou 3 pour la visualisation.")
            
        return fig, reduced_df