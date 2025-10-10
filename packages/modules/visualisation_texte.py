"""Visualisation texte simple: wordcloud, aperit, etc. Placeholders utilitaires."""

from typing import List
from collections import Counter

class TextVisualizer:
    """Outils simples pour visualiser des textes (placeholder).

    Méthodes:
    - top_words(text, n=20): renvoie les n mots les plus fréquents
    """

    @staticmethod
    def top_words(text: str, n: int = 20):
        if not text:
            return []
        # simple tokenisation
        words = [w.strip("\n\t.,;:!?()[]\"'\-_").lower() for w in text.split() if w.strip()]
        counts = Counter(words)
        return counts.most_common(n)


if __name__ == '__main__':
    sample = "Ceci est un exemple. Ceci est un test. Test exemple exemple."
    print(TextVisualizer.top_words(sample, 5))
