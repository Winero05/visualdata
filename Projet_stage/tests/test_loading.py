# tests/test_loading.py

from typing import Union
import pandas as pd
import numpy as np
from packages.modules.loading import DataLoader

class TestDataLoader:
    """
    Test la classe `DataLoader`.
    """

    def test_chargement_fichier(self):
        """
        Test le chargement des données depuis la fichier `loading.py`."""

        # Chemin absolu vers ton fichier CSV
        chemin ="/home/adama/visualdata/Projet_stage/tests/data/csv/insurance.csv"
        
        # Initialisation de la classe
        chargeur = DataLoader()
        
        # Chargement des données
        data = chargeur.load(file_path=chemin)
        
        # Tests
        assert data is not None
        assert not data.empty
        # assert "Sleep Duration" in data.columns  # Exemple d’une colonne attendue
        
    def get_data(self) -> Union[pd.DataFrame, np.ndarray, str]:
                    
        # Chemin absolu vers ton fichier CSV
        chemin ="/home/adama/visualdata/Projet_stage/tests/data/csv/insurance.csv"
        
        # Initialisation de la classe
        chargeur = DataLoader()
        
        # Chargement des données
        df = chargeur.load(file_path=chemin)
        
        return df
