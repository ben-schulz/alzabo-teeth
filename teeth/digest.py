from teeth.tokenizer import tokenize
from teeth.filter import no_separators
from teeth.stemmer import stem

class Digest:

    def __init__( self, text ):

        tokens = tokenize( text )
        words = no_separators( tokens )

        self.tokens = list( tokens )

        self.raw_vocab = set(
            map( lambda x: x.lower(), words ) )

        word_stems = stem( no_separators( tokens ) )
        self.stemmed_vocab = set( word_stems )
