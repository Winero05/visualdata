"""Poit d'entré de l'API."""

# Il faut s'assurer que les importations se présente sous la forme:
# from modules.nom_du_module import nom_de_la_class

from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Annotated,
    # Optional
    )
# from cfg.config_db import DbCreateRequest
from fastapi import (
    FastAPI,
    status,
    Query,
    # Form,
    # Depends,
    HTTPException
    )
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    JSONResponse,
    # FileResponse,
    # HTMLResponse
    )
# from pydantic import BaseModel
from modules.analysis import Analyse
from modules.clean_dataframe_for_json import CleanDataframeForJson
from modules.loading import (
    DataLoader,
    FilePayload,
    )

# from modules.save_in_data_base import SaveInDataBase
from modules.visualisation_2d import (
    BuildGraphic2DSlot,
    Visualisation2D,
    ReadGraphic2DSlot,
    )
from modules.visualisation_3d import (
    BuildGraphic3DSlot,
    Visualisation3D,
    ReadGraphic3DSlot,
    )

#---------------- FastAPI informations --------------------

TITLE = "Projet d'outil de visualisation de données."

SUMMARY = """Ce projet permet de faire la visualisation des données numéric
en deux ou trois dimension en fonction du choix de l'utilisateur"""

DESCRIPTION = """Avant toute action avec cette API, il faut faire
la **configuration de l'emplacement des données** à lire et à visualiser.

Cependant, il est possible de **choisir les données soit en local sur un disque local,
ou bien une base de données local**(nous avons prise en compte **PostgreSQL**, 
**MySQL** et **SQLite**) ou bien les données peuvent aussi être **choisi à distant 
depuis un serveur**.

Une fois l'emplacement des données choisi, l'utilisateur doit également **choisir où 
conserver les données après traitement ou modification**, c'est-à-dire que les rendu 
doivent être conservé en local ou bien sur un serveur distant."""

VERSION = "0.0.1"

class Routes:
    """Cette classe contient les différente route des endpoints.
    """
    LOADING_DATA = "/v_01/data/"
    ANALYSE_DATA = "/v_01/analyse/"
    VISUALISATION_2D = "/v_01/visualisation/2d/"
    VISUALISATION_3D = "/v_01/visualisation/3d/"

class Tags(str, Enum):
    """Cette classe déclare le nom des points des endpoints.

    Args:
        (str): Le type de chaque valeur de cette classe.
        (Enum): Chaque nom à une valeur qui lui assossiée.
    """
    LOADING_DATA = "loading_data"
    ANALYSE_DATA = "analyse_data"
    VISUALISATION_2D = "visualisation_data_2d"
    VISUALISATION_3D = "visualisation_data_3d"
    ITEMS = "items"
    USERS = "users"


#----------------------------------------------------------

app = FastAPI(
    title=TITLE,
    summary=SUMMARY,
    description=DESCRIPTION,
    version=VERSION
    )

app.state.data_frame = None
app.state.file_path = None
app.state.folder_path = None

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

# config_info: dict[str, Any] = {}

# DB_CONFIG = "/v_01/db_config/"

# @app.post(
#     DB_CONFIG,
#     summary="Choix de la base de données à configurer.")
# def config_db(
#     payload: DbCreateRequest,
#     ) -> dict[str, Any]:
#     """Point de terminaison pour faire la configuration
#     d'une base de données devant contenir les données.

#     Args:
#         db_config (DbType): db_config permetra d'avoir une configuration de la base de données.

#     Returns:
#         ConfigDb: L'argument de la fonction est renvoyé.
#     """

#     config_info["db_type_"] = payload.db_type

#     match payload.db_type:
#         case "psql":
#             cfg = payload.params
#         case "mysql":
#             cfg = payload.params
#         case "sqlite":
#             cfg = payload.params

#     config_info["dsn_"] = cfg.to_dsn()

#     print("\n===================\n")
#     print(cfg)
#     print(type(cfg))
#     print("\n===================\n")

#     return {"statu": "success", "db_type": payload.db_type, "config": cfg, "dsn": cfg.to_dsn()}

# # READ route (GET)

# @app.get(
#     DB_CONFIG+'/{db_type}',
#     summary="Lecture de la configuration de la base de données.")
# def read_db_cfg(db_type: str)-> Any:
#     """Cette route permet de lire une configuration si elle existe.

