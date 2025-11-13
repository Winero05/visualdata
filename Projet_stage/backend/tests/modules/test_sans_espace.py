"""Test le module `Projet_stage/backend/modules/sans_espace.py`.
"""

from modules.sans_espace import StringUtils

class TestStringUtils:
    """Tests unitaires pour la méthode `sans_espace` de la classe `StringUtils`.
    Cette suite vérifie le comportement attendu de `sans_espace` dans plusieurs cas :
    - Remplacement des espaces par des underscores : "Chaîne avec des espaces" -> "Chaîne_avec_des_espaces".
    - Chaîne sans espaces : la méthode est idempotente et retourne la même chaîne.
    - Plusieurs espaces consécutifs : chaque espace est remplacé par un underscore, préservant le nombre d'espaces consécutifs.
    - Chaîne vide : retourne une chaîne vide.
    - Chaîne composée uniquement d'espaces : retourne une chaîne d'underscores de même longueur.
    Chaque test instancie `StringUtils` et appelle `sans_espace` pour valider la sortie attendue.
    """

    def test_sans_espace(self) -> None:
        """Test la méthode `sans_espace`.
        """
        chaine = "Chaîne avec des espaces"
        #Instanciation de classe.
        chargeur_string_utils = StringUtils()
        result = chargeur_string_utils.sans_espace(chaine)
        assert result == "Chaîne_avec_des_espaces"

    def test_sans_espace_no_spaces(self) -> None:
        """Test la méthode `sans_espace` avec une chaîne sans espaces."""
        chaine = "SansEspaces"
        chargeur_string_utils = StringUtils()
        result = chargeur_string_utils.sans_espace(chaine)
        assert result == "SansEspaces"

    def test_sans_espace_multiple_spaces(self) -> None:
        """Test la méthode `sans_espace` avec plusieurs espaces consécutifs."""
        chaine = "Chaîne  avec   plusieurs espaces"
        chargeur_string_utils = StringUtils()
        result = chargeur_string_utils.sans_espace(chaine)
        assert result == "Chaîne__avec___plusieurs_espaces"

    def test_sans_espace_empty_string(self) -> None:
        """Test la méthode `sans_espace` avec une chaîne vide."""
        chaine = ""
        chargeur_string_utils = StringUtils()
        result = chargeur_string_utils.sans_espace(chaine)
        assert result == ""

    def test_sans_espace_only_spaces(self) -> None:
        """Test la méthode `sans_espace` avec une chaîne contenant uniquement des espaces."""
        chaine = "   "
        chargeur_string_utils = StringUtils()
        result = chargeur_string_utils.sans_espace(chaine)
        assert result == "___"
