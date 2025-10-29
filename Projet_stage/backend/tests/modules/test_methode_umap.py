from tests.test_numeric_data import TestNumericData
from backend.modules.methode_umap import MethodeUMAP

class TestMethodeUMAP:
    def test_umap_reduction(self):
        chargeur_num_data = TestNumericData()
        
        data = chargeur_num_data.send_numeric_data()
        
        chargeur_umap = MethodeUMAP(data)
        
        X_umap = chargeur_umap.umap_reduction(nombre_de_dimension=2)
        
        assert X_umap is not None