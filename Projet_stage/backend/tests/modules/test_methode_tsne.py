"""Test du module `Projet_stage/backend/modules/methode_tsne.py`.
"""

from modules.methode_tsne import MethodeTSNE
from tests.modules.test_numeric_data import TestNumericData

class TestMethodeTSNE:
    """Test de la classe `MethodeTSNE`.
    """

    def test_methode_tsne(self) -> None:
        """Test de la méthode `tsne_reduction`.
        """

        chargeur_num_data = TestNumericData()

        data = chargeur_num_data.send_numeric_data()

        chargeur_tsne = MethodeTSNE(data)

        x_tsne = chargeur_tsne.tsne_reduction(nombre_de_dimension=2)

        assert x_tsne is not None
