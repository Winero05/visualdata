from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from loading import DataLoader


intance_de_class = DataLoader()

chemin_de_donnees = "Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"

df = intance_de_class.load(chemin_de_donnees)

X = df["Sleep Duration"].values

Y = df["Quality of Sleep"].values

normalisation = StandardScaler()

X_normaliser = normalisation.fit_transform(X)

acp = PCA()

X_acp = acp(X_normaliser)

# X_acp = df[nom_colonne] # Les valeurs d'entrées

# # Réduction de dimension avec PCA
# pca = PCA(n_components=3)
# X_acp = pca.fit_transform(X)

# # Graphiques interactifs 3D
# fig_pca = px.scatter_3d(
#     x=X_pca[:, 0], y=X_pca[:, 1], z=X_pca[:, 2],
#     color=y.astype(str), title="PCA en 3D (Interactif)",
#     labels={"x": "PC1", "y": "PC2", "z": "PC3"}
# )
# fig_pca.show()