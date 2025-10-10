from pathlib import Path
from typing import Any, Dict, List, Optional


def make_tree_from_paths(paths: List[str]) -> Dict[str, Any]:
    """Construire une structure arborescente (dict) à partir d'une liste de chemins.

    Chaque noeud est un dict: { 'name': str, 'children': {name: node}, 'is_file': bool, 'path': Optional[str], 'meta': {} }
    """
    root: Dict[str, Any] = {"name": "", "children": {}, "is_file": False, "path": None, "meta": {}}

    for p in paths:
        # Normaliser le séparateur
        pp = Path(p)
        parts = pp.parts
        node = root
        for i, part in enumerate(parts):
            if part not in node["children"]:
                node["children"][part] = {
                    "name": part,
                    "children": {},
                    "is_file": (i == len(parts) - 1 and pp.is_file()),
                    "path": str(pp) if i == len(parts) - 1 else None,
                    "meta": {},
                }
            node = node["children"][part]

    return root


def select_paths_from_tree(tree: Dict[str, Any], select_path: str) -> List[str]:
    """Retourne la liste des chemins de fichiers correspondant au `select_path` dans l'arbre.

    select_path peut être une chaîne de type 'dossier/sousdossier' ou un nom de fichier.
    """
    parts = Path(select_path).parts
    node = tree
    for part in parts:
        if not part:
            continue
        if part in node["children"]:
            node = node["children"][part]
        else:
            # chemin introuvable -> retourne vide
            return []

    # maintenant collecter récursivement tous les fichiers sous ce noeud
    result: List[str] = []

    def _collect(n: Dict[str, Any]):
        if n.get("is_file") and n.get("path"):
            result.append(n["path"])
        for child in n.get("children", {}).values():
            _collect(child)

    _collect(node)
    return result


def make_variable_tree_from_df(df) -> Dict[str, Any]:
    """Construire une arborescence simple des variables à partir des colonnes d'un DataFrame.

    Heuristique : si un nom de colonne contient '/', '.' ou '__' ou '_' on peut déduire une hiérarchie.
    Renvoie un dict similaire au file tree mais avec 'is_leaf' indiquant variable.
    """
    root = {"name": "", "children": {}, "is_leaf": False}

    for col in df.columns:
        # choisir séparateur heuristique
        if '/' in col:
            parts = col.split('/')
        elif '.' in col:
            parts = col.split('.')
        elif '__' in col:
            parts = col.split('__')
        elif '_' in col:
            parts = col.split('_')
        else:
            parts = [col]

        node = root
        for i, part in enumerate(parts):
            if part not in node['children']:
                node['children'][part] = {"name": part, "children": {}, "is_leaf": False, "meta": {}}
            node = node['children'][part]
            if i == len(parts) - 1:
                node['is_leaf'] = True
                node['meta']['full_name'] = col

    return root
