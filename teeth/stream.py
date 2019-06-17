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

    def __init__( self, pattern, data, keep_separators=False ):

        self.pattern = pattern
        self._regex = re.compile( self.pattern )
        self.data = data
        self.length = len( self.data )
        self.position = -1

        self.keep_separators = keep_separators


    def __iter__( self ):

        match = self._regex.finditer( self.data )

        try:
            token = next( match )
            span = Span( *( token.span() ) )

            if self.keep_separators:
                yield Span( 0, span.start )

            while True:

                self.position = span.stop
                yield span

                token = next( match )
                span = Span( *( token.span() ) )

                if self.keep_separators:
                    yield Span( self.position, span.start )

        except StopIteration:

            if self.position < self.length - 1 and self.keep_separators:
                yield Span( self.position, self.length )

class Flux:

    def __init__( self, data, outer_pattern,
                  inner_pattern=None,
                  keep_separators=False
    ):

        if not isinstance( outer_pattern, str ):
            raise TypeError( '\'Flux\' expects type \'str\' in '
                             'second argument.' )

        if ( inner_pattern is not None
             and not isinstance( inner_pattern, str ) ):

             raise TypeError( '\'Flux\' expects type \'str\' in '
                              'kwarg \'inner_pattern\'.' )

        self.splits = tuple( x for x in ( outer_pattern, inner_pattern )
                        if x is not None )

        self.data = data
        self.keep_separators = keep_separators

        self._cursors = None
        self._rewind()


    def _rewind( self ):
        self._cursors = [ RegexCursor( s, self.data )
                          for s in self.splits ]


    def outerpos( self ):
        return self._cursors[ 0 ].position

    def innerpos( self ):

        if 1 < len( self.splits ):
            return self._cursors[ 1 ].position

        return None


    def __iter__( self ):


        def _iterate_inner( outer_token ):

            subtokens = []
            try:
                while self.innerpos() < outer_token.stop:
                    subtokens.append( next( inner ) )

            except StopIteration:
                pass

            if subtokens:
                outer_token.stratify( subtokens )

            return ( outer_token.apply( self.data ),
                     outer_token )


        cursors = [ iter( c ) for c in self._cursors ]
        outer = cursors[ 0 ]

        try:
            if 2 > len( cursors ):

                while True:
                    outer_token = next( outer )
                    token = ( outer_token.apply( self.data ),
                            outer_token )

                    yield token

            else:

                inner = cursors[ 1 ]
                while True:
                    outer_token = next( outer )
                    token = _iterate_inner( outer_token )
                    yield token

        except StopIteration:
            return
