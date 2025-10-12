# VisualData — Application de visualisation et d'analyse de données

Ce dépôt contient une application de visualisation de données écrite en Python avec une interface PyQt5. Elle fournit :

- Un front-end graphique (fenêtre PyQt5) pour charger des fichiers, parcourir un arbre de fichiers et visualiser des données en 2D/3D.
- Un backend léger pour charger différents formats (CSV, JSON, images, SQL, etc.), préparer des arbres hiérarchiques de fichiers et exposer des fonctions d'analyse (ACP / PCA, t-SNE et UMAP optionnel).

Ce README couvre : installation, exécution, structure du projet, guide d'utilisation pour un nouvel utilisateur et guide pour développeurs.

---

## Table des matières

- [Prérequis](#prérequis)
- [Installation rapide (Windows Powershell)](#installation-rapide-windows-powershell)
- [Lancer l'application](#lancer-lapplication)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Guide d'utilisation (utilisateur)](#guide-dutilisation-utilisateur)
- [Guide développeur (contribuer / modifier le code)](#guide-développeur-contribuer--modifier-le-code)
- [Tests](#tests)
- [Packaging (création d'un exécutable)](#packaging-création-dun-exécutable)
- [Dépannage (troubleshooting)](#dépannage-troubleshooting)
- [Licence & contact](#licence--contact)

---

## Prérequis

- Python 3.10+ (le projet a été développé et testé avec Python 3.13 — assurez-vous d'avoir la version adéquate).
- pip
- Sous Windows, le shell PowerShell est recommandé pour les exemples ci-dessous.

Fichiers importants pour dépendances :
- `requirements.txt` — dépendances principales.
- `requirements_no_open3d.txt` — variante si vous ne voulez pas installer open3d.

Packages clés utilisés : PyQt5, pandas, numpy, matplotlib, scikit-learn (PCA, t-SNE), umap-learn (optionnel), pillow.

---

## Installation rapide (Windows PowerShell)

Ouvrez PowerShell dans le dossier du projet (le dossier contenant `PyQt5_Complete_App.py`). Exécutez :

```powershell
# créer et activer un environnement virtuel
python -m venv .venv
# sous PowerShell
.\.venv\Scripts\Activate.ps1

# installer les dépendances
pip install -r requirements.txt
```

Remarque : si vous ne souhaitez pas installer certaines dépendances lourdes (par ex. open3d), installez `requirements_no_open3d.txt` à la place.

---

## Lancer l'application

Depuis la racine du projet (après activation du venv) :

```powershell
python PyQt5_Complete_App.py
```

Sur certaines machines, il peut être nécessaire d'utiliser un chemin explicite vers l'exécutable Python. Par exemple :

```powershell
& C:/Users/USER/AppData/Local/Microsoft/WindowsApps/python3.13.exe PyQt5_Complete_App.py
```

L'application ouvrira une fenêtre principale avec :
- Colonne gauche : zone de chargement + arbre de fichiers + variables
- Colonne droite : visualisations (onglet Méthode de réduction)

---

## Structure du projet (vue simplifiée)

- `PyQt5_Complete_App.py` — point d'entrée et UI principale (Front-end PyQt5)
- `db.py` — interactions SQLite locales (historique des fichiers)
- `requirements.txt` — dépendances
- `packages/` — backend applicatif
	- `modules/` — modules utilitaires
		- `loading.py` — classe `DataLoader` : charge CSV/JSON/Images/SQL et retourne DataFrame ou contenu brut
		- `file_tree.py` — helpers pour construire un arbre hiérarchique des fichiers / variables
		- `visualisation_2D.py`, `visualisation_3D.py` — fonctions/objets de visualisation
		- `analysis.py`, `netoyage.py`, `methode_acp.py`, `methode_tsne.py`, `methode_umap.py` — fonctions d'analyse
- `tests/` — tests unitaires
- `build/` et `PyQt5_Complete_App.spec` — artefacts pour PyInstaller (si packagé)


---

## Fonctionnalités principales

- Chargement de fichiers : CSV, TXT, JSON, Images, SQL via l'interface ou glisser-déposer.
- Arbre hiérarchique des fichiers chargés (colonne gauche) qui peut être utilisé pour sélectionner un jeu de données.
- Affichage des variables (colonnes) et sélection de celles-ci pour la visualisation.
- Méthodes de réduction de dimension intégrées : PCA (ACP), t-SNE, UMAP (optionnel, si installé).
- Choix d'affichage 2D ou 3D.
- Export des graphiques en PNG/JPEG/SVG via l'icône "💾 Teleharger image".
- Mode jour / nuit basculable avec un bouton (icône ☀ / 🌙).
- Le rendu des légendes a été désactivé par défaut (pas d'étiquettes par point), et les légendes globales ont été retirées pour éviter le débordement.

---

## Guide d'utilisation (nouvel utilisateur)

1. Lancer l'application (voir section précédente).
2. Charger un fichier :
	 - Utilisez le bouton "📁 Charger un fichier" (colonne gauche) ou glissez un fichier dans la zone prévue.
	 - Les fichiers pris en charge sont listés dans l'interface (CSV, JSON, images, SQL).
3. Sélectionner un fichier depuis l'arbre de fichiers (colonne gauche). L'interface construira un objet fichier interne et affichera la visualisation.
4. Choisir la méthode de réduction (ACP / t-SNE / UMAP) dans le menu déroulant.
5. Basculer entre 2D / 3D avec les boutons "2D" / "3D".
6. Exporter l'image si nécessaire en cliquant sur l'icône de téléchargement.
7. Activer le mode nuit en cliquant sur le bouton ☀ (il deviendra 🌙). Cliquer à nouveau pour revenir au mode jour.

Notes :
- Si `UMAP` n'est pas installé, il est montré comme "UMAP (non installé)" dans le menu et l'option est ignorée.
- En cas d'erreur lors de la visualisation, l'UI affiche désormais la traceback complète dans la zone de visualisation (utile pour déboguer les jeux de données incompatibles).

---

## Guide développeur — comment travailler sur le code

Objectif : expliquer rapidement où modifier le code pour les tâches courantes.

1. Architecture UI
	 - `PyQt5_Complete_App.py` contient la classe principale `MainWindow` et les sections UI importantes :
		 - `FileUploadSection` : zone de chargement et liste de fichiers
		 - `VisualizationSection` : panneaux et code de rendu (méthode `updateVisualization`)
		 - `VariablesSection` : panneau de variables (colonne gauche)
	 - Le `VisualizationSection` appelle les fonctions d'analyse (PCA/t-SNE/UMAP) et construit le canvas Matplotlib (`MplCanvas`).

2. Backend & loading
	 - `packages/modules/loading.py` : centralisez le code de chargement de fichiers ici via `DataLoader.load(path)`.
	 - `packages/modules/file_tree.py` : constructeurs d'arbre hiérarchique utilisés pour la colonne gauche.

3. Ajouter une nouvelle méthode d'analyse
	 - Ajouter la fonction dans `packages/modules/` (ex. `methode_new.py`) en suivant les signatures existantes (entrée : DataFrame / sortie : matrice 2D/3D à tracer).
	 - Mettre à jour l'UI : `self.method_combo.addItems([...])` et adapter `VisualizationSection.updateVisualization` pour gérer le nouvel index.

4. Rendre le plot respectueux du thème
	 - `MainWindow.apply_theme` gère le thème global via `setStyleSheet`. Pour que les figures Matplotlib suivent le thème, ajustez `matplotlib.rcParams` au moment d'appliquer le thème (par ex. `rcParams['figure.facecolor']`, `rcParams['axes.facecolor']`, `rcParams['text.color']`, etc.).

5. Débogage
	 - L'application affiche la traceback dans l'UI lorsque `updateVisualization` lève une exception. Copiez le texte pour comprendre l'erreur.
	 - Vous pouvez également exécuter `PyQt5_Complete_App.py` depuis un terminal pour voir stdout/stderr.

---

## Tests

Les tests unitaires se trouvent dans le dossier `tests/`.
Utilisez `pytest` depuis la racine du projet :

```powershell
pip install pytest
pytest -q tests
```

---

## Packaging (création d'un exécutable)

Le dépôt contient un fichier `PyQt5_Complete_App.spec` (artefacts PyInstaller). Pour créer un exécutable :

```powershell
pip install pyinstaller
pyinstaller PyQt5_Complete_App.spec
```

ou pour un exécutable unique :

```powershell
pyinstaller --onefile --windowed PyQt5_Complete_App.py
```

Note : le packaging peut nécessiter des ajustements pour inclure des ressources (images, données) ou corriger des chemins absolus.

---

## Dépannage (FAQs & résolutions)

- Problème : l'application ne s'ouvre pas / plante à l'exécution.
	- Vérifiez que vous utilisez la bonne version de Python (3.10+).
	- Activez l'environnement virtuel et réinstallez les dépendances.
	- Lancez depuis un terminal pour voir la sortie d'erreur : `python PyQt5_Complete_App.py`.

- Problème : UMAP non trouvé
	- Installer : `pip install umap-learn`.

- Problème : légende qui déborde / prend trop de place
	- Les légendes par-point ont été désactivées et la légende globale a été supprimée pour éviter les débordements. Si vous voulez un comportement différent (barre de légende rétractable ou multi-lignes), modifiez `updateVisualization` dans `VisualizationSection`.

- Problème : erreur AttributeError 'toggle_theme' appelée depuis une section
	- Le bouton thème a été connecté via un handler qui appelle la méthode du `QMainWindow` parent (robuste même si le bouton est créé dans une section enfant).

- Problème : erreurs inconnues dans la visualisation
	- L'app affiche maintenant la traceback complète dans la zone de visualisation. Copiez-la et recherchez les appels problématiques (p.ex. accès aux colonnes non-existantes, types non numériques, erreurs de réduction de dimension avec peu d'échantillons).

---

## Contribution

PRs bienvenues. Pour contribuer :

1. Forkez le dépôt.
2. Créez une branche feature/bugfix.
3. Ouvrez une Pull Request décrivant le changement.

Merci de documenter les changements majeurs et d'ajouter/mettre à jour les tests.

---

## Licence

Ajoutez ici la licence de votre choix (ex. MIT) ou contactez le mainteneur.

---

## Contact

Si vous avez besoin d'aide, ouvrez une issue dans le dépôt ou contactez le mainteneur indiqué dans le dépôt.


Bonne exploration et développement !
