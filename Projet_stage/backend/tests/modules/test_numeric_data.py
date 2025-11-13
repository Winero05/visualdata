"""Test du module `Projet_stage/backend/modules/numeric_data.py`.

Returns:
    pd.DataFrame: Un tableau de données numérique est retourné.
"""

from tests.modules.test_loading import TestDataLoader
from modules.numeric_data import NumericData
import pandas as pd

class TestNumericData:
    """
    TestNumericData
    ---------------

    Unit test container for validating numeric column extraction from tabular data
    using the NumericData helper.
    This test class relies on a TestDataLoader to provide example data and on the
    NumericData class to perform extraction of numeric columns.

    Methods
    -------

    - test_numeric_colonne(self)
        - Purpose: Execute an end-to-end assertion that NumericData.num_col() returns
            a non-None result when provided with the sample dataset.
        - Behavior: Instantiates TestDataLoader, obtains a DataFrame-like object,
            constructs a NumericData instance with that DataFrame, calls num_col(),
            and asserts the returned value is not None.
        - Expected outcome: The test passes if num_col() yields a valid tabular
            representation (e.g., DataFrame, dict, or list) of numeric columns.
    - send_numeric_data(self)
        - Purpose: Helper method to obtain and return the numeric-only tabular data
            produced by NumericData.num_col() for reuse in other tests or assertions.
        - Behavior: Mirrors the setup in test_numeric_colonne but returns the result
            instead of asserting on it.
        - Note: As named, this is a utility and not discovered as a test by typical
            testing frameworks; treat it as a support method for test composition.

    Dependencies
    ------------

    - TestDataLoader: must implement get_data() and provide representative test data.
    - NumericData: must accept a DataFrame-like object via df= and implement num_col().

    Usage guidance
    --------------

    - Ensure TestDataLoader returns a structure compatible with NumericData.num_col().
    - Consider adding explicit type/structure assertions to validate the exact shape
        and type of the returned numeric data for stronger tests.
    """

    def test_numeric_colonne(self) -> None:
        """
        Test that NumericData.num_col() returns numeric columns from the loaded dataset.
        This test verifies that:
        - Data can be loaded using TestDataLoader
        - NumericData class properly initializes with the loaded dataframe
        - num_col() method returns a non-None result containing numeric columns
        Raises:
            AssertionError: If donnees_tabulaire is None
        """
        chargeur_de_donnees = TestDataLoader()

        data = chargeur_de_donnees.get_data()

        chargeur_num_col = NumericData(df=data)

        donnees_tabulaire = chargeur_num_col.num_col()

        assert donnees_tabulaire is not None

    def send_numeric_data(self) -> pd.DataFrame:
        """
        Load test data and return only the numeric columns as a pandas DataFrame.
        This helper method performs the following steps:
        1. Instantiate TestDataLoader and load the raw test dataset via get_data().
        2. Create a NumericData processor with the loaded DataFrame.
        3. Call NumericData.num_col() to extract/return the numeric-only tabular data.
        Returns:
            pd.DataFrame: A DataFrame containing the numeric columns extracted from the test dataset.
                          Column order and dtype are determined by NumericData.num_col().
        Raises:
            Any exception raised by TestDataLoader.get_data() or NumericData.num_col() is propagated.
            For example, errors may occur if the test data cannot be loaded, if the returned object
            is not a DataFrame, or if no numeric columns are present (behavior depends on NumericData).
        Notes:
            - This method does not mutate the original loaded DataFrame; it returns the processed result.
            - Intended for use in testing contexts to obtain numeric-only tabular fixtures.
        """
        chargeur_de_donnees = TestDataLoader()

        data = chargeur_de_donnees.get_data()

        chargeur_num_col = NumericData(df=data)

        donnees_tabulaire_numeric = chargeur_num_col.num_col()

        return donnees_tabulaire_numeric
