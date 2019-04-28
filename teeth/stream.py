class Flux:

    def __init__( self, data, *args, **kwargs ):

        self.data = data
        self.steps = []

    def __iter__( self ):
        return iter( self.data )
