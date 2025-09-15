# data_loader/cleaning.py
import pandas as pd
import numpy as np

def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean', column: str = None) -> pd.DataFrame:
    """
    Gère les valeurs manquantes d'un DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        print("⚠️ L'opération n'est applicable qu'aux DataFrames.")
        return df

    df_copy = df.copy() # On travaille sur une copie pour ne pas modifier l'original

    if strategy == 'drop':
        df_copy.dropna(inplace=True)
        print("🗑️ Les lignes avec des valeurs manquantes ont été supprimées.")
    else:
        columns_to_handle = [column] if column else df_copy.select_dtypes(include=np.number).columns
        if not columns_to_handle.empty:
            for col in columns_to_handle:
                if strategy == 'mean':
                    fill_value = df_copy[col].mean()
                elif strategy == 'median':
                    fill_value = df_copy[col].median()
                elif strategy == 'fill':
                    fill_value = 0
                else:
                    print("⚠️ Stratégie d'imputation non valide.")
                    return df
                df_copy[col].fillna(fill_value, inplace=True)
                print(f"🔧 Valeurs manquantes de la colonne '{col}' imputées avec la stratégie '{strategy}'.")
        else:
            print("⚠️ Aucune colonne numérique trouvée pour l'imputation.")

    return df_copy

def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les lignes dupliquées d'un DataFrame."""
    if not isinstance(df, pd.DataFrame):
        print("⚠️ L'opération n'est applicable qu'aux DataFrames.")
        return df

    initial_rows = len(df)
    df_copy = df.drop_duplicates().copy()
    dropped_rows = initial_rows - len(df_copy)
    print(f"🧹 {dropped_rows} lignes dupliquées ont été supprimées.")
    return df_copy