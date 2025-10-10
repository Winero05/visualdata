"""Package d'export des modules internes.

Ce fichier expose les classes principales pour simplifier les imports depuis
`packages` ou directement depuis `packages.modules`.
"""

from .loading import DataLoader
from .analysis import Analyse
from .netoyage import Netoyage
from .sansEspace import StringUtils
from .methode_acp import MethodeACP
from .methode_tsne import MethodeTSNE
from .methode_umap import MethodeUMAP
from .visualisation_2D import Visualisation_2D
from .visualisation_3D import Visualisation_3D
from .visualisation_image import ImageVisualizer

# Modules ajoutés / optionnels
try:
	from .visualisation_texte import TextVisualizer
except Exception:
	TextVisualizer = None

try:
	from .visualisation_csv import TabularVisualizer
except Exception:
	TabularVisualizer = None

__all__ = [
	'DataLoader', 'Analyse', 'Netoyage', 'StringUtils',
	'MethodeACP', 'MethodeTSNE', 'MethodeUMAP',
	'Visualisation_2D', 'Visualisation_3D', 'ImageVisualizer',
	'TextVisualizer', 'TabularVisualizer'
]
