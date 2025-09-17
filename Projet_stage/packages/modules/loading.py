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
    """

    def __init__(self):
        self.df = None
        self.format = None

    def load(self, file_path: str, file_type: str = None, sql_query: str = None, db_path: str = None,
             image_as_dataframe: bool = True) -> Union[pd.DataFrame, np.ndarray, str]:
        """
        Chargement des données en fonction des fichiers chargés. Les extensions de fichier supportées sont : CSV, Excel, JSON, YAML, Parquet, SQL, Image (vers DataFrame), Texte (vers string).
        """
        if not file_type:
            file_type = Path(file_path).suffix.lower().replace('.', '')

        self.format = file_type

        try:
            if file_type == 'csv':
                try:
                    self.df = pd.read_csv(file_path, sep=',')
                except pd.errors.ParserError:
                    self.df = pd.read_csv(file_path, sep=';')
            elif file_type in ['xls', 'xlsx']:
                self.df = pd.read_excel(file_path)
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
                raise ValueError("Format de fichier non supporté ou paramètres manquants.")

            print(f"\nFichier '{file_path}' chargé avec succès.")
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Erreur : Le fichier à l'adresse '{file_path}' est introuvable.")
        except Exception as e:
            raise Exception(f"Une erreur est survenue lors du chargement : {e}")