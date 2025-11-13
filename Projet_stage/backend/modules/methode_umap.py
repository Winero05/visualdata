"""Module de réduction de dimension avec la méthode UMAP.

Returns:
    np.ndarray: Matrice de réduction de données obtenu grâce à la méthode UMAP.
"""

from typing import Union
import pandas as pd
import numpy as np
import umap
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MethodeUMAP:
    """Classe de réduction de dimension avec la méthode UMAP.
    """

    df: Union[pd.DataFrame, np.ndarray, str]

    def umap_reduction(self, nombre_de_dimension: int = 1) -> np.ndarray:
        """Méthode de réduction de dimension UPAM.

        Args:
            nombre_de_dimension (int, optional): _description_. Defaults to 1.

        Returns:
            np.ndarray: Matrice de réduction de données obtenu grâce à la méthode UMAP.
        """

        _umap = umap.UMAP(n_components= nombre_de_dimension)

        x_umap = _umap.fit_transform(self.df)

        return x_umap
