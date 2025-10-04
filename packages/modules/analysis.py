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
    Prépare automatiquement un DataFrame pour la réduction de dimension :
    - Convertit les colonnes numériques mal typées
    - Encode les colonnes catégorielles (One-Hot)
    - Gère les valeurs manquantes
    - Élimine les colonnes vides et dupliquées
    """
    
    df_processed = df.copy()

    # 🔹 Étape 1 : Détection et conversion automatique des colonnes numériques
    for col in df_processed.columns:
        # Si plus de 70% des valeurs peuvent être converties en nombre, on la force en numérique
        try:
            numeric_version = pd.to_numeric(df_processed[col], errors="coerce")
            ratio_numeric = numeric_version.notna().mean()
            if ratio_numeric > 0.7:
                df_processed[col] = numeric_version
        except Exception:
            pass

    # 🔹 Étape 2 : Gérer les valeurs manquantes dans les colonnes numériques
    numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        median_value = df_processed[col].median()
        df_processed[col] = df_processed[col].fillna(median_value)

    # 🔹 Étape 3 : Supprimer les colonnes vides ou constantes
    df_processed = df_processed.loc[:, df_processed.nunique() > 1]

    # 🔹 Étape 4 : Encodage des colonnes catégorielles (texte)
    categorical_cols = df_processed.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        df_processed = pd.get_dummies(df_processed, columns=categorical_cols, dummy_na=True)

    # 🔹 Étape 5 : Remplacer les valeurs infinies et remplir les NaN restants
    df_processed = df_processed.replace([np.inf, -np.inf], np.nan).fillna(0)

    # 🔹 Étape 6 : Éviter les doublons de colonnes
    df_processed = df_processed.loc[:, ~df_processed.columns.duplicated()]

    # 🔹 Étape 7 : Vérification finale
    if df_processed.select_dtypes(include=[np.number]).empty:
        raise ValueError("Aucune donnée numérique exploitable pour la réduction de dimension après le prétraitement.")

    return df_processed



    

