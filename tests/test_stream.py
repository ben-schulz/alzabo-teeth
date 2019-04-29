from teeth.stream import Flux

def test__empty__is_a_plain_iterable():

    f = iter( Flux( "the cat sat on the mat." ) )

    first = next( f )
    second = next( f )

    assert 't' == first
    assert 'h' == second


def test__wind__applies_a_transformation():

    f = Flux( "the cat sat on the mat." )

    def lower( x ):
        return x.upper()

    f.wind( lower )

    flow = iter( f )

    first = next( flow )
    second = next( flow )

    assert 'T' == first
    assert 'H' == second


def test__iter__produces_stop_iteration_on_no_more_data():

    f = Flux( "the" )

    def lower( x ):
        return x.upper()

    f.wind( lower )

    flow = iter( f )

    assert 'T' == next( flow )
    assert 'H' == next( flow )
    assert 'E' == next( flow )

    try:
        next( flow )

    except StopIteration:
        pass
        return

    assert False, "expected 'StopIteration raised."


def test__wind__applies_multiple_subsequent_transformation():

    f = Flux( "abcdabcd" )

    def upper( x ):
        return x.upper()

    def replace( target, replacement ):

        def _replace( x ):
            if x == target:
                return replacement
            else:
                return x

        return _replace

    f.wind( replace( 'd', '-' ) )
    f.wind( upper )
    f.wind( replace( '-', 'e' ) )

    flow = iter( f )

    result = []

    while True:
        try:
            result.append( next( flow ) )
        except StopIteration:
            break

    assert result == list( 'ABCeABCe' )
