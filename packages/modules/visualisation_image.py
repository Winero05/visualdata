#visualisation_image.py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import os

class ImageVisualizer:
    def __init__(self, image_path: str = None):
        self.image_path = None
        self.image = None
        self.image_array = None
        if image_path:
            self.load_image_from_path(image_path)

    def load_image_from_path(self, image_path: str):
        """Charge une image depuis un chemin de fichier."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier {image_path} est introuvable")
        self.image_path = image_path
        self.image = Image.open(image_path).convert("RGB")
        self.image_array = np.array(self.image)

    def load_image_from_object(self, file_object):
        """Charge une image depuis un objet fichier (ex: UploadFile)."""
        self.image = Image.open(file_object).convert("RGB")
        self.image_array = np.array(self.image)
        self.image_path = None # Pas de chemin de fichier dans ce cas

    def _check_image_loaded(self):
        if self.image is None:
            raise ValueError("Aucune image n'a été chargée. Utilisez 'load_image_from_path' ou 'load_image_from_object'.")

    def show_image(self, title="Image originale", retourner_fig=False):
        """Affichage simple de l'image"""
        fig, ax = plt.subplots()
        ax.imshow(self.image)
        ax.axis("off")
        ax.set_title(title)
        if retourner_fig:
            return fig
        plt.show()

    def show_multiple(self, images, titles=None, retourner_fig=False):
        """Affichage de plusieurs images côte à côte"""
        n = len(images)
        fig, axes = plt.subplots(1, n, figsize=(15, 5))
        for i, img in enumerate(images):
            ax = axes[i] if n > 1 else axes
            ax.imshow(img)
            ax.axis("off")
            if titles:
                ax.set_title(titles[i])
        if retourner_fig:
            return fig
        plt.show()

    def histogram_intensity(self, retourner_fig=False):
        """Histogramme des intensités par canal"""
        self._check_image_loaded()
        colors = ("r", "g", "b")
        fig, ax = plt.subplots(figsize=(8, 5))
        for i, col in enumerate(colors):
            hist = cv2.calcHist([self.image_array], [i], None, [256], [0, 256])
            ax.plot(hist, color=col)
        ax.set_title("Histogramme des intensités (R, G, B)")
        ax.set_xlabel("Valeurs de pixels")
        ax.set_ylabel("Fréquence")
        if retourner_fig:
            return fig
        plt.show()

    def heatmap_gray(self, retourner_fig=False):
        """Visualisation en heatmap de l'image en niveaux de gris"""
        self._check_image_loaded()
        gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        fig, ax = plt.subplots()
        im = ax.imshow(gray, cmap="hot")
        fig.colorbar(im, ax=ax)
        ax.set_title("Heatmap (niveaux de gris)")
        if retourner_fig:
            return fig
        plt.show()

    def edges(self, retourner_fig=False):
        """Détection des contours avec Canny"""
        self._check_image_loaded()
        gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        fig, ax = plt.subplots()
        ax.imshow(edges, cmap="gray")
        ax.set_title("Contours (Canny)")
        ax.axis("off")
        if retourner_fig:
            return fig
        plt.show()

    def pixel_scatter(self, n_points=5000, retourner_fig=False):
        """Nuage de pixels dans l’espace RGB"""
        self._check_image_loaded()
        pixels = self.image_array.reshape(-1, 3)
        idx = np.random.choice(len(pixels), size=min(n_points, len(pixels)), replace=False)
        sample = pixels[idx]

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(projection="3d")
        ax.scatter(sample[:, 0], sample[:, 1], sample[:, 2],
                   c=sample / 255.0, marker=".")
        ax.set_xlabel("Rouge")
        ax.set_ylabel("Vert")
        ax.set_zlabel("Bleu")
        ax.set_title("Nuage de pixels (espace RGB)")
        if retourner_fig:
            return fig
        plt.show()

# === Exemple d'utilisation ===
if __name__ == "__main__":
    path = "Projet_stage/packages/data/img/Capture001.png"  # Remplacer par vôtre chemin
    visualizer = ImageVisualizer(path)

    visualizer.show_image()
    visualizer.histogram_intensity()
    visualizer.heatmap_gray()
    visualizer.edges()
    visualizer.pixel_scatter()
