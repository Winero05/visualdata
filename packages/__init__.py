"""Facade d'accès aux modules du package `packages`.

Les importations sont effectuées dans des blocs try/except pour éviter que
l'import du package entier échoue si l'environnement n'a pas toutes les
dépendances (pandas, sklearn, umap, etc.). Les utilisateurs peuvent vérifier
la disponibilité d'un module via e.g. `if packages.DataLoader is None:`.
"""

def _try_import(module_path, name):
	try:
		module = __import__(module_path, fromlist=[name])
		return getattr(module, name)
	except Exception as exc:  # pragma: no cover - resilience for missing deps
		print(f"Warning: could not import {module_path}.{name}: {exc}")
		return None


DataLoader = _try_import('packages.modules.loading', 'DataLoader')
Analyse = _try_import('packages.modules.analysis', 'Analyse')
Netoyage = _try_import('packages.modules.netoyage', 'Netoyage')
StringUtils = _try_import('packages.modules.sansEspace', 'StringUtils')
MethodeACP = _try_import('packages.modules.methode_acp', 'MethodeACP')
MethodeTSNE = _try_import('packages.modules.methode_tsne', 'MethodeTSNE')
MethodeUMAP = _try_import('packages.modules.methode_umap', 'MethodeUMAP')
Visualisation_2D = _try_import('packages.modules.visualisation_2D', 'Visualisation_2D')
Visualisation_3D = _try_import('packages.modules.visualisation_3D', 'Visualisation_3D')
ImageVisualizer = _try_import('packages.modules.visualisation_image', 'ImageVisualizer')
TextVisualizer = _try_import('packages.modules.visualisation_texte', 'TextVisualizer')
TabularVisualizer = _try_import('packages.modules.visualisation_csv', 'TabularVisualizer')

__all__ = [
	'DataLoader', 'Analyse', 'Netoyage', 'StringUtils',
	'MethodeACP', 'MethodeTSNE', 'MethodeUMAP',
	'Visualisation_2D', 'Visualisation_3D', 'ImageVisualizer',
	'TextVisualizer', 'TabularVisualizer'
]