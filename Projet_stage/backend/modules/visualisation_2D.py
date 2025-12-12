"""Ce module permet de créer des vues graphiques en 2 dimention,
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

class GraphicVueFolder2D(BaseModel):
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
class Visualisation2D:
    """Cette classe permet de faire la construction des figures en 2 dimentions.
    """

    axes = 2
    df: pd.DataFrame
    color_col: Optional[str] = None  # La colonne devant permettre la coloration
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

    def visualisation_2d_acp(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode ACP.
        """

        apc_2d_instance = MethodeACP(self.df)

        x_acp = apc_2d_instance.acp_reduction(nombre_dimenssion= self.axes)

        title = "Méthode de réduction de données avec ACP en 2D."

        label = {"x": "PC_1", "y": "PC_2"}

        df_acp = pd.DataFrame(x_acp, columns=["PC_1: Composante 1", "PC_2: Composante 2"])

        df_acp["age"] = self.df["age"].values

        fig = px.scatter(df_acp,
                x="PC_1: Composante 1",
                y= "PC_2: Composante 2",
                color= self.color_col,
                title=title,
                labels=label
            )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_ACP_2D.png", format="svg")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_ACP_2D.html")

    def visualisation_2d_tsne(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode t-SNE.
        """

        chargeur_tsne = MethodeTSNE(self.df)
        x_tsne = chargeur_tsne.tsne_reduction(nombre_de_dimension=self.axes)
        title = "Méthode de réduction de données avec t-SNE en 2D."

        label = {"x": "t-SNE_1", "y": "t-SNE_2"}

        df_tsne = pd.DataFrame(x_tsne, columns=["t-SNE_1", "t-SNE_2"])

        df_tsne["age"] = self.df["age"].values

        fig = px.scatter(df_tsne,
                x="t-SNE_1",
                y= "t-SNE_2",
                color= self.color_col,
                title=title,
                labels=label
            )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_t-SNE_2D.png", format="png")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_t-SNE_2D.html")

    def visualisation_2d_umap(self) -> None:
        """Cette méthode permet de faire la visualisation 2D avec la méthode UMAP.
        """

        chargeur_umap = MethodeUMAP(self.df)

        x_umap = chargeur_umap.umap_reduction(nombre_de_dimension=self.axes)

        title = "Méthode de réduction de données avec UMAP en 2D."

        label = {"x": "UMAP_1", "y": "UMAP_2"}

        df_umap = pd.DataFrame(x_umap, columns=["UMAP_1", "UMAP_2"])

        df_umap["age"] = self.df["age"].values

        fig = px.scatter(df_umap,
                x="UMAP_1",
                y= "UMAP_2",
                color= self.color_col,
                title=title,
                labels=label
            )

        fig.write_image(self.graphic_vue_forder + "/img/" + f"{self.file_name}_UMAP_2D.png", format="png")
        fig.write_html(self.graphic_vue_forder + "/html/" + f"{self.file_name}_UMAP_2D.html")

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
