from teeth.digest import Digest

text = """There came a time when the old gods died! 
The brave died with the cunning! The noble perished,
locked in battle with unleashed evil!

It was the last day for them! 

An ancient era was passing in fiery holocaust!"""


def test__digest__produces_sentence_word_tokenize():

    d = Digest( text )

    expect = [ [ 'There', 'came', 'a', 'time',
                'when', 'the', 'old', 'gods', 'died' ],
              [ 'The', 'brave', 'died', 'with', 'the', 'cunning' ],
              [ 'The', 'noble', 'perished',
                'locked', 'in', 'battle', 'with', 'unleashed', 'evil' ],
              [ 'It', 'was', 'the', 'last', 'day', 'for', 'them' ],
              [ 'An', 'ancient', 'era', 'was',
                'passing', 'in', 'fiery', 'holocaust' ],
    ]


    assert expect == d.tokens


def test__digest__produces_sentence_word_tokenize():

    d = Digest( text )

    with open( 'tests/test_pickle.pkl', 'wb' ) as f:
        d.dump( f )


    with open( 'tests/test_pickle.pkl', 'rb' ) as f:
        result = Digest.load( f )

    expect = [ [ 'There', 'came', 'a', 'time',
                'when', 'the', 'old', 'gods', 'died' ],
              [ 'The', 'brave', 'died', 'with', 'the', 'cunning' ],
              [ 'The', 'noble', 'perished',
                'locked', 'in', 'battle', 'with', 'unleashed', 'evil' ],
              [ 'It', 'was', 'the', 'last', 'day', 'for', 'them' ],
              [ 'An', 'ancient', 'era', 'was',
                'passing', 'in', 'fiery', 'holocaust' ],
    ]


    assert expect == result.tokens
