##methode_acp.py

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import plotly.express as px

class MethodePCA:
    """Méthode de réduction de dimenssion avec l'ACP."""
    
    def __init__(self, n_components: int = 2):
        """
        Initialise la classe avec le nombre de composantes souhaitées.
        
        Args:
            n_components (int): Le nombre de dimensions à conserver.
        """
        self.n_components = n_components
        self.pca = PCA(n_components=self.n_components)
        self.scaler = StandardScaler()

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Applique la standardisation et la réduction PCA sur les colonnes numériques d'un DataFrame.
        
        Args:
            df (pd.DataFrame): Le DataFrame contenant les données à réduire.
            
        Returns:
            np.ndarray: Le tableau numpy avec les données réduites.
        """
        numeric_df = df.select_dtypes(include=np.number)
        if numeric_df.empty:
            raise ValueError("Le DataFrame ne contient aucune colonne numérique pour la PCA.")

        X_scaled = self.scaler.fit_transform(numeric_df)
        X_pca = self.pca.fit_transform(X_scaled)
        
        return X_pca

    def visualize(self, df: pd.DataFrame, color_by_col: str = None, original_df: pd.DataFrame = None):
        """
        Applique la PCA et retourne une figure Plotly.
        
        Args:
            df (pd.DataFrame): Le DataFrame prétraité (numérique).
            color_by_col (str, optional): Colonne pour la coloration.
            original_df (pd.DataFrame, optional): DataFrame original pour récupérer la colonne de coloration.
            
        Returns:
            tuple[plotly.graph_objects.Figure, pd.DataFrame]: La figure Plotly et le DataFrame des données réduites.
        """
        X_pca = self.fit_transform(df)
        
        color_data = None
        if color_by_col and original_df is not None and color_by_col in original_df.columns:
            color_data = original_df[color_by_col]

        pca_cols = [f"PC{i+1}" for i in range(self.n_components)]
        reduced_df = pd.DataFrame(X_pca, columns=pca_cols)

        if self.n_components == 2:
            fig = px.scatter(reduced_df, x="PC1", y="PC2", color=color_data, title="ACP en 2D",
                             labels={"color": color_by_col})
        elif self.n_components == 3:
            fig = px.scatter_3d(reduced_df, x="PC1", y="PC2", z="PC3", color=color_data, title="ACP en 3D",
                                labels={"color": color_by_col})
        else:
            raise ValueError("La visualisation n'est supportée que pour 2 ou 3 composantes.")
        
        return fig, reduced_df
    
