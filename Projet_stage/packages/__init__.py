# data_loader/__init__.py
from .modules.loading import DataLoader
from .modules.netoyage import handle_missing_values 
from .modules.netoyage import handle_duplicates
from .modules.analysis import summarize, get_descriptive_stats
#from .visualization import cluster_colors, visualize_wordcloud, visualize_distributions, visualize_correlation
from .modules.visualisation_image import ImageVisualizer
from .modules.visualisation_texte import TextVisualizer
from .modules.visualisation_csv import TabularVisualizer