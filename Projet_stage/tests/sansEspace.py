# lambda chaine: chaine.replace(" ", "_")

class SansEspace:
    """Suppression des espaces vide dans le nom des colonnes."""
    def sansEspace(chaine):
        """Retourne des chaîne de caractère sans espace."""
        return chaine.replace(" ", "_")