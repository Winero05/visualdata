import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import numpy as np
import re

class TextVisualizer:
    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError("Les données doivent être un texte (string).")
        self.text = text
        self.words = re.findall(r'\b\w+\b', text.lower())  # liste des mots en minuscules

    def basic_stats(self):
        """Affiche des statistiques simples sur le texte"""
        n_chars = len(self.text)
        n_words = len(self.words)
        n_lines = self.text.count("\n") + 1
        print(f"Nombre de caractères : {n_chars}")
        print(f"Nombre de mots : {n_words}")
        print(f"Nombre de lignes : {n_lines}")

    def word_length_hist(self):
        """Histogramme de la longueur des mots"""
        lengths = [len(w) for w in self.words]
        plt.figure(figsize=(8,5))
        plt.hist(lengths, bins=range(1, max(lengths)+2), color='skyblue', edgecolor='black')
        plt.title("Distribution des longueurs de mots")
        plt.xlabel("Longueur des mots")
        plt.ylabel("Fréquence")
        plt.show()

    def sentence_length_hist(self):
        """Histogramme de la longueur des phrases"""
        sentences = re.split(r'[.!?]+', self.text)
        lengths = [len(s.split()) for s in sentences if len(s.strip()) > 0]
        plt.figure(figsize=(8,5))
        plt.hist(lengths, bins=range(1, max(lengths)+2), color='salmon', edgecolor='black')
        plt.title("Distribution de la longueur des phrases (en mots)")
        plt.xlabel("Nombre de mots par phrase")
        plt.ylabel("Fréquence")
        plt.show()

    def most_common_words(self, top_n=20):
        """Barplot des mots les plus fréquents"""
        counter = Counter([w for w in self.words if w not in STOPWORDS])
        common = counter.most_common(top_n)
        words, counts = zip(*common)

        plt.figure(figsize=(10,6))
        plt.bar(words, counts, color='lightgreen', edgecolor='black')
        plt.xticks(rotation=45)
        plt.title(f"Top {top_n} mots les plus fréquents")
        plt.ylabel("Fréquence")
        plt.show()

    def generate_wordcloud(self, max_words=200):
        """Nuage de mots"""
        wc = WordCloud(width=800, height=400, background_color='white',
                       stopwords=STOPWORDS, max_words=max_words, collocations=False).generate(self.text)
        plt.figure(figsize=(12,6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.title("Nuage de mots")
        plt.show()

    def bigram_analysis(self, top_n=20):
        """Analyse des bigrams les plus fréquents"""
        from nltk import bigrams
        bigram_list = list(bigrams(self.words))
        counter = Counter(bigram_list)
        common = counter.most_common(top_n)
        bigrams_str = [' '.join(b) for b, _ in common]
        counts = [c for _, c in common]

        plt.figure(figsize=(12,6))
        plt.bar(bigrams_str, counts, color='orange', edgecolor='black')
        plt.xticks(rotation=45)
        plt.title(f"Top {top_n} bigrams les plus fréquents")
        plt.ylabel("Fréquence")
        plt.show()
'''
=== Exemple d'utilisation ===
if __name__ == "__main__":
    text = """Ceci est un exemple de texte. Il contient plusieurs phrases.
              Vous pouvez tester les différentes visualisations ici!"""
    tv = TextVisualizer(text)
    tv.basic_stats()
    tv.word_length_hist()
    tv.sentence_length_hist()
    tv.most_common_words()
    tv.generate_wordcloud()
    tv.bigram_analysis()
'''