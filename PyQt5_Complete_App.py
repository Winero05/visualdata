"""
Application PyQt5 complète de visualisation de données
Avec support PCA, t-SNE, UMAP et visualisations 2D/3D
Couleurs: Bleu (#3b82f6), Violet (#8b5cf6), Jaune (#fbbf24)
"""

import sys
import json
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem,
    QTextEdit, QTableWidget, QTableWidgetItem, QComboBox, QTabWidget,
    QScrollArea, QFrame, QSplitter, QDialog, QGridLayout, QGroupBox,
    QRadioButton, QButtonGroup, QMessageBox, QSizePolicy
)
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from packages.modules.loading import DataLoader
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette, QDragEnterEvent, QDropEvent, QIcon, QCursor

# Local DB for history
try:
    from . import db
except Exception:
    # fallback if run as script from same folder
    import db

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Qt5Agg')
import traceback
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines

# Essayer d'importer UMAP (optionnel)
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    print("UMAP non disponible. Installez avec: pip install umap-learn")


# ==================== COULEURS THEME ====================
class Theme:
    """Couleurs du thème de l'application"""
    BLUE = "#3b82f6"
    VIOLET = "#8b5cf6"
    YELLOW = "#fbbf24"
    BLUE_LIGHT = "rgba(59, 130, 246, 0.1)"
    VIOLET_LIGHT = "rgba(139, 92, 246, 0.1)"
    YELLOW_LIGHT = "rgba(251, 191, 36, 0.1)"
    GRADIENT_BLUE_VIOLET = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(59, 130, 246, 0.2), stop:1 rgba(139, 92, 246, 0.2))"
    GRADIENT_YELLOW_VIOLET = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(251, 191, 36, 0.2), stop:1 rgba(139, 92, 246, 0.2))"
    GRADIENT_BLUE_YELLOW = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(59, 130, 246, 0.1), stop:1 rgba(251, 191, 36, 0.1))"
    BORDER_BLUE = f"border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 8px;"
    BORDER_VIOLET = f"border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 8px;"
    BORDER_YELLOW = f"border: 2px solid rgba(251, 191, 36, 0.3); border-radius: 8px;"


# ==================== ZONE DE DEPOT DE FICHIERS ====================
class DropZone(QFrame):
    """Zone de glisser-déposer pour les fichiers"""
    fileDropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Icône Upload (simulé avec texte)
        '''icon_label = QLabel("📤")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(f"font-size: 72px; color: {Theme.VIOLET};")'''
        
        # Titre
        '''title = QLabel("Glissez un fichier ici pour commencer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {Theme.VIOLET}; margin: 20px;")'''
        
        # Sous-titre
        subtitle = QLabel("Utilisez le bouton de chargement à gauche")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; margin-bottom: 30px;")
        
        # Grid des formats supportés
        formats_widget = QWidget()
        formats_layout = QGridLayout()

        formats = [
            ("\ud83d\udcca", "CSV", Theme.BLUE),
            ("\ud83d\udcc4", "TXT", Theme.VIOLET),
            ("\ud83d\uddbc\ufe0f", "Images", Theme.YELLOW),
            ("{ }", "JSON", Theme.BLUE),
            ("\ud83d\uddc4\ufe0f", "SQL", Theme.VIOLET)
        ]

        for i, (icon, name, color) in enumerate(formats):
            format_frame = QFrame()
            format_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {color.replace('#', 'rgba(') + ', 0.1)'};
                    border-radius: 8px;
                    padding: 15px;
                }}
            """)
            format_layout = QVBoxLayout()

            icon_lbl = QLabel(icon)
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet("font-size: 32px;")

            name_lbl = QLabel(name)
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(f"color: {color}; font-weight: bold;")

            format_layout.addWidget(icon_lbl)
            format_layout.addWidget(name_lbl)
            format_frame.setLayout(format_layout)

            formats_layout.addWidget(format_frame, 0, i)

        formats_widget.setLayout(formats_layout)
        
        # Message formats supportés
        formats_msg = QLabel("Formats supportés: CSV, TXT, PNG, JPG, JPEG, BMP, JSON, SQL")
        formats_msg.setAlignment(Qt.AlignCenter)
        formats_msg.setStyleSheet(f"""
            background: {Theme.GRADIENT_BLUE_YELLOW};
            {Theme.BORDER_VIOLET}
            padding: 15px;
            margin: 20px 50px;
            color: gray;
        """)
        
        #layout.addWidget(icon_label)
        #layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(formats_widget)
        layout.addWidget(formats_msg)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                border: 4px dashed rgba(139, 92, 246, 0.4);
                border-radius: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.05), 
                    stop:0.5 rgba(139, 92, 246, 0.05), 
                    stop:1 rgba(251, 191, 36, 0.05));
            }}
        """)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                QFrame {{
                    border: 4px dashed {Theme.BLUE};
                    border-radius: 16px;
                    background-color: rgba(59, 130, 246, 0.1);
                }}
            """)
            
    def dragLeaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame {{
                border: 4px dashed rgba(139, 92, 246, 0.4);
                border-radius: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.05), 
                    stop:0.5 rgba(139, 92, 246, 0.05), 
                    stop:1 rgba(251, 191, 36, 0.05));
            }}
        """)
        
    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.fileDropped.emit(files[0])
        self.dragLeaveEvent(None)


