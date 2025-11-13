"""Ce modules se charge de retourner un tableau de données contenant
des données numérique uniquement (int, float, etc.)

Returns:
    pd.DataFrame: Nouveau tableau de données numérique uniquement.
"""

from dataclasses import dataclass
import pandas as pd
from pandas.api.types import is_numeric_dtype

@dataclass
class NumericData:
    """
    NumericData
    -----------
    Utility class for extracting numeric columns from a tabular dataset.

    Attributes
    ----------

        df pd.DataFrame:
            Input dataset. Expected to be a pandas DataFrame; other types are accepted
            by annotation but should be converted or assigned such that column access
            (self.df.columns and self.df[col]) is valid.

    Methods
    -------
        num_col() -> pd.DataFrame

            Return a pandas DataFrame containing only the columns of self.df whose
            dtypes are numeric (as determined by pandas.api.types.is_numeric_dtype).
            Non-numeric columns are omitted. If no numeric columns are found, an
            empty DataFrame is returned.

    Notes
    -----
        - This class relies on pandas' dtype detection; mixed-type or object columns
            that contain numeric-like values will not be selected unless their dtype
            is numeric.
        - The returned DataFrame is newly constructed from the selected columns,
            preserving original column order.

    Example
    -------
        >>> df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"], "c": [3.0, 4.5]})
        >>> nd = NumericData(df=df)
        >>> nd.num_col()
           a    c
        0  1  3.0
        1  2  4.5
    """

    df: pd.DataFrame

    def num_col(self) -> pd.DataFrame:
        """Méthode de sélection des colonne numérique dans un tableau.

        Returns:
            pd.DataFrame: Table de données numérique est retourné.
        """
        # Sélection des données de type numérique (int, float etc) dans un dictionnaire
        data = {col: self.df[col] for col in self.df.columns if is_numeric_dtype(self.df[col])}
        return pd.DataFrame(data=data)
