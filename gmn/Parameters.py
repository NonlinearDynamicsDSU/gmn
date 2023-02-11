
#---------------------------------------------------------------
#---------------------------------------------------------------
class Parameters:
    '''
    Parameters object for all entities. 

    Network has one. Each Node has one. 

    If a node.cfg file is found read Parameters and data from it.
    If not found, use Network Parameters and data. See Node.py
    '''

    def __init__( self ):
        '''Constructor'''

        # GMN
        self.mode             = None
        self.predictionStart  = None
        self.predictionLength = None
        self.outPath          = None
        self.dataOutCSV       = None
        self.showPlot         = None
        self.plotType         = None
        self.plotColumns      = None
        self.plotFile         = None

        # Network
        self.networkName      = None
        self.targetNode       = None
        self.networkFile      = None
        self.networkData      = None

        # Node
        self.nodeInfo         = None
        self.function         = None
        self.nodeData         = None
        self.nodeConfigPath   = None

        # EDM
        self.lib              = None
        self.pred             = None
        self.E                = None
        self.Tp               = None
        self.knn              = None
        self.tau              = None
        self.theta            = None
        self.exclusionRadius  = None
        self.columns          = None
        self.target           = None
        self.solver           = None
        self.embedded         = None
        self.validLib         = None
        self.generateSteps    = None
        self.libSizes         = None
        self.sample           = None
        self.random           = None
        self.includeData      = None
        self.seed             = None

        # Scale
        self.factor           = None
        self.offset           = None

    #-----------------------------------------------------------
    #-----------------------------------------------------------
    def Print( self ):
        print( 'Parameters: ----------------------------------' )

        # GMN
        print( '\t', 'mode',             self.mode )
        print( '\t', 'predictionStart',  self.predictionStart  )
        print( '\t', 'predictionLength', self.predictionLength )
        print( '\t', 'outPath',          self.outPath     )
        print( '\t', 'dataOutCSV',       self.dataOutCSV  )
        print( '\t', 'showPlot',         self.showPlot    )
        print( '\t', 'plotType',         self.plotType    )
        print( '\t', 'plotColumns',      self.plotColumns )
        print( '\t', 'plotFile',         self.plotFile    )

        # Network
        print( '\t', 'networkName', self.networkName )
        print( '\t', 'targetNode',  self.targetNode  )
        print( '\t', 'networkFile', self.networkFile )
        print( '\t', 'networkData', self.networkData )

        # Node
        print( '\t', 'nodeInfo',    self.nodeInfo )
        print( '\t', 'nodeData',    self.nodeData )
        print( '\t', 'function',    self.function )

        # EDM
        print( '\t', 'lib',             self.lib   )
        print( '\t', 'pred',            self.pred  )
        print( '\t', 'E',               self.E     )
        print( '\t', 'Tp',              self.Tp    )
        print( '\t', 'knn',             self.knn   )
        print( '\t', 'tau',             self.tau   )
        print( '\t', 'theta',           self.theta )
        print( '\t', 'exclusionRadius', self.exclusionRadius )
        print( '\t', 'columns',         self.columns  )
        print( '\t', 'target',          self.target   )
        print( '\t', 'solver',          self.solver   )
        print( '\t', 'embedded',        self.embedded )
        print( '\t', 'validLib',        self.validLib )
        print( '\t', 'generateSteps',   self.generateSteps )
        print( '\t', 'libSizes',        self.libSizes )
        print( '\t', 'sample',          self.sample   )
        print( '\t', 'random',          self.random   )
        print( '\t', 'includeData',     self.includeData )
        print( '\t', 'seed',            self.seed, flush = True )

        print( '\t', 'factor',          self.factor, flush = True )
        print( '\t', 'offset',          self.offset, flush = True )