# ==================== SECTION CHARGEMENT DE FICHIERS ====================
class FileUploadSection(QWidget):
    """Section de chargement de fichiers (1/6 gauche haut)"""
    fileLoaded = pyqtSignal(dict)
    fileSelected = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.loaded_files = []
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Header avec gradient
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: {Theme.GRADIENT_BLUE_VIOLET};
                {Theme.BORDER_BLUE}
                padding: 10px;
            }}
        """)
        header_layout = QVBoxLayout()
        
        title = QLabel("Chargement")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        subtitle = QLabel("Fichiers internes")
        subtitle.setStyleSheet(f"color: {Theme.VIOLET};")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header.setLayout(header_layout)
        
        # Zone de drop (petite)
        drop_frame = QFrame()
        drop_frame.setStyleSheet(f"""
            QFrame {{
                border: 2px dashed rgba(139, 92, 246, 0.3);
                border-radius: 8px;
                background-color: rgba(139, 92, 246, 0.05);
                padding: 20px;
            }}
        """)
        #drop_layout = QVBoxLayout()
        #drop_icon = QLabel("📤")
        #drop_icon.setAlignment(Qt.AlignCenter)
        #drop_icon.setStyleSheet(f"font-size: 32px; color: {Theme.VIOLET};")
        #drop_text = QLabel("Glissez un fichier ici")
        #drop_text.setAlignment(Qt.AlignCenter)
        #drop_text.setStyleSheet(f"color: {Theme.VIOLET};")
        #drop_layout.addWidget(drop_icon)
        #drop_layout.addWidget(drop_text)
        #drop_frame.setLayout(drop_layout)
        drop_frame.setAcceptDrops(True)
        
        # Bouton de chargement principal
        btn_load = QPushButton("📁 Charger un fichier")
        btn_load.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {Theme.BLUE}, stop:1 {Theme.VIOLET});
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {Theme.VIOLET}, stop:1 {Theme.BLUE});
            }}
        """)
        btn_load.clicked.connect(self.loadFile)
        
        formats_label = QLabel("CSV, TXT, Images, JSON, SQL")
        formats_label.setAlignment(Qt.AlignCenter)
        formats_label.setStyleSheet(f"color: {Theme.VIOLET}; font-size: 11px;")
        

         # Bouton exemple ligne 264
        '''btn_example = QPushButton("📊 Charger exemple")
        btn_example.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.YELLOW};
                border: 2px solid {Theme.YELLOW};
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(251, 191, 36, 0.1);
            }}
        """)
        btn_example.clicked.connect(self.loadExample)
        '''


        # Liste des fichiers chargés
        files_header = QFrame()
        files_header.setStyleSheet(f"""
            QFrame {{
                background: {Theme.GRADIENT_YELLOW_VIOLET};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        files_title = QLabel("Fichiers chargés")
        files_title.setStyleSheet("font-weight: bold;")
        files_header_layout = QVBoxLayout()
        files_header_layout.addWidget(files_title)
        files_header.setLayout(files_header_layout)
        
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 6px;
            }
            QListWidget::item:hover {
                background-color: rgba(139, 92, 246, 0.1);
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(59, 130, 246, 0.2), stop:1 rgba(139, 92, 246, 0.2));
                border: 1px solid rgba(139, 92, 246, 0.4);
            }
        """)
        self.file_list.itemClicked.connect(self.onFileItemClicked)
        
        # Layout assembly
        layout.addWidget(header)
        layout.addWidget(drop_frame)
        layout.addWidget(btn_load)
        layout.addWidget(formats_label)
        # Toggle button to show/hide the loaded files list (dropdown-like)
        self.btn_toggle_files = QPushButton("Voir fichiers chargés ▾")
        self.btn_toggle_files.setCheckable(True)
        self.btn_toggle_files.setChecked(False)
        self.btn_toggle_files.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Theme.VIOLET};
                border: 1px solid rgba(139,92,246,0.12);
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }}
        """)
        self.btn_toggle_files.clicked.connect(self.toggleFilesList)
        layout.addWidget(self.btn_toggle_files)
        #layout.addWidget(btn_example)
        layout.addWidget(files_header)
        layout.addWidget(self.file_list)
        # start hidden; user toggles to show
        self.file_list.hide()
        
        self.setLayout(layout)
        
        # Style général avec fond gradient
        self.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(59, 130, 246, 0.05), 
                    stop:0.5 rgba(139, 92, 246, 0.05), 
                    stop:1 rgba(251, 191, 36, 0.05));
            }}
        """)
        
    def loadFile(self):
        """Charge un fichier via dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un fichier", 
            "", 
            "All Files (*.csv *.txt *.json *.sql *.png *.jpg *.jpeg *.bmp);;CSV (*.csv);;Text (*.txt);;JSON (*.json);;SQL (*.sql);;Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.processFile(file_path)
            
    def processFile(self, file_path):
        """Traite le fichier chargé"""
        file_name = file_path.split('/')[-1]
        file_ext = file_name.split('.')[-1].lower()
        
        file_data = {
            'name': file_name,
            'path': file_path,
            'type': file_ext,
            'content': None,
            'variables': [],
            'data': None
        }
        
        try:
            if file_ext == 'csv':
                df = pd.read_csv(file_path)
                file_data['data'] = df
                file_data['variables'] = list(df.columns)
                file_data['content'] = df.to_string()
                
            elif file_ext == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    file_data['content'] = json.dumps(json_data, indent=2)
                    if isinstance(json_data, list) and len(json_data) > 0:
                        file_data['data'] = pd.DataFrame(json_data)
                        file_data['variables'] = list(file_data['data'].columns)
                        
            elif file_ext in ['txt', 'sql']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data['content'] = f.read()
                    
            elif file_ext in ['png', 'jpg', 'jpeg', 'bmp']:
                file_data['type'] = 'image'
                file_data['content'] = QPixmap(file_path)
                
            self.loaded_files.append(file_data)
            # Persist in local DB and store db_id for later updates
            try:
                db_id = db.insert_file(file_data)
                file_data['db_id'] = db_id
            except Exception:
                file_data['db_id'] = None

            self.addFileToList(file_data)
            self.fileLoaded.emit(file_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
            
    def loadExample(self):
        """Charge un fichier d'exemple"""
        # Créer des données d'exemple
        data = {
            'x': [1.2, 2.1, 1.8, 2.5, 1.5, 3.2, 2.8, 1.9, 2.3, 2.0],
            'y': [2.3, 3.2, 2.9, 3.8, 2.5, 4.1, 3.5, 2.7, 3.4, 3.0],
            'z': [3.4, 2.8, 3.1, 2.5, 3.6, 3.9, 2.2, 3.3, 2.9, 3.2],
            'categorie': ['A', 'B', 'A', 'C', 'B', 'A', 'C', 'A', 'B', 'C']
        }
        df = pd.DataFrame(data)
        
        file_data = {
            'name': 'donnees_sample.csv',
            'path': 'exemple',
            'type': 'csv',
            'content': df.to_string(),
            'variables': list(df.columns),
            'data': df
        }
        
        self.loaded_files.append(file_data)
        try:
            db_id = db.insert_file(file_data)
            file_data['db_id'] = db_id
        except Exception:
            file_data['db_id'] = None

        self.addFileToList(file_data)
        self.fileLoaded.emit(file_data)
        
    def addFileToList(self, file_data):
        """Ajoute un fichier à la liste"""
        # Prefer a small upload image if present in workspace; otherwise fallback to emoji icon
        upload_img = None
        try:
            candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'file-analysis-app', 'public', 'logo192.png'))
            if os.path.exists(candidate):
                upload_img = candidate
        except Exception:
            upload_img = None

        if upload_img:
            icon = QIcon(upload_img)
            item = QListWidgetItem(file_data['name'])
            item.setIcon(icon)
        else:
            # emoji fallback
            if file_data.get('type') == 'image':
                icon_text = '🖼️'
            else:
                icon_text = '📄'
            item = QListWidgetItem(f"{icon_text} {file_data['name']}")

        item.setData(Qt.UserRole, file_data)
        self.file_list.addItem(item)
        
        # If the list is hidden, keep it hidden until user toggles; do nothing

    def toggleFilesList(self):
        """Show/hide the loaded files list (dropdown-like behavior)."""
        if self.file_list.isVisible():
            self.file_list.hide()
            self.btn_toggle_files.setText("Voir fichiers chargés ▾")
            self.btn_toggle_files.setChecked(False)
        else:
            self.file_list.show()
            self.btn_toggle_files.setText("Masquer fichiers ▴")
            self.btn_toggle_files.setChecked(True)
        
    def onFileItemClicked(self, item):
        """Quand un fichier est cliqué"""
        file_data = item.data(Qt.UserRole)
        self.fileSelected.emit(file_data)


