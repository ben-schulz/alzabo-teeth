import re
import string

import teeth.tokens

english_alpha_word = '[a-zA-Z]+'
english_sentence = '[^.?!]+'

punctuation = '[{}]+'.format(
    re.escape( string.punctuation + '\u2018\u2019\u201c\u201d' +
    '\u0060\u00b4\u0022\u0027' ) )

sentence_terminator = '[.?!]+'

def matches( pattern ):

    if isinstance( pattern, str ):
        rexpr = re.compile( pattern )
    else:
        rexpr = pattern

    def _only( x ):

        if rexpr.search( x ):
            return True
        else:
            return False

    return _only
