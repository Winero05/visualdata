# Contenu de test/test_visualisation_csv_2D.py

from modules.visualisation_3D import Visualisation_3D
from tests.modules.test_numeric_data import TestNumericData

class TestVisualisation_3D:
    def test_visualisation_3D_acp(self):        
        chargeur_numeric_colonne = TestNumericData()
        
        data = chargeur_numeric_colonne.send_numeric_data()
        
        chargeur_visualisation_3D = Visualisation_3D(df = data)
        
        chargeur_visualisation_3D.visualisation_3D_acp()
        
    def test_visualisation_3D_tsne(self):
        chargeur_numeric_colonne = TestNumericData()
        
        data = chargeur_numeric_colonne.send_numeric_data()
        
        chargeur_visualisation_3D = Visualisation_3D(df = data)
        
        chargeur_visualisation_3D.visualisation_3D_tsne()

    def test_visualisation_3D_umap(self):
        chargeur_numeric_colonne = TestNumericData()
        
        data = chargeur_numeric_colonne.send_numeric_data()
        
        chargeur_visualisation_3D = Visualisation_3D(df = data)
        
        chargeur_visualisation_3D.visualisation_3D_umap()