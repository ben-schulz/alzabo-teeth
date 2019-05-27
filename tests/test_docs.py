"""
these tests verify that the working examples
used by the notebooks in the 'docs' folder
do, in fact, work.

if they fail, then either the code is broke
or the docs need to be updated.

(2019.05.22) \0
"""

import os

this_file = os.path.abspath( __file__ )
this_dir = os.path.join( os.path.dirname( this_file ) )
parent_dir = os.path.join( this_dir, '..' )

raw_text_path = os.path.join( parent_dir, 'docs/moby_dick.txt' )

def test__array_module__examples_work():

    with open( raw_text_path, 'r') as f:
        raw_text = f.read()

    assert 'MOBY-DICK;\n\nor, THE WHALE.\n' == raw_text[ 0 : 27 ]

    from teeth.array import TextStrata

    t = TextStrata( raw_text )

    assert 'MOBY-DICK;\n\nor, THE WHALE.\n' == t[ 0 : 27 ]

    from teeth.array import split

    def not_a_word( x ):
        return x in ' \n'

    with split( not_a_word, t ) as words:
        assert ( [
            'MOBY-DICK;', '\n\n', 'or,',
            ' ', 'THE', ' ', 'WHALE.' ] == words[ 0 : 7 ] )

    def not_a_word( x ):
        return x in ' \n;,.!?'

    with split( not_a_word, t ) as words:
        assert ( [
            'MOBY-DICK', ';\n\n', 'or',
            ', ', 'THE', ' ', 'WHALE' ] == words[ 0 : 7 ] )

    assert 'MOBY-DI' == t[ 0 : 7 ]

    t.split_where( not_a_word )

    assert ( [ 'MOBY-DICK', ';\n\n', 'or', ', ', 'THE', ' ', 'WHALE']
             == t[ 0 : 7 ] )

    assert ( [ 'He', ' ', 'is', ' ', 'seldom', ' ', 'seen', ';\n',
               'at', ' ', 'least', ' ', 'I', ' ', 'have', ' ', 'never',
               ' ', 'seen', ' ', 'him', ' ', 'except', ' ', 'in', ' ',
               'the', ' ', 'remoter', ' ', 'southern', ' ', 'seas',
               ', ', 'and', '\n', 'then', ' ', 'always', ' ', 'at',
               ' ', 'too', ' ', 'great', ' ', 'a', ' ', 'distance',
               ' ', 'to', ' ', 'study', ' ', 'his', ' ',
               'countenance', '. ']
             == t[ 111198 : 111256 ] )

    expected = [ 'MOBY-DICK', ';\n\n', 'or', ', ', 'THE', ' ', 'WHALE']
    token = iter( t )
    for ix in range( 7 ):
        assert next( token ) == expected[ ix ]


    def sentence_ends( x ):
        return 0 < len( x ) and x[ 0 ][ 0 ] in '.?!'

    expected = [
        ['“‘Come', ' ', 'out', ' ', 'of', ' ', 'that', ', ', 'ye', ' ', 'pirates'],
        ['!'],
        ['’', ' ', 'roared', ' ', 'the', ' ', 'captain', ', ', 'now', ' ', 'menacing', ' ', 'them', '\n', 'with', ' ', 'a', ' ', 'pistol', ' ', 'in', ' ', 'each', ' ', 'hand', ', ', 'just', ' ', 'brought', ' ', 'to', ' ', 'him', ' ', 'by', ' ', 'the', ' ', 'steward'],
        ['. '],
        ['‘Come', '\n', 'out', ' ', 'of', ' ', 'that', ', ', 'ye', ' ', 'cut-throats'],
        ['!'],
        ['’', '\n\n', '“Steelkilt', ' ', 'leaped', ' ', 'on', ' ', 'the', ' ', 'barricade', ', ', 'and', ' ', 'striding', ' ', 'up', ' ', 'and', ' ', 'down', ' ', 'there', ',\n', 'defied', ' ', 'the', ' ', 'worst', ' ', 'the', ' ', 'pistols', ' ', 'could', ' ', 'do', '; ', 'but', ' ', 'gave', ' ', 'the', ' ', 'captain', ' ', 'to', '\n', 'understand', ' ', 'distinctly', ', ', 'that', ' ', 'his', ' ', '(Steelkilt’s)', ' ', 'death', ' ', 'would', ' ', 'be', ' ', 'the', ' ', 'signal', '\n', 'for', ' ', 'a', ' ', 'murderous', ' ', 'mutiny', ' ', 'on', ' ', 'the', ' ', 'part', ' ', 'of', ' ', 'all', ' ', 'hands'],
        ['. '],
        ['Fearing', ' ', 'in', ' ', 'his', ' ', 'heart', '\n', 'lest', ' ', 'this', ' ', 'might', ' ', 'prove', ' ', 'but', ' ', 'too', ' ', 'true', ', ', 'the', ' ', 'captain', ' ', 'a', ' ', 'little', ' ', 'desisted', ', ', 'but', '\n', 'still', ' ', 'commanded', ' ', 'the', ' ', 'insurgents', ' ', 'instantly', ' ', 'to', ' ', 'return', ' ', 'to', ' ', 'their', ' ', 'duty'],
        ['.\n\n']
    ]

    with split( sentence_ends, t ) as sentences:
        for ix in range( 10050, 10060 ):
            assert expected[ ix - 10050 ] == sentences[ ix ]

    from teeth.array import layer

    with layer( 0, t ) as char_level:
        assert ( 'MOBY-DICK;\n\nor, THE WHALE.\n'
                     == char_level[ 0 : 27 ] )

    with layer( 1, t ) as word_level:
        assert ( ['MOBY-DICK', ';\n\n', 'or', ', ', 'THE', ' ', 'WHALE'] == word_level[ 0 : 7 ] )
