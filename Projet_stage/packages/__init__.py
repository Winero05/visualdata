# packages/__init__.py

# Importation des modules minimum pour l'utilisateur

# __all__ = ['modules/loading']

from packages.modules.loading import DataLoader
from packages.modules.analysis import Analyse
from packages.modules.netoyage import  Netoyage
from packages.modules.sansEspace import StringUtils
from packages.modules.methode_acp import  MethodeACP
from packages.modules.methode_tsne import  MethodeTSNE
from packages.modules.methode_umap import  MethodeUMAP
from packages.modules.auto_selector import  AutoSelector
from packages.modules.visualisation_2D import Visualisation_2D
from packages.modules.visualisation_3D import Visualisation_3D
