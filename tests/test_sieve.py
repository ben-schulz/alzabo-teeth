import teeth.sieve

removed = teeth.sieve.removed

def test__only__replaces_tokens_not_in_list():

    words = 'the cat sat on the mat'.split( ' ' )

    keep = 'the sat on the '.split( ' ' )

    result = teeth.sieve.only( words, keep )

    assert ( [ 'the', removed, 'sat', 'on', 'the', removed ]
             == result )

def test__only_structure__replaces_all_non_stopwords():

    words = 'the cat sat on the mat .'.split( ' ' )

    keep = 'the on the '.split( ' ' )

    result = teeth.sieve.only_structure( words )

    assert ( [ 'the', removed, removed, 'on', 'the', removed, '.' ]
             == result )

