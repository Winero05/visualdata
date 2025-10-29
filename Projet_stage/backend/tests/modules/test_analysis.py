# Contenue test/test_analysis.py

from tests.test_loading import TestDataLoader
from backend.modules.analysis import Analyse

class TestAnalyse:
    """
    Test la class `Analyse` des données du fichier `analysis.py`.
    """
    def test_summarize(self):
        """
        Analyse des données.
        
        Description: Voir le nombre de `ligne` et de `colonne`, le `type des colonne` à analyser, les `valeurs manquantes` des colonnes, les `valeurs dupliquées`.
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
