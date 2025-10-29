# packages/__init__.py

# Importation des modules minimum pour l'utilisateur

# __all__ = ['modules/loading']

from backend.modules.loading import DataLoader
from backend.modules.clean_dataframe_for_json import CleanDataframeForJson
from backend.modules.analysis import Analyse
from backend.modules.netoyage import  Netoyage
from backend.modules.sansEspace import StringUtils
from backend.modules.methode_acp import  MethodeACP
from backend.modules.methode_tsne import  MethodeTSNE
from backend.modules.methode_umap import  MethodeUMAP
from backend.modules.auto_selector import  AutoSelector
from backend.modules.visualisation_2D import Visualisation_2D
from backend.modules.visualisation_3D import Visualisation_3D
