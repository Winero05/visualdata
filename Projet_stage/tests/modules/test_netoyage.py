# Contenu tests/test_netoyage.py

from tests.test_loading import TestDataLoader
from packages.modules.netoyage import Netoyage

class TestNetoyage:
    def test_gerer_les_valeurs_manquantes(self):
        chargeur_data = TestDataLoader()
        
        data = chargeur_data.get_data()
        
        chargeur_netoyage = Netoyage(data)
        
        data_netoyer = chargeur_netoyage.gerer_les_valeurs_manquantes()
        
        assert data_netoyer is not None
        assert not data_netoyer.empty
    
    def test_gerer_les_valeurs_duplicates(self):
        chargeur_data = TestDataLoader()
        
        data = chargeur_data.get_data()
        
        chargeur_netoyer = Netoyage(data)
        
        data_netoyer = chargeur_netoyer.gerer_les_valeurs_duplicates()
        
        assert data_netoyer is not None
        assert not data_netoyer.empty
        