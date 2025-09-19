# Test de la class MethodePCA du module Projet_stage/packages/modules/methode_acp.py

import pandas as pd
import plotly.express as px

from packages.modules.methode_acp import MethodePCA

chemin_de_donnees = "Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"

apc_2d_instance = MethodePCA(chemin_de_donnees=chemin_de_donnees)

X_acp, df = apc_2d_instance.pca_reduction(nombre_dimenssion=2)

print(df.head())
print(X_acp.head())