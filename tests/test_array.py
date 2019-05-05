from teeth.array import CharArray, TextStrata, TokenSequence
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


def test__textstrata__layers_splits():

    text = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them!
Life is the evil here!
And death the great goal!"""

    t = TextStrata( text )

    def word_ends( x ):
        return str.isspace( x )

    def sentence_ends( x ):
        return '!' == x

    t.split_where( word_ends )
    t.split_where( sentence_ends )

#    assert 6 == len( t )

    first = """Apokolips is an armed camp
where those who live with weapons
rule the wretches who build them"""

#    assert first == t[ 0 ]
