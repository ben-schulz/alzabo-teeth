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


    def stratify( self, subspans, relative=False ):

        if not hasattr( subspans, '__iter__' ):
            raise TypeError( 'first argument to \'self.stratify\''
                             ' must be iterable.' )

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


class RegexCursor:

    def __init__( self, pattern, data ):

        self.pattern = pattern
        self._regex = re.compile( self.pattern )
        self.data = data
        self.position = -1

    def __iter__( self ):

        match = self._regex.finditer( self.data )

        try:
            while True:
                token = next( match )
                span = Span( *( token.span() ) )
                self.position = span.stop
                yield span

        except StopIteration:
            pass

class Flux:

    def __init__( self, data, splits=None ):

        self.splits = splits or []
        self.data = data

        self._cursors = None
        self._rewind()


    def _rewind( self ):
        self._cursors = [ RegexCursor( s, self.data )
                          for s in self.splits ]


    def __iter__( self ):

        cursors = [ iter( c ) for c in self._cursors ]
        outer = cursors[ 0 ]

        try:
            while True:
                outer_token = next( outer )

                strata = []
                for ( layer, c ) in enumerate( cursors[ 1 : ] ):

                    subtokens = []

                    cursor = self._cursors[ layer + 1 ]
                    try:
                        while cursor.position < outer_token.stop:
                            subtokens.append( next( c ) )

                    except StopIteration:
                        pass

                    strata.append( subtokens )

                if 0 < len( strata ):
                    outer_token.stratify( strata[ 0 ] )

                yield ( outer_token.apply( self.data ), outer_token )

        except StopIteration:
            return
