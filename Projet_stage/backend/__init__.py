"""Fichier d'initialisation du package ``backend`` à ne pas toucher.
"""

# backend/__init__.py

# Importation des modules minimum pour l'utilisateur
__all__ = [
	'DataLoader',
	'CleanDataframeForJson',
	'SaveInDataBase',
	'ConfigDb',
	'Analyse',
	'Nettoyage',
	'NumericData',
	'StringUtils',
	'MethodeACP',
	'MethodeTSNE',
	'MethodeUMAP',
	'AutoSelector',
	'Visualisation_2D',
	'Visualisation_3D'
]

# Les modules/classes devant intervenir dans l'API
from modules.loading import DataLoader
from modules.save_in_data_base import SaveInDataBase

# Les modules/classes qui le bon fonctionnement des autres modules/classes.
from modules.string_tool import StringTools
from modules.clean_dataframe_for_json import CleanDataframeForJson
from modules.config_db import ConfigDb
from modules.analysis import Analyse
from modules.nettoyage import  Nettoyage
from modules.numeric_data import NumericData
from modules.sans_espace import StringUtils
from modules.methode_acp import  MethodeACP
from modules.methode_tsne import  MethodeTSNE
from modules.methode_umap import  MethodeUMAP
from modules.auto_selector import  AutoSelector
from modules.visualisation_2D import Visualisation_2D
from modules.visualisation_3D import Visualisation_3D

__version__ = "0.0.1"
