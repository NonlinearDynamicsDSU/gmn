
# Python distribution modules
import pickle

# Community modules
from networkx import topological_sort
from pandas   import DataFrame, read_csv

# Local modules 
from gmn.Node import Node

#---------------------------------------------------------------
#---------------------------------------------------------------
class Network:
    '''
    Network object instantiated from GMN.__init__. Stored in GMN.Network.

    Reads networkx DiGraph file from CreateNetwork.py

    Loads Network data if Parameters.networkData specified. This is default
    data for Nodes. Node will override data if a node configuration file
    is specified (a file in Node.configPath named NodeName.cfg) and the node
    configuration file specifies a Node.data filename.

    Creates Node objects corresponding to GMN.Network.nodes (networkx DiGraph 
    nodes). The Node class objects are stored as "attributes"
    ( dict { 'Node' : Node Object } ) in the corresponding self.Graph.nodes. 
    '''

    def __init__( self, args, parameters ):
        '''Constructor'''
        self.Parameters        = parameters
        self.Graph             = None
        self.NetworkMap        = None
        self.TopologicalSorted = None
        self.data              = None  # All input data
        self.dataLib_i         = None  # indices to subset data "library"
        self.timeColumnName    = None

        # Read network graph : See CreateNetwork.py
        graphFile = parameters.networkFile
        with open( graphFile, 'rb' ) as f :
            NetworkGraphDict = pickle.load( f )
            self.Graph       = NetworkGraphDict[ 'Graph' ]
            self.NetworkMap  = NetworkGraphDict[ 'Map'   ] # Not used

            if args.DEBUG_ALL :
                print( '-> Network.__init__()' )
                self.Parameters.Print()

                print( 'Graph.nodes : ---------------------' )
                print( self.Graph.nodes )
                print( 'NetworkMap : ----------------------' )
                print( self.NetworkMap )

                if args.Plot :
                    import matplotlib.pyplot as plt
                    from   networkx import draw, shell_layout
                    plt.figure()
                    draw( self.Graph,
                          pos = shell_layout( self.Graph ),
                          node_size = 30, with_labels = True,
                          font_size = 14, font_weight = 'bold', alpha = 0.5 )
                    plt.show()

        # Sort for execution order : target node last
        # Note: topological_sort() returns a generator, store in list for reuse
        self.TopologicalSorted = list( topological_sort( self.Graph ) )

        # Load Network data as Pandas DataFrame
        if parameters.networkData and not parameters.networkData.isspace() :
            self.data = read_csv( parameters.networkData )

            if self.data.shape[0] <= parameters.predictionStart - 1:
                errMsg = "Network.__init__(): Nummber of data rows " +\
                         str( self.data.shape[0] ) +\
                         " is less than predictionStart " +\
                         str( parameters.predictionStart )
                raise RuntimeError( errMsg )

            if "generate" in parameters.mode.lower() :
                # Indices for "data library" from index 1 to predictionStart
                self.dataLib_i = range( parameters.predictionStart )
            else :
                # Forecast mode : all data
                self.dataLib_i = range( self.data.shape[0] )

            if args.DEBUG or args.DEBUG_ALL :
                print( "Network.__init__() Loaded",
                       parameters.networkData, " shape :", str(self.data.shape) )
                print( self.data.iloc[ self.dataLib_i ].tail(2) )

        self.timeColumnName = self.data.columns[0] # PRESUME column 1 is time

        # Instantiate Node objects. Store in self.Graph.nodes[ nodeName ]
        #   networkx.org/documentation/stable/reference/classes/digraph.html#
        for nodeName in self.Graph :
            # Node constructor can override Network data
            newNode = Node( args, self, nodeName )

            # Assign newNode object as attribute to this Graph node
            self.Graph.nodes[ nodeName ][ 'Node' ] = newNode

        # Validate all Nodes have data
        for nodeName in self.Graph:
            node = self.Graph.nodes[ nodeName ]['Node']

            if node.data is None:
                errMsg = "Network.__init__(): Node" + node.name +\
                         " has no data."
                raise RuntimeError( errMsg )
