from typing import Union, List, Dict, Any
import pandas as pd
import numpy as np
from packages.modules.methode_acp import MethodeACP
from packages.modules.methode_tsne import MethodeTSNE
from packages.modules.methode_umap import MethodeUMAP
from packages.modules.loading import DataLoader
from packages.modules.file_tree import select_paths_from_tree
import plotly.express as px

class Visualisation_2D:
    def __init__(self, df: Union[pd.DataFrame, np.ndarray, str] = None, file_tree: Dict[str, Any] = None, select_path: str = None):
        """df: existing dataframe (unchanged behaviour)
        file_tree + select_path: alternative - select data files from tree, will load the first matching file.
        """
        self.axes = 2
        self.df = df
        self.file_tree = file_tree
        self.select_path = select_path
        self.loader = DataLoader()

        # If file_tree and select_path are provided, attempt to load the first matching file as dataframe
        if self.df is None and self.file_tree and self.select_path:
            paths = select_paths_from_tree(self.file_tree, self.select_path)
            if paths:
                # attempt to load the first path that returns a DataFrame
                for p in paths:
                    try:
                        loaded = self.loader.load(p)
                        if isinstance(loaded, pd.DataFrame):
                            self.df = loaded
                            break
                    except Exception:
                        continue
            else:
                raise FileNotFoundError(f"Aucun fichier trouvé pour la sélection '{self.select_path}' dans l'arbre fourni.")
    
    def visualisation_2D_acp(self):
        apc_2d_instance = MethodeACP(self.df)

        X_acp = apc_2d_instance.acp_reduction(nombre_dimenssion=self.axes)

        title = "Méthode de réduction de données avec ACP en 2D."

        label = {"x": "PC_1", "y": "PC_2"}

        df_acp = pd.DataFrame(X_acp, columns=["PC_1: Composante 1", "PC_2: Composante 2"])

        df_acp["age"] = self.df["age"].values

        fig = px.scatter(
            df_acp,
            x="PC_1: Composante 1",
            y="PC_2: Composante 2",
            color="age",
            title=title,
            labels=label,
        )

        fig.write_image("/home/adama/visualdata/Projet_stage/tests/resultats/img/2D/Reduction_ACP_2D.png", format="png")
        fig.write_html("/home/adama/visualdata/Projet_stage/tests/resultats/html/2D/Reduction_ACP_2D.html")
        
    def visualisation_2D_tsne(self):
        chargeur_tsne = MethodeTSNE(self.df)
        X_tsne = chargeur_tsne.tsne_reduction(nombre_de_dimension=self.axes)
        title = "Méthode de réduction de données avec t-SNE en 2D."
        
        label = {"x": "t-SNE_1", "y": "t-SNE_2"}
        
        df_tsne = pd.DataFrame(X_tsne, columns=["t-SNE_1", "t-SNE_2"])
        
        df_tsne["age"] = self.df["age"].values

        fig = px.scatter(df_tsne,
                x="t-SNE_1",
                y= "t-SNE_2",
                color= "age",
                title=title,
                labels=label
            )
        fig.write_image("/home/adama/visualdata/Projet_stage/tests/resultats/img/2D/Reduction_t-SNE_2D.png", format="png")
        fig.write_html("/home/adama/visualdata/Projet_stage/tests/resultats/html/2D/Reduction_t-SNE_2D.html")

    def visualisation_2D_umap(self):
        chargeur_umap = MethodeUMAP(self.df)
        
        X_umap = chargeur_umap.umap_reduction(nombre_de_dimension=self.axes)
        
        title = "Méthode de réduction de données avec UMAP en 2D."
        
        label = {"x": "UMAP_1", "y": "UMAP_2"}
        
        df_umap = pd.DataFrame(X_umap, columns=["UMAP_1", "UMAP_2"])
        
        df_umap["age"] = self.df["age"].values

        fig = px.scatter(df_umap,
                x="UMAP_1",
                y= "UMAP_2",
                color= "age",
                title=title,
                labels=label
            )
        fig.write_image("/home/adama/visualdata/Projet_stage/tests/resultats/img/2D/Reduction_UMAP_2D.png", format="png")
        fig.write_html("/home/adama/visualdata/Projet_stage/tests/resultats/html/2D/Reduction_UMAP_2D.html")
