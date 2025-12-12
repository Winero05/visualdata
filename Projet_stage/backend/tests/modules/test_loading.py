"""Fichier test du module Projet_stage/backend/modules/loading.py
"""

# test de tests/modules/test_loading.py
from typing import Union
# from tests import __FILE_PATH_TEST__
import pandas as pd
import numpy as np
from modules.loading import DataLoader

class TestDataLoader:
    """
    Test la classe `DataLoader` du module Projet_stage/backend/modules.loding.py.
    """
    def test_chargement_fichier(self) -> None:
        """
        Test le chargement des données depuis le module
        `Projet_stage/backend/modulesloading.py`.
        """

        # Veuillez modifier les deux variables suivante.
        absolut = "C:\\Users\\adama\\AllCodeProjets\\visualdata"
        path = "\\Projet_stage\\backend\\tests\\data\\csv\\insurance.csv"

        __file_absolut_path__ = absolut+path

        # Initialisation de la classe
        chargeur = DataLoader(df=None, format=None)

        # Chargement des données
        data = chargeur.load(file_path=__file_absolut_path__)

        # Tests
        assert data is not None
        # assert not data.empty
        # assert "Sleep Duration" in data.columns  # Exemple d’une colonne attendue

    def get_data(self) -> Union[pd.DataFrame, np.ndarray, str]:
        """Méthode de lecture des données pour permettre l'exécution d'autre méthodes de tests.

        Returns:
            Union[pd.DataFrame, np.ndarray, str]: Une valeur de retour de l'union est retournée.
        """

        # Initialisation de la classe
        chargeur = DataLoader(df=None, format=None)

        absolut = "C:\\Users\\adama\\AllCodeProjets\\visualdata"
        path = "\\Projet_stage\\backend\\tests\\data\\csv\\insurance.csv"

        __file_absolut_path__ = absolut+path

        # Chargement des données
        df = chargeur.load(file_path=__file_absolut_path__)

        return df
