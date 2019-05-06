import numpy

def isscalar( sl ):

    try:
        start = sl.start
    except AttributeError:
        return True

    return False


class CharArray:

    def __init__( self, text, *args, **kwargs ):

        cs = [ ord( c ) for c in text ]
        self._data = numpy.array( cs )


    def __getitem__( self, sl ):

        try:
            start = sl.start
        except AttributeError:
            start = None

        try:
            stop = sl.stop
        except AttributeError:
            stop = None

        value = self._data[ sl ]

        if start is None and stop is None:
            return chr( value )

        return str.join( '', [ chr( c ) for c in value ] )


    def __len__( self ):
        return len( self._data )


class TokenSequence:

    def __init__( self, indices):
        self._indices = indices

    def __len__( self ):
        return 1 + len( self._indices )

    def __getitem__( self, sl ):

        if isscalar( sl ):

            if 0 < sl and sl < len( self._indices ):
                start = self._indices[ sl - 1 ]
                end = self._indices[ sl ]
                return slice( start, end )

            elif sl == len( self._indices ):
                return slice( self._indices[ -1 ], None )

            return slice( 0, self._indices[ sl ] )


        if 2 > len( self ):
            return slice( None )

        if 0 == sl.start:
            results = [ slice( 0, self._indices[ sl.start ] ) ]
        else:
            start = self._indices[ sl.start - 1 ]
            stop = self._indices[ sl.start ]
            results = [ slice( start, stop ) ]

        ix = 0
        indices = self._indices[ sl ]
        result_count = len( indices ) - 1
        while ix < result_count:
            start = indices[ ix ]
            stop = indices[ ix + 1 ]
            results.append( slice( start, stop ) )
            ix += 1

        if sl.stop is None:
            results.append( slice( indices[ ix ], None ) )

        return results


    def __iter__( self ):

        if 1 > len( self._indices ):
            return

        nxt = self._indices[ 0 ]
        yield slice( 0, nxt )

        for ix in self._indices[ 1 : ]:
            yield slice( nxt, ix )
            nxt = ix

        yield( slice( nxt, None ) )


class TextStrata:

    def __init__( self, text, *args, **kwargs ):

        self._data = CharArray( text )
        self._layers = []


    def __len__( self ):

        if 0 < self.depth:
            return len( self.top_layer )
        
        return len( self._data )


    def __getitem__( self, sl ):

        if 1 > self.depth:
            return self._data[ sl ]

        depth = self.depth - 1
        _slice = self._layers[ depth ][ sl ]
        layers = []
        while 0 < depth:
            depth -= 1

        try:
            slices = iter( _slice )
        except TypeError:
            return self._data[ _slice ]

        return [ self._data[ s ] for s in slices ]


    @property
    def depth( self ):
        return len( self._layers )

    @property
    def top_layer( self ):

        if 0 < self.depth:
            return self._layers[ self.depth - 1 ]

        return [ slice( len( self._data ) ) ]


    def tokens( self ):

        if 1 > self.depth:
            return list( self._data )

        return [ self._data[ sl ] for sl in self.top_layer ]


    def split_where( self, p ):

        layer = []
        prev_condition = p( self[ 0 ] )

        for ix in range( 0, len( self ) ):

            this_condition = p( self[ ix ] )
            is_boundary = prev_condition != this_condition

            if is_boundary:
                layer.append( ix )

            prev_condition = this_condition

        self._layers.append( TokenSequence( layer ) )
