class OneHot:

    def __init__( self, vocab, **kwargs ):

        self.vocab = vocab
        self.dim = 1 + len( vocab )
        self._encoding = { v : n
                           for n, v in enumerate( vocab, start=1 ) }

        self._decoding = { n : v
                           for n, v in enumerate( vocab, start=1 ) }


    def encode( self, vector ):

        result = []

        for v in vector:
            encoded = [ 0 for _ in range( self.dim ) ]
            position = self._encoding.get( v, 0 )
            encoded[ position ] = 1
            result.append( encoded )

        return result

    def decode( self, vector ):

        result = []
        for v in vector:
            position = v.index( max( v ) )
            result.append( self._decoding.get( position, '' ) )

        return result
