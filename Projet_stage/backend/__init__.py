"""Fichier d'initialisation du package backend à ne pas toucher.
"""

# packages/__init__.py

# Importation des modules minimum pour l'utilisateur

__all__ = [
	'DataLoader',
	'CleanDataframeForJson',
	'SaveInDataBase',
	'ConfigDb',
	'Analyse',
	'Netoyage',
	'StringUtils',
	'MethodeACP',
	'MethodeTSNE',
	'MethodeUMAP',
	'AutoSelector',
	'Visualisation_2D',
	'Visualisation_3D'
]

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

__version__ = "0.0.1"