#     Args:
#         db_type (str): Ce paramètre récupère le type de configuration (psql, mysql ou sqlite).

#     Returns:
#         Any: _description_
#     """

#     if db_type != config_info["db_type_"]:
#         raise HTTPException(
#             status_code=404,
#             detail="Le type de configuration demandé n'est pas trouvé.")
#     return {"db_type": db_type, "dsn": config_info["dsn_"]}
# --------------------------------------------------------------

# CRUD OF LOADING DATA

# CREAT ROUTER (POST)

SUMMARY = "Création(POST) d'une resource à base d'un chemin utilisateur."
RESPONSE_DESCRIPTION = """Création des données depuis une URL."""

LOADING_DATA = "/v_01/data/"

@app.post(
    path=Routes.LOADING_DATA,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.LOADING_DATA],
    summary=SUMMARY,
    response_description=RESPONSE_DESCRIPTION,
    name="create_loading_data"
    )
def send_data(payload: FilePayload) -> JSONResponse:
    """L'utilisateur envoie le chemin d'un fichier de données et ce chemin
    sera lu par le endpoint pour renvoyer en retour une réponse
    au format JSON.

    Args:
        payload (FilePayload): Ce paramètre récupère le chemin d'un fichier de données.

    Returns:
        JSONResponse: Une réponse JSONResponse est retourné par le serveur backend.
    """

    # Stocker le chemin du fichier des données dans une variable.
    file_path = payload.file_path

    # Remplacer les back-slach en slache.
    if "\\" in file_path:
        file_path = "/".join(file_path.split("\\"))

    # Ce chemin est en suite fixé en mémoire au dela de ce endpoint.
    app.state.file_path = Path(file_path)

    # Chargement des données dans un data_frame.
    df = chargeur_data.load(file_path=file_path)

    # Nettoyer les données invalides pour un rendu JSON au frontend.
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=df)

    # Fixer la data_frame en mémoire au dela de ce endpoint.
    #https://fastapi.tiangolo.com/reference/fastapi/?h=state#fastapi.FastAPI.state
    app.state.data_frame = df

    # Conserver la data_frame sous forme d'un dictionnaire python.
    dict_object = df.to_dict(orient="records")

    # Puis retourner le rendu sous forme d'une réponse JSON au frontend.
    return JSONResponse(
        content=jsonable_encoder(dict_object),
        status_code=status.HTTP_201_CREATED)

# READ ROUTER (GET)

SUMMARY = "Lecture(GET) d'une resource à base d'un chemin utilisateur déjà fixé en mémoire."
RESPONSE_DESCRIPTION = """Lecture des données depuis l'URL de chargement des données."""

@app.get(
    path=Routes.LOADING_DATA,
    tags=[Tags.LOADING_DATA],
    summary=SUMMARY,
    response_description=RESPONSE_DESCRIPTION,
    name="read_loading_data")
def read_data() -> JSONResponse:
    """Le chemin du fichier envoyé par l'utilisateur pour le chargement
    de données est relu en mémoire et est utilisé par le endpoint
    pour renvoyer en retour une réponse au format JSON.

    Returns:
        JSONResponse: Une réponse JSON contenant un message est retourné.
    """

    # Vérifier si la data_frame fixée en mémoire est présent.
    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, la convertire dans un dictionnaire python.
    dict_object = app.state.data_frame.to_dict(orient="records")

    # Puis retourner le rendu sous forme d'une réponse JSON au frontend.
    return JSONResponse(content=jsonable_encoder(dict_object))

# DELETE ROUTER (DELETE)

@app.delete(
    path=Routes.LOADING_DATA,
    tags=[Tags.LOADING_DATA],
    summary="Suppression de la route.",
    name="delete_loading_data")
def delete_data() -> JSONResponse:
    """Supprimer les données sur (`http://127.0.0.1:8000/v_01/data/`).

    Returns:
        JSONResponse: Un objet au format JSON contenant un message et un code lié à ce message.
    """

    # Vérifier si la data_frame fixée en mémoire est présent.
    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, supprimer les colonnes.
    app.state.data_frame.drop(columns=[col for col in app.state.data_frame.columns], inplace=True)
    app.state.data_frame = None

    return JSONResponse(content={"message": "Données supprimées avec succès."})

