import re

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

class PredCursor:

    def __init__( self, predicate, data ):
        self.predicate = predicate
        self.data = data
        self._len = len( data )

        self.index = 0
        self.token = None


    def __iter__( self ):

        for ix in range( 0, self._len ):

            token = self.data[ ix ]
            if self.predicate( token ):
                self.index = ix
                self.token = self.data[ ix ]
                yield ( ix, token )

class RegexCursor:

    def __init__( self, pattern, data ):

        self.pattern = pattern
        self._regex = re.compile( self.pattern )
        self.data = data

    def __iter__( self ):

        match = self._regex.finditer( self.data )

        try:
            while True:
                token = next( match )
                yield Span( *( token.span() ) )

        except StopIteration:
            pass

class Flux:

    def __init__( self, data, splits=None ):

        self.splits = splits or []
        self.data = data

        self._cursors = None
        self._rewind()


    def _rewind( self ):
        self._cursors = [ iter( RegexCursor( s, self.data ) )
                                for s in self.splits ]


    def __iter__( self ):

        outer = self._cursors[ 0 ]

        try:
            separator = next( outer )

        except StopIteration:
            return

        if 0 < separator.start:
            start_index = 0

        else:
            start_index = separator.stop

        try:
            while True:

                separator = next( outer )

                span = Span( start_index, separator.start )
                yield span

                start_index = separator.stop

        except StopIteration:
            return



    def __nope__( self ):

        if self._cursors is None or 0 == len( self._cursors ):
            return

        cursors = [ iter( c ) for c in self._cursors ]
        outer = cursors[ -1 ]

        prev_limit = -1
        while True:

            try:
                limit, _ = next( outer )
            except StopIteration:
                break

            if limit == prev_limit + 1:
                prev_limit = limit
                continue

            span = Span( prev_limit + 1, limit )

            layers = []
            sublayers = cursors[ 0 : len( self.splits ) - 1 ]
            for ( ix, c ) in enumerate( sublayers ):

                layer = []

                pos = self._cursors[ ix ].index
                while pos < limit:
                    layer.append( pos )
                    pos, _ = next( c )

                layer.append( limit )

                subspans = [
                    Span( start + 1, end ) for ( start, end )
                    in zip( layer[ 1 : -1 ], layer[ 2 : ] )
                    if start + 1 < end
                ]

                if prev_limit < layer[ 0 ]:
                    first_token = Span( layer[ 0 ], layer[ 1 ] )
                    subspans.insert( 0, first_token )

                if layer[ -1 ] < limit:
                    subspans.append( Span( layer[ -1 ], limit ) )

                layers.append( subspans )

            if 0 < len( layers ):
                span.stratify( *( layers[ 0 ] ) )

            yield ( span.apply( self.data ), span )

            prev_limit = limit
