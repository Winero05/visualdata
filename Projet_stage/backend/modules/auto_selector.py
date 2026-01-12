"""
Détecter automatiquement la meilleure méthode de réduction de dimension (ACP, t-SNE, UMAP)
selon la nature et la structure du jeu de données.
"""

import warnings
from typing import (
    Any,
    Union,
    Literal,)
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

# Import des méthodes de réduction
from modules.methode_acp import MethodeACP
from modules.methode_tsne import MethodeTSNE
from modules.methode_umap import MethodeUMAP

warnings.filterwarnings("ignore")

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class AutoSelector:
    """Cette classe choisi la méthode de réduction automatiquement sans l'intervention humaine.
    """

    nombre_de_dimension: int
    df: Union[pd.DataFrame, np.ndarray]
    sample_size: int = 1000

    def __post_init__(self) -> None:
        """Initialisation des variables selon leur type et leur taille.
        """
        self.df = pd.DataFrame(self.df) if isinstance(self.df, np.ndarray) else self.df
        self.sample_size = min(self.sample_size, len(self.df))

    def _echantillonner(self) -> pd.DataFrame:
        """Échantillonne une portion du jeu de données pour accélérer la détection.
        
        Args:
            df (pd.DataFrame) : Le jeu de données à étudier.
        
        Returns:
            pd.DataFrame : Un échantillon de donnée prise dans l'ensemble de jeu de données est retourné.
        """
        df = pd.DataFrame(self.df) if isinstance(self.df, np.ndarray) else self.df
        return df.sample(n=self.sample_size, random_state=42).reset_index(drop=True)

    def _calculer_score_linearite(self, df_num: pd.DataFrame) -> float:
        """Calcule un score de linéarité moyen basé sur la corrélation absolue.
        Args:
            df_num (pd.DataFrame) : Le jeu de données numérique prise de façon aléatoire.

        Returns:
            floating[Any] : La moyenne de la matrice de corrélation est retournée.
        """

        corr = abs(df_num.corr()).values
        moyenne_corr = np.mean(corr[np.triu_indices_from(corr, k=1)])
        return moyenne_corr

    def _score_structure(self, x_proj: np.ndarray, x_original: np.ndarray) -> float:
        """
        Calcule une mesure de qualité structurelle entre distances dans l’espace original et réduit.
        Plus la corrélation est proche de 1, plus la structure est bien préservée.
        
        Args:
            x_proj (np.ndarray) : Projection suivant le premier vecteur unitaire.
            x_original (np.ndarray) :

        Returns:
            float : La corrélation est retourné.
        """
        idx = np.random.choice(len(x_original), size=min(300, len(x_original)), replace=False)
        dist_orig = pairwise_distances(x_original[idx])
        dist_proj = pairwise_distances(x_proj[idx])
        corr = np.corrcoef(dist_orig.flatten(), dist_proj.flatten())[0, 1]
        return corr

    def detecter_methode(self) -> Literal['acp', 'tsne', 'umap']:
        """
        Détermine automatiquement la meilleure méthode selon :
            - le nombre de colonnes
            - la linéarité
            - un score de préservation de la structure après réduction

        Returns:
            str : 
        """

        df_sample = self._echantillonner()
        df_num = df_sample.select_dtypes(include=[np.number])
        _x = StandardScaler().fit_transform(df_num.values)

        n, p = _x.shape
        score_linearite = self._calculer_score_linearite(df_num)

        print(f"\nDonnées : {n} échantillons, {p} variables\n")
        print(f"\nScore de linéarité moyenne : {score_linearite:.3f}\n")

        # Étape 1 — Choix initial heuristique
        methode: Literal['acp', 'tsne', 'umap']
        if p <= 20 and score_linearite > 0.6:
            methode = "acp"
        elif (20 < p <= 100 and 0.3 <= score_linearite <= 0.6) or n < 10000:
            methode = "tsne"
        else:
            methode = "umap"

        print(f"\nMéthode initialement pressentie : {methode.upper()}\n")

        # Étape 2 — Validation par score de qualité structurelle (test rapide)
        # resultats: dict[str, Any] = {}
        # try:
        #     # ACP
        #     x_acp = MethodeACP(df_num).acp_reduction(nombre_dimenssion=self.nombre_de_dimension)
        #     resultats["acp"] = self._score_structure(x_acp, _x)

        #     # t-SNE (échantillon plus petit si dataset volumineux)
        #     x_small = _x[: min(700, len(_x))]
        #     x_tsne = MethodeTSNE(
        #         df=pd.DataFrame(x_small)).tsne_reduction(
        #             nombre_de_dimension=self.nombre_de_dimension)
        #     resultats["tsne"] = self._score_structure(x_tsne, x_small)

        #     # UMAP
        #     x_umap = MethodeUMAP(df_num).umap_reduction(nombre_de_dimension=2)
        #     resultats["umap"] = self._score_structure(x_umap, _x)
        # except ImportError as e:
        #     print(f"\nErreur durant l’évaluation structurelle : {e}\n")

        # if resultats:
        #     meilleure_methode = max(resultats, key=resultats.__getitem__)
        #     print(f"\nScores structurels : {resultats}\n")
        #     print(f"\nMéthode sélectionnée : {meilleure_methode.upper()}\n")
        #     return meilleure_methode

        return methode
