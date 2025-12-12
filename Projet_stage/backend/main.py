"""Chargement des modules depuis le packages du dossier `Projet_stage`"""

# Il faut s'assurer que les importations se présente sous la forme:
# from modules.nom_du_module import nom_de_la_class

from typing import (
    Any,
    # Optional
    )

from cfg.config_db import DbCreateRequest
from fastapi import (
    FastAPI,
    HTTPException)
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    JSONResponse,
    # HTMLResponse
    )  # Formateur JSON
from pydantic import BaseModel
from modules.analysis import Analyse
from modules.clean_dataframe_for_json import CleanDataframeForJson
from modules.loading import (
    DataLoader,
    FilePayload,
    )

# from modules.save_in_data_base import SaveInDataBase
from modules.visualisation_2D import (
    GraphicVueFolder2D,
    Visualisation2D,
    )
from modules.visualisation_3D import (
    GraphicVueFolder3D,
    Visualisation3D
    )

import pandas as pd

#---------------- FastAPI informations --------------------

TITLE = "Projet d'outil de visualisation de données."

SUMMARY = """Ce projet permet de faire la visualisation des données numéric
en deux ou trois dimension en fonction du choix de l'utilisateur"""

DESCRIPTIONS = """Avant toute action avec cette API, il faut faire
la **configuration de l'emplacement des données** à lire et à visualiser.

Cependant, il est possible de **choisir les données soit en local sur un disque local,
ou bien une base de données local**(nous avons prise en compte **PostgreSQL**, 
**MySQL** et **SQLite**) ou bien les données peuvent aussi être **choisi à distant 
depuis un serveur**.

Une fois l'emplacement des données choisi, l'utilisateur doit également **choisir où 
conserver les données après traitement ou modification**, c'est-à-dire que les rendu 
doivent être conservé en local ou bien sur un serveur distant."""

VERSION = "0.0.1"

#----------------------------------------------------------

app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    description=DESCRIPTIONS,
    version=VERSION
    )

origines = [
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

# Autoriser le frontend à accéder au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origines,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin absolut que l'utilisateur doit entrer pour voir les données qu'il/elle charge.
LOACL_FILE_READ = "/file/{file_path:path}"

# Pour chaque endpoint il faut qu'il respecte le CRUD.
# Endpoints SEND(POST method) data on server since local files
DB_CONFIG = "/v_01/db_config/"
LOADING_DATA = "/v_01/data/"
ENDPOINT_FOR_DATA_2 = "/v_01/data_2/"

URL_GET_DATA_ON_SERVER = "/v_01/loading_data/"
URL_ANALYSE_DATA = "/v_01/analyse/"
URL_VISUALISATION_2D = "/v_01/visualisation_2d/"
URL_VISUALISATION_3D = "/v_01/visualisation_3d/"

# Instanciation de classe
chargeur_data = DataLoader()
chargeur_clean_df_for_json = CleanDataframeForJson()
chargeur_analyse = Analyse()

@app.get('/')
def root() -> dict[str, str]:
    """Vérification du fonctionnement du serveur backend.

    Returns:
        dict: Un dictionnaire montrant la bonne marche du serveur backend est retourné.
    """
    return {"message": "Le serveur tourne sans problème..."}

# ---------------- CRUD of DB_CONFIG ----------------
# CREATE route (POST)

config_info: dict[str, Any] = {}

@app.post(
    DB_CONFIG,
    summary="Choix de la base de données à configurer.")
def config_db(
    payload: DbCreateRequest,
    ) -> dict[str, Any]:
    """Point de terminaison pour faire la configuration
    d'une base de données devant contenir les données.

    Args:
        db_config (DbType): db_config permetra d'avoir une configuration de la base de données.

    Returns:
        ConfigDb: L'argument de la fonction est renvoyé.
    """

    config_info["db_type_"] = payload.db_type

    match payload.db_type:
        case "psql":
            cfg = payload.params
        case "mysql":
            cfg = payload.params
        case "sqlite":
            cfg = payload.params

    config_info["dsn_"] = cfg.to_dsn()

    print("\n===================\n")
    print(cfg)
    print(type(cfg))
    print("\n===================\n")

    return {"statu": "success", "db_type": payload.db_type, "config": cfg, "dsn": cfg.to_dsn()}

# READ route (GET)

@app.get(
    DB_CONFIG+'/{db_type}',
    summary="Lecture de la configuration de la base de données.")
def read_db_cfg(db_type: str)-> Any:
    """Cette route permet de lire une configuration si elle existe.

    Args:
        db_type (str): Ce paramètre récupère le type de configuration (psql, mysql ou sqlite).

    Returns:
        Any: _description_
    """

    if db_type != config_info["db_type_"]:
        raise HTTPException(
            status_code=404,
            detail="Le type de configuration demandé n'est pas trouvé.")
    return {"db_type": db_type, "dsn": config_info["dsn_"]}
# --------------------------------------------------------------


# CRUD OF LOADING OF DATA
# CREAT ROUTER (POST)

df: pd.DataFrame

# class FilePayload(BaseModel):
#     """Cette classe reçoi le chemin ou les données qui doivent être lu pour le chargement.

#     Args:
#         BaseModel (Model): Cette classe assure la sérialisation et la validation de la classe.
#     """

#     file_path: str

@app.post(LOADING_DATA)
def send_data(payload: FilePayload) -> JSONResponse:
    """Envoie des données sur (`http://127.0.0.1:8000/v_01/data/`) pour faire des dépôt de données.

    Returns:
        JSONResponse: Un Objet JSON de données est retourné sur le serveur backend.
    """

    file_path = payload.file_path

    global df

    # Chargement des données
    df = chargeur_data.load(file_path=file_path)

    # Nettoyer les données invalides pour JSON

    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)

    dict_object = df.to_dict(orient="records")

    return JSONResponse(content=jsonable_encoder(dict_object))

