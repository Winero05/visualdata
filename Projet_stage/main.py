# main.py

# --- Section 1: Importations ---
# Importez les classes et fonctions du paquet data_loader
from data_loader.loading import DataLoader
from data_loader.netoyage import handle_missing_values
from data_loader.analysis import summarize
from data_loader.visualisation_image import ImageVisualizer
from data_loader.visualisation_texte import TextVisualizer
from data_loader.visualisation_tabulaire import TabularVisualizer
def main():
    chemin = input("C:/Users/LENOVO/Downloads/Products.csv")

    print(f"Vous avez saisi : {chemin}")
    '''
    # Exemple : ouvrir et lire le fichier
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
            print("=== Contenu du fichier ===")
            print(contenu)
    except FileNotFoundError:
        print("⚠️ Fichier introuvable. Vérifiez le chemin.")
    except Exception as e:
        print("⚠️ Erreur :", e)
    '''
    dataloader = DataLoader()
    df = dataloader.load(chemin)
    dfn = handle_missing_values(df)
    resume = summarize(dfn)
    
if __name__ == "__main__":
    main()