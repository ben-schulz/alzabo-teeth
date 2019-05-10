from teeth.array import CharArray, TextStrata, TokenSequence
from teeth.array import Strata
from teeth.array import isscalar

def test__isscalar__detects_slice_structure():

    assert isscalar( 2 )
    assert not isscalar( slice( 2 ) )
    assert not isscalar( slice( 2, 5 ) )
    assert not isscalar( slice( 2, 5, 2 ) )


def test__chararray__getitem__returns_slice():

    a = CharArray( 'ok wow' )

    assert 'o' == a[ 0 ]
    assert 'ok ' == a[ slice( 3 ) ]
    assert 'ok' == a[ 0 : 2 ]
    assert 'wow' == a[ 3 : ]

    assert 'wow k' == a[ slice( -1, -6, -1 ) ]
    assert 'k wo' == a[ slice( -5, -1, 1 ) ]


def test__strata__empty__layers_returns_whole_list():

    s = Strata()
    data = 'ok wow'

    assert data == s.sieve( data )


def test__strata__applies_slices_from_single_layer():

    s = Strata()
    s.layer( [ 0, 3, 5, 10 ] )

    data = '0123456789'

    assert [ '012', '34', '56789' ] == s.sieve( data )


def test__strata__slices_multiple_subsequent_layers():

    s = Strata()

    s.layer( [ 0, 3, 5, 10 ] )
    s.layer( [ 0, 2, 3 ] )

    data = '0123456789'

    assert [ [ '012', '34' ], [ '56789' ] ] == s.sieve( data )


def test__strata__interprets_none_as_remainder_of_iterable():

    s = Strata()
    s.layer( [ 0, 3, 5, None ] )

    data = '0123456789'

    assert [ '012', '34', '56789' ] == s.sieve( data )

    s.layer( [ 0, 2, None ] )

    assert [ [ '012', '34' ], [ '56789' ] ] == s.sieve( data )


def test__strata__creates_from_nested_list():

    data = '0123456789abcdef'
    s = Strata( layers=[ [ 5, 10 ] ] )
    assert [ '56789' ] == s.sieve( data )


def test__strata__returns_instance_restriced_to_given_slice():

    data = '0123456789abcdef'

    s = Strata()
    s.layer( [ 0, 3, 5, 10, 13, 17, 23 ] )

    scalar_0 = s[ 3 ]

    assert [ 'abc' ] == scalar_0.sieve( data )

    s.layer( [ 0, 2, 4, None ] )

    scalar_1 = s[ 1 ]

    assert [ '56789', 'abc' ] == scalar_1.sieve( data )



def test__textstrata__getitem__returns_slice_at_zero_level():

    t = TextStrata( 'ok wow' )

    assert 'k' == t[ 1 ]
    assert 'wow' == t[ 3: ]

    assert 'wow k' == t[ slice( -1, -6, -1 ) ]
    assert 'k wo' == t[ slice( -5, -1, 1 ) ]


def test__tokensequence__iterates_over_intervals():

    t = TextStrata( 'ok wow neat' )

    seq = TokenSequence( [ 2, 3, 6, 7 ] )

    result = iter( seq )

    assert 'ok' == t[ next( result ) ]
    assert ' ' == t[ next( result ) ]
    assert 'wow' == t[ next( result ) ]
    assert ' ' == t[ next( result ) ]
    assert 'neat' == t[ next( result ) ]

def test__tokensequence__getitem__returns_slices():

    seq = TokenSequence( [ 2, 3, 6, 7 ] )

    assert slice( 0, 2 ) == seq[ 0 ]
    assert slice( 2, 3 ) == seq[ 1 ]
    assert slice( 3, 6 ) == seq[ 2 ]
    assert slice( 6, 7 ) == seq[ 3 ]


def test__tokensequence__getitem__admits_cross_slicing():

    seq_lower = TokenSequence( [ 2, 3, 6, 7, 9, 11, 17, 20 ] )
    seq_upper = TokenSequence( [ 2, 5 ] )

    result = [ seq_lower[ sl ] for sl in seq_upper ]

    assert 3 == len( result )

    assert [ slice( 0, 2 ),
             slice( 2, 3 ) ] == result[ 0 ]

    assert [ slice( 3, 6 ),
             slice( 6, 7 ),
             slice( 7, 9 ) ] == result[ 1 ]

    assert [ slice( 9, 11 ),
             slice( 11, 17 ),
             slice( 17, 20 ),
             slice( 20, None ) ] == result[ 2 ]


def test__tokensequence__getitem__interprets_negative_indices():

    seq = TokenSequence( [ 2, 5 ] )

    assert slice( 5, None ) == seq[ -1 ]
    assert slice( 2, 5 ) == seq[ -2 ]


def test__tokensequence__getitem__indexes_single_element():

    seq = TokenSequence( [ 2 ] )

    assert slice( 2, None ) == seq[ -1 ]
    assert seq[ -1 ].stop is None


def test__textstrata__splits_on_predicate():

    t = TextStrata( 'ok wow neat' )

    def word_ends( x ):
        return ' ' == x 

    t.split_where( word_ends )

    assert 5 == len( t )
    assert [ 'ok', ' ', 'wow', ' ', 'neat' ] == t.tokens()

    assert t[ 0 ] == 'ok'
    assert t[ 1 ] == ' '
    assert t[ 2 ] == 'wow'
    assert t[ 3 ] == ' '
    assert t[ 4 ] == 'neat'


def test__textstrata__adds_first_layers_manually():

    t = TextStrata( 'ok wow neat. that is great.' )

    t.add_layer( TokenSequence(
        [ 2, 3, 6, 7, 12, 13, 17, 18, 20, 21 ] ) )

    first = [ 'ok', ' ',  'wow', ' ', 'neat.',
              ' ', 'that', ' ', 'is', ' ',  'great.' ]

    for ix, token in enumerate( first ):
        assert token == t.get_token( ix )

    assert len( first ) == len( t.get_slice( slice( 0, None ) ) )


def test__textstrata__adds_subsequent_layers_manually():

    t = TextStrata( 'ok wow neat. that is great.' )

    t.add_layer( TokenSequence(
        [ 2, 3, 6, 7, 12, 13, 17, 18, 20, 21 ] ) )

    first = [ 'ok', ' ',  'wow', ' ', 'neat.',
              ' ', 'that', ' ', 'is', ' ',  'great.' ]

    t.add_layer( TokenSequence( [ 3, 5 ] ) )

    second = [ [ 'ok', ' ',  'wow' ], [ ' ', 'neat.' ],
               [ ' ', 'that', ' ', 'is', ' ',  'great.' ] ]

    foo = t.get_slice( slice( 0, 3 ) )


###    assert second[ 0 ] == foo[ 0 ]
#    assert second[ 1 ] == foo[ 1 ]
#    assert second[ 2 ] == foo[ 2 ]


def test__textstrata__layers_splits():

    text = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them!
Life is the evil here!
And death the great goal!"""

    t = TextStrata( text )

    def word_ends( x ):
        return not str.isalpha( x )

    def sentence_ends( x ):
        return '!' == x[ 0 ]

    t.split_where( word_ends )
    t.split_where( sentence_ends )

    assert 6 == len( t )

    first = [ 'Apokolips', ' ', 'is', ' ', 'an', ' ', 'armed',
              ' ', 'camp', ' ', 'where', ' ', 'those', ' ',
              'who', ' ', 'live', ' ', 'with', ' ',  'weapons',
              ' ', 'rule', ' ',  'the', ' ',  'wretches', ' ',
              'who', ' ', 'build', ' ', 'them' ]

#    assert first == t[ 0 ]
