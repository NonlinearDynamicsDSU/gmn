
# Python distribution modules
from glob import glob
from enum import Enum
from copy import copy

# Community modules
from pandas import read_csv, concat
from pyEDM  import Simplex, SMap, Embed

try:
    from math                 import dist
    from sklearn              import neighbors
    from sklearn.svm          import SVR
    from sklearn.linear_model import LinearRegression
except ImportError as err:
    print( err, "SVR, knn, Linear not available" )

# Local modules 
from gmn.ConfigParser import ReadConfig

#-----------------------------------------------------------
#-----------------------------------------------------------
class FunctionType( Enum ):
    '''Enumeration for Function types'''
    Simplex = 1
    SMap    = 2
    Linear  = 3
    SVR     = 4
    knn     = 5

#-----------------------------------------------------------
#-----------------------------------------------------------
class Node:
    '''
    A node in the network.

    If a Parameter node.cfg file is found: read Parameters and data from it.
    If not found, use copy() of Network Parameters and data.

    A copy of the Network.data is made : each node has its' own data and
    will append output from all nodes (set into GMN.lastDataOut) after
    each iteration through the network (end of each prediction timestep).

    Note the data "library" is limited to Parameters.predictionStart. It 
    does not grow as generated values are added to node data.

    Generate() method performs prediction. Called from GMN Generate() in the
    Network Node loop. Dispatch the specified FunctionType. Return a single
    prediction value.'''

    #----------------------------------------------------------------------
    def __init__( self, args, Network, nodeName ):
        '''Constructor'''
        self.name         = nodeName
        self.args         = args
        self.Network      = Network
        self.Parameters   = None  # from Network, or node.cfg file, if any
        self.Function     = None  # Reference to Simplex, SMap...
        self.FunctionType = None  # Enumeration
        self.data         = None  # self copy of input data + generated
        self.libEnd_i     = None  # EDM library end: Constant @ predictionStart

        if args.DEBUG_ALL :
            print( '-> Node.__init__() : ', nodeName )

        # Look in NetworkParameters networkPath for node config files
        # If not found, use existing Network args.configFile parameters
        nodeFile  = self.Network.Parameters.networkPath + nodeName + '.cfg'
        nodeQuery = self.Network.Parameters.networkPath + '*.cfg'

        nodeParameters = False
        if nodeFile in glob( nodeQuery ) :
            nodeParameters  = True
            self.Parameters = ReadConfig( args, nodeFile )

            if args.DEBUG_ALL :
                print( nodeFile + " Found in ", nodeQuery )
        else :
            self.Parameters = copy( self.Network.Parameters )

        # Copy node data: subset to dataLib_i : DataFrame.copy(deep=True) 
        # Network: dataLib_i = range( parameters.predictionStart )
        #   iloc[] returns a view (slice) of the object
        #   www.practicaldatascience.org/html/views_and_copies_in_pandas.html
        self.data = Network.data.iloc[ self.Network.dataLib_i ].copy()

        # If nodeParameters was read, get data if specified
        if nodeParameters :
            #-----------------------------------------------------------
            # JP TODO:
            # With all nodes sharing global data : lastDataOut is the same
            # for all nodes, appending new data from the previous prediction
            # is clear. If different data is used, each node must indpendently
            # save/append it's output for the next iteration.
            # Not clear how to do that.
            #-----------------------------------------------------------

            # Load node data as Pandas DataFrame if self.Parameters.data
            if self.Parameters.data and not self.Parameters.data.isspace() :
                data = read_csv( self.Parameters.data ) # JP: All data needed?

                # Subset to "data library"
                # Network: dataLib_i = range( predictionStart )
                self.data = data.iloc[ self.Network.dataLib_i ]

                if args.DEBUG_ALL :
                    print( "Node.__init__() Loaded", self.Parameters.data,
                           " shape :", str( self.data.shape ) )
                    print( self.data.tail(2) )

        # Assign columns and target : target is the node name
        if len(self.Parameters.target) == 0 or self.Parameters.target.isspace():
             self.Parameters.target = self.name

        # columns are inputs to the node + target
        if len(self.Parameters.columns)==0 or self.Parameters.columns.isspace():
            # predecessors(n) returns an iterator over predecessor nodes of n.
            self.Parameters.columns = \
                [ n for n in self.Network.Graph.predecessors( self.name ) ]
            self.Parameters.columns.append( self.name )

        # Assign node FunctionType and Function
        nodeFunction = self.Parameters.function.lower()

        if "simplex" in nodeFunction :
            self.FunctionType = FunctionType.Simplex
            self.Function     = Simplex

            # EDM lib index based on input data (subset to predictionStart)
            self.libEnd_i = self.data.shape[0]

        elif "smap" in nodeFunction :
            self.FunctionType = FunctionType.SMap
            self.Function     = SMap

            # EDM lib index with offset from embedding time shift
            offset = ( self.Parameters.E ) * abs( self.Parameters.tau )
            self.libEnd_i = self.data.shape[0] - offset

        elif "linear" in nodeFunction :
            self.FunctionType = FunctionType.Linear
            self.Function     = None

        elif "svr" in nodeFunction :
            self.FunctionType = FunctionType.SVR
            self.Function     = None

        elif "knn" in nodeFunction :
            self.FunctionType = FunctionType.knn
            self.Function     = None

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    def Generate( self, lastDataOut ):
        '''Called from GMN Generate() in the Network Node loop'''

        if self.args.DEBUG_ALL :
            print( '-----> Node:Generate() : ',self.FunctionType.name, self.name)
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
        elif self.FunctionType.value == FunctionType.Linear.value :

            X = data[ Parameters.columns ]
            #if len( Parameters.columns ) > 1 :
            #    X  = X.drop( self.name, axis = 'columns' )
            X = X.values
            y = data[ Parameters.target ].values.copy()

            lr = LinearRegression()
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

            svr = SVR( kernel = 'rbf', gamma = 'scale', tol = 0.001,
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
            knn = neighbors.KNeighborsRegressor( n_neighbors = 10,
                                                 weights = 'distance' )
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
