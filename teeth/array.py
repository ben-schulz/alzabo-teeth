import contextlib
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


class SliceArray:

    def __init__( self, data ):
        self._data = numpy.array( data )
        self.start = self._data[ 0 ]
        self.stop = self._data[ -1 ]


    def __len__( self ):
        return len( self._data ) - 1


    def __iter__( self ):
        for ix in range( 0, self.__len__() ):
            start = self._data[ ix ]
            stop = self._data[ ix + 1 ]
            yield slice( start, stop )


    def __getitem__( self, k ):

        def __getitem__int( k ):

            if k > self.__len__():
                raise IndexError

            return slice( self._data[ k ], self._data[ k + 1 ] )


        def __getitem__slice( start, stop ):

            try:
                _stop = stop + 1
            except TypeError:
                _stop = None

            return SliceArray( self._data[ start : _stop ] )

        try:
            k = int( k )
            return __getitem__int( k )

        except TypeError:
            return __getitem__slice( k.start, k.stop )


    def shift( self, phase ):
        return SliceArray( [ ix + phase for ix in self._data ] )


class Strata:

    def __init__( self, layers=None ):

        self._layers = list()

        if layers is not None:
            for l in layers:
                self.add_layer( l )


    @property
    def depth( self ):
        return len( self._layers )


    def __len__( self ):
        return len( self.top )


    @property
    def top( self ):

        if 0 < self.depth:
            return self._layers[ self.depth - 1 ]

        return Strata()


    def __getitem__( self, sl ):

        try:
            int( sl )
            start = sl
            stop = sl + 1

        except TypeError:
            start = sl.start
            stop = sl.stop

        if 0 == self.depth:
            raise IndexError

        original_layers = []

        for l in self._layers[ : : -1 ]:

            this_sl = l[ start : stop ]
            original_layers.insert( 0, this_sl )

            start = this_sl.start
            stop = this_sl.stop

        relative_layers = []
        for ix, l in enumerate( original_layers[ : 0 : -1 ] ):

            prev_layer = original_layers[ self.depth - ix - 1 ]
            this_layer = l.shift( - prev_layer.start )
            relative_layers.insert( 0, this_layer )

        relative_layers.insert( 0, original_layers[ 0 ] )

        return Strata( layers=relative_layers )


    def add_layer( self, indices ):

        if isinstance( indices, SliceArray ):
            self._layers.append( indices )

        else:
            self._layers.append( SliceArray( indices ) )

    def pop_layer( self ):

        return self._layers.pop()


    def items( self ):
        return [ list( l ) for l in self._layers ]


    def sieve( self, data ):

        result = data
        for l in self._layers:
            nxt = [ result[ sl ] for sl in l ]
            result = nxt

        return result


class TextStrata:

    def __init__( self, text, *args, **kwargs ):

        self._data = CharArray( text )
        self._layers = Strata()
        self._depth = self._layers.depth


    def __len__( self ):

        if 0 < self.depth:
            return len( self._layers.top )
        
        return len( self._data )


    def __getitem__( self, sl ):

        if 1 > self.depth:
            return self._data[ sl ]

        value = self._layers[ sl ].sieve( self._data )

        if 1 == len( value ):
            return value[ 0 ]

        return value


    @property
    def depth( self ):
        return self._depth

    @property
    def top_layer( self ):

        if 0 < self.depth:
            return self._layers[ self.depth - 1 ]

        return [ slice( len( self._data ) ) ]


    def items( self ):

        if 1 > self.depth:
            return list( self._data )

        return [ l.sieve( self._data )
                 for l in self._layers ]


    def split_where( self, p ):

        if 0 == self.depth:

            layer = [ 0 ]
            prev_condition = p( self._data[ 0 ] )

            item_count = len( self._data )

            for ix in range( 0, item_count ):
                this_condition = p( self._data[ ix ] )
                is_boundary = prev_condition != this_condition

                if is_boundary:
                    layer.append( ix )

                prev_condition = this_condition

            layer.append( item_count )
            self._layers.add_layer( SliceArray( layer ) )
            self._depth += 1

            return

        layer = [ 0 ]
        first_item = self._layers[ 0 ].sieve( self._data )
        prev_condition = p( first_item )
        item_count = len( self._layers.top )

        for ix in range( 0, item_count ):

            item = self._layers[ ix ].sieve( self._data )
            this_condition = p( item )
            is_boundary = prev_condition != this_condition

            if is_boundary:
                layer.append( ix )

            prev_condition = this_condition

        layer.append( item_count )

        self._layers.add_layer( SliceArray( layer ) )
        self._depth += 1

@contextlib.contextmanager
def layer( depth, strata ):

    prev_depth = strata.depth

    depth_diff = prev_depth - depth

    if 0 > depth_diff:
        raise IndexError

    excluded_layers = []
    for _ in range( 0, depth_diff ):
        excluded_layers.insert( 0, strata._layers.pop_layer() )

    strata._depth = depth

    yield strata

    while strata._depth > depth:
        strata._layers.pop_layer()
        strata._depth -= 1

    strata._depth = prev_depth
    for l in excluded_layers:
        strata._layers.add_layer( l )
