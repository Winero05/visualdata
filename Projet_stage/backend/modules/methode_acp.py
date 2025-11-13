"""Modules de réduction de dimention avec la méthode ACP.

Classes:
    MethodeACP:
        Réduction de dimenssion avec l'ACP.

        df: Union[pd.DataFrame, np.ndarray, str]

        Methodes:
            acp_reduction(self, nombre_dimenssion: int = 1) -> np.ndarray:
                Méthode de réduction d'ACP

                Args:
                    nombre_dimenssion (int, optional): Le nombre de dimention de réduction. Defaults to 1.

                Returns:
                    ndarray: Matrice construite par la méthode d'ACP.
Returns:
    ndarray: Matrice construite par la méthode d'ACP.
"""

from typing import Union
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class MethodeACP:
    """Réduction de dimenssion avec l'ACP."""

    df: Union[pd.DataFrame, np.ndarray, str]

    def acp_reduction(self, nombre_dimenssion: int = 1) -> np.ndarray:
        """Méthode de réduction d'ACP

        Args:
            nombre_dimenssion (int, optional): Le nombre de dimention de réduction. Defaults to 1.

        Returns:
            ndarray: Matrice construite par la méthode d'ACP.
        """

        normalisation = StandardScaler()

        x_normaliser = normalisation.fit_transform(self.df)

        acp = PCA(n_components=nombre_dimenssion) # n_components mentionne les axes (dimenssions)

        x_acp = acp.fit_transform(x_normaliser)

        x_reconstructed = acp.inverse_transform(x_acp)

        return x_reconstructed
