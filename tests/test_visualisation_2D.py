# Contenu de test/test_visualisation_csv_2D.py

from packages.modules.visualisation_2D import Visualisation_2D
from tests.test_numeric_data import TestNumericData

class TestVisualisation_2D:
    """
    Tester la visualisation 2D du module `visualisation_2D.py`.
    """
    def test_visualisation_2D_acp(self):
        """
        Cette classe teste la méthode `visualisation_2D` des donnée en utilisant la méthode d'ACP.
        """
        chargeur_numeric_data = TestNumericData()
        
        data = chargeur_numeric_data.send_numeric_data()
        
        chargeur_visualisation_2D = Visualisation_2D(df = data)
        
        chargeur_visualisation_2D.visualisation_2D_acp()
    
    def test_visualisation_2D_tsne(self):
        """
        Cette classe teste la méthode `visualisation_2D` des donnée en utilisant la méthode de `t-SNE`.
        """
        chargeur_numeric_data = TestNumericData()
        
        data = chargeur_numeric_data.send_numeric_data()
        
        chargeur_visualisation_2D = Visualisation_2D(df = data)
        
        chargeur_visualisation_2D.visualisation_2D_tsne()
    
    def test_visualisation_2D_umap(self):
        """
        Cette classe teste la méthode `visualisation_2D` des donnée en utilisant la méthode de `UMAP`.
        """

        chargeur_numeric_data = TestNumericData()
        
        data = chargeur_numeric_data.send_numeric_data()
        
        chargeur_visualisation_2D = Visualisation_2D(df = data)
        
        chargeur_visualisation_2D.visualisation_2D_umap()

        