from teeth.array import CharArray, SliceArray, Strata
from teeth.array import TextStrata, layer

from teeth.pattern import matches


def test__chararray__getitem__returns_slice():

    a = CharArray( 'ok wow' )

    assert 'o' == a[ 0 ]
    assert 'ok ' == a[ slice( 3 ) ]
    assert 'ok' == a[ 0 : 2 ]
    assert 'wow' == a[ 3 : ]

    assert 'wow k' == a[ slice( -1, -6, -1 ) ]
    assert 'k wo' == a[ slice( -5, -1, 1 ) ]


def test__slicearray__creates_iterable_of_slices():

    s = SliceArray( [ 0, 2, 5 ] )

    assert 2 == len( s )

    _slice = iter( s )

    assert slice( 0, 2 ) == next( _slice )
    assert slice( 2, 5 ) == next( _slice )

    try:
        next( _slice )
    except StopIteration:
        return

    raise AssertionError( 'expected \'StopIteration\' raised.' )


def test__slicearray__indexes_by_integer():

    s = SliceArray( [ 0, 2, 5, 13 ] )

    assert slice( 0, 2 ) == s[ 0 ]
    assert slice( 2, 5 ) == s[ 1 ]
    assert slice( 5, 13 ) == s[ 2 ]

    try:
        x = s[ 3 ]
    except IndexError:
        return

    raise AssertionError( 'expected \'IndexError\' raised' )


def test__slicearray__indexes_by_slice():

    s = SliceArray( [ 0, 2, 5, 13, 23, 29 ] )

    sl0 = s[ 1 : 3 ]

    assert slice( 2, 5 ) == sl0[ 0 ]
    assert slice( 5, 13 ) == sl0[ 1 ]

    sl1 = s[ 3 : ]

    assert slice( 13, 23 ) == sl1[ 0 ]
    assert slice( 23, 29 ) == sl1[ 1 ]

    try:
        x = sl1[ 2 ]
    except IndexError:
        return

    raise AssertionError( 'expected \'IndexError\' raised.' )


def test__slicearray__identifies_first_and_last_indices():

    s = SliceArray( [ 5, 13, 23, 29 ] )

    assert 5 == s.start
    assert 29 == s.stop


def test__slicearray__shifts_both_left_and_right():

    s = SliceArray( [ 5, 13, 23, 29 ] )

    left = s.shift( 3 )

    assert 8 == left.start
    assert 32 == left.stop
    assert slice( 8, 16 ) == left[ 0 ]
    assert slice( 16, 26 ) == left[ 1 ]
    assert slice( 26, 32 ) == left[ 2 ]

    right = s.shift( -2 )

    assert 3 == right.start
    assert 27 == right.stop
    assert slice( 3, 11 ) == right[ 0 ]
    assert slice( 11, 21 ) == right[ 1 ]
    assert slice( 21, 27 ) == right[ 2 ]


def test__strata__empty__layers_returns_whole_list():

    s = Strata()
    data = 'ok wow'

    assert data == s.sieve( data )


def test__strata__applies_slices_from_single_layer():

    s = Strata()
    s.add_layer( [ 0, 3, 5, 10 ] )

    data = '0123456789'

    assert [ '012', '34', '56789' ] == s.sieve( data )


def test__strata__slices_multiple_subsequent_layers():

    s = Strata()

    s.add_layer( [ 0, 3, 5, 10 ] )
    s.add_layer( [ 0, 2, 3 ] )

    data = '0123456789'

    assert [ [ '012', '34' ], [ '56789' ] ] == s.sieve( data )


def test__strata__interprets_none_as_remainder_of_iterable():

    s = Strata()
    s.add_layer( [ 0, 3, 5, None ] )

    data = '0123456789'

    assert [ '012', '34', '56789' ] == s.sieve( data )

    s.add_layer( [ 0, 2, None ] )

    assert [ [ '012', '34' ], [ '56789' ] ] == s.sieve( data )


def test__strata__creates_from_nested_list():

    data = '0123456789abcdef'

    s = Strata( layers=[ [ 5, 10, 13 ] ] )

    assert [ '56789', 'abc' ] == s.sieve( data )


