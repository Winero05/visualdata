"""Ce module permet de créer des vues graphiques en 3 dimention,
interactif avec le curseur avec Plotly.

Returns:
    None: Rien n'est retourné par les classes une fois les vue générées.
"""

from typing import (
    Any,
    Literal,
    Optional,
    Annotated,
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

class BuildGraphic3DSlot(BaseModel):
    """Cette classe prend le chemin d'un emplacement local où stocker les graphiques
    qui seront générées ainsi que les colonnes à visuliser.

    Args:
        BaseModel (Model): Cette classe assure la validation et la sérialisation de la classe.
        folder_path (str): Emplacement local où stocker les vue graphiques.
        visualize_column (dict[str, bool]) : Un dictionnaire contenant les colonnes à visuliser.

    Raises:
        TypeError: Une erreur est levé si un champs reçois type ne lui correspondant pas.

    Returns:
        None: Rien n'est retournée comme valeur.
    """


    folder_path: Annotated[
        str,
        Field(
            title="folder_path",
            min_length=1,
            description="Emplacement local où stocker les vue graphiques."
        ),
        WithJsonSchema(
            json_schema={'type':'string'},
            mode='serialization'
            )
    ]  # Pas de chaîne vide.

    visualize_col: Annotated[
        dict[str, bool],
        Field(
            title="visualize_col",
            min_length=3,
            example={
                "col_1": True,
                "col_x": False,
                "col_n": True
                },
            description="Colonnes numérique à visuliser."
        ),
        WithJsonSchema(
            json_schema={'type':'dict[str, bool]'},
            mode='serialization')
    ]

@dataclass
class Visualisation3D:
    """Cette classe permet de faire la construction des figures en 3 dimentions.
    """

    axes: Annotated[
        int,
        Field(
            default=3,
            title="axes",
            description="Ce paramètre défini le nombre d'axe(dimension) réduction.",
            examples=["3"]
        ),
        WithJsonSchema(
            json_schema={'type':'Integer'},
            mode='serialization')]

    color_col: Annotated[
        str,
        Field(
            title="color_col",
            description="""Ce paramètre le nom d'une colonne
            pour défini la coloration du graphique.""",
            examples=["colonne-1"]
        ),
        WithJsonSchema(
            json_schema={'type':'String'},
            mode="serialisation"
        )]

    df: Annotated[
        pd.DataFrame,
        Field(
            title="df",
            description="""Ce paramètre reçoit un DataFrame
            pour permettre la visualisation des données de
            l'utilisateur."""
        )]

    file_name: Annotated[
        str,
        Field(
            title="file_name",
            description="""Ce paramètre reçoit le nom du
            fichier des données chargé pour créer le nom
            de la visualisation graphique correspondant.""",
            examples=["data-1"]
        ),
        WithJsonSchema(
            json_schema={'type':'String'},
            mode="serialisation"
        )]

    graphic_vue_folder: Annotated[
        str,
        Field(
            title="graphic_vue_folder",
            description="""Ce paramètre reçoit le nom du
            répertoire qui doit stocker les visualisations
            graphique correspondant à chaque données chargées.""",
            examples=["data-1"]
        ),
        WithJsonSchema(
            json_schema={'type':'String'},
            mode="serialisation"
        )]

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
        # ne fini pas par '3D', '/3D' ou '/3D/'.
        if not folder.endswith(('3D', '/3D', '/3D/')):
            # 2. Créer une chaîne de caratère finissant par '/2D/'.
            folder_name = folder + "/3D/"
            # 3. Puis créer ce dossier s'il n'existe pas.
            if not Path(folder_name).is_dir():
                # 4. os.makedirs crée les dossiers parents si nécessaire
                os.makedirs(folder_name, exist_ok=True)

        # 4. Nom du fichier de la vue graphique
        file_name = f"{file}_{method}_3D.html"

        # 5. Définir le nom du fichier et le chemin complet
        # (i.e Créer une chaîne de caractère spécifiant l'emplacement de la vue graphique).
        return os.path.join(folder_name, file_name) # Recommandé pour la compatibilité OS.


    def visualisation_3d_acp(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode ACP.
        """

        # 1. Instancier la classe avec la méthode d'ACP avec une data_frame.
        apc_3d_instance = MethodeACP(self.df)

        # 2. Appliquer la méthode de réduction d'ACP suivant les axes (ici 2).
        x_acp = apc_3d_instance.acp_reduction(nombre_dimenssion=self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données ACP en 3D(Interactif)."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {
            "x": "PC_1: Composant 1",
            "y": "PC_2: Composant 2",
            "z": "PC_3: Composant 3"
            }

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_acp = pd.DataFrame(x_acp, columns=["PC_1","PC_2","PC_3"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter_3d(df_acp,
                x= x_acp[:, 0],
                y= x_acp[:, 1],
                z= x_acp[:, 2],
                color= df_acp.columns[0],
                title=title,
                labels=label
                )

        # 7. Créer la vue graphique.
        fig.write_html(self.output_html_path(
            folder=self.graphic_vue_folder,
            file=self.file_name,
            method="ACP"))

    def visualisation_3d_tsne(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode t-SNE.
        """

        # 1. Instancier la classe avec la méthode de t-SNE avec une data_frame.
        tsne_3d_instance = MethodeTSNE(self.df)

        # 2. Appliquer la méthode de réduction de t-SNE suivant les axes (ici 2).
        x_tsne = tsne_3d_instance.tsne_reduction(nombre_de_dimension=self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données avec t-SNE en 3D(Iteratif)."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {
            "x": "t-SNE_1: Composant 1",
            "y": "t-SNE_2: Composant 2",
            "z": "t-SNE_3: Composant 3"
            }

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_tsne = pd.DataFrame(x_tsne, columns=["t-SNE_1","t-SNE_2","t-SNE_3"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter_3d(df_tsne,
                x= x_tsne[:, 0],
                y= x_tsne[:, 1],
                z= x_tsne[:, 2],
                color= self.color_col,
                title=title,
                labels=label
                )

        fig.write_html(self.output_html_path(
            folder=self.graphic_vue_folder,
            file=self.file_name,
            method="t-SNE"))

    def visualisation_3d_umap(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode UMAP.
        """

        # 1. Instancier la classe avec la méthode de UMAP avec une data_frame.
        umap_3d_instance = MethodeUMAP(self.df)

        # 2. Appliquer la méthode de réduction de UMAP suivant les axes (ici 2).
        x_umap = umap_3d_instance.umap_reduction(nombre_de_dimension=self.axes)

        # 3. Définir un titre à la vue graphique finale.
        title = "Méthode de réduction de données avec UMAP en 3D(Iteratif)."

        # 4. Définir les noms des axes de la vue graphique finale.
        label = {"x": "UMAP_1: Composant 1", "y": "UMAP_2: Composant 2", "z": "UMAP_3: Composant 3"}

        # 5. Créer un data_frame après réduction de dimension sur la data_frame
        # d'initailiasation.
        df_umap = pd.DataFrame(x_umap, columns=["UMAP_1","UMAP_2","UMAP_3"])

        # 6. Construire une figure graphique dans une variable 'fig'.
        fig = px.scatter_3d(df_umap,
                x= x_umap[:, 0],
                y= x_umap[:, 1],
                z= x_umap[:, 2],
                color= self.color_col,
                title=title,
                labels=label
                )

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

        auto = AutoSelector(nombre_de_dimension=3, df=self.df,)
        methode = auto.detecter_methode()
        match methode:
            case 'pca':
                return self.visualisation_3d_acp()
            case 'tsne':
                return self.visualisation_3d_tsne()
            case 'umap':
                return self.visualisation_3d_umap()

class ReadGraphic3DSlot(BaseModel):
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
