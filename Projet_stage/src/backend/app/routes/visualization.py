from fastapi import APIRouter
from app.services.dimensionality_reduction import apply_pca, apply_tsne, apply_umap

router = APIRouter()

@router.get("/reduce/pca")
def reduce_with_pca():
    result = apply_pca()
    return {"x": result[:, 0].tolist(), "y": result[:, 1].tolist()}

# @router.get("/reduce/tsne")
# def reduce_with_tsne():
#     result = apply_tsne()
#     return {"x": result[:, 0].tolist(), "y": result[:, 1].tolist()}

# @router.get("/reduce/umap")
# def reduce_with_umap():
#     result = apply_umap()
#     return {"x": result[:, 0].tolist(), "y": result[:, 1].tolist()}
