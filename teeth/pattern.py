import re
import string

alpha_word = re.compile( '[a-zA-Z]+' )
non_word = re.compile( '[^a-zA-Z]+' )
alphanum_word = re.compile( '[a-zA-Z]+' )

punctuation = re.compile( '[{}]+'.format(
    re.escape( string.punctuation ) ) )

sentence_terminator = re.compile( '[.?!]+' )

def matches( pattern ):

    if isinstance( pattern, str ):
        rexpr = re.compile( pattern )
    else:
        rexpr = pattern

    def _only( x ):
        return rexpr.search( x )

    return _only
