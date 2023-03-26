
# Python distribution modules

# Community modules
from pandas import concat

# Local modules
from gmn.Common import *

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def Generate( self, lastDataOut ):
    '''Node method
       Called from GMN Generate() in the Network Node loop'''

    if self.args.DEBUG_ALL :
        print( '-----> Node:Generate() : ', self.FunctionType.name, self.name )
        print( self.data.tail( 2 ) );
        print( 'lastDataOut:' ); print( lastDataOut )

    # Append new data to end of node data : except on time step 0
    # Do not insert via .loc[] : stackoverflow.com/questions/57000903/
    if not ( lastDataOut is None ):
        self.data = concat( [ self.data, lastDataOut ] )

    # Local References for convenience and readability
    Parameters = self.Parameters
    data       = self.data

    if self.args.DEBUG_ALL :
        print( '  Appended data : shape: ', data.shape );
        print( data.tail( 3 ) ); print()

    #--------------------------------------------------------------------
    if self.FunctionType.value == FunctionType.Simplex.value :

        # If lib or pred are set in Parameters, use them
        # otherwise lib = [1, libEnd_i], pred = [N-1, N] N = data.shape[0]
        if len( Parameters.lib ) and not Parameters.lib.isspace():
            lib = Parameters.lib
        else:
            lib = "1 %d" % self.libEnd_i # Constant... for now

        if len( Parameters.pred ) and not Parameters.pred.isspace():
            pred = Parameters.pred
        else:
            pred = "%d %d" % ( data.shape[0] - 1, data.shape[0] )

        S = self.Function( dataFrame       = data,
                           lib             = lib,
                           pred            = pred,
                           E               = Parameters.E,
                           Tp              = Parameters.Tp,
                           knn             = Parameters.knn,
                           tau             = Parameters.tau,
                           exclusionRadius = Parameters.exclusionRadius,
                           columns         = Parameters.columns,
                           target          = Parameters.target,
                           embedded        = Parameters.embedded,
                           validLib        = Parameters.validLib,
                           generateSteps   = Parameters.generateSteps )

        val = S['Predictions'].iloc[-1]

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.SMap.value :

        # JP TODO: Add sklearn solver import/functions...
        # Convert Parameters.solver to None if empty
        # if len( Parameters.solver ) == 0 or Parameters.solver.isspace():
        #     self.Parameters.solver = None

        # SMap multivariate requires embedded = True
        # Embed data to E, tau
        df = Embed( dataFrame = data, E = Parameters.E,
                    tau = Parameters.tau, columns = Parameters.columns )

        # Remove leading NaN from the time shift
        df = df.dropna()

        # Insert time column for SMap dataFrame
        df.insert( 0, data.columns[0], data.iloc[:,0] )

        # If lib or pred are set in Parameters, use them
        # otherwise lib = [1, libEnd_i], pred = [N-1, N] N = df.shape[0]
        if len( Parameters.lib ) and not Parameters.lib.isspace():
            lib = Parameters.lib
        else :
            lib  = "1 %d" % self.libEnd_i # Constant... for now

        if len( Parameters.pred ) and not Parameters.pred.isspace():
            pred = Parameters.pred
        else:
            pred = "%d %d" % ( df.shape[0] - 1, df.shape[0] )

        # Note: dataFrame = df, columns, target from embedding
        S = self.Function( dataFrame       = df,
                           lib             = lib,
                           pred            = pred,
                           E               = Parameters.E,
                           Tp              = Parameters.Tp,
                           knn             = Parameters.knn,
                           tau             = Parameters.tau,
                           theta           = Parameters.theta,
                           exclusionRadius = Parameters.exclusionRadius,
                           columns         = df.columns[1:-1],
                           target          = Parameters.target + '(t-0)',
                           solver          = None, # Parameters.solver,
                           embedded        = Parameters.embedded,
                           validLib        = Parameters.validLib,
                           generateSteps   = Parameters.generateSteps )

        val = S['predictions']['Predictions'].iloc[-1]

        # SMap can diverge if E, tau are not appropriate
        if abs( val ) > 1E15 :
            raise RuntimeError( "Generate:SMap() Node: " + self.name +\
                                "   Divergence detected (>1E15)" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.kedmSimplex.value :

        # Get library and target for kedm simplex as ndarray
        data_ = data[ Parameters.columns ] # DataFrame; includes target

        library = data_.iloc[ : self.libEnd_i, : ].values

        # JP kedm seems to core if not enough target data...
        targetLen = Parameters.E * abs( Parameters.tau )
        # JP kedm simplex MV target must be same number of columns as library
        #    and in the same order as columns
        target = data_.iloc[ -targetLen : ].values

        S = self.Function( library = library,
                           target  = target,
                           E       = Parameters.E,
                           tau     = abs( Parameters.tau ),
                           Tp      = Parameters.Tp )

        # JP target was the last column in data_, use S last column 
        val = S[ -1, S.shape[1] - 1 ] # numpy.ndarray

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.kedmSMap.value :

        # JP: kedm smap is univariate, ndarray
        data_ = data[ self.name ] # Series

        # Get library and target
        library = data_.iloc[ : self.libEnd_i ].values

        # JP kedm seems to core if not enough target data...
        targetLen = Parameters.E * abs( Parameters.tau )
        target    = data_.iloc[ -targetLen : ].values

        S = self.Function( library = library,
                           target  = target,
                           E       = Parameters.E,
                           tau     = abs( Parameters.tau ),
                           Tp      = Parameters.Tp,
                           theta   = Parameters.theta )

        val = S[-1] # numpy.ndarray

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.Linear.value :

        X = data[ Parameters.columns ]
        #if len( Parameters.columns ) > 1 :
        #    X  = X.drop( self.name, axis = 'columns' )
        X = X.values
        y = data[ Parameters.target ].values.copy()

        lr = self.Function()
        lr.fit( X, y )

        nextX = self.FindNextX( X )
        pred  = lr.predict( nextX )
        val   = pred[ 0 ]

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.SVR.value :

        X = data[ Parameters.columns ]
        #if len( Parameters.columns ) > 1 :
        #    X  = X.drop( self.name, axis = 'columns' )
        X = X.values
        y = data[ Parameters.target ].values.copy()

        svr = self.Function( kernel = 'rbf', gamma = 'scale', tol = 0.001,
                             epsilon = 0.1, shrinking = True, cache_size = 200,
                             verbose = False, max_iter = -1 )
        svr.fit( X, y )

        nextX = self.FindNextX( X )
        pred  = svr.predict( nextX )
        val   = pred[ 0 ]

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.knn.value :

        X = data[ Parameters.columns ]

        if len( Parameters.columns ) > 1 :
            # Remove self from X
            X  = X.drop( self.name, axis = 'columns' )

        X = X.values
        y = data[ Parameters.target ].values.copy()

        # JP: n_neighbors should be a Parameter
        knn = self.Function( n_neighbors = 10, weights = 'distance' )
        knn.fit( X, y )

        nextX = self.FindNextX( X )
        pred  = knn.predict( nextX )
        val   = pred[ 0 ]

    if self.args.DEBUG_ALL :
        print( self.name, "val:", val )
        print( '<----- Node:Generate() : ',self.FunctionType.name,self.name )
        print()

    return val

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def FindNextX( self, X ):
    '''Find closest X not equal to X[-1,:], Tp step ahead '''

    x    = X[-1,:]
    Dmin = 1E15
    imin = None

    # Limit X to the data "library" as in EDM
    for i in range( self.Parameters.predictionStart ) :
        xi = X[i,:]
        D  = dist( x, xi )
        if D < Dmin :
            Dmin = D
            imin = i

    # Tp steps ahead
    #if imin + self.Parameters.Tp < X.shape[ 0 ] :
    #    imin = imin + self.Parameters.Tp

    return( X[imin + 1,:].reshape(1,-1) )
