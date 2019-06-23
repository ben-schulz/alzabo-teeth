import re
import pickle

from teeth.pattern import english_alpha_word, english_sentence
from teeth.stream import Span, RegexCursor, stratify
from teeth.transforms import lower

class Digest:

    def __init__( self, text,
                  outer_pattern=english_sentence,
                  inner_pattern=english_alpha_word,
                  keep_inner_separators=False,
                  keep_outer_separators=False,

                  _spans=None,
                  _vocab=None,
    ):

        self.text = text

        self.outer_pattern = outer_pattern
        self.inner_pattern = inner_pattern
        
        if _spans is None:
            outer_tokens = [ span for span in RegexCursor(
                outer_pattern, text,
                keep_separators=keep_outer_separators ) ]

            inner_tokens = [ span for span in RegexCursor(
                inner_pattern, text,
                keep_separators=keep_inner_separators ) ]

            self.spans = stratify( outer_tokens, inner_tokens )

        else:
            self.spans = _spans

        self.tokens = [ [ span.apply( text ) for span in token ]
                        for token in self.spans ]

        if _vocab is None:
            vocab = set()
            for outer in self.tokens:
                for inner in outer:
                    vocab.add( lower( inner ) )
            self.vocab = tuple( vocab )

        else:
            self.vocab = _vocab        


    def dump( self, f ):

        obj = {
            'text': self.text,
            'spans': self.spans,
            'vocab': self.vocab,
        }

        pickle.dump( obj, f )


    def load( f ):

        obj = pickle.load( f )

        text = obj[ 'text' ]
        spans= obj[ 'spans' ]
        vocab = obj[ 'vocab' ]

        return Digest( text, _spans=spans, _vocab=vocab )
