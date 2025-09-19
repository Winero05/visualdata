from methode_acp import MethodePCA
# from ..modules.methode_tsne
# from ..modules.methode_umap
import plotly.express as px
import pandas as pd

chemin_de_donnees = "Projet_stage/packages/data/csv/Ensemble_de_données_sur_la_sante_du_sommeil_et_le_mode_de_vie/Sleep_health_and_lifestyle_dataset.csv"

apc_2d_instance = MethodePCA(chemin_de_donnees=chemin_de_donnees)



X_acp, df = apc_2d_instance.pca_reduction(nombre_dimenssion=2)

title = "Méthode de réduction ACP en 2D."

fig = px.scatter(
        x=X_acp,
        y= df["Quality of Sleep"],
        title=title,
        labels={"x": "Sleep Duration", "y": "Quality of Sleep"}
    )


fig.show()