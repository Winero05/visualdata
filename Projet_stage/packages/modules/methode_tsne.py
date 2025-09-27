from typing import Union
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE

class MethodeTSNE:
    def __init__(self, df: Union[pd.DataFrame, np.ndarray, str]):
        self.df = df
    
    def tsne_reduction(self, nombre_de_dimension = 1) -> np.ndarray:
        tsne = TSNE(n_components= nombre_de_dimension)
        X_tsne = tsne.fit_transform(self.df)
        return X_tsne
        