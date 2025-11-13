"""Test du module `Projet_stage/backend/modules/nettoyage.py`.
"""

# Contenu tests/modules/test_netoyage.py

from tests.modules.test_loading import TestDataLoader
from modules.nettoyage import Nettoyage

class TestNettoyage:
    """Test de la classe `Nettoyage`.
    """
    def test_gerer_les_valeurs_manquantes(self) -> None:
        """Test de la méthode `gerer_les_valeurs_manquantes`.
        """

        chargeur_data = TestDataLoader()

        data = chargeur_data.get_data()

        chargeur_netoyage = Nettoyage(data)

        # Veuillez spécifier la stractégie de remplissage des cellules
        # vides dans le tableau de données chargé.
        data_netoyer = chargeur_netoyage.gerer_les_valeurs_manquantes(strategy="mean")

        assert data_netoyer is not None
        assert not data_netoyer.empty

    def test_gerer_les_valeurs_duplicates(self) -> None:
        """Test de la méthode `gerer_les_valeurs_duplicates`.
        """

        chargeur_data = TestDataLoader()

        data = chargeur_data.get_data()

        chargeur_netoyer = Nettoyage(data)

        data_netoyer = chargeur_netoyer.gerer_les_valeurs_duplicates()

        assert data_netoyer is not None
        assert not data_netoyer.empty
