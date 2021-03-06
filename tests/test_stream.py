import re

from teeth.stream import Span, Flux, RegexCursor, stratify

def test__span__splits_at_single_index():

    span = Span( 2, 11 )

    ( left, right ) = span.split( 5 )

    assert 2 == left.start
    assert 5 == left.stop

    assert 5 == right.start
    assert 11 == right.stop


def test__span__excises_an_interior_interval():

    span = Span( 5, 29 )

    ( left, right ) = span.excise( 11, 23 )

    assert left.start == 5
    assert left.stop == 11

    assert right.start == 22
    assert right.stop == 29

    ( left, right ) = span.excise( *Span( 11, 23 ) )

    assert left.start == 5
    assert left.stop == 11

    assert right.start == 22
    assert right.stop == 29


def test__span__apply__works_like_slice_for_strings():

    text = "the cat sat on the mat."

    span = Span( 4, 11 )

    result = span.apply( text )

    assert 'cat sat' == result


def test__span__apply__nests_subspans_in_result():

    text = '0123456789abcdef'

    span = Span( 7, 15 )

    subspans = [ Span( 1, 3 ), Span( 4, 7 ) ]
    span.stratify( subspans, relative=True )

    result = span.apply( text )

    assert [ '89', 'bcd' ] == result

    span = Span( 7, 15 )

    subspans = [ Span( 8, 10 ), Span( 11, 14 ) ]
    span.stratify( subspans, relative=False )

    result = span.apply( text )

    assert [ '89', 'bcd' ] == result


def test__span__apply__nests_subspans_recursively():

    text = '0123456789abcdef0123456789abcdef'

    span = Span( 2, 31 )

    assert '23456789abcdef0123456789abcde' == span.apply( text )

    ( left, right ) = span.excise( 10, 17 )

    assert '23456789' == left.apply( text )
    assert '0123456789abcde' == right.apply( text )

    span.stratify( [ left, right ] )

    result = span.apply( text )

    assert [ '23456789', '0123456789abcde' ] == result


def test__regexcursor__iterates_over_matches():

    text = 'ok wow. yes! is that it ... ? ok.'

    pattern = '[\n ]*[.?!]+[^a-zA-Z0-9]*'

    cursor = RegexCursor( pattern, text )
    token = iter( cursor )

    assert '. ' == next( token ).apply( text )
    assert '! ' == next( token ).apply( text )
    assert ' ... ? ' == next( token ).apply( text )
    assert '.' == next( token ).apply( text )

    try:
        next( token )
        raise AssertionError( 'expected \'StopIteration\' raised.' )

    except StopIteration:
        pass


def test__regexcursor__optionally_keeps_separators():

    text = 'ok wow. yes! is that it ... ? ok.'

    pattern = '[\n ]*[.?!]+[^a-zA-Z0-9]*'

    cursor = RegexCursor( pattern, text, keep_separators=True )
    token = iter( cursor )

    assert 'ok wow' == next( token ).apply( text )
    assert '. ' == next( token ).apply( text )
    assert 'yes' == next( token ).apply( text )
    assert '! ' == next( token ).apply( text )
    assert 'is that it' == next( token ).apply( text )
    assert ' ... ? ' == next( token ).apply( text )
    assert 'ok' == next( token ).apply( text )
    assert '.' == next( token ).apply( text )

    try:
        next( token )
        raise AssertionError( 'expected \'StopIteration\' raised.' )

    except StopIteration:
        pass


def test__stratify__creates_tree_from_two_iterables():

    text = """There came a time when the old gods died!
The brave died with the cunning! The noble perished,
locked in battle with unleashed evil!

It was the last day for them!

An ancient era was passing in fiery holocaust!"""

    word_pattern = '[a-zA-Z]+'
    word_splits = [ span for span in
                    RegexCursor( word_pattern, text ) ]

    sentence_pattern = '[^.?!]+'
    sentence_splits = [ span for span in
                        RegexCursor( sentence_pattern, text ) ]

    flow = stratify( sentence_splits, word_splits )

    first = [ 'There', 'came', 'a', 'time',
              'when', 'the', 'old', 'gods', 'died' ]
    first_result = [ s.apply( text ) for s in flow[ 0 ] ]
    assert first == first_result

    second = [ 'The', 'brave', 'died', 'with', 'the', 'cunning' ]
    second_result = [ s.apply( text ) for s in flow[ 1 ] ]
    assert second == second_result

    third = [ 'The', 'noble', 'perished',
              'locked', 'in', 'battle', 'with', 'unleashed', 'evil' ]
    third_result = [ s.apply( text ) for s in flow[ 2 ] ]
    assert third == third_result

    fourth = [ 'It', 'was', 'the', 'last', 'day', 'for', 'them' ]
    fourth_result = [ s.apply( text ) for s in flow[ 3 ] ]
    assert fourth == fourth_result

    fifth = [ 'An', 'ancient', 'era', 'was',
              'passing', 'in', 'fiery', 'holocaust' ]
    fifth_result = [ s.apply( text ) for s in flow[ 4 ] ]
    assert fifth == fifth_result


def test__flux__tokenizes_at_simplex_level():

    raw = ' There came a time when the old gods died!'

    word_pattern = '[^ \t\n,.?!]+'

    flux = Flux( raw, word_pattern )

    words = [ 'There', 'came', 'a', 'time',
              'when', 'the', 'old', 'gods', 'died' ]

    assert words == [ w for ( w, _ ) in iter( flux ) ]


def test__flux__tokenizes_at_duplex_level():

    raw = """There came a time when the old gods died!
The brave died with the cunning! The noble perished,
locked in battle with unleashed evil!

It was the last day for them!

An ancient era was passing in fiery holocaust!"""

    sentence_end_pattern = re.compile( '[ ]*[.?!][ ]*' )

    sentence_pattern = '[^.?!]+'
    word_pattern = '[^ \n\t.?!,]+'

    flow = iter( Flux( raw,
                       sentence_pattern, inner_pattern=word_pattern ) )

    first = [ 'There', 'came', 'a', 'time',
              'when', 'the', 'old', 'gods', 'died' ]

    first_result, _ = next( flow )
    assert first == first_result

    second = [ 'The', 'brave', 'died', 'with', 'the', 'cunning' ]

    second_result, _ = next( flow )
    assert second == second_result

    third = [ 'The', 'noble', 'perished',
              'locked', 'in', 'battle', 'with', 'unleashed', 'evil' ]

    third_result, _ = next( flow )
    assert third == third_result