# ==================== SECTION PREVISUALISATION ====================
# FilePreviewSection removed: preview and variable tree UI have been eliminated per request


class VariablesSection(QWidget):
    """Simple widget to display variables (columns) of the selected dataset."""
    variableSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        header = QLabel("Variables")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)

        self.var_list = QTreeWidget()
        self.var_list.setHeaderHidden(True)
        self.var_list.setIndentation(8)
        layout.addWidget(self.var_list)

        self.setLayout(layout)

        # clicking a variable emits signal with variable name
        self.var_list.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item, column):
        try:
            name = item.text(0)
            self.variableSelected.emit(name)
        except Exception:
            pass

    def setVariables(self, file_data: dict):
        """Populate the variable list from file_data. Accepts file_data with 'variables' or a pandas DataFrame under 'data' or 'df'."""
        self.var_list.clear()
        try:
            vars_list = []
            if file_data is None:
                vars_list = []
            elif isinstance(file_data, dict):
                if 'variables' in file_data and file_data.get('variables'):
                    vars_list = list(file_data.get('variables'))
                elif file_data.get('data') is not None:
                    try:
                        vars_list = list(file_data.get('data').columns)
                    except Exception:
                        vars_list = []
                elif file_data.get('df') is not None:
                    try:
                        vars_list = list(file_data.get('df').columns)
                    except Exception:
                        vars_list = []
            else:
                # fallback: if a DataFrame was passed directly
                try:
                    import pandas as _pd
                    if isinstance(file_data, _pd.DataFrame):
                        vars_list = list(file_data.columns)
                except Exception:
                    vars_list = []

            for v in vars_list:
                it = QTreeWidgetItem([str(v)])
                self.var_list.addTopLevelItem(it)
        except Exception:
            pass


