import pandas as pd
import numpy as np
from typing import Union
from .sansEspace import SansEspace

class Analyse:
    def summarize(data: Union[pd.DataFrame, np.ndarray, str]) -> dict:
        """Retourne un résumé statistique de la donnée chargée."""
 
        if data is None:
            raise ValueError("Aucune donnée chargée.")

        if isinstance(data, pd.DataFrame):
            return {
                'shape': data.shape,
                'columns': list(data.columns),
                'types': data.dtypes.astype(str).to_dict(),
                'missing_values': data.isnull().sum().to_dict(),
                'duplicates': data.duplicated().sum()
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
                'lines': data.count('\n') + 1
            }
        else:
            raise TypeError("Type de données non supporté pour le résumé.")

    def get_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
        """
        Retourne des statistiques descriptives pour les colonnes numériques et catégorielles d'un DataFrame.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Les données ne sont pas tabulaires (DataFrame).")
        
        numeric_stats = df.describe(include=np.number).transpose()
        categorical_stats = df.describe(include='object').transpose()
        
        return pd.concat([numeric_stats, categorical_stats])

def preprocess_for_reduction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prépare un DataFrame pour la réduction de dimension en encodant les
    colonnes catégorielles et en remplissant les valeurs manquantes.
    """
    df_processed = df.copy()
    
    # Gérer les valeurs manquantes dans les colonnes numériques
    numeric_cols = df_processed.select_dtypes(include=np.number).columns
    df_processed[numeric_cols] = df_processed[numeric_cols].fillna(df_processed[numeric_cols].median())

    # Encodage One-Hot des variables catégorielles
    categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns
    df_processed = pd.get_dummies(df_processed, columns=categorical_cols, dummy_na=True)
    
    return df_processed