"""Tester le module `Projet_stage/backend/modules/clean_dataframe_for_json.py`.
"""

from modules.clean_dataframe_for_json import CleanDataframeForJson
from tests.modules.test_loading import TestDataLoader

class TestCleanDataframeForJson:
    """Test la classe `CleanDataframeForJson`.
    """

    def test_clean_dataframe_for_json(self) -> None:
        """Test la méthode `clean_dataframe_for_json`."""

        # Instanciation des classes.
        chargeur_data = TestDataLoader()
        chargeur_dataframe_for_json = CleanDataframeForJson()
        data = chargeur_data.get_data()
        data_df_json = chargeur_dataframe_for_json.clean_dataframe_for_json(df=data)
        print(data_df_json.head())
