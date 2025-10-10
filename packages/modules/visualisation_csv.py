"""Visualisation tabulaire légère (placeholder): afficher head, info, histogrammes basiques."""

import pandas as pd

class TabularVisualizer:
    """Outils pour visualiser rapidement des DataFrame."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def head(self, n=5):
        return self.df.head(n)

    def info(self):
        buf = []
        buf.append(f"shape: {self.df.shape}")
        buf.append(self.df.dtypes.to_string())
        return "\n".join(buf)

    def describe(self):
        return self.df.describe()


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame({'a': [1,2,3], 'b': ['x','y','z']})
    viz = TabularVisualizer(df)
    print(viz.head())
    print(viz.info())
