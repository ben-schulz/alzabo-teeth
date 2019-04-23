import re

alpha_word = re.compile( '[a-zA-Z]+' )

def no_separators( tokens ):
    return filter( lambda t: re.match( alpha_word, t ), tokens )
