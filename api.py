# api.py

# --- Importations des bibliothèques de base ---
from enum import Enum
from typing_extensions import Literal
from fastapi import Body, FastAPI, HTTPException, Response, File, UploadFile, Form, Depends

from fastapi.responses import FileResponse
#from matplotlib.pylab import Literal
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Union
import io
import pandas as pd
import json
import base64
import markdown
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import os # Pour la gestion du chemin dans les fonctions utilitaires

# Importez toutes vos classes et fonctions de vos modules
from packages.modules.loading import DataLoader
from packages.modules.netoyage import handle_missing_values # Note: Il y a une faute de frappe dans le nom du module "netoyage" -> "nettoyage"
from packages.modules.analysis import preprocess_for_reduction
from packages.modules.methode_acp import MethodePCA
from packages.modules.visualisation_image import ImageVisualizer
from packages.modules.visualisation_texte import TextVisualizer
from packages.modules.visualisation_csv import TabularVisualizer
from packages.modules.methode_tsne import TSNEVisualizer
from packages.modules.methode_umap import UMAPVisualizer

from fastapi.responses import HTMLResponse

# --- Modèles de Données Pydantic ---
# Ces modèles définissent la structure des données attendues en entrée (requêtes)
# et des données renvoyées en sortie (réponses). Ils sont cruciaux pour la validation
# automatique et la documentation de l'API.

# Les Enums permettent de limiter les valeurs possibles pour un paramètre.
class ReductionMethod(str, Enum):
    acp = "acp"
    umap = "umap"
    tsne = "tsne"

class TabularVizType(str, Enum):
    distributions = "distributions"
    correlations = "correlations"

class ImageVizType(str, Enum):
    image = "image"
    histogramme = "histogramme"

# Modèle de réponse standard pour les endpoints de visualisation.
class VisualisationResponse(BaseModel):
    status: str = "success"
    graph_type: str
    title: str
    image_data: str
    message: Optional[str] = None
    
# --- Modèles pour la Réduction de Dimension ---
# L'utilisation de `Union` avec des modèles ayant un champ `Literal` est une
# technique puissante de FastAPI/Pydantic. Elle permet de créer un "schéma JSON"
# dynamique où les champs disponibles dépendent de la valeur d'un autre champ (ici, "methode").

class BaseReductionParams(BaseModel):
    """Paramètres communs à toutes les méthodes de réduction."""
    n_components: int = Field(2, ge=2, le=3 , description="Nombre de dimensions de sortie (2 ou 3).")
    color_by_col: Optional[str] = Field(None, description="Nom de la colonne à utiliser pour colorer les points.")

class PCAParams(BaseReductionParams):
    methode: Literal[ReductionMethod.acp]

class UMAPParams(BaseReductionParams):
    methode: Literal[ReductionMethod.umap]
    n_neighbors: Optional[int] = Field(15, ge=2, description="[UMAP] Nombre de voisins à considérer pour la construction du graphe.")
    min_dist: Optional[float] = Field(0.1, ge=0.0, description="[UMAP] Distance minimale entre les points dans l'espace de faible dimension.")

class TSNEParams(BaseReductionParams):
    methode: Literal[ReductionMethod.tsne]
    perplexity: Optional[int] = Field(30, ge=1, description="[t-SNE] Perplexité. Liée au nombre de voisins les plus proches considérés pour chaque point.")


# Union des différents modèles de paramètres. FastAPI s'en servira pour créer une sélection dynamique dans l'UI.
# C'est ce qui permet à l'utilisateur de choisir "acp", "umap" ou "tsne" et de voir les paramètres correspondants.
ReductionParams = Union[PCAParams, UMAPParams, TSNEParams]

class ReductionResponse(BaseModel):
    """
    Réponse de l'endpoint de réduction de dimension.
    Inclut l'image du graphique et les données projetées.
    """
    status: str = "success"
    message: Optional[str] = None
    image_data: str # L'image encodée
    reduced_data: List[Dict[str, Any]] # Les données réduites en JSON

# --- Modèles pour le Pipeline d'Analyse Complet ---

