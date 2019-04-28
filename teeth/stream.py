class Flux:

    def __init__( self, data, *args, **kwargs ):

        self.data = data
        self.steps = []

    def __iter__( self ):

        _iter = iter( self.data )

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
