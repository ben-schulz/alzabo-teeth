from nltk.stem.snowball import EnglishStemmer

def stem( tokens ):

    stm = EnglishStemmer()

    return map( stm.stem, tokens )
