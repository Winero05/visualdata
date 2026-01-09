"""Ce module permet de créer des vues graphiques interactives avec le curseur en 2 dimension
avec Plotly.

Returns:
    None: Rien n'est retourné par les classes une fois les vue générées.
"""

from typing import (
    Any,
    Optional,
    Annotated,
    Literal,
    # Union,
    )
from dataclasses import dataclass
from pathlib import Path
import os
import pandas as pd
from modules.methode_acp import MethodeACP
from modules.methode_tsne import MethodeTSNE
from modules.methode_umap import MethodeUMAP
from modules.auto_selector import AutoSelector
import plotly.express as px
import plotly.io as pio
from pydantic import (
    Field,
    BaseModel,
    WithJsonSchema,
    )
# from fastapi.responses import FileResponse

class BuildGraphic2DSlot(BaseModel):
    """Cette classe prend le chemin d'un emplacement local où stocker les graphiques
    qui seront générées ainsi que les colonnes à visuliser.

    Args:
        BaseModel (Model): Cette classe assure la validation et la sérialisation de la classe.
        folder_path (str): Emplacement local où stocker les vue graphiques.
        visualize_column (dict[str, bool]) : Un dictionnaire contenant les colonnes à visuliser.

    Raises:
        TypeError: Une erreur est levée si un champs reçoit un type qui ne lui correspond pas.

    Returns:
        None: Rien n'est retournée.
    """

    folder_path: Annotated[
        str,
        Field(
            title="folder_path",
            min_length=1, # Le champ ne doit pas être vide
            description="Emplacement local où stocker les vue graphiques."
        ),
        WithJsonSchema(
            json_schema={'type':'string'},
            mode='serialization')
    ]  # Pas de chaîne vide.

    visualize_column: Annotated[
        dict[str, str],
        Field(
            title="visualize_column",
            example={
                "col_1": 'True',
                "col_x": 'False',
                "col_n": 'True'
                },
            description="Colonnes numérique à visuliser.",
            min_length=2, # Le champ ne doit pas être vide
        ),
        WithJsonSchema(
            json_schema={'type':'dict[str, str]'},
            mode='serialization')
    ]

