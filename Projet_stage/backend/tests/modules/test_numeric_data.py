from tests.test_loading import TestDataLoader
from backend.modules.numeric_data import Numeric_data

class TestNumericData:
    def test_numeric_colonne(self):
        chargeur_de_donnees = TestDataLoader()
        
        data = chargeur_de_donnees.get_data()
        
        chargeur_num_col = Numeric_data(df=data)
        
        donnees_tabulaire = chargeur_num_col.num_col()
        
        assert donnees_tabulaire is not None

    def send_numeric_data(self):
        chargeur_de_donnees = TestDataLoader()
        
        data = chargeur_de_donnees.get_data()
        
        chargeur_num_col = Numeric_data(df=data)
        
        donnees_tabulaire_numeric = chargeur_num_col.num_col()
        
        return donnees_tabulaire_numeric