"""Ce module se charge de remplacer les empaces vides d'une
chaîne de caractère par des underscores.

Returns:
    str: Chaîne de caractère avec des underscores.
"""

class StringUtils:
    """
    Classe utilitaire pour les opérations sur les chaînes de caractères.
    Fournit des méthodes utilitaires sans état pour transformer des chaînes.
    Actuellement, la classe expose des fonctions utilitaires implémentées comme méthodes statiques.

    Méthodes
    -------

    sans_espace(chaine: str) -> str
        Retourne une nouvelle chaîne où tous les caractères d'espacement simples (' ')
        sont remplacés par des underscores ('_').

            chaine (str): Chaîne d'entrée potentiellement contenant des espaces.
            str: Nouvelle chaîne avec les espaces remplacés par des underscores.

        Exemple:
            >>> StringUtils.sans_espace("colonne avec espace")
    >>> colonne_avec_espace
    """


    def sans_espace(self, chaine: str) -> str:
        """
        Remplace les espaces par des underscores dans une chaîne de caractères.

        Args:
            chaine (str): Chaîne de caractères pouvant contenir des espaces.

        Returns:
            str: Chaîne de caractères avec les espaces remplacés par des underscores.
        
        Example:
        >>> chaine = "colonne avec espace"
        >>> chaine_modifier = sans_espace(chaine)
        >>> print(chaine_modifier)
        'colonne_avec_espace'
        """
        return chaine.replace(" ", "_")
