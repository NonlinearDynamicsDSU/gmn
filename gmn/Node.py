
# Python distribution modules
from copy    import copy
from pathlib import Path

# Community modules
from pyEDM import Simplex, SMap, Embed

try:
    from math                 import dist
    from sklearn              import neighbors
    from sklearn.svm          import SVR
    from sklearn.linear_model import LinearRegression
except ImportError as err:
    print( err, "Node: SVR, knn, Linear not available", flush = True )

try:
    from os import environ
    environ[ 'OMP_PROC_BIND' ] = 'false' # Kokkos warning OpenMP
    from kedm import simplex as kedm_simplex
    from kedm import smap    as kedm_smap
except ImportError as err:
    print( err, "Node: kedm not loaded", flush = True )

# Local modules 
from gmn.ConfigParser import ReadConfig
from gmn.Common       import *
from gmn.Auxiliary    import ReadDataFrame

#-----------------------------------------------------------
#-----------------------------------------------------------
class Node:
    '''
    A node in the network. Each node has its own data and Parameters.  

    By default, the node is initialized with a copy() of Network.Parameters
    and Network.data.

    If a Parameter node.cfg file is found: read Parameters and data from it.

    Network output at the end of each timestep is appended to the node data. 
    Thus all nodes share generated data, but can be initialized with 
    individual data and parameters.

    Note the data "library" is limited to Parameters.predictionStart. It 
    does not grow as generated values are added to node data.

    Generate() method performs prediction. Called from GMN Generate() in the
    Network Node loop to dispatch the specified FunctionType and return a 
    single prediction value collected across all nodes in GMN.lastDataOut.
    '''

    # import Generate, Forecast as a Node class method
    from gmn.Generate import Generate
    from gmn.Forecast import Forecast

    #----------------------------------------------------------------------
    def __init__( self, args, Network, nodeName ):
        '''Constructor'''
        self.name         = nodeName
        self.args         = args
        self.Network      = Network
        self.Parameters   = None  # from Network, or node.cfg file, if any
        self.Function     = None  # Reference to Simplex, SMap...
        self.FunctionType = None  # Enumeration
        self.data         = None  # input data (copy or read) + generated
        self.libEnd_i     = None  # EDM library end: Constant @ predictionStart

        if args.DEBUG :
            print( '-> Node.__init__() : ', nodeName, flush = True )

        # Set nodeParameters = True if node config file found
        nodeParameters = False

        if self.Network.Parameters.nodeConfigPath :
            # Use pathlib.Path() class object for OS independence 
            nodePath = Path( self.Network.Parameters.nodeConfigPath )
            nodeFile = Path( self.Network.Parameters.nodeConfigPath + \
                             nodeName + '.cfg' )

            queryGen = nodePath.glob( '*.cfg' ) # Path.glob returns generator
            query    = [ str( x ) for x in queryGen ]

            if str( nodeFile ) in query :
                nodeParameters = True

                if args.DEBUG :
                    print( str( nodeFile ) + " Found in ", query, flush = True )

        if nodeParameters :
            # Found node.cfg : Get config Parameters & data if specified
            self.Parameters = ReadConfig( args, nodeFile )

            if self.Parameters.nodeData :
                # Load node data as Pandas DataFrame
                # JP: All data needed?
                data = ReadDataFrame( self.Parameters.nodeData,
                                      verbose = args.verbose )

                # Subset to "data library"
                # Network: dataLib_i = range( predictionStart )
                self.data = data.iloc[ self.Network.dataLib_i ]

                if args.DEBUG :
                    print( "Node.__init__() Loaded", self.Parameters.nodeData,
                           " shape :", str( self.data.shape ) )
                    print( self.data.tail(2), flush = True )
            else:
                # No Node data specified. Make copy of network data
                self.data = Network.data.iloc[ self.Network.dataLib_i ].copy()

        else :  # default to Network config & data
            self.Parameters = copy( self.Network.Parameters )

            # Copy node data: subset to dataLib_i : DataFrame.copy(deep=True) 
            # Network: dataLib_i = range( parameters.predictionStart )
            #   iloc[] returns a view (slice) of the object
            #   www.practicaldatascience.org/html/views_and_copies_in_pandas.html
            self.data = Network.data.iloc[ self.Network.dataLib_i ].copy()

        # Assign columns and target : target is the node name
        if len(self.Parameters.target) == 0 or self.Parameters.target.isspace():
             self.Parameters.target = self.name

        # columns are inputs to the node + target
        # target required if node has no input, predict the var itself
        if len(self.Parameters.columns)==0 or self.Parameters.columns.isspace():
            # predecessors(n) returns an iterator over predecessor nodes of n.
            self.Parameters.columns = \
                [ n for n in self.Network.Graph.predecessors( self.name ) ]
            self.Parameters.columns.append( self.name )

        # Assign node FunctionType and Function
        nodeFunction = self.Parameters.function.lower()

        if "simplex" == nodeFunction :
            self.FunctionType = FunctionType.Simplex
            self.Function     = Simplex

            # EDM lib index based on input data (subset to predictionStart)
            self.libEnd_i = self.data.shape[0]

        elif "smap" == nodeFunction :
            self.FunctionType = FunctionType.SMap
            self.Function     = SMap

            # EDM lib index with offset from embedding time shift
            # since SMap multivariate requires embedded = True
            offset = ( self.Parameters.E ) * abs( self.Parameters.tau )
            self.libEnd_i = self.data.shape[0] - offset

        elif "kedmsimplex" == nodeFunction or "kedm_simplex" == nodeFunction:
            self.FunctionType = FunctionType.kedmSimplex
            self.Function     = kedm_simplex

            # EDM lib index based on input data (subset to predictionStart)
            self.libEnd_i = self.data.shape[0]

        elif "kedmsmap" == nodeFunction or "kedm_smap" == nodeFunction:
            self.FunctionType = FunctionType.kedmSMap
            self.Function     = kedm_smap

            # EDM lib index based on input data (subset to predictionStart)
            self.libEnd_i = self.data.shape[0]

        elif "linear" == nodeFunction :
            self.FunctionType = FunctionType.Linear
            self.Function     = LinearRegression

        elif "svr" == nodeFunction :
            self.FunctionType = FunctionType.SVR
            self.Function     = SVR

        elif "knn" == nodeFunction :
            self.FunctionType = FunctionType.knn
            self.Function     = neighbors.KNeighborsRegressor

        else :
            raise RuntimeError( "Node(): " + nodeName +\
                                " Invalid node function: " + nodeFunction )

        if args.DEBUG :
            print( 'columns:', self.Parameters.columns )
            print( 'target:',  self.Parameters.target  )
            print( str( self.FunctionType ), str( self.Function ) ) 
            print( '<- Node.__init__() : ', nodeName, flush = True )