def test__strata__returns_instance_restriced_to_given_top_index():

    data = '0123456789abcdef'

    s = Strata()
    s.add_layer( [ 0, 3, 5, 10, 13, 17, 23 ] )

    scalar_0 = s[ 3 ]

    assert [ 'abc' ] == scalar_0.sieve( data )

    s.add_layer( [ 0, 2, 4, None ] )

    scalar_1 = s[ 1 ]

    assert [ [ '56789', 'abc' ] ] == scalar_1.sieve( data )

    s.add_layer( [ 0, 1, 2 ] )

    scalar_2_0 = s[ 0 ]

    assert [ [ [ '012', '34' ] ] ] == scalar_2_0.sieve( data )

    scalar_2_1 = s[ 1 ]

    assert [ [ [ '56789', 'abc' ] ] ] == scalar_2_1.sieve( data )


def test__textstrata__getitem__returns_slice_at_zero_level():

    t = TextStrata( 'ok wow' )

    assert 'k' == t[ 1 ]
    assert 'wow' == t[ 3: ]

    assert 'wow k' == t[ slice( -1, -6, -1 ) ]
    assert 'k wo' == t[ slice( -5, -1, 1 ) ]


def test__textstrata__splits_on_predicate():

    t = TextStrata( 'ok wow neat' )

    def word_ends( x ):
        return ' ' == x 

    t.split_where( word_ends )

    assert 5 == len( t )

    assert t[ 0 ] == 'ok'
    assert t[ 1 ] == ' '
    assert t[ 2 ] == 'wow'
    assert t[ 3 ] == ' '
    assert t[ 4 ] == 'neat'


def test__textstrata__layers_splits():

    text = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them!
Life is the evil here!
And death the great goal!"""

    t = TextStrata( text )

    def word_ends( x ):
        return matches( '[ \n!]+' )( x )

    t.split_where( word_ends )

    assert 56 == len( t )

    def sentence_ends( x ):
        return 0 < len( x ) and x[ 0 ] in '.?!'

    t.split_where( sentence_ends )

    assert 6 == len( t )

    first = [ 'Apokolips', ' ', 'is', ' ', 'an', ' ', 'armed',
              ' ', 'camp', '\n', 'where', ' ', 'those', ' ',
              'who', ' ', 'live', ' ', 'with', ' ',  'weapons',
              '\n', 'rule', ' ',  'the', ' ',  'wretches', ' ',
              'who', ' ', 'build', ' ', 'them' ]

    assert first == t[ 0 ]

    second = [ '!' ]

    assert second == t[ 1 ]

    third = [ '\n', 'Life', ' ', 'is', ' ',
              'the', ' ', 'evil', ' ', 'here' ]

    assert third == t[ 2 ]

    fourth = [ '!' ]

    assert fourth == t[ 3 ]


def test__textstrata__iterable_by_item():

    text = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them!
Life is the evil here!
And death the great goal!"""

    t = TextStrata( text )

    def word_ends( x ):
        return matches( '[ \n!]+' )( x )

    t.split_where( word_ends )

    def sentence_ends( x ):
        return 0 < len( x ) and x[ 0 ] in '.?!'

    t.split_where( sentence_ends )

    item = iter( t )

    first = [ 'Apokolips', ' ', 'is', ' ', 'an', ' ', 'armed',
              ' ', 'camp', '\n', 'where', ' ', 'those', ' ',
              'who', ' ', 'live', ' ', 'with', ' ',  'weapons',
              '\n', 'rule', ' ',  'the', ' ',  'wretches', ' ',
              'who', ' ', 'build', ' ', 'them' ]

    assert first == next( item )

    second = [ '!' ]

    assert second == next( item )

    third = [ '\n', 'Life', ' ', 'is', ' ',
              'the', ' ', 'evil', ' ', 'here' ]

    assert third == next( item )

    fourth = [ '!' ]

    assert fourth == next( item )


def test__layer_context__evaluates_at_a_given_depth():

    text = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them!
Life is the evil here!
And death the great goal!"""

    t = TextStrata( text )

    def word_ends( x ):
        return matches( '[ \n!]+' )( x )

    t.split_where( word_ends )

    with layer( 0, t ) as l:
        assert 0 == l.depth
        assert 'is an armed ' == l[ 10 : 22 ]

    assert 1 == t.depth
    assert 'where' == t[ 10 ]
