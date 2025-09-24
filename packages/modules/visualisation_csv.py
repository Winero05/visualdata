#visualisation_csv.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler, LabelEncoder

class TabularVisualizer:
    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Les données doivent être un DataFrame pandas.")
        self.df = df.copy()
        self.numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        self.categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        
    # --- Statistiques de base ---
    def basic_stats(self):
        print("=== Statistiques numériques ===")
        print(self.df[self.numeric_cols].describe())
        print("\n=== Statistiques catégorielles ===")
        print(self.df[self.categorical_cols].describe())
        
    # --- Distribution des variables ---
    def plot_distributions(self, return_fig: bool = False):
        """Génère les graphiques de distribution pour les colonnes.
        
        Args:
            return_fig (bool): Si True, retourne une liste de figures Matplotlib au lieu de les afficher.
        """
        figures = []
        # Créer une figure par colonne pour plus de clarté
        for col in self.numeric_cols + self.categorical_cols:
            fig = plt.figure(figsize=(12, 5))
            if col in self.numeric_cols:
                ax1 = fig.add_subplot(1, 2, 1)
                sns.histplot(self.df[col], kde=True, ax=ax1)
                ax1.set_title(f"Histogramme de {col}")
                
                ax2 = fig.add_subplot(1, 2, 2)
                sns.boxplot(x=self.df[col], ax=ax2)
                ax2.set_title(f"Boxplot de {col}")
            else: # Colonne catégorielle
                ax = fig.add_subplot(1, 1, 1)
                sns.countplot(x=self.df[col], order=self.df[col].value_counts().index, ax=ax)
                ax.set_title(f"Distribution de {col}")
                plt.xticks(rotation=45)
            
            fig.tight_layout()
            figures.append(fig)

        if return_fig:
            return figures
        
        for fig in figures:
            plt.show()
        plt.close('all') # Ferme toutes les figures après affichage
    
    # --- Corrélations et pairplots ---
    def plot_correlations(self, return_fig: bool = False):
        """Génère la matrice de corrélation et le pairplot.
        
        Args:
            return_fig (bool): Si True, retourne une liste de figures Matplotlib.
        """
        figures = []
        if self.numeric_cols:
            corr = self.df[self.numeric_cols].corr()
            fig1 = plt.figure(figsize=(10,8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Matrice de corrélation")
            figures.append(fig1)

            # Le pairplot peut être très lourd, à utiliser avec prudence
            if len(self.numeric_cols) < 10: # Limite pour éviter les crashs
                fig2 = sns.pairplot(self.df[self.numeric_cols])
                figures.append(fig2.fig) # sns.pairplot retourne un PairGrid, on récupère la figure
        
        if return_fig:
            return figures

        plt.show()
        plt.close('all')
    
    # --- Analyse en Composantes Principales (PCA) ---
    def pca_visualization(self, n_components=3):
        if not self.numeric_cols:
            print("Aucune colonne numérique pour PCA.")
            return
        X = self.df[self.numeric_cols].fillna(0)
        X_scaled = StandardScaler().fit_transform(X)
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X_scaled)
        
        print(f"Variance expliquée par chaque composante : {pca.explained_variance_ratio_}")
        
        if n_components >= 2:
            plt.figure(figsize=(8,6))
            plt.scatter(X_pca[:,0], X_pca[:,1])
            plt.xlabel("PC1")
            plt.ylabel("PC2")
            plt.title("Projection PCA 2D")
            plt.show()
        if n_components >= 3:
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(8,6))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X_pca[:,0], X_pca[:,1], X_pca[:,2])
            ax.set_xlabel("PC1")
            ax.set_ylabel("PC2")
            ax.set_zlabel("PC3")
            plt.title("Projection PCA 3D")
            plt.show()
    
    # --- t-SNE ---
    def tsne_visualization(self, n_components=2, perplexity=30, random_state=42):
        if not self.numeric_cols:
            print("Aucune colonne numérique pour t-SNE.")
            return
        X = self.df[self.numeric_cols].fillna(0)
        X_scaled = StandardScaler().fit_transform(X)
        tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
        X_tsne = tsne.fit_transform(X_scaled)
        
        if n_components == 2:
            plt.figure(figsize=(8,6))
            plt.scatter(X_tsne[:,0], X_tsne[:,1])
            plt.title("t-SNE 2D")
            plt.show()
        elif n_components == 3:
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(8,6))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X_tsne[:,0], X_tsne[:,1], X_tsne[:,2])
            plt.title("t-SNE 3D")
            plt.show()
    
    # --- Encodage et correspondances pour catégorielles ---
    def encode_categorical(self):
        """Encode les colonnes catégorielles avec LabelEncoder"""
        self.encoded_df = self.df.copy()
        self.label_encoders = {}
        for col in self.categorical_cols:
            le = LabelEncoder()
            self.encoded_df[col] = le.fit_transform(self.df[col].astype(str))
            self.label_encoders[col] = le
        print("Colonnes catégorielles encodées.")
'''
# === Exemple d'utilisation ===
if __name__ == "__main__":
    # Exemple avec un dataset fictif
    df = pd.read_csv("C:/Users/LENOVO/Downloads/excel_exercise_dataset.csv")
    tv = TabularVisualizer(df)
    tv.basic_stats()
    tv.plot_distributions()
    tv.plot_correlations()
    tv.encode_categorical()
    tv.pca_visualization(n_components=3)
    tv.tsne_visualization(n_components=2)
'''