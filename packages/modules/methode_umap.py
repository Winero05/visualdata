from typing import Union
import pandas as pd
import numpy as np
import umap

class MethodeUMAP:
    def __init__(self, df: Union[pd.DataFrame, np.ndarray, str]):
        self.df = df
    
    def umap_reduction(self, nombre_de_dimension = 1) -> np.ndarray:
        _umap = umap.UMAP(n_components= nombre_de_dimension)
        X_umap = _umap.fit_transform(self.df)
        return X_umap
        