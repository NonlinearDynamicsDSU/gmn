#! /usr/bin/env python3

# Distribution modules
import time, argparse, pickle, json

# Community modules
import matplotlib.pyplot as plt
from   networkx import DiGraph, is_directed_acyclic_graph, draw, shell_layout
from   networkx import node_link_data, topological_sort

# Local modules
from gmn.Auxiliary import ReadDataFrame

#----------------------------------------------------------------------------
def main():
    ''' Create a GMN network using networkx directed graph DiGraph.
    An interaction matrix (args.interactionFile) is required input.
    The imatrix rows quantify interaction for each node. The node in the
    first column of a row is the driven node, nodes in the other columns
    along the row are potential drivers. 

    CreateNetwork() writes binary networkx.DiGraph() object to args.outputFile,
    or a .json file if args.json is True.
    '''
    args = ParseCmdLine()

    interactMatrix = ReadMatrix( args )

    CreateNetwork( args, interactMatrix )

#----------------------------------------------------------------------------
def CreateNetwork( args, interactionMatrix ):
    '''Starting with a list of target nodes (args.targetCols) link the strongest
    args.numDrivers to each target node. Then, recursively add nodes that 
    link to the established target nodes and drivers. 

    Write binary networkx.DiGraph() & dict objects to args.outputFile.
    Return { Graph : network_graph, Map : network_dict }.'''

    startTime = time.time()

    network_graph = DiGraph() # for assessing graph properties
    network_nodes = []        # nodes already added to network

    # nodes to be explored start at targetCols
    explore_queue = args.targetCols.copy()  
    network_dict  = {}  # { node : [drivers] }
    network_cycle = {}  # nodes that create loops (not used)

    # Starting at args.targetCols, keep adding nodes until no more
    # nodes in explore_queue
    while len( explore_queue ):
        node_id = explore_queue.pop(0)

        if node_id in network_nodes:
            continue

        network_nodes.append( node_id )
        network_dict [ node_id ] = [] # empty list of drivers for new node
        network_cycle[ node_id ] = [] # empty list of cyclic nodes for new node

        # Sort & rank iMatrix (ascending if CMI
        # Store node_ids that exceed threshold (or meet if CMI)
        if args.cmi :
            # Rank iMatrix ascending, not descending
            # df.loc[ x ] returns the row x as a Series.
            top_drivers =\
                interactionMatrix.loc[ node_id ].sort_values( ascending = True )
            # Threshold iMatrix >= to allow 0 MI as best rank
            top_drivers =\
                top_drivers[( top_drivers >= args.threshold ) & \
                            ( top_drivers.index != node_id )][:args.numDrivers]
        else :
            # df.loc[ x ] returns the row x as a Series.
            top_drivers =\
                interactionMatrix.loc[ node_id ].sort_values()

            top_drivers =\
                top_drivers[( top_drivers > args.threshold ) & \
                            ( top_drivers.index != node_id )][:args.numDrivers]

        for driver_id in top_drivers.index:
            # Try adding driver -> current node & edge to network
            network_graph.add_node( driver_id )
            network_graph.add_edge( driver_id, node_id )

            if is_directed_acyclic_graph( network_graph ):
                network_dict[ node_id ].append( driver_id )
            else:
                # driver_id created a cycle, remove edge
                network_graph.remove_edge( driver_id, node_id )

                if not network_graph.has_node( node_id ) :
                    # node_id not in network, remove the driver
                    network_graph.remove_node( driver_id )

                # store driver_id in network_cycle (for reporting)
                network_cycle[ node_id ].append( driver_id )

        # Add driver nodes to explore_queue for upstream nodes
        for driver_id in network_dict[ node_id ]:
            explore_queue.append( driver_id )

    print( len( network_graph ), 'nodes.' )
    if args.cmi :
        print( 'NOTE: --cmi : iMatrix sorted ascending, threshold >=' )

    if args.verbose :
        print( "Network Dictionary { Node : ( [Drivers] ), ... }" )
        print( network_dict )
        print( "Network Cycle { Node : [], ... }" )
        print( network_cycle )

    Network = { 'Graph' : network_graph, 'Map' : network_dict }

    #----------------------------------------------------------
    if args.outputFile :
        if args.json:
            obj = node_link_data( network_graph )
            obj[ 'topological_ordering' ] =\
                list( topological_sort( network_graph ) )
            obj[ 'target_cols' ] = args.targetCols

            with open( args.outputFile, 'w' ) as fdOut:
                json.dump( obj, fdOut )
        else:
            with open( args.outputFile, 'wb' ) as fdOut:
                pickle.dump( Network, fdOut )

    elapsedTime = time.time() - startTime
    print( "Elapsed time:", round( elapsedTime, 4 ) )

    #----------------------------------------------------------
    if args.plotNetwork :
        plt.figure()
        draw( network_graph,
              pos = shell_layout( network_graph ),
              node_size = 30, with_labels = True,
              font_size = args.fontSize,
              font_weight = 'bold', alpha = 0.5 )
        plt.show()

