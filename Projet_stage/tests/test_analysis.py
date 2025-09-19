import pandas as pd
import numpy as np
from typing import Union
from sansEspace import SansEspace

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
    
    def donnees_numerique_unique(df: pd.DataFrame) -> pd.DataFrame:
        """Cette fonction supprime les espaces dans les noms de la colonne du DataFrame, change les valeurs manquantent par une chaîne de caractère défini, converti les colonnes de type `Objet` en `category` et fait l'encodage de ces colonnes.
        
        Args:
            df(pd.DataFrame) : Les données chargées par l'utilisateur.
            
        Return:
            df_copy(pd.DataFrame) : Copie de la DataFrame chargé et modifié.
            
        """
        
        # Copie de la DataFrame reçu.
        df_copy = df.copy()
        
        # Renommer les colonnes contenant des espaces.
        df_copy.rename(SansEspace.sansEspace, axis = "columns", inplace = True)
        
        # Changer les valeurs manquantent par une chaîne de caractère `Aucune`
        df_copy.fillna("Aucune", inplace=True)
                
        # Conversion des valeurs (données) des colonnes de type `Objet` en `category`.
        df_copy['Gender'] = df_copy["Gender"].astype('category')
        df_copy['Occupation'] = df_copy["Occupation"].astype('category')
        df_copy['BMI_Category'] = df_copy["BMI_Category"].astype('category')
                
        # Encodage des valeurs catégorielles avec la méthode de N-1 Encoding dans de nouvelle colonne (On obtiendra des valeur de type `bool`).
        df_copy_col_sexe = pd.get_dummies(df_copy["Gender"], drop_first=True)
        df_copy_col_profession = pd.get_dummies(df_copy["Occupation"], drop_first=True)
        df_copy_col_imc = pd.get_dummies(df_copy["BMI_Category"], drop_first=True)

        ### Conversion des valeurs de type `bool` obtenu en valeur numériques.
        df_copy_col_sexe = df_copy_col_sexe.astype(int)
        df_copy_col_profession = df_copy_col_profession.astype(int)
        df_copy_col_sexe = df_copy_col_sexe.astype(int)
        df_copy_col_imc = df_copy_col_imc.astype(int)
        
        # Concatenation du DataFrame copié avec les nouvelle valeur encodées.
        df_concat = pd.concat([df_copy, df_copy_col_sexe, df_copy_col_profession, df_copy_col_imc], axis="columns")
        
        print(df_concat.head())
        
        df_concat.rename(SansEspace.sansEspace, inplace = True)
        
        df_concat.to_csv("Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/")
    
        return df_copy
        