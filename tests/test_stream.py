import re
import string

from teeth.stream import Flux
from teeth.transforms import upper, lower, replace, remove


def test__empty__is_a_plain_iterable():

    f = iter( Flux( 'the cat sat on the mat.' ) )

    first = next( f )
    second = next( f )

    assert 't' == first
    assert 'h' == second


def test__wind__applies_a_transformation():

    f = Flux( 'the cat sat on the mat.' )

    f.wind( upper )

    flow = iter( f )

    first = next( flow )
    second = next( flow )

    assert 'T' == first
    assert 'H' == second


def test__iter__produces_stop_iteration_on_no_more_data():

    f = Flux( 'the' )

    f.wind( upper )

    flow = iter( f )

    assert 'T' == next( flow )
    assert 'H' == next( flow )
    assert 'E' == next( flow )

    try:
        next( flow )

    except StopIteration:
        return

    assert False, 'expected \'StopIteration\' raised.'


def test__wind__applies_multiple_subsequent_transformation():

    f = Flux( 'abcdabcd' )

    f.wind( replace( 'd', '-' ) )
    f.wind( upper )
    f.wind( replace( '-', 'e' ) )

    flow = iter( f )

    result = []

    while True:
        try:
            result.append( next( flow ) )
        except StopIteration:
            break

    assert result == list( 'ABCeABCe' )

def test__unwind__removes_the_last_applied_transform():

    f = Flux( 'abcdabcd' )

    f.wind( replace( 'd', '-' ) )
    f.wind( upper )
    f.wind( replace( '-', 'e' ) )

    f.unwind()

    flow = iter( f )

    result = []

    while True:
        try:
            result.append( next( flow ) )
        except StopIteration:
            break

    assert result == list( 'ABC-ABC-' )


def test__getitem__return_slice_with_transforms():

    f = Flux( 'the cat sat on the mat.' )

    f.wind( upper )

    result = f[ 4:11 ]

    assert result == 'CAT SAT'


def test__split__returns_new_iterable_of_tokens():

    f = Flux( 'the cat sat on the mat.' )

    def on_nonword( x ):
        return x == ' ' or x == '.'

    result = f.split( on_nonword ).items()

    assert [ 'the', ' ', 'cat', ' ', 'sat', ' ',
             'on', ' ', 'the', ' ', 'mat', '.' ]


def test__usecase__sentence_tokenize():

    raw = """There came a time when the old gods died! 
The brave died with the cunning! The noble perished,
locked in battle with unleashed evil!

It was the last day for them! 

An ancient era was passing in fiery holocaust!"""

    char_level = Flux( raw )

    char_level.wind( lower )
    char_level.wind( remove( '\n' ) )

    assert ( 'there came a time when the old gods died! the' ==
             char_level[ 0 : 46 ] )

    nonalpha = re.compile( '[^A-Za-z]' )
    def on_nonalpha( x ):
        return nonalpha.match( x )

    word_level = char_level.split( on_nonalpha )

    assert ( [ 'there', ' ', 'came', ' ', 'a', ' ', 'time', ' ',
               'when', ' ', 'the', ' ', 'old', ' ', 'gods', ' ',
               'died', '!', ' ', 'the' ] == word_level[ 0 : 20 ] )

    def on_sentence( x ):
        return x in '.!?'

    sentence_level = word_level.split( on_sentence )

    assert [ 'there', ' ', 'came', ' ', 'a', ' ', 'time', ' ',
             'when', ' ', 'the', ' ', 'old', ' ', 'gods', ' ',
             'died' ] == sentence_level[ 0 ]

    assert [ '!' ] == sentence_level[ 1 ]
    assert 10 == len( sentence_level )