#----------------------------------------------------------------------------
def ReadMatrix( args ):
    '''Read data file of interaction matrix into pandas DataFrame.'''

    # Read interaction matrix into pandas DataFrame
    interactMatrix = ReadDataFrame( args.interactionMatrix, index_col = 0 )

    if len( args.excludeColumns ) :
        interactMatrix.drop( columns = args.excludeColumns, inplace = True )

    if args.verbose :
        print( "Interaction Matrix shape :", end = "  " )
        print( interactMatrix.shape )
        print( "Interaction Matrix:" )
        print( interactMatrix.round( 4 ) )

    return interactMatrix

#----------------------------------------------------------------------------
def ParseCmdLine():
    parser = argparse.ArgumentParser( description = 'Create Network' )

    parser.add_argument('-i', '--interactionMatrix',
                        dest    = 'interactionMatrix', type = str, 
                        action  = 'store',
                        default = './ABCD_rhoDiff.csv',
                        help    = 'Interaction matrix: .csv or .feather.')

    parser.add_argument('-t', '--targetCols', nargs = '+',
                        dest    = 'targetCols', type = str, 
                        action  = 'store',
                        default = ["Out"],
                        help    = 'Target columns.')

    parser.add_argument('-c', '--cmi',
                        dest   = 'cmi',
                        action = 'store_true',  default = False,
                        help   = 'Interaction matrix row sort ascending,' +\
                                 'threshold >= to allow 0 MI')

    parser.add_argument('-o', '--outputFile',
                        dest    = 'outputFile', type = str, 
                        action  = 'store', default = None,
                        help    = 'Output file name.')

    parser.add_argument('-j', '--json',
                        dest   = 'json',
                        action = 'store_true',  default = False,
                        help   = 'Write output as a JSON file')

    parser.add_argument('-T', '--threshold',
                        dest   = 'threshold', type = float,
                        action = 'store',  default = 0,
                        help   = 'threshold of node interaction.')

    parser.add_argument('-d', '--numDrivers',
                        dest   = 'numDrivers', type = int, 
                        action = 'store',  default = 4,
                        help   = 'Number of driver timeseries.')

    parser.add_argument('-x', '--excludeColumns', nargs = '*',
                        dest   = 'excludeColumns', type = str, 
                        action = 'store',  default = [],
                        help   = 'Columns to exclude.')

    parser.add_argument('-P', '--plotNetwork',
                        dest   = 'plotNetwork', 
                        action = 'store_true',  default = False,
                        help   = 'Render network graph.')

    parser.add_argument('-fs', '--fontSize',
                        dest   = 'fontSize', type = int, 
                        action = 'store',  default = 12,
                        help   = 'Node font size.')

    parser.add_argument('-v', '--verbose',
                        dest   = 'verbose', 
                        action = 'store_true',  default = False,
                        help   = 'Verbose output.')

    args = parser.parse_args()

    if args.verbose :
        print( args )

    return args

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
