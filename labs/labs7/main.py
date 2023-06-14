import random
from argparse import ArgumentParser, Namespace
from typing import Text

import nltk
import ssl
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk.book

ssl._create_default_https_context = ssl._create_unverified_context


def setup(libs: list[str]) -> None:
    for lib in libs:
        nltk.download(lib)


def tree_from_text(text: str) -> None:
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    tree = nltk.ne_chunk(tags)
    print(f"Tree: {tree}")


def gutenberg_analysis(resource: str, word: str, dispersions: list[str]):
    text = nltk.Text(nltk.corpus.gutenberg.words(resource))
    print(f"Concordance: {text.concordance(word)}")
    text.dispersion_plot(dispersions)
    plt.show()

    nltk.FreqDist(
        [
            word for word in text
            if word not in nltk.corpus.stopwords.words("english")
        ]
    ).plot(20, cumulative=False)
    print(f"Collocations: {text.collocations()}")


def twitter_analysis():
    sia = SentimentIntensityAnalyzer()
    tweets = [
        t.replace("://", "//") for t in nltk.corpus.twitter_samples.strings()
    ]

    for t in random.sample(tweets, 10):
        score = sia.polarity_scores(t)
        print(score) if score.get("compound") < 0 else None


def book_analysis(resource: str, words: list[str]):
    o = nltk.book.text8.concordance('lady')
    print(type(o))
    exit()
    print(f"o -> {o}")
    print(f"Concordance: {nltk.book.text8.concordance('lady')}")
    nltk.book.text8.dispersion_plot(words)
    plt.show()


def args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-d", "--download", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = args()
    if args.download:
        setup([
            'punkt',
            'gutenberg',
            'averaged_perceptron_tagger',
            'maxent_ne_chunker',
            'words',
            'stopwords',
            'book',
            'draw',
            'vader_lexicon',
            'twitter_samples']
        )
    # print(nltk.corpus.gutenberg.fileids())
    # gutenberg_analysis("shakespeare-macbeth.txt", "doth", ["Macbeth", "King", "hath"])
    twitter_analysis()
    book_analysis(
        "text-8.txt:",
        ["woman", "lady", "girl", "man", "gentleman", "boy", "guy"]
    )


