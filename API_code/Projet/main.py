# main.py

# --- Section 1: Importations ---
# Importez les classes et fonctions du paquet packages
from packages.modules.loading import DataLoader
from packages.modules.netoyage import handle_missing_values, handle_duplicates
from packages.modules.analysis import Analyse
from packages.modules.visualisation_image import ImageVisualizer
from packages.modules.visualisation_texte import TextVisualizer
from packages.modules.visualisation_csv import TabularVisualizer


def main():
    """Chargement des données.
    """
    # path = input("C:/Users/LENOVO/Downloads/Products.csv")
    
    path = input("C:/Users/User/Downloads/dataset_200_fixed.csv")

    print(f"Vous avez saisi : {path}")

    dataloader = DataLoader()
    df = dataloader.load(path)
    print("Original DataFrame:")
    print(df)
    resume = Analyse.summarize(df)
    print("\nSummary:")
    print(resume)

if __name__ == "__main__":
    main()
