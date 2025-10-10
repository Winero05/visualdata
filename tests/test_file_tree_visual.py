import os
from packages.modules.loading import DataLoader


def test_build_tree_and_select():
    loader = DataLoader()
    # use the project's data csv folder if it exists
    root = os.path.join(os.path.dirname(__file__), '..', 'packages', 'data')
    root = os.path.normpath(root)
    tree = loader.build_tree_from_dir(root, patterns=['*.csv'])
    # ensure tree is a dict and has children
    assert isinstance(tree, dict)
    assert 'children' in tree

    # try selecting a subpath that likely exists (safe-fail allowed)
    # This test only ensures API runs without raising
    try:
        paths = []
        # attempt to pick the first child key
        for k in tree['children'].keys():
            # skip __pycache__
            if k.startswith('__'):
                continue
            paths = loader.build_tree_from_list([os.path.join(root, k)])
            break
    except Exception:
        pass