# UPDATE ROUTER (UPDATE)
# PATCH ROUTER (PATCH)

# -----------------------------------------------

# CRUD OF ANALYSE OF DATA LOADING
# CREATE ROUTER (POST)

SUMMARY="""Création des informations d'analyses des données chargé."""

@app.post(
    path=Routes.ANALYSE_DATA,
    tags=[Tags.ANALYSE_DATA],
    summary=SUMMARY,
    name="create_analyse_infos")
def send_data_analyse() -> JSONResponse:
    """Une fois les données chargées, une analyse de ces derniers est
    faite automatiquement pour l'utilisateur.

    Returns:
        JSONResponse: Un objet au format JSON est retourné.
    """

    if app.state.data_frame is None:
        return JSONResponse(
            content={"Error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Nettoyer les données invalides pour JSON.
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=app.state.data_frame)

    # Résumer des données
    dict_object = chargeur_analyse.summarize(df)

    return JSONResponse(
        content=jsonable_encoder(dict_object),
        status_code=status.HTTP_201_CREATED)

# # READ ROUTER (GET)

SUMMARY="""Lecture des informations d'analyses des données chargé."""
RESPONSE_DESCRIPTION="""Les informations des données chargées sont lu avec succès."""

@app.get(
    path=Routes.ANALYSE_DATA,
    tags=[Tags.ANALYSE_DATA],
    summary=SUMMARY,
    response_description=RESPONSE_DESCRIPTION,
    name="read_analyse_infos")
def read_data_analyse() -> JSONResponse:
    """L'analyse étant faite, les informations de l'analyse sont retournées à l'utilisateur.

    Returns:
        JSONResponse: Un objet au format JSON est retourné.
    """

    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Nettoyer les données invalides pour JSON.
    df =  chargeur_clean_df_for_json.clean_dataframe_for_json(df=app.state.data_frame)

    # Résumer des données
    dict_object = chargeur_analyse.summarize(df)

    return JSONResponse(content=jsonable_encoder(dict_object))

# # DELETE ROUTER (DELETE)

SUMMARY="""Suppression des informations d'analyses des données chargé."""

@app.delete(
    path=Routes.ANALYSE_DATA,
    tags=[Tags.ANALYSE_DATA],
    summary=SUMMARY,
    name="delete_analyse_infos")
def delete_data_analyse() -> JSONResponse:
    """Après l'avoir créer et lu, les informations peuvent être supprimer sur cette route.

    Returns:
        JSONResponse: Une réponse JSON est retournée avec un message.
    """

    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    app.state.data_frame = None

    return JSONResponse(content={"message": "Données supprimées avec succès."})

# UPDATE ROUTER (UPDATE)
# PATCH ROUTER (PATCH)

# ---------------------- CRUD OF VISUALIZATION 2D ----------------------
# CREATE VISULIZATION (POST)

SUMMARY="""Créations de la visualisation graphique en 2 dimension des colonnes numérique."""

@app.post(
    path=Routes.VISUALISATION_2D,
    tags=[Tags.VISUALISATION_2D],
    summary=SUMMARY,
    name="create_2d_visualisation")
def post_data_visualisation_2d(payload: BuildGraphic2DSlot) -> JSONResponse:
    """Mise en place de la visualisation 2D dans un dossier local après analyse.
    - Seul les colonnes numérique sélectionnées par l'utilisateur
    seront utilisées pour construire le graphique.

    Returns:
        JSONResponse: Une réponse JSON est retourné avec un message et un code lié à ce message.
    """

    # Lire le chemin du répertoire devant contenir les vues graphique,
    # puis changer les back-slache en slashe s'il existe.
    if "\\" in payload.folder_path:
        payload.folder_path = "/".join(payload.folder_path.split("\\"))

    # Vérifier si le répertoire existe sur le disque ou en mémoire.
    try:
        if not Path(payload.folder_path).is_dir():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dossier introuvable")
    except FileNotFoundError as fnfe:
        fnfe.add_note("\nVeuillez entrer le chemin d'un dossier du disque.\n")
        raise

    # Ainsi que les colonnes numérique des données à visualiser dans une liste.
    visualize_column = list(payload.visualize_column.keys())

    # Vérifier si le chemin du fichier des données ayant permit le chargement existe en mémoire.
    if app.state.file_path is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, lire le chemin.
    file_path: Path = app.state.file_path
    file_name = file_path.stem

    # Vérifier si les données à chargées existent en mémoire.
    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, les lire.
    df = app.state.data_frame

    # Stocké en mémoire le chemin du répertoire devant contenir les vues graphiques.
    app.state.folder_path = Path(payload.folder_path)

    # Instancier la classe de visualisation graphique en 2 dimensions.
    chargeur_visualisation_2d = Visualisation2D(
        axes=2,
        df=df[visualize_column],
        color_col=None,
        graphic_vue_folder=payload.folder_path,
        file_name=file_name)

    # Puis construire le graphique avec la méthode dédié.
    chargeur_visualisation_2d.visualisation_automatique()

    # Un message est retourné après la création de la vue graphique.
    return JSONResponse(
        content={
            "message":"Visualisation est crée avec succès."},
        status_code=status.HTTP_201_CREATED)

# READ VISUALIZATION (GET)

SUMMARY="""Lecture de la visualisation graphique en 2 dimension des colonnes numérique."""

@app.get(
    path=Routes.VISUALISATION_2D,
    tags=[Tags.VISUALISATION_2D],
    summary=SUMMARY,
    name="read_2d_visualisation")
def get_data_visualisation_2d(
    html_file_s: Annotated[
        ReadGraphic2DSlot,
        Query(
            title="html_file_s is query parameter.",
            description="""This parameter allowed to read one
            HTML file or all files that represent the graphic
            vue file generate by plotly library.""")]) -> Any:
    """Lecture d'un fichier ou de tous les vues 2D depuis un dossier local.
    L'utilisateur peut visualiser les colonnes numériques crées en 2 dimensions via cette route.

    Returns:
        ReadGraphic2DSlot: Cette classe prend le chemin d'un emplacement local
        où lire les graphiques qui sont générées, le status de l'action de lecture
        ainsi qu'un message d'une telle action.
    """

    # Il faut vérifier si le répertoire devant contenir les vues graphiques existe.
    if app.state.folder_path is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Aucune donnée chargée"}
        )

    # S'il exite, se rendre dans le sous répertoire des graphiques en 2 dimensions.
    html_dir = app.state.folder_path / "2D"

    # Puis vérifier si ce sous-répertoire existe.
    if not html_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier ou fichier introuvable."
        )

    # S'il existe, alors lire les fichiers HTML dans une liste.
    html_files = [f.name for f in html_dir.glob("*.html")]

    # S'il n'y a pas de fichier HTML alors lever une exception au client.
    if not html_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune vue graphique à visualiser."
        )

    # Si le nom d'un fichier HTML est donné.
    if html_file_s.html_file:
        # Supprimer les appostrophes.
        html_file_s.html_file = html_file_s.html_file[1 : len(html_file_s.html_file) - 1]
        # Vérifier si le nom du fichier existe dans la liste des fichiers HTML.
        if html_file_s.html_file in html_files:
            # Si oui, alors renvoyer le fichier correspondant.
            return JSONResponse(
                content=jsonable_encoder(html_file_s))
        else :
            # Sinon lever une exception au client.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Le fichier {html_file_s.html_file} est introuvable."
            )
    # Si aucun nom de fichier n'est donné alors retourné l'ensemble des vues graphiques présent.
    return JSONResponse(
        content=jsonable_encoder(
            ReadGraphic2DSlot(
                html_files=[str(Path(f)) for f in html_dir.glob("*.html")])))