class DataSource(BaseModel):
    """Définit la source des données pour le pipeline d'analyse."""
    donnees_brutes: Optional[List[Dict[str, Any]]] = Field(None, description="Données directement fournies en JSON (tableau d'objets).")
    chemin_fichier: Optional[str] = Field(None, description="Chemin vers un fichier de données sur le serveur.")
    contenu_base64: Optional[str] = Field(None, description="Contenu d'un fichier (CSV/Excel) encodé en Base64.")
    nom_fichier: Optional[str] = Field(None, description="Nom du fichier (ex: 'data.csv') si contenu_base64 est utilisé, pour déterminer le type.")

    # Validation pour s'assurer qu'une seule source est fournie
    @field_validator('chemin_fichier', mode="before")
    def unique_source_check(cls, v, values):
        sources_provided = sum([
            'donnees_brutes' in values and values['donnees_brutes'] is not None,
            v is not None,
            'contenu_base64' in values and values['contenu_base64'] is not None
        ])
        if sources_provided != 1:
            raise ValueError("Veuillez fournir une et une seule source de données: 'donnees_brutes', 'chemin_fichier', ou 'contenu_base64'.")
        return v

class CleaningParams(BaseModel):
    """Paramètres pour l'étape de nettoyage."""
    supprimer_lignes_na: bool = Field(False, description="Si vrai, supprime toutes les lignes contenant au moins une valeur manquante.")
    supprimer_doublons: bool = Field(False, description="Si vrai, supprime les lignes dupliquées.")
    strategie_imputation: Optional[Literal['mean', 'median', 'fill']] = Field(None, description="Stratégie pour imputer les valeurs manquantes restantes (après suppressions).")
    colonnes_imputation: Optional[Union[str, List[str]]] = Field(None, description="Colonne(s) sur lesquelles appliquer l'imputation. Si non spécifié, s'applique aux colonnes numériques.")

class AnalysisPipelineRequest(BaseModel):
    """Modèle complet pour la requête du pipeline d'analyse et de visualisation."""
    source_donnees: DataSource
    parametres_reduction: ReductionParams = Field(..., discriminator="methode")
    parametres_nettoyage: Optional[CleaningParams] = None
class CleaningResponse(BaseModel):
    """Réponse de l'endpoint de nettoyage."""
    status: str = "success"
    message: str
    cleaned_data: List[Dict[str, Any]]
# --- Fonctions Utilitaires & Dépendances FastAPI ---
def fig_to_base64(fig) -> str:
    """
    Convertit une figure Matplotlib ou Plotly en une chaîne de caractères Base64.
    Cela permet d'intégrer l'image directement dans une réponse JSON, que le client
    (ex: un navigateur web) pourra ensuite décoder et afficher.
    """
    buf = io.BytesIO()
    if hasattr(fig, "write_image"):  # Plotly
        fig.write_image(buf, format="png")
    else:  # Matplotlib
        fig.savefig(buf, format="png")
        plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_dataframe_from_file(file: UploadFile):
    """
    Fonction d'aide pour charger un DataFrame depuis un objet UploadFile en mémoire.
    Elle gère différents formats de fichiers tabulaires (CSV, Excel).
    """
    # Utiliser 'with' garantit que le fichier est fermé même en cas d'erreur.
    with file.file as f:
        if file.filename.endswith('.csv'):
            # La lecture directe depuis le file-like object est plus efficace
            return pd.read_csv(io.StringIO(f.read().decode('utf-8')))
        elif file.filename.endswith(('.xls', '.xlsx')):
            return pd.read_excel(f)
        else:
            raise HTTPException(status_code=400, detail="Type de fichier non supporté. Veuillez téléverser un fichier CSV ou Excel.")

