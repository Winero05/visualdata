from packages.modules.methode_tsne import MethodeTSNE
from tests.test_numeric_data import TestNumericData

class TestMethodeTSNE:
    def test_methode_tsne(self):
        chargeur_num_data = TestNumericData()
        
        data = chargeur_num_data.send_numeric_data()
        
        chargeur_tsne = MethodeTSNE(data)
        
        X_tsne = chargeur_tsne.tsne_reduction(nombre_de_dimension=2)
        
        assert X_tsne is not None