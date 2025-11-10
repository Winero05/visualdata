"""Fichier d'initialisation du package des tests backend à ne pas toucher.
"""

# Package de Projet_stage/backend/tests/__init__.py

# Importation des modules minimum pour l'utilisateur

# __all__ = []

from backend.modules.loading import DataLoader
from backend.modules.clean_dataframe_for_json import CleanDataframeForJson
from backend.modules.save_in_data_base import SaveInDataBase
from backend.modules.config_db import ConfigDb
from backend.modules.analysis import Analyse
from backend.modules.netoyage import  Netoyage
from backend.modules.sansEspace import StringUtils
from backend.modules.methode_acp import  MethodeACP
from backend.modules.methode_tsne import  MethodeTSNE
from backend.modules.methode_umap import  MethodeUMAP
from backend.modules.auto_selector import  AutoSelector
from backend.modules.visualisation_2D import Visualisation_2D
from backend.modules.visualisation_3D import Visualisation_3D

# Version actuelle du travail.
__version__ = "0.0.1"

# Chemin de test des différents fichier de tests dans Projet_stage/backend/tests/*.py
# Veuillez personnaliser le chemin suivant pour avoir accès à vos propre données.

ABSOLU = "C:\\Users\\adama\\AllCodeProjets\\visualdata"
PATH = "\\Projet_stage\\backend\\tests\\data\\csv\\insurance.csv"
__FILE_PATH_TEST__ = ABSOLU+PATH