# ==================== CANVAS MATPLOTLIB ====================
class MplCanvas(FigureCanvas):
    """Canvas Matplotlib pour les graphiques"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100, projection=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        if projection == '3d':
            self.axes = self.fig.add_subplot(111, projection='3d')
        else:
            self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)


# ==================== SECTION VISUALISATION ====================
class VisualizationSection(QWidget):
    """Section de visualisation et analyse (5/6 droite)"""
    requestClean = pyqtSignal()
    requestFileLoad = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.dimension = '2d'
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Header avec gradient et contrôles
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(59, 130, 246, 0.08), 
                    stop:0.5 rgba(139, 92, 246, 0.08), 
                    stop:1 rgba(251, 191, 36, 0.08));
                border-bottom: 1px solid rgba(139, 92, 246, 0.2);
                padding: 15px;
            }}
        """)
        header_layout = QVBoxLayout()
        
        #title = QLabel("Visualisation et Analyse")
        #title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        # Grid de contrôles
        controls = QWidget()
        controls_layout = QGridLayout()
        
        # Méthode de réduction
        method_label = QLabel("Méthode de réduction de dimension")
        method_label.setStyleSheet("font-weight: bold;")
        self.method_combo = QComboBox()
        # correspondance d'index attendue par updateVisualization: 0=PCA,1=t-SNE,2=UMAP
        self.method_combo.addItems([
            "ACP (Analyse en Composantes Principales)",
            "t-SNE (t-Distributed Stochastic Neighbor Embedding)",
            "UMAP (Uniform Manifold Approximation and Projection)"
        ])
        self.method_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 6px;
                background-color: white;
            }
        """)
        self.method_combo.currentIndexChanged.connect(self.updateVisualization)
        # Indiquer si UMAP n'est pas installé
        if not UMAP_AVAILABLE:
            # garder l'item pour l'index, mais marquer comme non disponible
            self.method_combo.setItemText(2, "UMAP (non installé)")
        
        # Type de graphique
        chart_label = QLabel("Type de graphique")
        chart_label.setStyleSheet("font-weight: bold;")
        self.chart_combo = QComboBox()
        # Removed histogram option as requested
        self.chart_combo.addItems([
            "📈 Nuage de points",
            "📉 Graphique linéaire"
        ])
        self.chart_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 6px;
                background-color: white;
            }
        """)
        
        # Boutons 2D/3D
        dimension_label = QLabel("Dimension")
        dimension_label.setStyleSheet("font-weight: bold;")
        
        dimension_widget = QWidget()
        dimension_layout = QHBoxLayout()
        dimension_layout.setSpacing(5)
        
        self.btn_2d = QPushButton("2D")
        self.btn_2d.setCheckable(True)
        self.btn_2d.setChecked(True)
        self.btn_2d.clicked.connect(lambda: self.setDimension('2d'))
        
        self.btn_3d = QPushButton("3D")
        self.btn_3d.setCheckable(True)
        self.btn_3d.clicked.connect(lambda: self.setDimension('3d'))
        
        for btn in [self.btn_2d, self.btn_3d]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    border: 2px solid {Theme.VIOLET};
                    color: {Theme.VIOLET};
                    border-radius: 6px;
                    padding: 8px 20px;
                    font-weight: bold;
                }}
                QPushButton:checked {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 {Theme.BLUE}, stop:1 {Theme.VIOLET});
                    color: white;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: rgba(139, 92, 246, 0.1);
                }}
            """)
        
        dimension_layout.addWidget(self.btn_2d)
        dimension_layout.addWidget(self.btn_3d)
        dimension_layout.addStretch()
        dimension_widget.setLayout(dimension_layout)
        
        controls_layout.addWidget(method_label, 0, 0)
        controls_layout.addWidget(self.method_combo, 1, 0)
        controls_layout.addWidget(chart_label, 0, 1)
        controls_layout.addWidget(self.chart_combo, 1, 1)
        controls_layout.addWidget(dimension_label, 0, 2)
        controls_layout.addWidget(dimension_widget, 1, 2)

        '''# Petit bouton pour demander le chargement d'un fichier (redirigé vers FileUploadSection)
        self.btn_load_here = QPushButton("📁 Charger")
        self.btn_load_here.setToolTip("Charger un fichier")
        self.btn_load_here.setFixedHeight(34)
        self.btn_load_here.clicked.connect(lambda: self.requestFileLoad.emit())
        controls_layout.addWidget(self.btn_load_here, 0, 3, 2, 1)'''

        # Export image
        self.btn_export = QPushButton("💾 Teleharger image")
        self.btn_export.setToolTip("Telecharger l'image affichée (PNG)")
        self.btn_export.setFixedHeight(34)
        self.btn_export.clicked.connect(self.exportCurrentImage)
        controls_layout.addWidget(self.btn_export, 0, 4, 2, 1)

        # Clean button in header (trigger preview cleaning)
        self.btn_clean_top = QPushButton("🧹 Nettoyer (suppr. vides)")
        self.btn_clean_top.setToolTip("Supprimer les lignes/colonnes vides du DataFrame affiché")
        self.btn_clean_top.setFixedHeight(34)
        # emit a signal; MainWindow will connect it to preview_section.cleanData
        self.btn_clean_top.clicked.connect(lambda: self.requestClean.emit())
        controls_layout.addWidget(self.btn_clean_top, 0, 5, 2, 1)
        
        controls.setLayout(controls_layout)
        
        # Info fichier actif banner removed per UX request
        
        #header_layout.addWidget(title)
        header_layout.addWidget(controls)
    # header_layout.addWidget(self.file_info)  # removed
        header.setLayout(header_layout)
        
        # Zone de contenu (drop zone ou visualisations)
        self.content_stack = QWidget()
        self.content_layout = QVBoxLayout()
        
        # Drop zone (affichée par défaut)
        self.drop_zone = DropZone()
        self.drop_zone.fileDropped.connect(self.onFileDropped)

        # Track last canvas to export later
        self.last_canvas = None
        
        # Tab widget pour les visualisations
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid rgba(139, 92, 246, 0.2);
                border-radius: 8px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: rgba(139, 92, 246, 0.1);
                color: {Theme.VIOLET};
                border: 1px solid rgba(139, 92, 246, 0.2);
                padding: 10px 20px;
                margin: 2px;
                border-radius: 6px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {Theme.BLUE}, stop:1 {Theme.VIOLET});
                color: white;
            }}
        """)
        
        # Onglets
        self.viz_widget = QWidget()
        self.viz_layout = QVBoxLayout()
        self.viz_widget.setLayout(self.viz_layout)
        
        # Only keep the reduction-method visualization tab
        self.tabs.addTab(self.viz_widget, "Méthode de réduction")
        self.tabs.hide()
        
        self.content_layout.addWidget(self.drop_zone)
        self.content_layout.addWidget(self.tabs)
        self.content_stack.setLayout(self.content_layout)
        
        main_layout.addWidget(header)
        main_layout.addWidget(self.content_stack)
        
        self.setLayout(main_layout)
        
    def setDimension(self, dim):
        """Change la dimension (2D/3D)"""
        self.dimension = dim
        self.btn_2d.setChecked(dim == '2d')
        self.btn_3d.setChecked(dim == '3d')
        self.updateVisualization()
        
    def onFileDropped(self, file_path):
        """Gère le fichier déposé"""
        # Émettre un signal pour que FileUploadSection traite le fichier
        # Pour simplifier, on affiche juste un message
        QMessageBox.information(self, "Fichier déposé", f"Fichier: {file_path}")
        
    def setFile(self, file_data):
        """Définit le fichier actuel et affiche les visualisations"""
        self.current_file = file_data
        
        # Masquer drop zone, afficher tabs
        self.drop_zone.hide()
        self.tabs.show()
        
        # File info banner removed; we rely on the preview section and tabs for context
        
        # Mettre à jour la visualisation
        self.updateVisualization()
        
    def updateVisualization(self):
        """Met à jour la visualisation selon les paramètres"""
        if not self.current_file or self.current_file['type'] not in ['csv', 'json']:
            return
        
        # Clear previous visualization
        for i in reversed(range(self.viz_layout.count())): 
            self.viz_layout.itemAt(i).widget().setParent(None)
        
        method_idx = self.method_combo.currentIndex()
        df = self.current_file.get('data')
        
        if df is None or len(df) == 0:
            return
        
        # Sélectionner les colonnes numériques
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) == 0:
            self.viz_layout.addWidget(QLabel("Aucune colonne numérique trouvée"))
            return
        
        # Info panel
        info_panel = QFrame()
        info_panel.setStyleSheet(f"""
            QFrame {{
                background: {Theme.GRADIENT_BLUE_VIOLET};
                {Theme.BORDER_BLUE}
                padding: 15px;
            }}
        """)
        info_layout = QHBoxLayout()
        
        # Créer le graphique
        try:
            X = df[numeric_cols].values
            
            if method_idx == 0:  # PCA
                method_name = "ACP"
                pca = PCA(n_components=min(3, len(numeric_cols)) if self.dimension == '3d' else 2)
                X_reduced = pca.fit_transform(X)
                
                # Variance expliquée
                var_exp = pca.explained_variance_ratio_
                info_text = f"<b style='color: {Theme.VIOLET};'>Variance expliquée PC1:</b> <span style='color: {Theme.BLUE};'>{var_exp[0]:.1%}</span>"
                if len(var_exp) > 1:
                    info_text += f" &nbsp;&nbsp; <b style='color: {Theme.VIOLET};'>PC2:</b> <span style='color: {Theme.BLUE};'>{var_exp[1]:.1%}</span>"
                
            elif method_idx == 1:  # t-SNE
                method_name = "t-SNE"
                n_comp = 3 if self.dimension == '3d' else 2
                tsne = TSNE(n_components=n_comp, random_state=42, perplexity=min(30, len(X)-1))
                X_reduced = tsne.fit_transform(X)
                
                info_text = f"<b style='color: {Theme.VIOLET};'>Perplexité:</b> <span style='color: {Theme.YELLOW};'>30</span> &nbsp; "
                info_text += f"<b style='color: {Theme.VIOLET};'>Itérations:</b> <span style='color: {Theme.YELLOW};'>1000</span> &nbsp; "
                info_text += f"<b style='color: {Theme.VIOLET};'>Learning rate:</b> <span style='color: {Theme.YELLOW};'>200</span>"
                
            else:  # UMAP
                method_name = "UMAP"
                if UMAP_AVAILABLE:
                    n_comp = 3 if self.dimension == '3d' else 2
                    reducer = umap.UMAP(n_components=n_comp, random_state=42)
                    X_reduced = reducer.fit_transform(X)
                    
                    info_text = f"<b style='color: {Theme.BLUE};'>Voisins:</b> <span style='color: {Theme.YELLOW};'>15</span> &nbsp; "
                    info_text += f"<b style='color: {Theme.BLUE};'>Distance minimale:</b> <span style='color: {Theme.YELLOW};'>0.1</span> &nbsp; "
                    info_text += f"<b style='color: {Theme.BLUE};'>Métrique:</b> <span style='color: {Theme.YELLOW};'>Euclidienne</span>"
                else:
                    self.viz_layout.addWidget(QLabel("UMAP non disponible. Installez avec: pip install umap-learn"))
                    return
            
            info_label = QLabel(info_text)
            info_layout.addWidget(info_label)
            info_panel.setLayout(info_layout)
            self.viz_layout.addWidget(info_panel)
            
            # Créer le canvas
            if self.dimension == '3d' and X_reduced.shape[1] >= 3:
                canvas = MplCanvas(self, width=8, height=6, projection='3d')
                ax = canvas.axes
                
                # Récupérer les catégories si disponibles
                cat_cols = df.select_dtypes(include=['object']).columns
                if len(cat_cols) > 0:
                    categories = df[cat_cols[0]]
                    unique_cats = categories.unique()
                    colors_map = {
                        unique_cats[i % len(unique_cats)]: [Theme.BLUE, Theme.VIOLET, Theme.YELLOW][i % 3]
                        for i in range(len(unique_cats))
                    }
                    
                    for cat in unique_cats:
                        mask = categories == cat
                        color = colors_map[cat]
                        # Do not set per-point labels to avoid many legend entries
                        ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1], X_reduced[mask, 2],
                                 c=color, s=50, alpha=0.6)
                else:
                    ax.scatter(X_reduced[:, 0], X_reduced[:, 1], X_reduced[:, 2],
                             c=Theme.BLUE, s=50, alpha=0.6)
                
                ax.set_xlabel(f'{method_name} 1', color=Theme.BLUE, fontweight='bold')
                ax.set_ylabel(f'{method_name} 2', color=Theme.VIOLET, fontweight='bold')
                ax.set_zlabel(f'{method_name} 3', color=Theme.YELLOW, fontweight='bold')
                # legend intentionally removed (no legend shown)
                ax.grid(True, alpha=0.3)
                
            else:  # 2D
                canvas = MplCanvas(self, width=8, height=6)
                # remember canvas for export
                self.last_canvas = canvas
                # remember canvas for export
                self.last_canvas = canvas
                # remember canvas for export
                self.last_canvas = canvas
                ax = canvas.axes
                
                # Récupérer les catégories si disponibles
                cat_cols = df.select_dtypes(include=['object']).columns
                if len(cat_cols) > 0:
                    categories = df[cat_cols[0]]
                    unique_cats = categories.unique()
                    colors_map = {
                        unique_cats[i % len(unique_cats)]: [Theme.BLUE, Theme.VIOLET, Theme.YELLOW][i % 3]
                        for i in range(len(unique_cats))
                    }
                    
                    for cat in unique_cats:
                        mask = categories == cat
                        color = colors_map[cat]
                        # Do not provide label per point; legend will be constructed from handles
                        ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1],
                                 c=color, s=100, alpha=0.6, edgecolors='white', linewidth=1)
                else:
                    ax.scatter(X_reduced[:, 0], X_reduced[:, 1],
                             c=Theme.BLUE, s=100, alpha=0.6, edgecolors='white', linewidth=1)
                
                ax.set_xlabel(f'{method_name} Dimension 1', color=Theme.BLUE, fontweight='bold', fontsize=12)
                ax.set_ylabel(f'{method_name} Dimension 2', color=Theme.VIOLET, fontweight='bold', fontsize=12)
                # legend intentionally removed (no legend shown)
                ax.grid(True, alpha=0.3)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
            
            # Style du graphique
            canvas.fig.patch.set_facecolor('#f8f9fa')
            ax.set_facecolor('#ffffff')
            canvas.fig.tight_layout()
            
            # Frame pour le canvas avec gradient
            canvas_frame = QFrame()
            canvas_frame.setStyleSheet(f"""
                QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 rgba(59, 130, 246, 0.05), 
                        stop:1 rgba(139, 92, 246, 0.05));
                    border-radius: 8px;
                    padding: 15px;
                }}
            """)
            canvas_layout = QVBoxLayout()
            # Add navigation toolbar for zoom/pan
            try:
                toolbar = NavigationToolbar(canvas, self)
                canvas_layout.addWidget(toolbar)
            except Exception:
                pass
            # connect scroll event for zoom (2D and 3D)
            try:
                canvas.mpl_connect('scroll_event', lambda event: self._on_scroll(event, canvas))
            except Exception:
                pass
            canvas_layout.addWidget(canvas)
            canvas_frame.setLayout(canvas_layout)
            
            self.viz_layout.addWidget(canvas_frame)
            
        except Exception as e:
            tb = traceback.format_exc()
            error_text = f"Erreur lors de la visualisation:\n{str(e)}\n\n{tb}"
            error_label = QTextEdit()
            error_label.setReadOnly(True)
            error_label.setText(error_text)
            error_label.setStyleSheet("color: red; padding: 6px; background: #fff0f0;")
            self.viz_layout.addWidget(error_label)

    def exportCurrentImage(self):
        """Export the last created matplotlib canvas to PNG via a Save dialog."""
        if not hasattr(self, 'last_canvas') or self.last_canvas is None:
            QMessageBox.information(self, "Export", "Aucun graphique disponible pour l'export.")
            return

        fname, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image", "plot.png", "PNG Image (*.png);;JPEG Image (*.jpg);;SVG Vector (*.svg)")
        if not fname:
            return

        try:
            # Save the figure associated with the canvas
            fig = self.last_canvas.fig
            fig.savefig(fname, dpi=150, bbox_inches='tight')
            QMessageBox.information(self, "Export", f"Image enregistrée: {fname}")
        except Exception as e:
            QMessageBox.critical(self, "Export", f"Erreur lors de l'enregistrement: {e}")

    def _on_scroll(self, event, canvas):
        """Zoom in/out on scroll. Works for 2D and 3D axes by adjusting view limits or elev/azim for 3D."""
        try:
            ax = canvas.axes
            base_scale = 1.1
            # get mouse position in data coords
            if event.button == 'up':
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                scale_factor = base_scale
            else:
                return

            if hasattr(ax, 'get_xbound') and not getattr(ax, 'name', '') == '3d':
                # 2D axes
                xleft, xright = ax.get_xlim()
                ybottom, ytop = ax.get_ylim()
                xdata = event.xdata if event.xdata is not None else (xleft + xright) / 2
                ydata = event.ydata if event.ydata is not None else (ybottom + ytop) / 2

                new_width = (xright - xleft) * scale_factor
                new_height = (ytop - ybottom) * scale_factor

                ax.set_xlim([xdata - new_width * ( (xdata - xleft) / (xright - xleft) ),
                             xdata + new_width * ( (xright - xdata) / (xright - xleft) )])
                ax.set_ylim([ydata - new_height * ( (ydata - ybottom) / (ytop - ybottom) ),
                             ydata + new_height * ( (ytop - ydata) / (ytop - ybottom) )])
            else:
                # 3D axes: adjust the distance by changing the view_init or scale the data limits
                # Simple approach: change elevation slightly
                try:
                    elev = ax.elev if hasattr(ax, 'elev') else ax.elev
                    azim = ax.azim if hasattr(ax, 'azim') else ax.azim
                    if event.button == 'up':
                        ax.view_init(elev=elev - 2, azim=azim)
                    else:
                        ax.view_init(elev=elev + 2, azim=azim)
                except Exception:
                    pass

            canvas.draw_idle()
        except Exception:
            pass


