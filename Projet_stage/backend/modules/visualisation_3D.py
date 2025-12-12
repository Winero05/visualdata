"""Ce module permet de créer des vues graphiques en 3 dimention,
interactif avec le curseur avec Plotly.

Returns:
    None: Rien n'est retourné par les classes une fois les vue générées.
"""

from typing import Optional
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from modules.methode_acp import MethodeACP
from modules.methode_tsne import MethodeTSNE
from modules.methode_umap import MethodeUMAP
from modules.auto_selector import AutoSelector
import plotly.express as px
from pydantic import BaseModel

class GraphicVueFolder3D(BaseModel):
    """Cette classe prend le chemin d'un emplacement local.

    Args:
        BaseModel (Model): Cette classe assure la validation et la sérialisation de la classe.

    Raises:
        TypeError: _description_

    Returns:
        None: Rien n'est retournée comme valeur.
    """

    folder_path: str
@dataclass
class Visualisation3D:
    """Cette classe permet de faire la construction des figures en 3 dimentions.
    """

    axes = 3
    df: pd.DataFrame
    color_col: Optional[str] = None # La colonne devant permettre la coloration
    graphic_vue_forder: str = ""
    file_name: str = ""

    def __post_init__(self) -> None:
        """Cette méthode vérifie si le chemin reçu par la classe existe dans l'OS.
        """

        try:
            if not Path(self.graphic_vue_forder).is_dir():
                raise TypeError("\nEmplacement not trouvé.\n")
        except FileNotFoundError as fnfe:
            fnfe.add_note("\nVeuillez entrer un chemin d'un emplacement local.\n")
        return None

    def visualisation_3d_acp(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode ACP.
        """

        apc_3d_instance = MethodeACP(self.df)

        x_acp = apc_3d_instance.acp_reduction(nombre_dimenssion=self.axes)

        df_acp = pd.DataFrame(x_acp, columns=["PC_1","PC_2","PC_3"])

        df_acp["age"] = self.df["age"].values

        title = "Méthode de réduction de données ACP en 3D(Interactif)."

        label = {"x": "PC_1: Composant 1", "y": "PC_2: Composant 2", "z": "PC_3: Composant 3"}

        # Graphiques interactifs 3D
        fig = px.scatter_3d(df_acp,
                x= x_acp[:, 0],
                y= x_acp[:, 1],
                z= x_acp[:, 2],
                color= self.color_col,
                title=title,
                labels=label
                )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_ACP_3D.png", format="svg")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_ACP_3D.html")

    def visualisation_3d_tsne(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode t-SNE.
        """

        tsne_3d_instance = MethodeTSNE(self.df)

        x_tsne = tsne_3d_instance.tsne_reduction(nombre_de_dimension=self.axes)

        df_tsne = pd.DataFrame(x_tsne, columns=["t-SNE_1","t-SNE_2","t-SNE_3"])

        df_tsne["age"] = self.df["age"].values

        title = "Méthode de réduction de données avec t-SNE en 3D(Iteratif)."

        label = {"x": "t-SNE_1: Composant 1", "y": "t-SNE_2: Composant 2", "z": "t-SNE_3: Composant 3"}

        # Graphiques interactifs 3D
        fig = px.scatter_3d(df_tsne,
                x= x_tsne[:, 0],
                y= x_tsne[:, 1],
                z= x_tsne[:, 2],
                color= self.color_col,
                title=title,
                labels=label
                )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_t-SNE_3D.png", format="png")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_t-SNE_3D.html")

    def visualisation_3d_umap(self) -> None:
        """Cette méthode permet de faire la visualisation 3D avec la méthode UMAP.
        """

        umap_3d_instance = MethodeUMAP(self.df)

        x_umap = umap_3d_instance.umap_reduction(nombre_de_dimension=self.axes)

        df_umap = pd.DataFrame(x_umap, columns=["UMAP_1","UMAP_2","UMAP_3"])

        df_umap["age"] = self.df["age"].values

        title = "Méthode de réduction de données avec UMAP en 3D(Iteratif)."

        label = {"x": "UMAP_1: Composant 1", "y": "UMAP_2: Composant 2", "z": "UMAP_3: Composant 3"}

        # Graphiques interactifs 3D
        fig = px.scatter_3d(df_umap,
                x= x_umap[:, 0],
                y= x_umap[:, 1],
                z= x_umap[:, 2],
                color= self.color_col,
                title=title,
                labels=label
                )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_UMAP_3D.png", format="png")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_UMAP_3D.html")

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
