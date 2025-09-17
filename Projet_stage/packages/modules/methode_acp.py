from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from loading import DataLoader
from analysis import Analyse

class MethodePCA:
    """Méthode de réduction de dimenssion avec l'ACP."""
    
    def __init__(self, chemin_de_donnees=None):
        if chemin_de_donnees == None:
            raise TypeError("Le chemin entré ne permet pas d'accéder aux données.")
        else:
            self.chemin_de_donnees = chemin_de_donnees
            # return self.chemin_de_donnees

    def pca_reduction(self, nombre_dimenssion = 1):
        if self.chemin_de_donnees == None:
            raise ValueError("\nLa méthode de réduction APC exige l'usage d'un DataFrame, veuillez controler la source de vos données.\n")
        else:
            intance_de_chargement = DataLoader()

            # chemin_de_donnees = "Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"

            df = intance_de_chargement.load(self.chemin_de_donnees)
            
            # df_no_header_no_row_1 = df.values.copy()
            
            df_no_header_no_row_1 = Analyse.donnees_numerique_unique(df)
            
            print(df_no_header_no_row_1.head())
            
            # df_copy_no_header.rename(SansEspace.sansEspace, axis="columns", inplace=True)

            normalisation = StandardScaler()

            X_normaliser = normalisation.fit_transform(df_no_header_no_row_1)

            print(type(X_normaliser))
            
            print(X_normaliser.shape)
            
            print(X_normaliser)
            
            acp = PCA(n_components=nombre_dimenssion) # n_components mentionne les axes (dimenssions)

            X_acp = acp.fit_transform(X_normaliser)
            
            return X_acp, df

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