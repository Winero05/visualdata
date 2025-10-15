# data_loader/loading.py
import pandas as pd
import json
import sqlite3
import yaml
import os
import pyarrow.parquet as pq
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Union

class DataLoader:
    """
    Chargement des données et les fichiers supportés sont : CSV, Excel, JSON, YAML, Parquet, SQL, Image, Texte.

    Attributs:
    
        Pas d'attribut.
    
    Méthodes:

        load(file_path, file_type, sql_query, db_path, image_as_dataframe) : Retourne un DataFrame ou une liste ou un chaîne de caractère en fonction de la nature des fichiers ayant les extensions précitées.
    """

    def __init__(self):
        self.df = None
        self.format = None

    # chemin = "/home/adama/visualdata/Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"

    def load(self, file_path: str, sql_query: str = None, db_path: str = None,
             image_as_dataframe: bool = False) -> Union[pd.DataFrame, np.ndarray, str]:
        """
        Chargement des données en fonction des fichiers chargés. Les extensions de fichier supportées sont : CSV, Excel, JSON, YAML, Parquet, SQL, Image, Texte.

        Args:
            file_path(String) : Reçoi le chemin de l'emplacement des données à charger.
            sql_query(String | None) : Reçoi une requête SQL si le fichier chargé a une extension `.sql`.
            db_path(String | None) : Reçoi le chemin d'une base de données si le fichier chargé à l'extension `.sql`.
            image_as_dataframe(Bool) : Cet argument confirme le chargement d'une image et sa valeur par défaut est `False`.
        
        Returns:
            La valeur retournée peut-être soit un DataFrame, un tableau ou une chaîne de caractère.
        """
        
        # Si le chemin du fichier contenant les données se trouve sous un OS Windows, il faut remplacer les antislashe (\) par des slashes (/).
        # if "\\" in file_path:
        #     file_path.remplace("\\", "/")

        # Récupération des données depuis une URL d'un serveur ou d'un chemin local
        try:
            if file_path.startswith("http://") or file_path.startswith("https://"):
                print(f"Chargement des données depuis une URL distante : {file_path}")
                self.df = pd.read_csv(file_path)
            elif os.path.exists(file_path):
            # Récupérer le suffix du chemin de données (i.e 'csv', 'json' etc).
                file_type = file_path.split(".")[-1]
                    
                self.format = file_type

                # Définir les différentes séparateur possible qui puissent être présent dans un fichier de données.
                sepateur_valeurs = [";", "|", "\t", ","]
                
                # Mettre dans `seperate_valees` l'emplacement du séparateur utilisé dans le fichier chargé et le stocké dans une variable `index_sepateur`.
                index_sepateur = 0
                
                # Lire la première ligne des données chargées pour connaître la nature du séparteur présent dans le fichier ainsi que son index dans la liste sepateur_valeurs.
                with open(file=file_path) as contenu_du_fichier:
                    for ligne in contenu_du_fichier:
                        for sep in sepateur_valeurs:
                            if sep not in ligne:
                                index_sepateur += 1
                                continue
                        break
                    if file_type == 'csv':
                        try:
                            self.df = pd.read_csv(file_path, sep=f"{sepateur_valeurs[index_sepateur] }")
                        except pd.errors.ParserError:
                            raise pd.errors.ParserError(f"Veuillez vous assurer que la nature des séparateurs utilisé dans le fichier chargé font partie des éléments suivant : {sepateur_valeurs}")
                    elif file_type in ['xls', 'xlsx']:
                        try:
                            self.df = pd.read_excel(file_path)
                        except pd.errors.ParserError:
                            raise pd.errors.ParserError(f"Veuillez vous assurer que la nature des séparateurs font partie des éléments suivant : {sepateur_valeurs}")
                    elif file_type == 'json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        self.df = pd.json_normalize(data)
                    elif file_type in ['yaml', 'yml']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                        self.df = pd.json_normalize(data)
                    elif file_type == 'parquet':
                        self.df = pd.read_parquet(file_path)
                    elif file_type == 'sql' and db_path and sql_query:
                        conn = sqlite3.connect(db_path)
                        self.df = pd.read_sql_query(sql_query, conn)
                        conn.close()
                    elif file_type in ['png', 'jpg', 'jpeg']:
                        image = Image.open(file_path).convert('RGB')
                        img_array = np.array(image)
                        if image_as_dataframe:
                            h, w, c = img_array.shape
                            pixels = img_array.reshape(-1, c)
                            coords = [(x, y) for y in range(h) for x in range(w)]
                            self.df = pd.DataFrame(pixels, columns=["R", "G", "B"])
                            self.df["x"] = [coord[0] for coord in coords]
                            self.df["y"] = [coord[1] for coord in coords]
                        else:
                            self.df = img_array
                    elif file_type == 'txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.df = f.read()
                    else:
                        raise ValueError("Format de fichier non supporté.")
                    print(f"\nFichier '{file_path.split("/")[-1]}' chargé avec succès.")
                    return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Erreur : Le fichier à l'adresse '{file_path.split("/")[-1]}' est introuvable.")
        except Exception as e:
            raise Exception(f"Une erreur est survenue lors du chargement : {e}")
        
        #         print(f"Chargement des données locales : {file_path}")
        #         df = pd.read_csv(file_path)
        #     else:
        #         raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
        #     print(f"Données chargées avec succès ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
        #     return df
        # except Exception as e:
        #     print(f"Erreur lors du chargement : {e}")
        #     raise e
