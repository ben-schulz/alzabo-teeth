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


def remove( target ):
    return replace( target, '' )


def replace_when( condition, transform ):

    def _replace( x ):
        if condition( x ):
            return transform( x )
        else:
            return x

    return _replace
