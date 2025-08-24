import os
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def ler_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def ler_pdf(filepath):
    texto = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            texto += page.extract_text() or ""
    return texto

def preprocessar_texto(texto):
    tokens = nltk.word_tokenize(texto.lower())
    stop_words = set(stopwords.words('portuguese'))
    tokens_filtrados = [t for t in tokens if t.isalpha() and t not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens_lemmatizados = [lemmatizer.lemmatize(t) for t in tokens_filtrados]
    return ' '.join(tokens_lemmatizados)

def processar_email(entrada):
    if os.path.isfile(entrada):
        ext = os.path.splitext(entrada)[1].lower()
        if ext == '.txt':
            texto = ler_txt(entrada)
        elif ext == '.pdf':
            texto = ler_pdf(entrada)
        else:
            raise ValueError("Formato não suportado.")
    else:
        texto = entrada
    return preprocessar_texto(texto)
