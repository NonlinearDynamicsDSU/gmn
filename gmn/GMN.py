
# Python distribution modules
from datetime import datetime

# Community modules
from pandas import DataFrame, concat

# Local modules 
from .Network      import Network
from .Auxiliary    import TimeExtension
from .CLI_Parser   import ParseCmdLine
from .ConfigParser import ReadConfig

#-----------------------------------------------------------------------
class GMN:
    '''Class for Generative Manifold Networks (GMN)
       ../apps/Run.py is a CLI to instantiate, configure and Run GMN.
    '''

    # import Plot as a GMN class method
    from .Plot import Plot

    #-------------------------------------------------------------------
    def __init__( self,
                  args        = None,  parameters = None,
                  configFile  = None,  configDir  = None,
                  outputFile  = None,  cores      = 4,
                  plot        = False, plotType   = 'state',
                  plotColumns = [],    plotFile   = None,
                  figureSize  = [8,8], verbose    = False, debug = False ):

        '''Constructor

        Full configuration is performed by instantiating GMN with
        args from .CLI_Parser.ParseCmdLine and parameters from
        from .ConfigParser.ReadConfig.

        If args is None GMN.__init__ arguments partially populate args.
        If parameters is None Parameters object is created from the args.
        '''

        if args is None:
            args = ParseCmdLine( argv = [] ) # set default args
            # Insert constructor arguments into args
            args.configFile  = configFile
            args.configDir   = configDir
            args.outputFile  = outputFile
            args.cores       = cores
            args.Plot        = plot
            args.plotType    = plotType
            args.plotColumns = plotColumns
            args.PlotFile    = plotFile
            args.FigureSize  = figureSize
            args.verbose     = verbose
            args.DEBUG       = debug

        if args.configDir is None and args.configFile is None:
            raise RuntimeError( 'GMN(): configFile is required.' )

        if parameters is None:
            parameters = ReadConfig( args )

        self.args        = args        # command line args
        self.Parameters  = parameters  # args.configFile Parameters
        self.Network     = None
        self.DataOut     = None
        self.lastDataOut = None

        if args.DEBUG :
            import faulthandler
            faulthandler.enable()

        # Instantiate Network : Read DiGraph and instantiate nodes
        self.Network = Network( args, parameters )

        # Allocate DataFrame for output data.
        self.DataOut = DataFrame( columns = self.Network.dataColumns,
                                  dtype = float )

    #-------------------------------------------------------------------
    def Generate( self ):
        '''Execute GMN generative loop for predictionLength steps
           calling the Generate() method of each Network Node. 
        '''

        if self.args.verbose or self.args.DEBUG :
            start = datetime.now()
            print( f'-> GMN:Generate() {start}', flush = True )

        # Local References for convenience and readability
        Network = self.Network
        Graph   = self.Network.Graph

        # Time Loop
        for t_i in range( self.Parameters.predictionLength ):
            if self.args.DEBUG :
                print( "===================== GMN Time:", t_i,
                       "=====================================", flush = True )

            # Allocate DataFrame for node outputs.
            NodeOutput = DataFrame( columns = self.Network.dataColumns,
                                    dtype = float )

            # Network Loop
            for nodeName in Network.TopologicalSorted :
                node = Graph.nodes[ nodeName ]['Node']

                if self.args.DEBUG :
                    print( "GMN:Generate Network Loop:", nodeName )
                    print( 'columns:', node.Parameters.columns, ':',
                           'target',   node.Parameters.target, flush = True )

                # Call node Generate method and store value in NodeOutput
                NodeOutput.at[ 0, nodeName ] = node.Generate( self.lastDataOut )

            # Set lastDataOut to node output for this time step, add to DataOut
            self.lastDataOut = NodeOutput
            self.DataOut     = concat( [ self.DataOut, NodeOutput ] )

        # if factor != 1 apply
        if self.Parameters.factor != 1 :
            self.DataOut = self.DataOut.mul( node.Parameters.factor )

        # Insert time column to DataOut
        # PRESUMED Network data column 1 is time
        newTime = TimeExtension(
            Network.data.iloc[ Network.dataLib_i ][ Network.timeColumnName ],
            self.Parameters.predictionLength )

        self.DataOut[ Network.timeColumnName ] = newTime

        # Reset DataFrame row labels to default 0-offset integers
        self.DataOut.reset_index( drop = True, inplace = True )

        if self.args.verbose or self.args.DEBUG :
            end = datetime.now()
            print( f'<- GMN:Generate() {end}  :  {end-start}', flush = True )

        self.Output()

    #-------------------------------------------------------------------
    def Forecast( self ):
        '''Execute GMN forecast calling the Forecast() method of each 
           Network Node. It is presumed that lib & pred are specified.
        '''

        if self.args.verbose or self.args.DEBUG :
            start = datetime.now()
            print( f'-> GMN:Forecast() {start}', flush = True )

        # Local References for convenience and readability
        Network = self.Network
        Graph   = self.Network.Graph

        # Network Loop
        for nodeName in Network.TopologicalSorted :
            node = Graph.nodes[ nodeName ]['Node']

            if self.args.DEBUG :
                print( "GMN:Forecast Network Loop:", nodeName )
                print( 'columns:', node.Parameters.columns, ':',
                       'target',   node.Parameters.target, flush = True )

            # Call node Forecast method and store in DataOut
            self.DataOut[ nodeName ] = node.Forecast()[1]

            if nodeName == Network.TopologicalSorted[0] :
                # Copy time values : only on first node
                self.DataOut[ Network.timeColumnName ] = node.Forecast()[0]

        # Reset DataFrame row labels to default 0-offset integers
        self.DataOut.reset_index( drop = True, inplace = True )

        if self.args.verbose or self.args.DEBUG :
            end = datetime.now()
            print( f'<- GMN:Forecast() {end}  :  {end-start}', flush = True )

        self.Output()

    #-------------------------------------------------------------------
    def Output( self ):
        '''Write DataOut file(s). Plot'''

        fmt = "%." + str( self.args.round ) + "f"
        
        # Write DataOut file(s)
        if self.args.outputFile:
            if '.csv' in self.args.outputFile[-4:] :
                self.DataOut.to_csv( self.args.outputFile,
                                     float_format = fmt, index = False )
            elif '.feather' in self.args.outputFile[-8:] :
                self.DataOut.to_feather( self.args.outputFile )
            else :
                print( 'GMN.Output(): Unrecognized output file format' )

        if len( self.Parameters.dataOutFile ) and \
           not self.Parameters.dataOutFile.isspace():
            outFile = self.Parameters.outPath + '/' + self.Parameters.dataOutFile
            if '.csv' in outFile[-4:] :
                self.DataOut.to_csv( outFile, float_format = fmt, index = False )
            elif '.feather' in outFile[-8:] :
                self.DataOut.to_feather( outFile )
            else :
                print( 'GMN.Output(): Unrecognized data out file format' )

        if self.args.DEBUG :
            print( "GMN.Output() DataOut:" )
            print( self.DataOut, flush = True )

        # Plot
        if self.args.Plot or self.args.StatePlot or \
           self.Parameters.showPlot or len( self.Parameters.plotFile ):
            self.Plot()
