class Flux:

    def __init__( self, data, *args, **kwargs ):

        self.data = data
        self.steps = []


    def __len__( self ):
        return len( self.data )

    def __getitem__( self, s ):

        d = self.data[ s ]
        s = list( self._makeiter( d ) )

        if isinstance( d, str ):
            return str.join( '',  s)
        else:
            return s


    def __iter__( self ):
        return self._makeiter( self.data )


    def _makeiter( self, data ):

        _iter = iter( data )

        while True:
            try:
                _next = next( _iter )
            except StopIteration:
                break

            for f in self.steps:
                _next = f( _next )

            yield _next

        return

    def items( self ):
        return [ x for x in iter( self ) ]

    def compare( self, sl ):
        return( self.data[ sl ], self[ sl ] )

    def wind( self, f ):
        self.steps.append( f )

    def unwind( self ):
        self.steps.pop()

    def split( self, p ):

        result = []
        token = []

        for x in iter( self ):

            if not p( x ):
                token.append( x )
                continue

            if 0 < len( token ):
                result.append( token )
                token = []

            result.append( [ x ] )


        if 0 < len( token ):
            result.append( token )

        def join( x ):
            return str.join( '', x )

        if isinstance( self.data, str ):
            return Flux( list( map( join, result ) ) )

        return Flux( result )
