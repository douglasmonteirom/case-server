import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from typing import List

class EmailProcessor:
    def __init__(self, language: str = "portuguese"):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words(language))

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        return nltk.word_tokenize(text)

    def lemmatize_token(self, tokens: List[str]) -> List[str]:
        return [self.lemmatizer.lemmatize(t.lower()) for t in tokens]

    def remove_stopword(self, tokens:List[str]) -> List[str]:
        return[t for t in tokens if t not in self.stop_words]

    def clean_text(self, text: str) -> str:
        tokens = self.tokenize(text)
        tokens = self.lemmatize_token(tokens)
        tokens = self.remove_stopword(tokens)
        return " ".join(tokens)