# ==================== FENETRE PRINCIPALE ====================
class MainWindow(QMainWindow):
    """Fenêtre principale de l'application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application d'Analyse de Données - PyQt5")
        self.setGeometry(100, 100, 1600, 900)
        
        # Widget central
        central = QWidget()
        main_layout = QHBoxLayout()
        
        # Splitter vertical pour la partie gauche (1/6)
        left_splitter = QSplitter(Qt.Vertical)
        
        # Section upload (haut gauche)
        self.upload_section = FileUploadSection()
        
        # Left column: only upload section (preview/variables removed)
        left_splitter.addWidget(self.upload_section)
        # Add a file-tree panel in the left column (hierarchical files)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setIndentation(12)
        # Remove visual white boxed background so the area above variables looks integrated
        try:
            self.file_tree.setStyleSheet("background: transparent; border: none;")
            # remove frame lines if present
            try:
                self.file_tree.setFrameShape(QFrame.NoFrame)
            except Exception:
                pass
            self.file_tree.setUniformRowHeights(True)
        except Exception:
            pass
        left_splitter.addWidget(self.file_tree)
        # Variables panel below the file tree
        self.variables_section = VariablesSection()
        left_splitter.addWidget(self.variables_section)
        left_splitter.setSizes([300, 300, 300])

        # populate the file tree from packages/data (best-effort)
        try:
            root_dir = os.path.join(os.path.dirname(__file__), 'packages', 'data')
            loader = DataLoader()
            tree = loader.build_tree_from_dir(root_dir)

            def add_nodes(parent_item, node):
                for name, child in sorted(node.get('children', {}).items()):
                    item = QTreeWidgetItem([name])
                    parent_item.addChild(item)
                    # if leaf file, store path
                    if child.get('is_file') and child.get('path'):
                        item.setData(0, Qt.UserRole, child.get('path'))
                    add_nodes(item, child)

            self.file_tree.clear()
            add_nodes(self.file_tree.invisibleRootItem(), tree)
            self.file_tree.expandToDepth(1)
            self.file_tree.itemClicked.connect(self._on_file_tree_item_clicked)
        except Exception:
            # leave tree empty if scan fails
            pass
        
        # Section visualisation (droite 5/6)
        self.viz_section = VisualizationSection()
        
        # Splitter horizontal principal
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(self.viz_section)
        # Empêcher les enfants de se replier automatiquement quand le contenu change
        main_splitter.setChildrenCollapsible(False)
        left_splitter.setChildrenCollapsible(False)
        # Utiliser des stretch factors pour maintenir une proportion 1/5 - 4/5
        # (le premier argument reçoit un poids de 1, le second un poids de 4)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 4)
        # Valeurs initiales raisonnables si la fenêtre n'est pas encore maximisée
        main_splitter.setSizes([320, 1280])

        main_layout.addWidget(main_splitter)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # Conserver des références pour contrôler la taille de la colonne gauche
        self.left_splitter = left_splitter
        self.main_splitter = main_splitter
        
        # Connexions des signaux
        self.upload_section.fileLoaded.connect(self.onFileLoaded)
        self.upload_section.fileSelected.connect(self.onFileSelected)
        # When visualization requests a clean, call onFileModified (default handler)
        self.viz_section.requestClean.connect(self.onFileModified)

        # Style général
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
        """)

        # --- Window controls (minimize / toggle fullscreen / close)
        self.is_fullscreen = False
        self.window_controls = QWidget(self)
        wc_layout = QHBoxLayout()
        wc_layout.setContentsMargins(4, 4, 4, 4)
        wc_layout.setSpacing(6)

        btn_min = QPushButton("▁")
        btn_min.setToolTip("Minimiser")
        btn_min.setFixedSize(28, 24)
        btn_min.clicked.connect(lambda: self.showMinimized())

        btn_toggle = QPushButton("❐")
        btn_toggle.setToolTip("Basculer plein écran / restaurer")
        btn_toggle.setFixedSize(28, 24)
        btn_toggle.clicked.connect(self.toggleFullScreen)

        btn_close = QPushButton("✕")
        btn_close.setToolTip("Fermer")
        btn_close.setFixedSize(28, 24)
        btn_close.clicked.connect(self.close)

        for b in (btn_min, btn_toggle, btn_close):
            b.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.4);
                    border: 1px solid rgba(0,0,0,0.08);
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.7);
                }
            """)

        wc_layout.addWidget(btn_min)
        wc_layout.addWidget(btn_toggle)
        wc_layout.addWidget(btn_close)
        self.window_controls.setLayout(wc_layout)
        self.window_controls.setFixedHeight(34)
        self.window_controls.show()

    def resizeEvent(self, event):
        # Fixer la largeur de la colonne gauche à 20% de la largeur de la fenêtre
        try:
            total_w = self.width()
            left_w = max(220, int(total_w * 0.20))
            # Bloquer la largeur gauche pour qu'elle ne soit pas affectée par la droite
            self.left_splitter.setFixedWidth(left_w)
        except Exception:
            pass
        return super().resizeEvent(event)

    def showEvent(self, event):
        # Fixer la largeur de la colonne gauche immédiatement à l'affichage
        try:
            total_w = self.width()
            left_w = max(220, int(total_w * 0.20))
            self.left_splitter.setFixedWidth(left_w)
        except Exception:
            pass
        return super().showEvent(event)

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True

    def keyPressEvent(self, event):
        # Esc to exit fullscreen
        try:
            if event.key() == Qt.Key_Escape and self.isFullScreen():
                self.showNormal()
                self.is_fullscreen = False
                return
        except Exception:
            pass
        return super().keyPressEvent(event)
        
    def onFileLoaded(self, file_data):
        """Appelé quand un fichier est chargé"""
        # Auto-sélectionner le fichier
        self.onFileSelected(file_data)
        
    def onFileSelected(self, file_data):
        """Appelé quand un fichier est sélectionné"""
        # preview_section removed — update visualization only
        try:
            # update variables panel
            try:
                self.variables_section.setVariables(file_data)
            except Exception:
                pass
            self.viz_section.setFile(file_data)
        except Exception:
            pass

    def onFileModified(self, file_data):
        """Mettre à jour les structures internes quand le fichier est modifié (ex: nettoyage)."""
        # Find the loaded file in upload_section.loaded_files and replace
        for i, f in enumerate(self.upload_section.loaded_files):
            if f.get('path') == file_data.get('path') and f.get('name') == file_data.get('name'):
                self.upload_section.loaded_files[i] = file_data
                # Update list widget item text (keep same index)
                item = self.upload_section.file_list.item(i)
                if item:
                    item.setText(f"📊 {file_data['name']}")
                break

        # Persist changes to DB if possible
        try:
            # If file_data has db_id, update; otherwise try to update by path/name
            if file_data.get('db_id'):
                db.update_file(file_data)
            else:
                # try to look up recent files and match by path
                try:
                    rows = db.get_all_files()
                    for r in rows:
                        if r.get('path') == file_data.get('path'):
                            file_data['db_id'] = r.get('id')
                            db.update_file(file_data)
                            break
                except Exception:
                    pass
        except Exception:
            pass

        # Refresh preview and visualizations
        # preview_section removed — refresh visualization only
        try:
            self.viz_section.setFile(file_data)
        except Exception:
            pass

    def _on_file_tree_item_clicked(self, item, column):
        """Handler when a file in the left tree is clicked. Attempts to load the file and forward to the visualizer."""
        try:
            path = item.data(0, Qt.UserRole)
            if not path:
                return
            loader = DataLoader()
            loaded = loader.load(path)
            # Build a minimal file_data structure expected by the app
            file_data = {
                'name': os.path.basename(path),
                'path': path,
            }
            # If loader returned a DataFrame, attach it under 'df'
            try:
                import pandas as _pd
                if isinstance(loaded, _pd.DataFrame):
                    file_data['df'] = loaded
                else:
                    file_data['raw'] = loaded
            except Exception:
                file_data['raw'] = loaded

            # Use existing selection handler to update visuals
            self.onFileSelected(file_data)
        except Exception as e:
            try:
                QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier: {e}")
            except Exception:
                pass


# ==================== MAIN ====================
def main():
    app = QApplication(sys.argv)
    
    # Font par défaut
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Fenêtre principale
    # Initialize local SQLite DB
    try:
        db.init_db()
    except Exception:
        pass

    window = MainWindow()
    # Positionne et maximise la fenêtre sur l'écran où se trouve le curseur (support multi-écrans)
    try:
        screen = None
        try:
            for s in QApplication.screens():
                if s.geometry().contains(QCursor.pos()):
                    screen = s
                    break
        except Exception:
            screen = QApplication.primaryScreen()

        if not screen:
            screen = QApplication.primaryScreen()

        if screen:
            geom = screen.availableGeometry()
            # set geometry to available area (respects taskbar) and maximize
            window.setGeometry(geom)
            window.showMaximized()
        else:
            window.showMaximized()
    except Exception:
        # fallback
        window.showMaximized()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
