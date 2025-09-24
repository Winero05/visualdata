# api.py

# --- Importations des bibliothèques de base ---
from enum import Enum
from typing_extensions import Literal
from fastapi import Body, FastAPI, HTTPException, Response, File, UploadFile, Form, Depends
#from matplotlib.pylab import Literal
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
import io
import pandas as pd
import json
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import plotly.express as px
import os # Pour la gestion du chemin dans les fonctions utilitaires

# Importez toutes vos classes et fonctions de vos modules
from packages.modules.loading import DataLoader
from packages.modules.netoyage import handle_missing_values
from packages.modules.analysis import Analyse, preprocess_for_reduction
from packages.modules.methode_acp import MethodePCA
from packages.modules.visualisation_image import ImageVisualizer
from packages.modules.visualisation_texte import TextVisualizer
from packages.modules.visualisation_csv import TabularVisualizer
from packages.modules.methode_tsne import TSNEVisualizer
from packages.modules.methode_umap import UMAPVisualizer

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

# --- Initialisation de l'Application FastAPI ---
app = FastAPI(
    title="API de Visualisation et d'Analyse de Données",
    description="Une API pour charger, analyser et visualiser différents types de données. La plupart des endpoints acceptent une source de données via un chemin de fichier, une chaîne JSON ou un téléversement.",
    version="1.0.0"
)

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

# Ce "wrapper" est nécessaire car FastAPI ne peut pas gérer une `Union` directement à la racine du corps JSON.
class ReductionWrapper(BaseModel):
    params: ReductionParams

class ReductionResponse(BaseModel):
    """
    Réponse de l'endpoint de réduction de dimension.
    Inclut l'image du graphique et les données projetées.
    """
    status: str = "success"
    message: Optional[str] = None
    image_data: str # L'image encodée
    reduced_data: List[Dict[str, Any]] # Les données réduites en JSON

# --- Endpoints ---
@app.get("/Accueil")
def bienvenue():
    """Endpoint de bienvenue simple pour vérifier que l'API est en ligne."""
    return {"Bienvenue sur l'API d'Analyse et de Visualisation de Données. Accédez à /docs pour la documentation interactive."}



@app.post("/nettoyer-donnees/", summary="Nettoie les valeurs manquantes", tags=["Nettoyage"])
def nettoyer_donnees(
    strategie: str = Form(..., description="Stratégie: 'mean', 'median', 'fill', 'drop'."),
    colonnes: Optional[str] = Form(None, description="Colonnes à nettoyer (séparées par des virgules)."),
    df_data: pd.DataFrame = Depends(get_data_source)
):
    """Nettoie les valeurs manquantes dans un jeu de données."""
    # Convertir la chaîne de colonnes en liste si elle est fournie.
    colonnes_list = colonnes.split(',') if colonnes else None
    df_nettoye = handle_missing_values(df_data, strategie, colonnes_list)
    
    return Response(content=df_nettoye.to_json(orient="records"), media_type="application/json")


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


@app.post("/reduire-dimension/", summary="Réduction de dimension", tags=["Réduction de dimension"])
def reduire_dimension(
    wrapper: ReductionWrapper,
    df_data: pd.DataFrame = Depends(get_data_source)
) -> ReductionResponse:

    """
    Génère un graphique de réduction de dimension avec la méthode spécifiée (ACP, UMAP ou t-SNE).
    
    - **acp**: Analyse en Composantes Principales. Rapide et efficace pour les relations linéaires.
    - **umap**: Uniform Manifold Approximation and Projection. Excellent pour la visualisation de clusters, préserve bien la structure globale.
    - **tsne**: t-distributed Stochastic Neighbor Embedding. Très bon pour visualiser des groupes bien séparés, mais peut mal préserver la structure globale.
    """
    try:
        params = wrapper.params
        fig = None
        reduced_df = None

        # Utiliser `isinstance` pour déterminer quelle méthode a été choisie par l'utilisateur.
        if isinstance(params, PCAParams):
            # Le prétraitement est spécifique à l'ACP dans cette implémentation.
            df_processed = preprocess_for_reduction(df_data)
            instance = MethodePCA(n_components=params.n_components)
            fig, reduced_df = instance.visualize(df_processed, color_by_col=params.color_by_col, original_df=df_data)
        
        elif isinstance(params, UMAPParams):
            instance = UMAPVisualizer(df_data)
            fig, reduced_df = instance.visualize(n_components=params.n_components, color_by_col=params.color_by_col, n_neighbors=params.n_neighbors, min_dist=params.min_dist)
        
        elif isinstance(params, TSNEParams):
            instance = TSNEVisualizer(df_data)
            fig, reduced_df = instance.visualize(n_components=params.n_components, color_by_col=params.color_by_col, perplexity=params.perplexity)

        # Vérifier que la visualisation a bien produit une figure et des données.
        if fig is None:
             raise HTTPException(status_code=500, detail="La figure n'a pas pu être générée.")
        if reduced_df is None:
             raise HTTPException(status_code=500, detail="Les données réduites n'ont pas pu être générées.")

        return ReductionResponse(
            # La réponse inclut à la fois l'image et les données brutes réduites.
            graph_type=params.methode.value,
            message=f"Réduction de dimension via {params.methode.upper()} réussie.",
            image_data=fig_to_base64(fig),
            reduced_data=reduced_df.to_dict(orient="records")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la réduction de dimension: {str(e)}")


# NOTE: Cet endpoint est un exemple conceptuel et n'est pas entièrement fonctionnel.
# Il montre comment on pourrait combiner plusieurs étapes (nettoyage, analyse, visualisation)
# en une seule requête API. Pour le rendre fonctionnel, il faudrait appeler la logique
# de `reduire_dimension` et retourner une réponse structurée.
@app.post("/analyser-et-visualiser/")
def analyser_et_visualiser_donnees(
    params: ReductionParams = Body(..., discriminator="methode"),
    strategie_nettoyage: Optional[str] = Form(None),
    colonnes_nettoyage: Optional[str] = Form(None),
    df_data: pd.DataFrame = Depends(get_data_source)
):
    # Logique de nettoyage optionnelle
    if strategie_nettoyage:
        df_data = handle_missing_values(df_data, strategie_nettoyage, colonnes_nettoyage)
    
    # TODO: Implémenter la logique de réduction de dimension ici, similaire à l'endpoint /reduire-dimension/
    # Par exemple, en appelant la fonction `reduire_dimension` avec les bons paramètres.
    # Il faudrait ensuite construire et retourner une `ReductionResponse`.
    
    raise HTTPException(status_code=501, detail="Endpoint non implémenté.")
