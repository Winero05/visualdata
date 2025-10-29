# Contenu de test_visualisation_image.py

from backend.modules.visualisation_image import ImageVisualizer

class TestImageVisualizer:
    def test_show_image(self):
        chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
        chargeur_img = ImageVisualizer(chemin)
        
        chargeur_img.show_image()
    
    # def test_show_multiple_image(self):
    #     chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
    #     chargeur_img = ImageVisualizer(chemin)
        
    #     chargeur_img.show_multiple_image()
    
    def test_histogram_intensity(self):
        chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
        chargeur_img = ImageVisualizer(chemin)
        
        chargeur_img.histogram_intensity()
    
    def test_heatmap_gray(self):
        chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
        chargeur_img = ImageVisualizer(chemin)
        
        chargeur_img.heatmap_gray()

    def test_edges(self):
        chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
        chargeur_img = ImageVisualizer(chemin)
        
        chargeur_img.edges()

    def test_pixel_scatter(self):
        chemin = "/home/adama/visualdata/Projet_stage/packages/data/img/bracelet.jpg"
        
        chargeur_img = ImageVisualizer(chemin)
        
        chargeur_img.pixel_scatter()
