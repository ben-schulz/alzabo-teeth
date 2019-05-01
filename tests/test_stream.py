from teeth.stream import Flux

def upper( x ):
    return x.upper()

def lower( x ):
    return x.lower()

def replace( target, replacement ):

    def _replace( x ):
        if x == target:
            return replacement
        else:
            return x

    return _replace


def test__empty__is_a_plain_iterable():

    f = iter( Flux( 'the cat sat on the mat.' ) )

    first = next( f )
    second = next( f )

    assert 't' == first
    assert 'h' == second


def test__wind__applies_a_transformation():

    f = Flux( 'the cat sat on the mat.' )

    f.wind( upper )

    flow = iter( f )

    first = next( flow )
    second = next( flow )

    assert 'T' == first
    assert 'H' == second


def test__iter__produces_stop_iteration_on_no_more_data():

    f = Flux( 'the' )

    f.wind( upper )

    flow = iter( f )

    assert 'T' == next( flow )
    assert 'H' == next( flow )
    assert 'E' == next( flow )

    try:
        next( flow )

    except StopIteration:
        return

    assert False, 'expected \'StopIteration\' raised.'


def test__wind__applies_multiple_subsequent_transformation():

    f = Flux( 'abcdabcd' )

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

def test__unwind__removes_the_last_applied_transform():

    f = Flux( 'abcdabcd' )

    f.wind( replace( 'd', '-' ) )
    f.wind( upper )
    f.wind( replace( '-', 'e' ) )

    f.unwind()

    flow = iter( f )

    result = []

    while True:
        try:
            result.append( next( flow ) )
        except StopIteration:
            break

    assert result == list( 'ABC-ABC-' )


def test__getitem__return_slice_with_transforms():

    f = Flux( 'the cat sat on the mat.' )

    f.wind( upper )

    result = f[ 4:11 ]

    assert result == 'CAT SAT'


def test__split__returns_new_iterable_of_tokens():

    f = Flux( 'the cat sat on the mat.' )

    def onspace( x ):
        return x == ' '

    result = f.split( onspace ).items()

    assert 'the cat sat on the mat.'.split() == result
