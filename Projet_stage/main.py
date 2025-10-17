from packages.modules.loading import DataLoader
from packages.modules.analysis import Analyse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
from packages.modules.visualisation_2D import Visualisation_2D
from packages.modules.visualisation_3D import Visualisation_3D

app = FastAPI()

# Autoriser le frontend à accéder au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fichiers à charger
data_path_1 = "C:\Users\adama\3D Objects\schoolProjet\courS6\projet_de_stage\visualdata\Projet_stage\packages\data\csv\Ensemble_de_donnees_sur_la_sante_du_sommeil_et_le_mode_de_vie\Sleep_health_and_lifestyle_dataset.csv"
data_path_2 = "C:\Users\adama\3D Objects\schoolProjet\courS6\projet_de_stage\visualdata\Projet_stage\packages\data\csv\Sante_mental_des_etudiants\Student_Mental_health.csv"
file_path = "C:\Users\adama\3D Objects\schoolProjet\courS6\projet_de_stage\visualdata\Projet_stage\tests\data\csv\insurance.csv"

# Endpoints
url_send_data_1_on_server = "/v_01/data_1"
url_send_data_2_on_server = "/v_01/data_2"
url_read_data_on_server = "/v_01/loading_data/"
url_analyse_data = "/v_01/analyse/"
url_visualisation_2d = "/v_01/visualisation_2d/"
url_visualisation_3d = "/v_01/visualisation_3d/"

# Classes
chargeur_data = DataLoader()
chargeur_analyse = Analyse()

@app.get('/')
def root():
    return {"message": "Le serveur tourne sans problème..."}

@app.post(url_send_data_1_on_server)
def endpoint_data_1():
    data_1 = chargeur_data.load(file_path=data_path_1)
    return data_1.to_dict(orient="records")

@app.post(url_send_data_2_on_server)
def endpoint_data_2():
    data_2 = chargeur_data.load(file_path=data_path_2)
    return data_2.to_dict(orient="records")

@app.get(url_read_data_on_server)
def endpoint_data_loading():
    df = chargeur_data.load(file_path=file_path)
    return df.to_dict(orient="records")

@app.post(url_analyse_data)
def endpoint_data_analyse():
    df = chargeur_data.load(file_path=file_path)
    df_summarize = chargeur_analyse.summarize(df)
    return df_summarize.to_dict(orient="records")

@app.post(url_visualisation_2d)
def endpoint_data_visualisation_2d():
    df = chargeur_data.load(file_path=file_path)
    chargeur_visualisation_2d = Visualisation_2D(df=df)
    return chargeur_visualisation_2d.visualisation_automatique()

@app.post(url_visualisation_3d)
def endpoint_data_visualisation_3d():
    df = chargeur_data.load(file_path=file_path)
    chargeur_visualisation_3d = Visualisation_3D(df=df)
    return chargeur_visualisation_3d.visualisation_automatique()
