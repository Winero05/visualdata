"""Test du module `Projet_stage/backend/modules/auto_selctor.py`
"""

from tests.modules.test_loading import TestDataLoader
from modules.auto_selector import AutoSelector

class TestAutoSelector:
    """Test de la classe `AutoSelector`.
    """

    def test_detecter_methode(self) -> None:
        """Méthode de test `dectecter_methode`."""

        # Instancialtion de classe
        chargeur_data = TestDataLoader()
        data = chargeur_data.get_data()
        chargeur_auto_selecteur_dim_1 = AutoSelector(nombre_de_dimension=1, df=data)
        chargeur_auto_selecteur_dim_2 = AutoSelector(nombre_de_dimension=2, df=data)
        chargeur_auto_selecteur_dim_3 = AutoSelector(nombre_de_dimension=3, df=data)

        detecter_methode_dim_1 = chargeur_auto_selecteur_dim_1.detecter_methode()
        detecter_methode_dim_2 = chargeur_auto_selecteur_dim_2.detecter_methode()
        detecter_methode_dim_3 = chargeur_auto_selecteur_dim_3.detecter_methode()

        print(detecter_methode_dim_1)
        print(detecter_methode_dim_2)
        print(detecter_methode_dim_3)
