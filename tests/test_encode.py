import teeth
import teeth.encode

def test__one_hot__generates_from_list():

    vocab = [ 'a', 'b', 'c', 'd' ]

    v1 = [ 'a', 'a', 'b', 'd' ]
    v2 = [ 'b', 'c', 'd', 'a' ]

    encoding = teeth.encode.OneHot( vocab )

    assert encoding.encode( v1 ) == [
        [ 0, 1, 0, 0, 0 ],
        [ 0, 1, 0, 0, 0 ],
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 0, 1 ],
    ]

    assert encoding.encode( v2 ) == [
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 1, 0 ],
        [ 0, 0, 0, 0, 1 ],
        [ 0, 1, 0, 0, 0 ],
    ]


def test__one_hot__places_unknown_token_first():

    vocab = [ 'a', 'b', 'c', 'd' ]

    v1 = [ 'a', 'x', 'x', 'd' ]
    v2 = [ 'b', 'c', 'd', 'x' ]

    encoding = teeth.encode.OneHot( vocab )

    assert encoding.encode( v1 ) == [
        [ 0, 1, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 1 ],
    ]

    assert encoding.encode( v2 ) == [
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 1, 0 ],
        [ 0, 0, 0, 0, 1 ],
        [ 1, 0, 0, 0, 0 ],
    ]


def test__one_hot__decodes_to_original_vocab():

    vocab = [ 'a', 'b', 'c', 'd' ]

    encoding = teeth.encode.OneHot( vocab )

    v1 = [
        [ 0, 1, 0, 0, 0 ],
        [ 0, 1, 0, 0, 0 ],
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 0, 1 ],
    ]

    v2 = [
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 1, 0 ],
        [ 0, 0, 0, 0, 1 ],
        [ 0, 1, 0, 0, 0 ],
    ]

    assert encoding.decode( v1 ) == [ 'a', 'a', 'b', 'd' ]
    assert encoding.decode( v2 ) == [ 'b', 'c', 'd', 'a' ]


def test__one_hot__decodes_first_dimension_to_empty():

    vocab = [ 'a', 'b', 'c', 'd' ]

    encoding = teeth.encode.OneHot( vocab )

    v1 = [
        [ 0, 1, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0 ],
        [ 1, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 1 ],

    ]

    v2 = [
        [ 0, 0, 1, 0, 0 ],
        [ 0, 0, 0, 1, 0 ],
        [ 0, 0, 0, 0, 1 ],
        [ 1, 0, 0, 0, 0 ],

    ]

    assert encoding.decode( v1 ) == [ 'a', '', '', 'd' ]
    assert encoding.decode( v2 ) == [ 'b', 'c', 'd', '' ]
