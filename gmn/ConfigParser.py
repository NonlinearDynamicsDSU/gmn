# Python distribution modules
import configparser

# Local modules 
from gmn.Parameters import Parameters

#------------------------------------------------------------------------
#------------------------------------------------------------------------
def ReadConfig( args, configurationFile = None ):
    '''Read configuration file, parse into Parameters object'''

    configFile = None
    if not configurationFile:
        configFile = args.configFile
    else :
        configFile = configurationFile

    if not configFile:
        raise RuntimeError( "ReadConfig(): configFile not specified." )

    config = configparser.ConfigParser()

    config.read( configFile )

    # Map config file values into param
    param = Parameters()

    param.mode             = config[ 'GMN' ][ 'mode' ]
    param.predictionStart  = config.getint( 'GMN', 'predictionStart'  )
    param.predictionLength = config.getint( 'GMN', 'predictionLength' )
    param.outPath          = config[ 'GMN' ][ 'outPath'     ]
    param.dataOutCSV       = config[ 'GMN' ][ 'dataOutCSV'  ]
    param.showPlot         = config.getboolean( 'GMN', 'showPlot' )
    param.plotType         = config[ 'GMN' ][ 'plotType'    ]
    param.plotColumns      = config[ 'GMN' ][ 'plotColumns' ]
    param.plotFile         = config[ 'GMN' ][ 'plotFile'    ]

    param.networkName      = config[ 'Network' ][ 'name' ]
    param.targetNode       = config[ 'Network' ][ 'targetNode' ]
    param.networkFile      = config[ 'Network' ][ 'file' ]
    param.networkData      = config[ 'Network' ][ 'data' ]

    param.nodeInfo         = config[ 'Node' ][ 'info' ]
    param.function         = config[ 'Node' ][ 'function' ]
    param.nodeData         = config[ 'Node' ][ 'data' ]
    param.nodeConfigPath   = config[ 'Node' ][ 'configPath' ]

    param.lib              = config [ 'EDM' ][ 'lib'  ]
    param.pred             = config [ 'EDM' ][ 'pred' ]
    param.E                = config.getint( 'EDM', 'E'   )
    param.Tp               = config.getint( 'EDM', 'Tp'  )
    param.knn              = config.getint( 'EDM', 'knn' )
    param.tau              = config.getint( 'EDM', 'tau' )
    param.theta            = config.getfloat( 'EDM', 'theta' )
    param.exclusionRadius  = config.getint( 'EDM', 'exclusionRadius' )
    param.columns          = config [ 'EDM' ][ 'columns' ]
    param.target           = config [ 'EDM' ][ 'target'  ]
    param.solver           = config [ 'EDM' ][ 'solver'  ]
    param.embedded         = config.getboolean( 'EDM', 'embedded' )
    param.validLib         = config [ 'EDM' ][ 'validLib' ]
    param.generateSteps    = config.getint( 'EDM', 'generateSteps' )
    param.libSizes         = config [ 'EDM' ][ 'libSizes' ]
    param.sample           = config.getint( 'EDM', 'sample' )
    param.random           = config.getboolean( 'EDM', 'random' )
    param.includeData      = config.getboolean( 'EDM', 'includeData' )
    param.seed             = config.getint( 'EDM', 'seed' )

    param.factor           = config.getfloat( 'Scale', 'factor' )
    param.offset           = config.getfloat( 'Scale', 'offset' )

    # Convert validLib to list of int if not empty
    if len( param.validLib ) == 0 or param.validLib.isspace():
        param.validLib = []
    else:
        param.validLib = [ int(x) for x in param.validLib.split() ]

    return param
