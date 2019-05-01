from nltk.stem.snowball import EnglishStemmer

nltk_english_stemmer = EnglishStemmer()

def stem( token ):
    return nltk_english_stemmer( token )
