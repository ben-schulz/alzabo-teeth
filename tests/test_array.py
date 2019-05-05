from teeth.array import CharArray, TextStrata, TokenSequence

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



def test__textstrata__splits_on_predicate():

    t = TextStrata( 'ok wow neat' )

    def word_ends( x ):
        return ' ' == x 

    t.split_where( word_ends )

    assert [ 'ok', ' ', 'wow', ' ', 'neat' ] == t.tokens()


def test__textstrata__layers_splits():
    pass
