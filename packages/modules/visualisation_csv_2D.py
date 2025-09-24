#visualisation_csv_2D
from methode_acp import MethodePCA # Supposant la version refactorisée
from loading import DataLoader
import plotly.express as px
import pandas as pd
import numpy as np

def preprocess_sleep_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prétraite les données sur le sommeil pour l'analyse."""
    # Gérer les valeurs manquantes si nécessaire
    df.fillna(0, inplace=True) # Stratégie simple, à adapter
    
    # Séparer la tension artérielle
    if 'Blood Pressure' in df.columns:
        df[['Systolic', 'Diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
        df = df.drop(columns=['Blood Pressure'])
        
    # Encodage simple des variables catégorielles (à améliorer avec get_dummies si besoin)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category').cat.codes
        
    return df

def main():
    chemin_de_donnees = "Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"
    
    # 1. Chargement et préparation
    loader = DataLoader()
    df_original = loader.load(chemin_de_donnees)
    df_processed = preprocess_sleep_data(df_original.copy())

    # 2. Réduction de dimension
    pca_instance = MethodePCA(n_components=2)
    X_pca = pca_instance.fit_transform(df_processed)

    # 3. Visualisation
    title = "Visualisation ACP en 2D des données sur le sommeil"
    fig = px.scatter(
        x=X_pca[:, 0],
        y=X_pca[:, 1],
        color=df_original["Quality of Sleep"], # Colorer par une variable pertinente
        title=title,
        labels={"x": "Composante Principale 1", "y": "Composante Principale 2", "color": "Qualité du sommeil"}
    )
    fig.show()

if __name__ == "__main__":
    main()