# Contenue de tests/test_methode_acp.py

from packages.modules.methode_acp import MethodeACP
import numpy as np
import pandas as pd
from tests.test_numeric_data import TestNumericData
class TestMethodePCA:
    def test_pca_reduction(self):
        chargeur_num_data = TestNumericData()
        
        data = chargeur_num_data.send_numeric_data()
        
        # Instanciation de la classe `MethodePCA` du fichier `methode_acp.py`.
        chargeur = MethodeACP(data)
        
        X_acp = chargeur.acp_reduction(nombre_dimenssion=3)
        
        assert X_acp is not None        
        # assert not X_acp.empty
    