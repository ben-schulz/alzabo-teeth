class Span:

    def __init__( self, start, end ):

        try:
            self.start = int( start )
            self.stop = int( end )
            self.subspans = None

        except:
            msg = '\'Span\' requires integer start and end values.'
            raise ValueError( msg )

    def __getitem__( self, index ):

        if 0 == index:
            return self.start

        if 1 == index:
            return self.stop

        raise IndexError


    def __iter__( self ):
        yield self[ 0 ]
        yield self[ 1 ]


    def split( self, index ):

        return ( Span( self.start, index ),
                 Span( index, self.stop ) )


    def excise( self, *interval ):

        stop = interval[ 0 ]
        resume = interval[ 1 ]

        return ( Span( self.start, stop ),
                 Span( resume - 1, self.stop ) )


    def stratify( self, *subspans, relative=False ):

        if not relative:
            self.subspans = [
                Span( s.start - self.start, s.stop - self.start )
                for s in subspans ]

            return

        self.subspans = subspans


    def apply( self, seq ):

        _this = seq[ self.start : self.stop ]

        if self.subspans is None:
            return _this

        result = []
        for subspan in self.subspans:
            result.append( subspan.apply( _this ) )

        return result

class Flux:

    def __init__( self, splits=None ):

        self.splits = splits or []

    def apply( self, data ):

        tokens = data
        for split in self.splits:
            prev = 0
            new = []
            for ( index, x ) in enumerate( tokens ):
                if split( x ):
                    new.append( Span( prev, index ) )
                    prev = index

            tokens = new

        return tokens


class __Flux:

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

    def asbytestring( self, sl ):

        def _asbytes( s ):
            return ( ':'.join( '{:02x}'.format( ord( c ) )
                               for c in s ) )

        if isinstance( self.data, str ):
            return _asbytes( self.data[ sl ] )
        else:
            return [ [ _asbytes( c ) for c in x ]
                     for x in self.data[ sl ] ]


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