@dataclass
class Visualisation2D:
    """Cette classe permet de faire la construction des figures en 2 dimentions.

    Args:
        axes (int): Le nombre de dimension dans laquelle il faut réduir les données.
        df (pd.DataFrame): Les données numérique à visualiser.
        file_name (str): Le nom du fichier graphique.
        graphic_vue_folder (str): Le chemin du dossier local devant contenir les vues graphique.
        color_col (Optional[str]): La colone devant servir de coloration des vues graphique
        (None par défaut).
    """

    df: pd.DataFrame
    file_name: str
    graphic_vue_folder: str
    axes: int = 2
    color_col: Optional[str] = None  # La colonne devant permettre la coloration

    def __post_init__(self) -> None:
        """Cette méthode vérifie si le chemin reçu par la classe existe dans l'OS.
        """

        # Fixer la nature du fichier d'image quand on veut télécharger le rendu graphique (html).
        pio.defaults.default_format = "svg"

        try:
            if not Path(self.graphic_vue_folder).is_dir():
                raise TypeError("\nEmplacement not trouvé.\n")
        except FileNotFoundError as fnfe:
            fnfe.add_note("\nVeuillez entrer un chemin d'un emplacement local.\n")
            raise
        return None

    def output_html_path(self, folder: str, file: str, method: str) -> str:
        """Cette méthode permet de créer une chaîne représentant où doit-être
        construite une vue graphique 2D.

        Args:
            folder (str): Le dossier devant comporter les vues graphiques.
            file (str): Le nom du fichier.
            method (str): La méthode ayant permit de générer la vue graphique.

        Returns:
            str: Le chemin complet devant permettre la construction du fichier est retourné.
        """

        # 1. Si le nom du répertoire de stockage des vues graphiques
        # ne fini pas par '2D', '/2D' ou '/2D/'.
        if not folder.endswith(('2D', '/2D', '/2D/')):
            # 2. Créer une chaîne de caratère finissant par '/2D/'.
            folder_name = folder + "/2D/"
            # 3. Puis créer ce dossier s'il n'existe pas.
            if not Path(folder_name).is_dir():
                # 4. os.makedirs crée les dossiers parents si nécessaire
                os.makedirs(folder_name, exist_ok=True)

        # 4. Nom du fichier de la vue graphique
        file_name = f"{file}_{method}_2D.html"

        # 5. Définir le nom du fichier et le chemin complet
        # (i.e Créer une chaîne de caractère spécifiant l'emplacement de la vue graphique).
        return os.path.join(folder_name, file_name) # Recommandé pour la compatibilité OS.

    def visualisation_2d_acp(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode ACP.
        """

        # 1. Instancier la classe avec la méthode d'ACP avec une data_frame.
        apc_2d_instance = MethodeACP(self.df)

        # 2. Appliquer la méthode de réduction d'ACP suivant les axes (ici 2).
        x_acp = apc_2d_instance.acp_reduction(nombre_dimenssion= self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données avec ACP en 2D."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {"x": "PC_1", "y": "PC_2"}

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_acp = pd.DataFrame(x_acp, columns=["PC_1: Composante 1", "PC_2: Composante 2"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter(
            data_frame=df_acp,
            x="PC_1: Composante 1",
            y= "PC_2: Composante 2",
            color= df_acp.columns[0],
            title=title,
            labels=label)

        # 7. Créer la vue graphique.
        fig.write_html(self.output_html_path(
            folder=self.graphic_vue_folder,
            file=self.file_name,
            method="ACP"))

    def visualisation_2d_tsne(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode t-SNE.
        """

        # 1. Instancier la classe avec la méthode de t-SNE avec une data_frame.
        chargeur_tsne = MethodeTSNE(self.df)

        # 2. Appliquer la méthode de réduction de t-SNE suivant les axes (ici 2).
        x_tsne = chargeur_tsne.tsne_reduction(nombre_de_dimension=self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données avec t-SNE en 2D."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {"x": "t-SNE_1", "y": "t-SNE_2"}

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_tsne = pd.DataFrame(x_tsne, columns=["t-SNE_1", "t-SNE_2"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter(
            data_frame=df_tsne,
            x="t-SNE_1",
            y= "t-SNE_2",
            color= df_tsne.columns[0],
            title=title,
            labels=label)

        # 7. Créer la vue graphique.
        fig.write_html(self.output_html_path(
            folder=self.graphic_vue_folder,
            file=self.file_name,
            method="t-SNE"))

    def visualisation_2d_umap(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode UMAP.
        """

        # 1. Instancier la classe avec la méthode de UMAP avec une data_frame.
        chargeur_umap = MethodeUMAP(self.df)

        # 2. Appliquer la méthode de réduction de UMAP suivant les axes (ici 2).
        x_umap = chargeur_umap.umap_reduction(nombre_de_dimension=self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données avec UMAP en 2D."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {"x": "UMAP_1", "y": "UMAP_2"}

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_umap = pd.DataFrame(x_umap, columns=["UMAP_1", "UMAP_2"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter(
            data_frame=df_umap,
            x="UMAP_1",
            y= "UMAP_2",
            color= df_umap.columns[0],
            title=title,
            labels=label)

        # 7. Créer la vue graphique.
        fig.write_html(self.output_html_path(
            folder=self.graphic_vue_folder,
            file=self.file_name,
            method="UMAP"))


    def visualisation_automatique(self) -> None:
        """Cette méthode sélectionne la méhtode réduction la plus adapté
        pour la visualisation des données.

        Returns:
            None: Rien n'est retourné par cette fonction.
        """

        auto = AutoSelector(nombre_de_dimension=2, df=self.df)
        methode = auto.detecter_methode()
        match methode:
            case 'pca':
                return self.visualisation_2d_acp()
            case 'tsne':
                return self.visualisation_2d_tsne()
            case 'umap':
                return self.visualisation_2d_umap()

class ReadGraphic2DSlot(BaseModel):
    """Cette classe prend le chemin d'un emplacement local où lire les graphiques
    qui sont générées, le statu de l'action de lecture ainsi qu'un message d'une telle action.

    Args:
        BaseModel (Model): Cette classe assure la validation et la sérialisation de la classe.
        html_file (str): Ce paramètre reçoit le nom d'un fichier HTML à lire.
        html_files (str): Ce paramètre reçoit le nom de tous les fichiers HTML dans un emplacement.

    Raises:
        TypeError: Une erreur est levé si un champs reçois un type qui ne lui correspondant pas.

    Returns:
        None: Rien n'est retournée comme valeur.
    """
    html_file: Annotated[
        str,
        Field(
            default=None,
            description="Ce champ reçoit le nom d'un fichier HTML à lire sur le disque.",
            examples=["data1.html"],
            title="html_file"),
        WithJsonSchema(
            json_schema={'type':'String'},
            mode='serialization')
            ]
    html_files: Annotated[
        list[str],
        Field(
            default=None,
            description="Ce champ reçoit une liste de tous les fichiers des vues graphiques.",
            examples=[["data1.html", "data2.html", "dataN.html"]],
            title="html_files"),
        WithJsonSchema(
            json_schema={'type':'list[str]'},
            mode='serialization')]
