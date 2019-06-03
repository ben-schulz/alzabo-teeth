from teeth.stream import Span, Flux

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

    span.stratify( Span( 1, 3 ), Span( 4, 7 ), relative=True )

    result = span.apply( text )

    assert [ '89', 'bcd' ] == result

    span = Span( 7, 15 )

    span.stratify( Span( 8, 10 ), Span( 11, 14 ), relative=False )

    result = span.apply( text )

    assert [ '89', 'bcd' ] == result


def test__span__apply__nests_subspans_recursively():

    text = '0123456789abcdef0123456789abcdef'

    span = Span( 2, 31 )

    assert '23456789abcdef0123456789abcde' == span.apply( text )

    ( left, right ) = span.excise( 10, 17 )

    assert '23456789' == left.apply( text )
    assert '0123456789abcde' == right.apply( text )

    span.stratify( left, right )

    result = span.apply( text )

    assert [ '23456789', '0123456789abcde' ] == result


def test__usecase__sentence_tokenize():

    raw = """There came a time when the old gods died! 
The brave died with the cunning! The noble perished,
locked in battle with unleashed evil!

It was the last day for them! 

An ancient era was passing in fiery holocaust!"""

    def sentence_end( x ):
        return x in '.?!'

    def word_end( x ):
        return x in ' \n,'

    flow = Flux( splits=( sentence_end, word_end ) )