def get_data_source(
    chemin_fichier: Optional[str] = None,
    donnees_json: Optional[str] = None,
    file: Optional[UploadFile] = None
):
    """
    Dépendance FastAPI pour centraliser la logique de chargement des données tabulaires.
    Elle garantit qu'une seule source de données est fournie et la transforme en DataFrame Pandas.
    L'utiliser avec `Depends(get_data_source)` dans les endpoints évite la duplication de code.
    """
    # S'assurer qu'une et une seule source de données est fournie.
    if sum([bool(chemin_fichier), bool(donnees_json), bool(file)]) != 1:
        raise HTTPException(status_code=400, detail="Veuillez fournir une et une seule source de données: 'chemin_fichier', 'donnees_json' ou 'file'.")
    
    # Charger les données en fonction de la source fournie.
    if file:
        return get_dataframe_from_file(file)
    
    elif chemin_fichier:
        try:
            loader = DataLoader()
            return loader.load(chemin_fichier)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Fichier non trouvé à l'adresse: {chemin_fichier}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors du chargement des données: {str(e)}")
    
    else: # donnees_json
        try:
            data = json.loads(donnees_json)
            return pd.DataFrame(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur lors du décodage du JSON : {e}")

def get_image_visualizer(
    chemin_fichier: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
) -> ImageVisualizer:
    """
    Dépendance FastAPI pour charger une image (depuis un chemin ou un upload)
    et retourner une instance prête à l'emploi de la classe `ImageVisualizer`.
    """
    # Valider qu'au moins une source est fournie, mais pas les deux.
    if not any([chemin_fichier, file]):
        raise HTTPException(status_code=400, detail="Veuillez fournir une source d'image : 'chemin_fichier' ou 'file'.")
    
    # On ne peut fournir qu'une seule source
    if all([chemin_fichier, file]):
        raise HTTPException(status_code=400, detail="Veuillez fournir 'chemin_fichier' OU 'file', mais pas les deux.")

    try:
        # Charger l'image dans l'objet visualiseur en fonction de la source.
        visualiseur = ImageVisualizer()
        if file:
            if not file.content_type or not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Le fichier téléversé n'est pas une image valide.")
            with file.file as f:
                visualiseur.load_image_from_object(f)
        else: # chemin_fichier doit exister
            visualiseur.load_image_from_path(chemin_fichier)
        return visualiseur
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement de l'image: {e}")

def get_dataframe_from_source_model(source: 'DataSource') -> pd.DataFrame:
    """
    Charge un DataFrame Pandas à partir du modèle Pydantic DataSource.
    """
    if source.donnees_brutes:
        return pd.DataFrame(source.donnees_brutes)
    
    if source.chemin_fichier:
        try:
            loader = DataLoader()
            return loader.load(source.chemin_fichier)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Fichier non trouvé: {source.chemin_fichier}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur de chargement: {e}")

    if source.contenu_base64:
        if not source.nom_fichier:
            raise HTTPException(status_code=400, detail="Le 'nom_fichier' est requis avec 'contenu_base64'.")
        try:
            decoded_content = base64.b64decode(source.contenu_base64)
            # Simuler un UploadFile pour réutiliser la logique existante
            fake_upload_file = UploadFile(filename=source.nom_fichier, file=io.BytesIO(decoded_content))
            return get_dataframe_from_file(fake_upload_file)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur lors du décodage ou de la lecture du contenu Base64: {e}")

    raise HTTPException(status_code=400, detail="Aucune source de données valide n'a été fournie.")

def execute_reduction(params: ReductionParams, df_data: pd.DataFrame) -> tuple[Any, pd.DataFrame]:
    """
    Fonction d'aide qui exécute la logique de réduction de dimension et retourne la figure et le dataframe réduit.
    Factorise le code commun entre les endpoints /reduire-dimension et /analyser-et-visualiser.
    """
    fig = None
    reduced_df = None

    if isinstance(params, PCAParams):
        df_processed = preprocess_for_reduction(df_data)
        instance = MethodePCA(n_components=params.n_components)
        fig, reduced_df = instance.visualize(df_processed, color_by_col=params.color_by_col, original_df=df_data)
    
    elif isinstance(params, UMAPParams):
        instance = UMAPVisualizer(df_data)
        fig, reduced_df = instance.visualize(n_components=params.n_components, color_by_col=params.color_by_col, n_neighbors=params.n_neighbors, min_dist=params.min_dist)
    
    elif isinstance(params, TSNEParams):
        instance = TSNEVisualizer(df_data)
        fig, reduced_df = instance.visualize(n_components=params.n_components, color_by_col=params.color_by_col, perplexity=params.perplexity)

    if fig is None or reduced_df is None:
        # Utiliser RuntimeError car c'est une erreur de logique interne, qui sera attrapée par le try/except de l'endpoint.
        raise RuntimeError(f"La réduction de dimension avec {params.methode} a échoué à produire un résultat.")

    return fig, reduced_df


# --- Initialisation de l'Application FastAPI ---
app = FastAPI(
    title="API de Visualisation et d'Analyse de Données",
    description="Une API pour charger, analyser et visualiser différents types de données. La plupart des endpoints acceptent une source de données via un chemin de fichier, une chaîne JSON ou un téléversement.",
    version="1.0.0"
)


async def favicon():
    return FileResponse("favicon.ico")

@app.get("/api-documentation", response_class=HTMLResponse, tags=["Documentation"], summary="Documentation complète du projet")
def get_api_documentation():
    """
    Affiche la documentation complète de l'API (html).
    """
    try:
        with open("doc_api.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # Convertir le Markdown en HTML
        html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
        
        # Ajouter un style CSS pour une meilleure lisibilité
        styled_html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Documentation de l'API</title>
                <link rel="icon" href="/favicon.ico" type="image/x-icon">
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                        line-height: 1.6;
                        padding: 20px 40px;
                        max-width: 900px;
                        margin: 20px auto;
                        color: #333;
                        background-color: #fff;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                    }}
                    h1, h2, h3 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
                    code {{ background-color: #f6f8fa; padding: 0.2em 0.4em; margin: 0; font-size: 85%; border-radius: 3px; }}
                    pre {{ background-color: #f6f8fa; padding: 16px; overflow: auto; border-radius: 3px; }}
                    table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """
        return HTMLResponse(content=styled_html)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Le fichier de documentation 'doc_api.md' n'a pas été trouvé.")

# --- Endpoints ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    return """
    <html>
        <head>
            <title>VISUALDATA API</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #f9f9f9; }
                h1 { color: #2c3e50; }
                p { font-size: 18px; color: #555; }
                .btn {
                    display: inline-block;
                    margin: 10px;
                    padding: 12px 25px;
                    font-size: 16px;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    transition: 0.3s;
                }
                .swagger { background-color: #3498db; }
                .swagger:hover { background-color: #2980b9; }
                .redoc { background-color: #27ae60; }
                .redoc:hover { background-color: #1e8449; }
            </style>
            <link rel="icon" href="/favicon.ico" type="image/x-icon">
        </head>
        <body>
            <h1>🚀 Bienvenue sur l API de VisualData</h1>
            <p>Cette API permet la réduction et la visualisation de données.</p>
        
            <h2>📌 Endpoints principaux :</h2>
            <ul>
                <li><code>/analyser-et-visualiser/</code> – Pipeline complet d'analyse</li>
                <li><code>/reduire-dimension/</code> – Réduction de dimension</li>
                <li><code>/visualiser/image</code> – Visualisation d'une image</li>
                <li><code>/visualiser/text</code> – Visualisation de texte</li>
            </ul>
            <p>Sélectionne une documentation interactive 💡⚡ :</p>
            <a href="/docs" class="btn swagger">📘 Swagger UI</a>
            <a href="/redoc" class="btn redoc">📗 ReDoc</a>
            <a href="/api-documentation" class="btn redoc" style="background-color: #f39c12;">📙 Documentation et utilisation de l API</a>

            </body>
    </html>
    """


@app.get("/Accueil")
def bienvenue():
    """Endpoint de bienvenue simple pour vérifier que l'API est en ligne."""
    return {"Bienvenue sur l'API d'Analyse et de Visualisation de Données. Accédez à /docs pour la documentation interactive."}


@app.post("/nettoyer-donnees/", summary="Nettoie un jeu de données", tags=["Nettoyage"], response_model=CleaningResponse)
def nettoyer_donnees(
    params: CleaningParams,
    df_data: pd.DataFrame = Depends(get_data_source)
) -> CleaningResponse:
    """
    Applique différentes étapes de nettoyage à un jeu de données.
    - Supprime les lignes dupliquées.
    - Supprime les lignes avec des valeurs manquantes.
    - Impute les valeurs manquantes restantes.
    """
    initial_rows = len(df_data)
    df_nettoye = df_data.copy()
    messages = []

    # Appliquer les suppressions en premier
    if params.supprimer_doublons:
        rows_before = len(df_nettoye)
        df_nettoye.drop_duplicates(inplace=True)
        rows_after = len(df_nettoye)
        messages.append(f"{rows_before - rows_after} lignes dupliquées supprimées.")

    if params.supprimer_lignes_na:
        rows_before = len(df_nettoye)
        df_nettoye.dropna(inplace=True)
        rows_after = len(df_nettoye)
        messages.append(f"{rows_before - rows_after} lignes avec NA supprimées.")

    # Appliquer l'imputation ensuite, si une stratégie est définie
    if params.strategie_imputation:
        df_nettoye = handle_missing_values(df_nettoye, params.strategie_imputation, params.colonnes_imputation)
        messages.append(f"Imputation appliquée avec la stratégie '{params.strategie_imputation}'.")

    final_message = "Nettoyage terminé. " + " ".join(messages) if messages else "Aucune opération de nettoyage effectuée."
    return CleaningResponse(message=final_message, cleaned_data=df_nettoye.to_dict(orient="records"))


@app.post("/visualiser/tabulaire/", summary="Visualisation de données tabulaires", tags=["Visualisation"])
def visualiser_tabulaire(
    type_graphique: TabularVizType = Form(..., description="Type de graphique à générer."),
    df_data: pd.DataFrame = Depends(get_data_source)
) -> VisualisationResponse:
    """Génère des visualisations pour des données tabulaires."""
    # Instancier le visualiseur avec les données chargées par la dépendance.
    visualiseur = TabularVisualizer(df_data)
    
    if type_graphique == TabularVizType.distributions:
        figures = visualiseur.plot_distributions(return_fig=True)

    elif type_graphique == TabularVizType.correlations:
        figures = visualiseur.plot_correlations(return_fig=True)
    else:
        raise HTTPException(status_code=400, detail=f"Type de graphique non supporté : {type_graphique}")
        
    if not figures:
        raise HTTPException(status_code=404, detail="Aucun graphique n'a pu être généré.")

    # plot_correlations peut retourner 2 figures (heatmap et pairplot)
    # On choisit la première (heatmap) qui est la plus commune et la moins lourde.
    fig = figures[0]
    return VisualisationResponse(
        graph_type=type_graphique.value,
        title=f"Visualisation tabulaire: {type_graphique.value}",
        image_data=fig_to_base64(fig)
    )


@app.post("/visualiser/image/", summary="Affiche une image ou son histogramme", tags=["Visualisation"])
def visualiser_image_endpoint(
    type_visualisation: ImageVizType = Form("image", description="Type de visualisation à générer pour l'image."),
    visualiseur: ImageVisualizer = Depends(get_image_visualizer)
) -> VisualisationResponse:
    """
    Génère une visualisation pour une image (affichage simple ou histogramme d'intensité)
    à partir d'un chemin de fichier local ou d'un fichier téléversé.
    """
    try:
        # Appeler la méthode de visualisation appropriée en fonction du paramètre.
        if type_visualisation == ImageVizType.image:
            fig = visualiseur.show_image(title="Image originale", retourner_fig=True)
            title = "Affichage de l'image"
        elif type_visualisation == ImageVizType.histogramme:
            fig = visualiseur.histogram_intensity(retourner_fig=True)
            title = "Histogramme des intensités"
        else:
            # Ce cas ne devrait pas arriver grâce à l'Enum, mais c'est une bonne pratique
            raise HTTPException(status_code=400, detail="Type de visualisation non valide.")

        return VisualisationResponse(
            graph_type=type_visualisation.value,
            title=title,
            image_data=fig_to_base64(fig)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération de la visualisation: {e}")


@app.post("/visualiser/texte/nuage-de-mots/", summary="Génère un nuage de mots", tags=["Visualisation"])
def visualiser_texte_nuage_de_mots(
    chemin_fichier: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
) -> VisualisationResponse:
    """Génère un nuage de mots à partir d'un fichier texte."""
    if not any([chemin_fichier, file]):
        raise HTTPException(status_code=400, detail="Veuillez fournir une source de données.")

    try:
        # Charger le contenu texte soit depuis le fichier téléversé, soit depuis un chemin.
        if file:
            with file.file as f:
                if file.content_type != "text/plain":
                    raise HTTPException(status_code=400, detail="Veuillez téléverser un fichier .txt.")
                donnees_texte = f.read().decode("utf-8")
        else:
            loader = DataLoader()
            donnees_texte = loader.load(chemin_fichier, file_type='txt')
        
        # Utiliser le visualiseur de texte pour générer le nuage de mots.
        visualiseur = TextVisualizer(donnees_texte)
        fig = visualiseur.generate_wordcloud(return_fig=True)
        return VisualisationResponse(
            graph_type="word_cloud",
            title="Nuage de mots",
            image_data=fig_to_base64(fig)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

DEFAULT_PARAMS_JSON = json.dumps({
    "methode": "acp",
    "n_components": 2,
    "color_by_col": "target"#, valeur par défaut courante(target qui signifie la cible dans les datasets de classification)
})

@app.post("/reduire-dimension/", summary="Réduction de dimension", tags=["Réduction de dimension"], response_model=ReductionResponse)
def reduire_dimension(
    params_json: str = Form(DEFAULT_PARAMS_JSON, description="Paramètres de réduction au format json"),
    df_data: pd.DataFrame = Depends(get_data_source)
) -> ReductionResponse:

    """
    Génère un graphique de réduction de dimension avec la méthode spécifiée (ACP, UMAP ou t-SNE).
    
    - **acp**: Analyse en Composantes Principales. Rapide et efficace pour les relations linéaires.
    - **umap**: Uniform Manifold Approximation and Projection. Excellent pour la visualisation de clusters, préserve bien la structure globale.
    - **tsne**: t-distributed Stochastic Neighbor Embedding. Très bon pour visualiser des groupes bien séparés, mais peut mal préserver la structure globale.
    """
    # Désérialiser la chaîne JSON en dictionnaire
    try:
        params_dict = json.loads(params_json)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Erreur de décodage JSON: {str(e)}")

    # Valider et instancier le bon modèle de paramètres selon la clé discriminante 'methode'.
    # Pydantic ne permet pas d'instancier directement un typing.Union via Union(**dict).
    # Nous choisissons ici une approche explicite: regarder la valeur de 'methode' et construire
    # l'instance du modèle correspondant. Cela fonctionne avec Pydantic v1 et v2.
    try:
        methode_val = params_dict.get("methode")
        if methode_val is None:
            raise ValueError("Le champ 'methode' est requis dans les paramètres de réduction.")

        methode_str = str(methode_val).lower()
        if methode_str == ReductionMethod.acp.value:
            params = PCAParams(**params_dict)
        elif methode_str == ReductionMethod.umap.value:
            params = UMAPParams(**params_dict)
        elif methode_str == ReductionMethod.tsne.value:
            params = TSNEParams(**params_dict)
        else:
            raise ValueError(f"Méthode inconnue: {methode_val}. Valeurs possibles: acp, umap, tsne")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erreur de validation des paramètres: {str(e)}")
    except Exception as e:
        # Renvoyer une erreur 400 pour la validation pydantic
        raise HTTPException(status_code=400, detail=f"Erreur de validation des paramètres: {str(e)}")

    # Exécuter la réduction
    try:
        fig, reduced_df = execute_reduction(params, df_data)
    except HTTPException:
        # Propager les HTTPException levées plus haut
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la réduction de dimension: {str(e)}")

    # Vérifier que la visualisation a bien produit une figure et des données.
    if fig is None:
         raise HTTPException(status_code=500, detail="La figure n'a pas pu être générée.")
    if reduced_df is None:
         raise HTTPException(status_code=500, detail="Les données réduites n'ont pas pu être générées.")

    return ReductionResponse(
        # La réponse inclut l'image et les données réduites.
        message=f"Réduction de dimension via {params.methode.upper()} réussie.",
        image_data=fig_to_base64(fig),
        reduced_data=reduced_df.to_dict(orient="records")
    )
    

@app.post("/analyser-et-visualiser/", summary="Pipeline complet: Nettoyage et Réduction", tags=["Pipeline"], response_model=ReductionResponse)
def analyser_et_visualiser_donnees(
    request: AnalysisPipelineRequest
) -> ReductionResponse:
    """
    Exécute un pipeline complet : chargement, nettoyage (optionnel) et réduction de dimension.
    Toute la configuration est passée dans un unique corps de requête JSON.
    """
    try:
        # 1. Chargement des données
        df_data = get_dataframe_from_source_model(request.source_donnees)

        # 2. Nettoyage optionnel
        if request.parametres_nettoyage:
            p_nettoyage = request.parametres_nettoyage
            if p_nettoyage.supprimer_doublons:
                # Il est important de réaligner les index après des suppressions si la coloration doit être correcte.
                df_data.drop_duplicates(inplace=True)
            if p_nettoyage.supprimer_lignes_na:
                df_data.dropna(inplace=True)

            if p_nettoyage.strategie_imputation:
                df_data = handle_missing_values(df_data, strategy=p_nettoyage.strategie_imputation, columns=p_nettoyage.colonnes_imputation)

            # Après avoir potentiellement supprimé des lignes, réinitialiser l'index est une bonne pratique pour éviter les problèmes d'alignement.
            df_data.reset_index(drop=True, inplace=True)

        # 3. Réduction de dimension (logique similaire à /reduire-dimension/)
        params = request.parametres_reduction
        # Appeler la même fonction d'aide avec le dataframe potentiellement nettoyé
        fig, reduced_df = execute_reduction(params, df_data)

        return ReductionResponse(
            message=f"Pipeline complet avec {params.methode.upper()} réussi.",
            image_data=fig_to_base64(fig),
            reduced_data=reduced_df.to_dict(orient="records")
        )
    except HTTPException as e:
        raise e # Re-lever les exceptions HTTP déjà formatées
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'exécution du pipeline: {str(e)}")
