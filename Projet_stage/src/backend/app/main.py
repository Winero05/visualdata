from fastapi import FastAPI
from app.services.dimensionality_reduction import apply_pca , apply_tsne, apply_umap
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Autoriser le frontend à accéder au backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # tu peux mettre ["http://localhost:5500"] par ex.
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS...
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Bienvenue dans l’API de visualisation de données"}

@app.post("/reduce/pca")
def pca_endpoint():
    return apply_pca()

@app.post("/reduce/tsne")
def tsne_endpoint():
    return apply_tsne()

@app.post("/reduce/umap")
def umap_endpoint():
    return apply_umap()
