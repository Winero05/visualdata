"""Ce fichier test permet de tester le module
`Projet_stage/backend/tests/modules/analysis.py`
"""
# Contenue test/test_analysis.py

from tests.modules.test_loading import TestDataLoader
from modules.analysis import Analyse
import pandas as pd

class TestAnalyse:
    """
    Test la class `Analyse` des données du fichier `analysis.py`.
    """
    def test_summarize(self) -> None:
        """Test la méthode `summarize`
        """

        # Initialisation de la classe `TestDataLoader` du fichier `test/test_loading.py`.
        chargeur = TestDataLoader()

        # Chargement des données à analyser.
        data = chargeur.get_data()

        # Initialisation de la classe `Analyse`.
        analyse = Analyse()

        # Analyse de données
        resultat = analyse.summarize(data=data)

        assert resultat is not None
        assert isinstance(resultat, dict)
        assert len(resultat) > 0

    def test_get_descriptive_stats(self) -> None:
        """Test la méthode `get_sescriptive_stats`.
        """

        # Initialisation de la classe `TestDataLoader` du fichier `test/test_loading.py`.
        chargeur = TestDataLoader()

        # Chargement des données à analyser.
        data = chargeur.get_data()

        # Initialisation de la classe `Analyse`.
        analyse = Analyse()

        # Analyse de données
        resultat = analyse.get_descriptive_stats(df=data)

        print(resultat.head())

        assert resultat is not None
        assert isinstance(resultat, pd.DataFrame)
        assert len(resultat) > 0
