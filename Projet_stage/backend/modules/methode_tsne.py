"""Module de réduction de dimmension avec la méthode t-SNE.

Returns:
    ndarray: Matrice de données obtenu après réduction avec t-SNE.
"""

from typing import Union
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MethodeTSNE:
    """Classe de réduction de dimension avec la méthode t-SNE.
    """

    df: Union[pd.DataFrame, np.ndarray, str]

    def tsne_reduction(self, nombre_de_dimension: int = 1) -> np.ndarray:
        """Méthode de réduction de dimension avec t-SNE.

        Args:
            nombre_de_dimension (int, optional): Le nombre de dimension de réduction. Defaults to 1.

        Returns:
            np.ndarray: Matrice de données réduite.
        """

        tsne = TSNE(n_components= nombre_de_dimension)

        x_tsne = tsne.fit_transform(self.df)

        return x_tsne
