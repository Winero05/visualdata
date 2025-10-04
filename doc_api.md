#Description Complète de l'API d'Analyse et de Visualisation
Cette documentation a pour but de décrire en détail l'API construite avec FastAPI, ses fonctionnalités, son utilité, et la manière de l'utiliser et de la lancer.

#1. Utilité et Objectif
L'objectif principal de cette API est de fournir une plateforme centralisée et accessible via le web pour l'analyse exploratoire de données (EDA - Exploratory Data Analysis). Elle permet à un utilisateur, qu'il soit développeur, data scientist ou analyste, d'effectuer des opérations courantes d'analyse et de visualisation de données sans avoir à écrire de code répétitif.

En résumé, elle transforme des scripts d'analyse de données complexes en services web simples à utiliser.

Importance :

Accessibilité : N'importe quelle application (une application web, un autre service, un script local) peut interagir avec l'API via de simples requêtes HTTP.
Standardisation : Elle offre une manière standardisée d'effectuer des tâches comme le nettoyage, la visualisation ou la réduction de dimension.
Rapidité : Permet d'obtenir rapidement des insights visuels sur un jeu de données sans mettre en place un environnement de développement complet.
Intégration : Peut servir de "backend" pour une application de tableau de bord (dashboard) interactive.
#2. Outils et Technologies
L'API est construite sur un écosystème Python moderne et robuste pour la science des données et le développement web.

Framework Web : FastAPI, un framework web haute performance pour construire des API, connu pour sa rapidité, sa validation de données intégrée et sa génération automatique de documentation.
Manipulation de Données : Pandas et NumPy, les bibliothèques de référence pour la manipulation de tableaux de données et les calculs numériques.
Visualisation :
Matplotlib & Seaborn : Pour la génération de graphiques statiques (histogrammes, heatmaps, etc.).
Plotly : Pour la création de graphiques interactifs, particulièrement utilisé pour les visualisations 3D (ACP, UMAP, t-SNE).
WordCloud : Pour la génération de nuages de mots à partir de texte.
Machine Learning & Réduction de Dimension :
Scikit-learn : Utilisé pour l'Analyse en Composantes Principales (ACP/PCA) et t-SNE.
UMAP-learn : Pour la réduction de dimension avec l'algorithme UMAP.
Traitement d'Image : Pillow (PIL) et OpenCV-Python pour charger, manipuler et analyser des images.
Validation de Données : Pydantic, utilisé par FastAPI pour définir des schémas de données clairs, valider les requêtes entrantes et sérialiser les réponses.
Serveur Web (implicite) : Uvicorn, le serveur ASGI recommandé pour exécuter des applications FastAPI.
#3. Lancement de l'API
Pour exécuter cette API sur la machine locale, vous devez suivre ces étapes :

Installation des dépendances : Assurez-vous que toutes les bibliothèques listées ci-dessus sont installées. Vous pouvez généralement les installer avec pip :


pip install fastapi "uvicorn[standard]" pandas numpy matplotlib seaborn plotly scikit-learn umap-learn python-multipart Pillow opencv-python-headless wordcloud
(Note : python-multipart est nécessaire pour la gestion des téléversements de fichiers).

Lancer le serveur : Ouvrez un terminal dans le répertoire racine du projet (où se trouve api.py) et exécutez la commande suivante :


uvicorn api:app --reload
api: Fait référence au fichier api.py.
app: Fait référence à l'objet FastAPI créé dans le fichier (app = FastAPI(...)).
--reload: Permet au serveur de redémarrer automatiquement après chaque modification du code.
Accéder à l'API : Une fois le serveur lancé, l'API sera accessible à l'adresse http://127.0.0.1:8000.

#4. Utilisation et Détails des Fonctionnalités
L'un des plus grands avantages de FastAPI est la documentation interactive automatique. Une fois l'API lancée, vous pouvez accéder à :

http://127.0.0.1:8000/docs pour une interface Swagger UI.
http://127.0.0.1:8000/redoc pour une interface ReDoc.
Ces interfaces vous permettent de voir tous les endpoints, leurs paramètres, et même de les tester directement depuis votre navigateur.

