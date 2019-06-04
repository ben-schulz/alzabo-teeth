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

        start = 0

        p = self.splits[ 0 ]

        layers = []
        for p in self.splits:

            prev = p( data[ 0 ] )
            spans = []
            for ( end, item ) in enumerate( data ):

                nxt = p( item )
                if prev and not nxt:
                    start = end

                if nxt and not prev:
                    spans.append( Span( start, end ) )
                    start = end

                prev = nxt

            layers.append( spans )

        result = []
        for l in layers:
            for s in self.splits:
                nxt = []
                for span in spans:
                    nxt.append( span.apply( data ) )

                result.append( nxt )

        return result
