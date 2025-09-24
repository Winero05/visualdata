# main.py

# NOTE: Ce fichier est un script de test local et n'est pas utilisé par l'API FastAPI.
# L'API est lancée avec la commande `uvicorn api:app --reload`.
# --- Section 1: Importations ---
# Importez les classes et fonctions du paquet packages
from packages.modules.loading import DataLoader
from packages.modules.netoyage import handle_missing_values, handle_duplicates
from packages.modules.analysis import Analyse
from packages.modules.visualisation_image import ImageVisualizer
from packages.modules.visualisation_texte import TextVisualizer
from packages.modules.visualisation_csv import TabularVisualizer


def main():
    """
    Fonction principale pour tester les modules en local, en dehors de l'API.
    """
    # Exemple de chemin, à adapter sur votre machine
    path = "C:/Users/User/Downloads/dataset_200_fixed.csv"

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
