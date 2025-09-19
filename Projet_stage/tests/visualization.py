# data_loader/visualization.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from wordcloud import WordCloud, STOPWORDS
from typing import Union

def cluster_colors(df: pd.DataFrame, n_clusters: int = 5, show_plot: bool = True) -> list:
    """
    Applique un clustering KMeans sur les couleurs d'une image et affiche les couleurs dominantes.
    """
    if not {"R", "G", "B"}.issubset(df.columns):
        raise ValueError("Le DataFrame doit être une image convertie avec les colonnes R, G, B.")

    pixels = df[["R", "G", "B"]].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)

    if show_plot:
        plt.figure(figsize=(10, 4))
        plt.title("Couleurs dominantes (KMeans)", fontsize=14)
        for i, color in enumerate(colors):
            plt.bar(i, 1, color=color/255, width=1, edgecolor='black')
        plt.xticks(range(n_clusters), [f"Cluster {i+1}" for i in range(n_clusters)])
        plt.yticks([])
        plt.show()

    return [tuple(map(int, c)) for c in colors]

def visualize_wordcloud(text: str, max_words: int = 100):
    """Génère un nuage de mots à partir d'un texte."""
    if not isinstance(text, str):
        raise ValueError("Les données doivent être un texte (string).")

    wc = WordCloud(width=800, height=400, background_color='white',
                   stopwords=STOPWORDS, max_words=max_words, collocations=False).generate(text)

    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("Nuage de mots", fontsize=16)
    plt.show()

def visualize_distributions(df: pd.DataFrame):
    """
    Génère des histogrammes et des boxplots pour les colonnes numériques.
    """
    if not isinstance(df, pd.DataFrame):
        print("La visualisation de la distribution n'est possible qu'avec un DataFrame.")
        return

    numeric_cols = df.select_dtypes(include=np.number).columns
    if numeric_cols.empty:
        print("Aucune colonne numérique à visualiser.")
        return

    fig, axes = plt.subplots(nrows=len(numeric_cols), ncols=2, figsize=(12, 4 * len(numeric_cols)))
    fig.suptitle('Distribution des variables numériques', fontsize=16, y=1.02)
    
    for i, col in enumerate(numeric_cols):
        sns.histplot(df[col], kde=True, ax=axes[i, 0])
        axes[i, 0].set_title(f'Histogramme de {col}')
        sns.boxplot(x=df[col], ax=axes[i, 1])
        axes[i, 1].set_title(f'Boxplot de {col}')
        
    plt.tight_layout()
    plt.show()

def visualize_correlations(df: pd.DataFrame):
    """
    Génère une heatmap de corrélation pour les colonnes numériques.
    """
    if not isinstance(df, pd.DataFrame):
        print("La visualisation des corrélations n'est possible qu'avec un DataFrame.")
        return

    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.empty:
        print("Aucune colonne numérique pour calculer la corrélation.")
        return

    correlation_matrix = numeric_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Matrice de corrélation des variables numériques", fontsize=14)
    plt.show()