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

from dataclasses import dataclass
import os
import json
import sqlite3
from typing import (
    Union,
    Optional,
    Annotated,
    )
import numpy as np
import yaml
import pandas as pd
from PIL import Image
from pydantic import (
    Field,
    BaseModel,
    # ConfigDict,
    )
# from pydantic.dataclasses import dataclass
from fastapi import (
    APIRouter,
    # status,
    # HTTPException
    )
# import pyarrow.parquet as pq
# from pathlib import Path

router = APIRouter()

class FilePayload(BaseModel):
    """Cette classe reçoi le chemin des données à lire pour le chargement.

    Args:
        BaseModel (Model): Cette classe assure la sérialisation et la validation de la classe.
        file_path (str): le chemin de fichier de données.
    """

    file_path: Annotated[
        str,
        Field(
        min_length=1, # Le champ ne doit pas être vide.
        title="file_path",
        description="Cette variable reçois le chemin des données à charger.",
    )]

# @dataclass(config=ConfigDict(arbitrary_types_allowed=True))
@dataclass
class DataLoader():
    """
    Chargement des données depuis un emplacement distant ou local.
    Fichiers supportés sont : CSV, Excel, JSON, YAML, Parquet, SQL, Image, Texte.

    Args:
        df: pd.DataFrame | None = None
        Cette variable reçoit les données chargées sous forme tabulaire.
        format: str | None = None
        Cette variable reçoit le format du fichier chargé.

    Méthodes:
        load(
            file_path,
            file_type,
            sql_query,
            db_path,
            image_as_dataframe
            ) -> Union[pd.DataFrame, np.ndarray, str]
    """
    # Veuillez mettre cette variable à "None" lors de l'initialisation de la classe.
    df: Optional[pd.DataFrame] = None
    # Veuillez mettre cette variable à "None" lors de l'initialisation de la classe.
    format: Optional[str] = None

    def load(
        self,
        file_path: str,
        sql_query: Optional[str] = None,
        db_path: Optional[str] = None,
        image_as_dataframe: bool = False
        ) -> Union[pd.DataFrame, np.ndarray, str]:
        """
        Cette méthode charge un fichier de données en fonction de son extension.
        - Les extensions supportées sont :
        **CSV**, **Excel**, **JSON**, **YAML**, **Parquet**, **SQL**, **Image**, **Texte**.

        Args:
            file_path (str): Reçoi le chemin de l'emplacement des données à charger.
            sql_query (str | None) : Reçoi une requête SQL pour lire dans une base de données.
            db_path (str | None) : Reçoi le DNS de la base de données.
            image_as_dataframe (bool) : Confirme le chargement d'une image (`False` par défaut).

        Returns:
            (Union[pd.DataFrame, np.ndarray, str]) : Au moins un type de l'union est retourné.
        """

        # Remplacer les back-slach en slache.
        if "\\" in file_path:
            file_path = "/".join(file_path.split("\\"))

        # Récupérer des données depuis un serveur ou en local
        try:
            if file_path.startswith(("http", "https")):
                print(f"Chargement des données depuis une URL distante : {file_path}")
                if file_path.endswith(".csv"):
                    self.df = pd.read_csv(
                        filepath_or_buffer=file_path,
                        delimiter=None, # Trouver le délimiteur automatiquement.
                        )
                if file_path.endswith(".json"):
                    self.df = pd.read_json(file_path)
                if file_path.endswith(".parquet"):
                    self.df = pd.read_parquet(file_path)
                if file_path.endswith(("xls", "xlsx")):
                    self.df = pd.read_excel(file_path)
            elif os.path.exists(file_path):
                # Récupérer le suffix du chemin de données (i.e 'csv', 'json' etc).
                self.format = file_path.split(".")[-1]

                try:
                    if self.format == 'csv':
                        self.df = pd.read_csv(
                            filepath_or_buffer=file_path,
                            delimiter=None, # Trouve le délimiteur automatiquement.
                            )
                    elif self.format in ['xls', 'xlsx']:
                        self.df = pd.read_excel(file_path)
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
                except pd.errors.ParserError as pe:
                    raise pd.errors.ParserError(
                        f"Error lors du chargement des données.") from pe
            return self.df
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Erreur : Le fichier à l'adresse '{file_path.split('/')[-1]}' est introuvable."
                ) from exc
        except Exception as e:
            raise ValueError(f"\nUne erreur est survenue lors du chargement : {e}\n") from e