Sources de Données
La plupart des endpoints sont très flexibles et acceptent les données de trois manières différentes, grâce à la dépendance get_data_source :

chemin_fichier (string) : Un chemin vers un fichier sur le serveur.
donnees_json (string) : Les données directement fournies sous forme de chaîne JSON.
file (UploadFile) : Un fichier téléversé via la requête HTTP (par exemple, depuis un formulaire web).
Détail des Endpoints
GET /Accueil

Description : Un simple endpoint de bienvenue.
POST /nettoyer-donnees/

Description : Nettoie les valeurs manquantes d'un jeu de données tabulaire (CSV/Excel).
Paramètres : La source de données, une strategie de nettoyage ('mean', 'median', 'drop'...), et optionnellement une liste de colonnes à cibler.
Retourne : Le DataFrame nettoyé au format JSON.
POST /visualiser/tabulaire/

Description : Génère des visualisations pour des données tabulaires.
Paramètres : La source de données et un type_graphique ('distributions' ou 'correlations').
Retourne : Une image du graphique (ex: heatmap des corrélations) encodée en Base64.
POST /visualiser/image/

Description : Affiche une image ou son histogramme de couleurs.
Paramètres : Une source d'image (chemin ou téléversement) et un type_visualisation ('image' ou 'histogramme').
Retourne : L'image demandée encodée en Base64.
POST /visualiser/texte/nuage-de-mots/

Description : Crée un nuage de mots à partir d'un fichier texte.
Paramètres : Une source de texte (chemin ou téléversement).
Retourne : L'image du nuage de mots encodée en Base64.
POST /reduire-dimension/

Description : C'est l'un des endpoints les plus puissants. Il applique une technique de réduction de dimension (ACP, UMAP, ou t-SNE) sur un jeu de données et retourne une visualisation 2D ou 3D.
Paramètres :
La source de données.
Un corps de requête JSON complexe qui spécifie la methode ('acp', 'umap', 'tsne') et ses paramètres spécifiques (ex: n_components, perplexity pour t-SNE, n_neighbors pour UMAP). L'utilisation de Union[PCAParams, UMAPParams, TSNEParams] est une manière élégante de gérer ces différents paramètres.
Retourne : Un objet JSON contenant :
image_data: Le graphique de la projection (ex: nuage de points) en Base64.
reduced_data: Les coordonnées des points dans l'espace réduit, au format JSON.

#5. Points d'Intérêt et Architecture
Structure Modulaire : Le code est bien organisé en "packages" et "modules" (loading, netoyage, analysis, visualisation_*, methode_*). Chaque fichier a une responsabilité unique, ce qui rend le code plus facile à maintenir et à étendre.
Dépendances FastAPI (Depends) : Le code utilise intelligemment le système d'injection de dépendances de FastAPI. Par exemple, Depends(get_data_source) centralise toute la logique de chargement des données, évitant la duplication de code dans chaque endpoint. Depends(get_image_visualizer) fait de même pour le chargement des images.
Modèles Pydantic Avancés : L'utilisation de Union et de Literal dans les modèles Pydantic (ReductionParams) permet de créer une API très descriptive et auto-validée. Dans l'interface Swagger, cela se traduit par un menu déroulant où l'utilisateur peut choisir la méthode de réduction, et les champs de paramètres s'adaptent dynamiquement.
Gestion des Retours : L'API ne retourne pas seulement des images. Pour la réduction de dimension, elle retourne aussi les données transformées, ce qui permet à une application cliente de réutiliser ces coordonnées pour des visualisations plus riches et interactives.
Gestion des Erreurs : L'API utilise HTTPException pour retourner des erreurs claires et des codes de statut HTTP appropriés (ex: 400 pour une mauvaise requête, 404 pour un fichier non trouvé), ce qui est une bonne pratique pour les API REST.
En conclusion, il s'agit d'une API très bien conçue, puissante et flexible, qui sert de boîte à outils pour l'analyse de données exploratoire. Elle est un excellent exemple de la manière de combiner la puissance des bibliothèques de science des données Python avec un framework web moderne comme FastAPI.

