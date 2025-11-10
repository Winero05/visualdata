"""Chargement des modules depuis le packages du dossier `Projet_stage`"""

# Il faut s'assurer que les importations se présente sous la forme:
# from modules.nom_du_module import nom_de_la_class
from backend.modules.loading import DataLoader
from backend.modules.config_db import ConfigDb
from backend.modules.clean_dataframe_for_json import CleanDataframeForJson
from backend.modules.analysis import Analyse
# from backend.modules.save_in_data_base import SaveInDataBase
# from backend.modules.visualisation_2D import Visualisation_2D
# from backend.modules.visualisation_3D import Visualisation_3D

from fastapi import FastAPI
from fastapi.responses import JSONResponse # Formateur JSON
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd

app = FastAPI()

# Autoriser le frontend à accéder au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin absolut que l'utilisateur doit entrer pour voir les données qu'il/elle charge.
LOACL_FILE_READ = "/file/{file_path:path}"

# Pour chaque endpoint il faut qu'il respecte le CRUD.
# Endpoints SEND(POST method) data on server since local files
DB_CONFIG = "/v_01/db_config"
ENDPOINT_FOR_DATA_1 = "/v_01/data_1"
ENDPOINT_FOR_DATA_2 = "/v_01/data_2"

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
        dict: Un dictionnaire contenant les informations
        personnalisé montrant la bonne marche du serveur backend est retourné.
    """
    return {"message": "Le serveur tourne sans problème..."}

@app.get(DB_CONFIG)
def config_db(db_config: ConfigDb()):
    """Point de terminaison pour faire la configuration
    de la base de données devant contenir les données.

    Args:
        db_config (ConfigDb): db_config permetra d'avoir une configuration de la base de données.

    Returns:
        ConfigDb: L'argument de la fonction est renvoyé.
    """
    return db_config

@app.post(ENDPOINT_FOR_DATA_1)
def endpoint_data_1(file_path: str) -> JSONResponse:
    """Envoie des données sur (`http://127.0.0.1:8000/v_01/data_1`) pour faire des dépôt de données.

    Returns:
        JSONResponse: Un Objet JSON de données est retourné sur le serveur backend.
    """

    # Chargement des données
    df = chargeur_data.load(file_path=file_path)

    # Nettoyer les données invalides pour JSON
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)
    dict_object = df.to_dict(orient="records")
    return JSONResponse(content=jsonable_encoder(dict_object))


@app.get(ENDPOINT_FOR_DATA_1)
def read_data() -> dict[str, str]:
    """Lire les données sur (`http://127.0.0.1:8000/v_01/data_1/send`)

    Args:
        file_path (str): Chemin du fichier à charger

    Returns:
        _type_: _description_
    """
    return {"message": "La lecture est possible à présent."}


# @app.post(URL_ANALYSE_DATA)
# def endpoint_data_analyse():
#     """Analyse de chaque données chargé par l'utilisateur sur (`http://127.0.0.1:8000/v_01/analyse`).

#     Returns:
#         dict: Un dictionnaire de données contenant les analyses des données chargées est retourné.
#     """
#     df = chargeur_data.load(file_path=FILE_PATH)
#     return chargeur_analyse.summarize(df)

# @app.post(URL_VISUALISATION_2D)
# def endpoint_data_visualisation_2d():
#     """Mise en place de la visualisation 2D sur (`http://127.0.0.1:8000/v_01/visualisation_2`) après analyse.

#     Returns:
#         None: Une figure 2D est retourné sur le serveur.
#     """
#     df = chargeur_data.load(file_path=FILE_PATH)
#     chargeur_visualisation_2d = Visualisation_2D(df=df)
#     return chargeur_visualisation_2d.visualisation_automatique()

# @app.post(URL_VISUALISATION_3D)
# def endpoint_data_visualisation_3d():
#     """Mise en place de la visualisation 3D sur (`http://127.0.0.1:8000/v_01/visualisation_3`) après analyse.

#     Returns:
#         None: Une figure 3D est retourné sur le serveur.
#     """
#     df = chargeur_data.load(file_path=FILE_PATH)
#     chargeur_visualisation_3d = Visualisation_3D(df=df)
#     return chargeur_visualisation_3d.visualisation_automatique()
