import re

from teeth.pattern import matches
import teeth.pattern
import teeth.tokens

def test__matches__identifies_matching_expressions():

    match = matches( 'a|bb*' )

    assert match( 'a' )
    assert match( 'bbb' )
    assert match( 'abb' )
    assert not match( 'c' )

    
def test__matches__identifies_from_compiled_expressions():

    match = matches( re.compile( 'a|bb*' ) )

    assert match( 'a' )
    assert match( 'bbb' )
    assert not match( 'c' )


def test__punctuation__matches_typical():

    match = matches( teeth.pattern.punctuation )

    assert match( '.' )
    assert match( '?!' )
    assert match( '???' )
    assert match( '--' )
    assert match( '...' )

    assert not match( 'ok' )
    assert not match( ' ' )


def test__unicode_characters_in_english_punctuation():
    assert '\u2019' in teeth.tokens.english_punctuation
