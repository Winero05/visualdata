"""Ce module permet de faire d'analyse de données.

Classes:

    Analyse:

        Analyse de données chargées depuis un emplacement local ou distant.
        Methodes:
            summarize(
                self,
                data: Union[pd.DataFrame, np.ndarray, str] = None
            ) -> dict:
            Retourne un résumé statistique de la donnée chargée.

            Args:
                data (Union[pd.DataFrame,np.ndarray,str]) : Les données à résumer (par défaut c'est `None`).

            Returns:
                dict: L'ensemble des informations résumé dans un dictionnaire.

            get_descriptive_stats(
                self,
                df: pd.DataFrame
                ) -> pd.DataFrame:
                Fait des statistiques descriptives pour les colonnes numériques et catégorielles.

                Args:
                    df (pd.DataFrame) : Prend les données et fourni des informations statistiques.

                Returns:
                    pd.DataFrame: Des données numériques et catégorielles traitées sont retourne.


Raises:
    ValueError: Une erreur de valeur est soulevée s'il n'y a pas de données à résumer.
    TypeError: Une erreur de typage est soulevée s'il n'y a pas de données repectant les types par défaut.
    TypeError: Une erreur de typage de données soulevée s'il n'y a pas de données tabulaire.

Returns:
    dict: Un dictionnaire de résumé est retourné avec la méthode `summarize`.

    pd.DataFrame: Des données numériques et catégorielles traitées sont retourné.
"""

from typing import Union
import pandas as pd
import numpy as np

class Analyse:
    """
    Analyse de données chargées depuis un emplacement local ou distant.
    """

    def summarize(self, data: Union[pd.DataFrame, np.ndarray, str] = None) -> dict:
        """
        Retourne un résumé statistique de la donnée chargée.

        Args:
            data (Union[pd.DataFrame,np.ndarray,str]) : Les données à résumer (par défaut c'est `None`).

        Returns:
            dict: L'ensemble des informations résumé dans un dictionnaire.
        """
        if data is None:
            raise ValueError("Aucune donnée chargée.")

        if isinstance(data, pd.DataFrame):
            return {
                'shape': data.shape,
                'columns': list(data.columns),
                'duplicates': int(data.duplicated().sum()),
                'missing_values': data.isnull().sum().to_dict(),
                'types': data.dtypes.astype(str).to_dict(),
                # 'infos': data.info(),
                'num_col': list(data.select_dtypes(include='number').columns),
            }
        elif isinstance(data, np.ndarray):
            return {
                'type': 'image',
                'shape': data.shape,
                'dtype': str(data.dtype)
            }
        elif isinstance(data, str):
            return {
                'type': 'text',
                'length': len(data),
                'lines': int(data.count('\n') + 1)
            }
        else:
            raise TypeError("Type de données non supporté pour le résumé.")

    def get_descriptive_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fait des statistiques descriptives pour les colonnes numériques et catégorielles.

        Args:
            df (pd.DataFrame) : Prend les données et fourni des informations statistiques.

        Returns:
            pd.DataFrame: Des données numériques et catégorielles traitées sont retourne.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Les données ne sont pas tabulaires (DataFrame).")

        numeric_stats = df.describe(include=np.number).transpose()
        categorical_stats = df.describe(include='object').transpose()

        return pd.concat([numeric_stats, categorical_stats])
