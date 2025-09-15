# data_loader/__init__.py
from .loading import DataLoader
from .netoyage import handle_missing_values 
from .netoyage import handle_duplicates
from .analysis import summarize, get_descriptive_stats
#from .visualization import cluster_colors, visualize_wordcloud, visualize_distributions, visualize_correlation
from .visualisation_image import ImageVisualizer
from .visualisation_texte import TextVisualizer
from .visualisation_tabulaire import TabularVisualizer