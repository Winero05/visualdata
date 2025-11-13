"""Test du module `Projet_stage/backend/modules/methode_acp.py`
"""

# Contenue de tests/test_methode_acp.py

from modules.methode_acp import MethodeACP
from tests.modules.test_numeric_data import TestNumericData

class TestMethodePCA:
    """Test de la classe `MethodeACP`.
    """
    def test_pca_reduction(self) -> None:
        """Test de la méthode `pca_reduction`.
        """

        chargeur_num_data = TestNumericData()

        data = chargeur_num_data.send_numeric_data()

        # Instanciation de la classe `MethodePCA` du fichier `methode_acp.py`.
        chargeur = MethodeACP(data)

        x_acp = chargeur.acp_reduction(nombre_dimenssion=3)

        assert x_acp is not None
        # assert not x_acp.empty