# ---------------------- CRUD OF VISUALIZATION 3D----------------------
# CREATE 3D VISULIZATION (POST)

SUMMARY="""Créations de la visualisation graphique en 3 dimension des colonnes numérique."""

@app.post(
    path=Routes.VISUALISATION_3D,
    tags=[Tags.VISUALISATION_3D],
    summary=SUMMARY,
    name="create_3d_visualisation")
def post_data_visualisation_3d(payload: BuildGraphic3DSlot) -> Any:
    """Mise en place de la visualisation 3D après analyse.
    L'utilisateur peut sélectionner les colonnes numériques à visualiser en
    3 dimensions via cette route.
    Returns:
        None: Rien n'est retourné sur le serveur.
    """

    # Lire le chemin du répertoire devant contenir les vues graphique,
    # puis changer les back-slache en slashe s'il existe.
    if "\\" in payload.folder_path:
        payload.folder_path = "/".join(payload.folder_path.split("\\"))

    # Vérifier si le répertoire existe sur le disque ou en mémoire.
    try:
        if not Path(payload.folder_path).is_dir():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dossier introuvable")
    except FileNotFoundError as fnfe:
        fnfe.add_note("\nVeuillez entrer le chemin d'un dossier du disque.\n")
        raise

    # Ainsi que les colonnes numérique des données à visualiser dans une liste.
    visualize_column = list(payload.visualize_col.keys())

    # Vérifier si le chemin du fichier des données ayant permit le chargement existe en mémoire.
    if app.state.file_path is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, lire le chemin.
    file_path: Path = app.state.file_path
    file_name = file_path.stem

    # Vérifier si les données à chargées existent en mémoire.
    if app.state.data_frame is None:
        return JSONResponse(
            content={"error": "Aucune donnée chargée"},
            status_code=status.HTTP_404_NOT_FOUND)

    # Si oui, les lire.
    df = app.state.data_frame

    # Stocké en mémoire le chemin du répertoire devant contenir les vues graphiques.
    app.state.folder_path = Path(payload.folder_path)

    # Instancier la classe de visualisation graphique en 3 dimensions.
    chargeur_visualisation_3d = Visualisation3D(
        axes=3,
        df=df[visualize_column],
        color_col=None,
        graphic_vue_folder=payload.folder_path,
        file_name=file_name)

    # Puis construire le graphique avec la méthode dédié.
    chargeur_visualisation_3d.visualisation_automatique()

    # Un message est retourné après la création de la vue graphique.
    return JSONResponse(
        content={"message":"Visualisation est crée avec succès."},
        status_code=status.HTTP_201_CREATED)

