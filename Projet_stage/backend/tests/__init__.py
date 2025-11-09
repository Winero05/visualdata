"""Fichier d'initialisation du package des tests backend à ne pas toucher.
"""

# Package de Projet_stage/backend/tests/__init__.py

# Importation des modules minimum pour l'utilisateur

# __all__ = []

from modules.loading import DataLoader
from modules.clean_dataframe_for_json import CleanDataframeForJson
from modules.save_in_data_base import SaveInDataBase
from modules.config_db import ConfigDb
from modules.analysis import Analyse
from modules.netoyage import  Netoyage
from modules.sansEspace import StringUtils
from modules.methode_acp import  MethodeACP
from modules.methode_tsne import  MethodeTSNE
from modules.methode_umap import  MethodeUMAP
from modules.auto_selector import  AutoSelector
from modules.visualisation_2D import Visualisation_2D
from modules.visualisation_3D import Visualisation_3D

# Version actuelle du travail.
__version__ = "0.0.1"

# Chemin de test des différents fichier de tests dans Projet_stage/backend/tests/*.py
# Veuillez personnaliser le chemin suivant pour avoir accès à vos propre données.

ABSOLU = "C:\\Users\\adama\\AllCodeProjets\\visualdata"
PATH = "\\Projet_stage\\backend\\tests\\data\\csv\\insurance.csv"
__FILE_PATH_TEST__ = ABSOLU+PATH
