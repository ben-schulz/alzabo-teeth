class Flux:

    def __init__( self, data, *args, **kwargs ):

        self.data = data
        self.steps = []


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

        def flow():

            while True:
                try:
                    _next = next( _iter )
                except StopIteration:
                    break

                for f in self.steps:
                    _next = f( _next )

                yield _next

            return

        return flow()

    def wind( self, f ):
        self.steps.append( f )

    def unwind( self ):
        self.steps.pop()