# READ ROUTER (GET)
@app.get(LOADING_DATA)
def read_data() -> JSONResponse:
    """Lire les données sur (`http://127.0.0.1:8000/v_01/data/`)

    Args:
        url_or_local_path (str): Chemin du fichier à charger

    Returns:
        JSONResponse: Un objet au format JSON est retourné.
    """

    global df

    # Nettoyer les données invalides pour JSON

    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)

    dict_object = df.to_dict(orient="records")

    return JSONResponse(content=jsonable_encoder(dict_object))

# DELETE ROUTER (DELETE)
@app.delete(LOADING_DATA)
def delete_data() -> None:
    """Lire les données sur (`http://127.0.0.1:8000/v_01/data/`)

    Args:
        url_or_local_path (str): Chemin du fichier à charger

    Returns:
        JSONResponse: Un objet au format JSON est retourné.
    """

    global df

    df.drop(colums=[col for col in df.colums], inplace=True)

    return None

# UPDATE ROUTER (UPDATE)
# PATCH ROUTER (PATCH)
# -----------------------------------------------

# CRUD OF ANALYSE OF DATA LOADING
# CREATE ROUTER (POST)
@app.post(URL_ANALYSE_DATA)
def send_data_analyse() -> JSONResponse:
    """Analyse des données chargé par l'utilisateur sur (`http://127.0.0.1:8000/v_01/analyse/`).

    Returns:
        dict: Un dictionnaire de données contenant les analyses des données chargées est retourné.
    """

    global df

    # Nettoyer les données invalides pour JSON.
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)

    # Résumer des données
    dict_object = chargeur_analyse.summarize(df)

    return JSONResponse(content=jsonable_encoder(dict_object))

# READ ROUTER (GET)
@app.get(URL_ANALYSE_DATA)
def read_data_analyse() -> JSONResponse:
    """Analyse des données chargé par l'utilisateur sur (`http://127.0.0.1:8000/v_01/analyse/`).

    Returns:
        dict: Un dictionnaire de données contenant les analyses des données chargées est retourné.
    """

    global df

    # Nettoyer les données invalides pour JSON.
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)

    # Résumer des données
    dict_object = chargeur_analyse.summarize(df)

    return JSONResponse(content=jsonable_encoder(dict_object))

# DELETE ROUTER (DELETE)
@app.delete(URL_ANALYSE_DATA)
def delete_data_analyse() -> None:
    """Analyse des données chargé par l'utilisateur sur (`http://127.0.0.1:8000/v_01/analyse/`).

    Returns:
        dict: Un dictionnaire de données contenant les analyses des données chargées est retourné.
    """

    global df

    df.drop(columns=[col for col in df.columns], inplace=True)

    return None

# UPDATE ROUTER (UPDATE)
# PATCH ROUTER (PATCH)

# ---------------------- CRUD OF VISUALIZATION 2D ----------------------
# CREATE VISULIZATION (POST)
@app.post(URL_VISUALISATION_2D)
def send_data_visualisation_2d(payload: GraphicVueFolder2D) -> None:
    """Mise en place de la visualisation 2D après analyse.

    Returns:
        None: Une figure 2D est retourné sur le serveur.
    """

    folder_path = payload.folder_path

    global df

    chargeur_visualisation_2d = Visualisation2D(df=df, color_col=None, graphic_vue_forder=folder_path)

    return chargeur_visualisation_2d.visualisation_automatique()

# READ VISUALIZATION (GET)
@app.get(URL_VISUALISATION_2D)
def read_data_visualisation_2d() -> None:
    """Mise en place de la visualisation 2D après analyse.

    Returns:
        None: Une figure 2D est retourné sur le serveur.
    """

    global df

    chargeur_visualisation_2d = Visualisation2D(df=df, color_col=None, graphic_vue=None)

    return chargeur_visualisation_2d.visualisation_automatique()

# ---------------------- CRUD OF VISUALIZATION 3D----------------------
# CREATE 3D VISULIZATION (POST)
@app.post(URL_VISUALISATION_3D)
def send_data_visualisation_3d(payload: GraphicVueFolder3D) -> None:
    """Mise en place de la visualisation 3D après analyse.

    Returns:
        None: Une figure 3D est retourné sur le serveur.
    """

    global df

    chargeur_visualisation_3d = Visualisation3D(df=df, color_col=None, graphic_vue=None)

    return chargeur_visualisation_3d.visualisation_automatique()

# READ 3D VISUALIZATION (GET)
@app.get(URL_VISUALISATION_3D)
def read_data_visualisation_3d() -> None:
    """Mise en place de la visualisation 3D après analyse.

    Returns:
        None: Une figure 3D est retourné sur le serveur.
    """
    # df = chargeur_data.load(file_path=FILE_PATH)

    global df

    chargeur_visualisation_3d = Visualisation3D(df=df, color_col=None, graphic_vue=None)

    return chargeur_visualisation_3d.visualisation_automatique()
