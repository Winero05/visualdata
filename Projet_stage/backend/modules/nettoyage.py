"""Ce module se charge de remplir les cellules vides d'un tableau
de données.

Returns:
    pd.DataFrame: Un nouveau table de données sans cellule vides.
"""

from typing import Union, Optional, Literal
from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class Nettoyage:
    """Cette classe remplace les cellules vides pas des valeurs
    personnalisé en fonction de la stractégie et/ou du choix des
    colonnes contenant les cellules vides.
    """

    df: Union[pd.DataFrame, np.ndarray, str]

    def gerer_les_valeurs_manquantes(
        self,
        column: Optional[list[str]] = None,
        strategy: Literal["mean", "fill", "drop", "median"] = 'mean'
        ) -> pd.DataFrame:
        """
        Gère les valeurs manquantes d'un tableau de données.

        Args:
            df       (pd.DataFrame) : Le tableau de données à traiter.
            strategy (Literal) : Valeurs de remplissage des cellules vide,
                par défaut c'est `mean` (valeur possibles: `mean`, `drop`, `median` ou `fill`).
            column   (list[str], Optionel) : Les colonnes à remplir.

        Returns:
            pd.DataFrame: Un nouveau tableau sans des valeurs manquantes est retourné.
        """

        if not isinstance(self.df, pd.DataFrame):
            print("Le nettoyage n'est possible qu'aux DataFrames.")
            return self.df

        df_copy = self.df.copy() # On travaille sur une copie pour ne pas modifier l'original

        if strategy == 'drop':
            df_copy.dropna(inplace=True)
            print("\nLes lignes avec des valeurs manquantes ont été supprimées.\n")
        else:
            colonne_a_remplire = column if column else df_copy.select_dtypes(
                include=np.number).columns.to_list()
            if colonne_a_remplire:
                try:
                    for col in colonne_a_remplire:
                        if strategy == 'mean':
                            valeur_moyenne_de_la_colonne_numerique = df_copy[col].mean()
                            df_copy[col].fillna(valeur_moyenne_de_la_colonne_numerique, inplace=True)
                            continue
                        elif strategy == 'median':
                            valeur_median_de_la_colonne_numerique = df_copy[col].median()
                            df_copy[col].fillna(valeur_median_de_la_colonne_numerique, inplace=True)
                            continue
                        elif strategy == 'fill':
                            cellules_vide = 0
                            df_copy[col].fillna(cellules_vide, inplace=True)
                            continue
                except ValueError as ve:
                    raise ValueError(f"\nLa valeur de la stragie non supporté: {ve}\n") from ve
            else:
                print("\nAucune colonne numérique trouvée pour le changement.\n")
        return df_copy

    def gerer_les_valeurs_duplicates(self) -> pd.DataFrame:
        """
        Supprime les lignes dupliquées d'un tableau s'il y a.
        
        Args:
            df (pd.DataFrame) : Prend le tableau des données.

        Return:
            pd.DataFrame: Renvoi un nouveau tableau sans des lignes dupliquées s'il y avait.
        """

        if not isinstance(self.df, pd.DataFrame):
            print("\nL'opération n'est applicable qu'aux DataFrames.\n")
            return self.df

        initial_rows = len(self.df)
        df_copy = self.df.drop_duplicates().copy()
        dropped_rows = initial_rows - len(df_copy)
        print(f"\n{dropped_rows} ligne(s) dupliquées ont été supprimées.\n")
        return df_copy
