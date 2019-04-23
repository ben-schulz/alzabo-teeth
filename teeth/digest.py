import pandas
import nltk.probability

from teeth.tokenizer import tokenize
from teeth.filter import no_separators
from teeth.stemmer import stem

class Digest:

    def __init__( self, text ):

        tokens = tokenize( text )
        self.tokens = list( tokens )

        self.words = list( no_separators( self.tokens ) )
        self.word_freqdist = nltk.probability.FreqDist( self.words )

        self.raw_vocab = set(
            map( lambda x: x.lower(), self.words ) )

        word_stems = stem( no_separators( tokens ) )
        self.stemmed_vocab = set( word_stems )


    def to_dataframe( self ):

        d = { k: [ k, v ] for k, v in self.word_freqdist.items() }

        return pandas.DataFrame.from_dict( d, orient='index',
                                 columns=[ 'lexeme', 'count' ] )