# READ 3D VISUALIZATION (GET)

SUMMARY="""Lecture de la visualisation graphique en 3 dimension des colonnes numérique."""

@app.get(
    path=Routes.VISUALISATION_3D,
    tags=[Tags.VISUALISATION_3D],
    summary=SUMMARY,
    name="read_3d_visualisation")
def read_data_visualisation_3d(
    html_file_s: Annotated[
        ReadGraphic3DSlot,
        Query(
            title="html_file_s is query parameter.",
            description="""This parameter allowed to read one
            HTML file or all files that represent the graphic
            vue file generate by plotly library.""")]) -> Any:
    """Mise en place de la visualisation 3D après analyse.
    L'utilisateur peut visualiser les colonnes numériques crées en 3 dimensions via cette route.
    Returns:
        None: Un emplacement où est stocké les vues graphique générées est retourné.
    """
    # Il faut vérifier si le répertoire devant contenir les vues graphiques existe.
    if app.state.folder_path is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Aucune donnée chargée"}
        )

    # S'il exite, se rendre dans le sous répertoire des graphiques en 2 dimensions.
    html_dir = app.state.folder_path / "3D"

    # Puis vérifier si ce sous-répertoire existe.
    if not html_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dossier ou fichier introuvable."
        )

    # S'il existe, alors lire les fichiers HTML dans une liste.
    html_files = [f.name for f in html_dir.glob("*.html")]

    # S'il n'y a pas de fichier HTML alors lever une exception au client.
    if not html_files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucune vue graphique à visualiser."
        )

    # Si le nom d'un fichier HTML est donné.
    if html_file_s.html_file:
        # Supprimer les appostrophes.
        html_file_s.html_file = html_file_s.html_file[1 : len(html_file_s.html_file) - 1]
        # Vérifier si le nom du fichier existe dans la liste des fichiers HTML.
        if html_file_s.html_file in html_files:
            # Si oui, alors renvoyer le fichier correspondant.
            return html_file_s
        else :
            # Sinon lever une exception au client.
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"Le fichier {html_file_s.html_file} est introuvable."
            )
    # Si aucun nom de fichier n'est donné alors retourné l'ensemble des vues graphiques présent.
    return ReadGraphic3DSlot(html_files=html_files)
