import numpy

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
            return len( self.top_layer ) - 1
        
        return len( self._data )


    def __getitem__( self, sl ):

        return self._data[ sl ]


    @property
    def depth( self ):
        return len( self._layers )

    @property
    def top_layer( self ):
        return self._layers[ self.depth - 1 ]


    def tokens( self ):

        if 1 > self.depth:
            return list( self._data )

        return [ self._data[ sl ] for sl in self.top_layer ]


    def split_where( self, p ):

        layer = []
        prev_condition = p( self._data[ 0 ] )

        for ix in range( 0, len( self._data ) ):

            this_condition = p( self._data[ ix ] )
            is_boundary = prev_condition != this_condition

            if is_boundary:
                layer.append( ix )

            prev_condition = this_condition

        self._layers.append( TokenSequence( layer ) )
