
# Python distribution modules

# Community modules
from pandas import DataFrame, concat

# Local modules 
from gmn.Network      import Network
from gmn.Auxiliary    import TimeExtension
from gmn.CLI_Parser   import ParseCmdLine
from gmn.ConfigParser import ReadConfig

#-----------------------------------------------------------------------
class GMN:
    '''Class for Generative Manifold Networks (GMN)
       ../apps/Run.py is a CLI to instantiate, configure and Run GMN.
    '''

    # import Plot as a GMN class method
    from gmn.Plot import Plot

    #-------------------------------------------------------------------
    def __init__( self, args  = None,  parameters = None,
                  configFile  = None,  configDir  = None,
                  outputFile  = None,  cores      = 4,
                  plot        = False, statePlot  = False,
                  plotColumns = [],    plotFile   = None,
                  debug       = False ):

        '''Constructor

        Full configuration is performed by instantiating GMN with
        args from gmn.CLI_Parser.ParseCmdLine and parameters from
        from gmn.ConfigParser.ReadConfig.

        If parameter args is None GMN.__init__ function arguments
        are used to partially populate args. If parameters is None
        Parameters object is created from the args.
        '''

        if args is None:
            args = ParseCmdLine() # set default args
            # Insert constructor arguments into args
            args.configFile  = configFile
            args.configDir   = configDir
            args.outputFile  = outputFile
            args.cores       = cores
            args.Plot        = plot
            args.StatePlot   = statePlot
            args.plotColumns = plotColumns
            args.PlotFile    = plotFile
            args.DEBUG       = debug

        if args.configFile is None:
            raise RuntimeError( 'GMN(): configFile is required.' )

        if parameters is None:
            parameters = ReadConfig( args )

        self.args        = args        # command line args
        self.Parameters  = parameters  # args.configFile Parameters
        self.Network     = None
        self.DataOut     = None
        self.lastDataOut = None

        if args.DEBUG or args.DEBUG_ALL :
            import faulthandler
            faulthandler.enable()

        # Instantiate Network : Read DiGraph and instantiate nodes
        self.Network = Network( args, parameters )

        # Allocate DataFrame for output data.
        self.DataOut = DataFrame( columns = self.Network.data.columns,
                                  dtype = float )

    #-------------------------------------------------------------------
    def Generate( self ):
        '''Execute GMN generative loop for predictionLength steps
           calling the Generate() method of each Network Node. 
        '''

        if self.args.DEBUG or self.args.DEBUG_ALL :
            print( '-> GMN:Generate()' )

        # Local References for convenience and readability
        Network = self.Network
        Graph   = self.Network.Graph

        # Time Loop
        for t_i in range( self.Parameters.predictionLength ):
            if self.args.DEBUG_ALL :
                print( "===================== GMN Time:", t_i,
                       "=====================================" )

            # Allocate DataFrame for node outputs.
            NodeOutput = DataFrame( columns = self.Network.data.columns,
                                    dtype = float )

            # Network Loop
            for nodeName in Network.TopologicalSorted :
                node = Graph.nodes[ nodeName ]['Node']

                if self.args.DEBUG_ALL :
                    print( "GMN:Generate Network Loop:", nodeName )
                    print( 'columns:', node.Parameters.columns, ':',
                           'target',   node.Parameters.target )

                # Call node Generate method and store value in NodeOutput
                NodeOutput.at[ 0, nodeName ] = node.Generate( self.lastDataOut )

            # Set lastDataOut to node output for this time step, add to DataOut
            self.lastDataOut = NodeOutput
            self.DataOut     = concat( [ self.DataOut, NodeOutput ] )

        # Insert time column to DataOut
        # PRESUMED Network data column 1 is time
        newTime = TimeExtension(
            Network.data.iloc[ Network.dataLib_i][ Network.timeColumnName ],
            self.Parameters.predictionLength )

        self.DataOut[ Network.timeColumnName ] = newTime

        # Reset DataFrame row labels to default 0-offset integers
        self.DataOut.reset_index( drop = True, inplace = True )

        self.Output()

    #-------------------------------------------------------------------
    def Forecast( self ):
        '''Execute GMN forecast calling the Forecast() method of each 
           Network Node. It is presumed that lib & pred are specified.
        '''

        if self.args.DEBUG or self.args.DEBUG_ALL :
            print( '-> GMN:Forecast()' )

        # Local References for convenience and readability
        Network = self.Network
        Graph   = self.Network.Graph

        # Network Loop
        for nodeName in Network.TopologicalSorted :
            node = Graph.nodes[ nodeName ]['Node']

            if self.args.DEBUG_ALL :
                print( "GMN:Forecast Network Loop:", nodeName )
                print( 'columns:', node.Parameters.columns, ':',
                       'target',   node.Parameters.target )

            # Call node Forecast method and store in DataOut
            self.DataOut[ nodeName ] = node.Forecast()[1]

            if nodeName == Network.TopologicalSorted[0] :
                # Copy time values : only on first node
                self.DataOut[ Network.timeColumnName ] = node.Forecast()[0]

        # Reset DataFrame row labels to default 0-offset integers
        self.DataOut.reset_index( drop = True, inplace = True )

        self.Output()

    #-------------------------------------------------------------------
    def Output( self ):
        '''Write DataOut CSV file(s). Plot'''

        # Write DataOut CSV file(s)
        if self.args.outputFile:
            fmt = "%." + str( self.args.round ) + "f"
            self.DataOut.to_csv( self.args.outputFile,
                                 float_format = fmt, index = False )

        if len( self.Parameters.dataOutCSV ) and \
           not self.Parameters.dataOutCSV.isspace():
            fmt = "%." + str( self.args.round ) + "f"
            outFile = self.Parameters.outPath + '/' + self.Parameters.dataOutCSV
            self.DataOut.to_csv( outFile, float_format = fmt, index = False )

        if self.args.DEBUG or self.args.DEBUG_ALL :
            print( "GMN DataOut:" )
            print( self.DataOut )

        # Plot
        if self.args.Plot or self.args.StatePlot or \
           self.Parameters.showPlot or len( self.Parameters.plotFile ):
            self.Plot()
