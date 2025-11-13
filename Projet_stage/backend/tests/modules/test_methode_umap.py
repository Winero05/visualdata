"""Test du module `Projet_stage/backend/modules/methode_umap.py`.
"""

from tests.modules.test_numeric_data import TestNumericData
from modules.methode_umap import MethodeUMAP

class TestMethodeUMAP:
    """Test de la classe `MethodeUMAP`.
    """
    def test_umap_reduction(self) -> None:
        """Test de la méthode `umpa_reduction`.
        """

        chargeur_num_data = TestNumericData()

        data = chargeur_num_data.send_numeric_data()

        chargeur_umap = MethodeUMAP(data)

        xumap = chargeur_umap.umap_reduction(nombre_de_dimension=2)

        assert xumap is not None
