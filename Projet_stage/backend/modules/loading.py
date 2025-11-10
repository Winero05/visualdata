r"""Ce module permet de charger des données venant d'un emplacement local ou distant.

class:

    DataLoader:
        Cette classe permet de charger des données depuis un emplacement local ou distant.
        Les extensions de fichiers supportés sont : `.csv`, `.xlx/xlsx`, `.json`, `.yml/.yaml`, Parquet, `.jpeg/.png/.jpg`, `.txt`.

        methodes:
            load(
                self,
                file_path,
                file_type,
                sql_query,
                db_path,
                image_as_dataframe
            )
            Cette méthode charge des données en fonction d\'un fichier chargés.
            Les extensions de fichier supportées sont :
            Les extensions de fichiers supportés sont : `.csv`, `.xlx/xlsx`, `.json`, `.yml/.yaml`, Parquet, `.jpeg/.png/.jpg`, `.txt`.

            Args:
                file_path (str) : Reçoi le chemin de l\'emplacement des données à charger.
                Le chemin peut-être local ou distant.
                sql_query (str | None) : Reçoi une requête SQL permettant de lire dans une base de données.
                db_path (str | None) : Reçoi le nom de la base de données dans laquelle il faut lire les données.
                image_as_dataframe (bool) : Cet argument confirme le chargement d\'une image. False est la valeur par défaut.

            Returns:
                (Union[pd.DataFrame, np.ndarray, str]) : La valeur retournée est l\'une des types de l\'union.
"""

import os
import json
import sqlite3
from typing import Union, Optional
import numpy as np
import yaml
import pandas as pd
from PIL import Image
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
# import pyarrow.parquet as pq
# from pathlib import Path

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class DataLoader:
    """
    Chargement des données depuis un emplacement distant ou local.
    Fichiers supportés sont : CSV, Excel, JSON, YAML, Parquet, SQL, Image, Texte.

    Méthodes:

        load(
            file_path,
            file_type,
            sql_query,
            db_path,
            image_as_dataframe
            ) -> Union[pd.DataFrame, np.ndarray, str]
    """
    df: Optional[pd.DataFrame]
    format: Optional[str]

    def load(
        self,
        file_path: str,
        sql_query: Optional[str] = None,
        db_path: Optional[str] = None,
        image_as_dataframe: bool = False
        ) -> Union[pd.DataFrame, np.ndarray, str]:
        """
        Cette méthode charge des données en fonction d'un fichier chargés.
        Les extensions de fichier supportées sont :
        **CSV**, **Excel**, **JSON**, **YAML**, **Parquet**, **SQL**, **Image**, **Texte**.

        Args:
            file_path (str): Reçoi le chemin de l'emplacement des données à charger.
            Le chemin peut-être local ou distant.
            sql_query (str | None) : Reçoi une requête SQL permettant de lire dans une base de données.
            db_path (str | None) : Reçoi le nom de la base de données dans laquelle il faut lire les données.
            image_as_dataframe (bool) : Cet argument confirme le chargement d'une image et sa valeur par défaut est `False`.

        Returns:
            (Union[pd.DataFrame, np.ndarray, str]) : La valeur retournée est l'une des types de l'union.
        """

        # Si le chemin du fichier contenant les données se trouve sous un OS Windows, il faut remplacer les antislashe (\) par des slashes (/).
        if "\\" in file_path:
            file_path = "/".join(file_path.split("\\"))

        # Récupération des données depuis une URL d'un serveur ou d'un chemin local
        try:
            if file_path.startswith("http") or file_path.startswith("https"):
                print(f"Chargement des données depuis une URL distante : {file_path}")
                self.df = pd.read_csv(file_path)
                return self.df
            elif os.path.exists(file_path):
                # Récupérer le suffix du chemin de données (i.e 'csv', 'json' etc).
                self.format = file_path.split(".")[-1]

                # Définir les différents séparateur possible qui peuvent être présent dans un fichier
                # de données.
                sepateur_valeurs = [";", "|", "\t", ","]

                # Mettre dans `seperate_valeurs` l'emplacement du séparateur utilisé dans le fichier chargé
                # et le stocké dans une variable `index_sepateur`.
                index_sepateur = 0

                # Lire la première ligne des données chargées pour connaître la nature du séparteur
                # présent dans le fichier ainsi que son index dans la liste sepateur_valeurs.
                with open(file=file_path, encoding="utf-8") as contenu_du_fichier:
                    for ligne in contenu_du_fichier:
                        for sep in sepateur_valeurs:
                            if sep not in ligne:
                                index_sepateur += 1
                                continue
                        break
                    if self.format == 'csv':
                        try:
                            self.df = pd.read_csv(
                                filepath_or_buffer=file_path,
                                sep=f"{sepateur_valeurs[index_sepateur]}"
                                )
                        except pd.errors.ParserError as pe:
                            raise pd.errors.ParserError(
                                f"Assurez-vous que les séparateur suivant: {sepateur_valeurs} sont utilisé dans le fichier chargé."
                                ) from pe
                    elif self.format in ['xls', 'xlsx']:
                        try:
                            self.df = pd.read_excel(file_path)
                        except pd.errors.ParserError as pe:
                            raise pd.errors.ParserError(
                                f"Assurez-vous que les séparateur suivant: {sepateur_valeurs} sont utilisé dans le fichier chargé."
                                ) from pe
                    elif self.format == 'json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        self.df = pd.json_normalize(data)
                    elif self.format in ['yaml', 'yml']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                        self.df = pd.json_normalize(data)
                    elif self.format == 'parquet':
                        self.df = pd.read_parquet(file_path)
                    elif self.format == 'sql' and db_path and sql_query:
                        conn = sqlite3.connect(db_path)
                        self.df = pd.read_sql_query(sql_query, conn)
                        conn.close()
                    elif self.format in ['png', 'jpg', 'jpeg']:
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
                    elif self.format == 'txt':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.df = f.read()
                    else:
                        raise ValueError("Format de fichier non supporté.")
                    print(f"\nFichier '{file_path.split('/')[-1]}' chargé avec succès.")
            return self.df
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Erreur : Le fichier à l'adresse '{file_path.split('/')[-1]}' est introuvable.") from exc
        except Exception as e:
            raise ValueError(f"\nUne erreur est survenue lors du chargement : {e}\n") from e
