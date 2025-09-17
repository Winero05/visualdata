# main.py

# --- Section 1: Importations ---
# Importez les classes et fonctions du paquet packages
from packages.modules.loading import DataLoader
from packages.modules.netoyage import handle_missing_values
from packages.modules.analysis import summarize
from packages.modules.visualisation_image import ImageVisualizer
from packages.modules.visualisation_texte import TextVisualizer
from packages.modules.visualisation_csv import TabularVisualizer
from packages.modules.visualisation_csv_2D

def main():
    """Chargement des données.
    """
    # path = input("C:/Users/LENOVO/Downloads/Products.csv")
    
    path = "Projet_stage/packages/data/csv/TB_CATEGORIE.csv"

    print(f"Vous avez saisi : {path}")

    dataloader = DataLoader()
    df = dataloader.load(path)
    dfn = handle_missing_values(df, strategy="fill", column="Sleep Disorder")
    resume = summarize(dfn)
    
if __name__ == "__main__":
    main()