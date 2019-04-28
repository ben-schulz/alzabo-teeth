from teeth.stream import Flux

def test__empty__is_a_plain_iterable():

    f = iter( Flux( "the cat sat on the mat." ) )

    first = next( f )
    second = next( f )

    assert 't' == first
    assert 'h' == second

    
