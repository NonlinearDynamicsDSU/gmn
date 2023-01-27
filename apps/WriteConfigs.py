#! /usr/bin/env python3

# Python distribution modules
import configparser
from   argparse import ArgumentParser
from   os       import mkdir, chdir

# Local modules 

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def main():
    '''Write configuration files.
       Create args.configDir directory
       In this dir create args.E directories (E*)
       In each E*/ create a *EX_tauY_TpZ.cfg with each .cfg values
       set for E, tau and the command line parameters.
    '''

    args = ParseCmdLine()

    config = DefaultConfig()

    # Replace default config with parameters
    config['GMN']['predictionLength'] = args.predLength
    config['GMN']['predictionStart']  = args.predStart
    config['GMN']['outPath']          = args.outPath
    config['GMN']['plotColumns']      = args.plotColumns

    config['Network']['targetNode'] = args.targetNode
    config['Network']['path']       = args.networkPath
    config['Network']['file']       = args.networkFile
    config['Network']['data']       = args.networkData

    config['EDM']['Tp'] = str( args.Tp )

    # Based on args, create directories of E* each with tau*
    # First, create the configDir and change dir
    try:
        mkdir( args.configDir )
    except FileExistsError:
        print( args.configDir, 'exists.' )

    chdir( args.configDir )

    # Create directories for E*
    for E in args.E :
        try:
            mkdir( 'E' + str( E ) )
        except FileExistsError:
            pass

    for E in args.E :
        config['EDM']['E'] = str( E )
        
        for tau in args.tau :
            # Write config files for tau*
            # Set config file tau
            config['EDM']['tau'] = str( tau )

            # File strings for .cfg, .csv, .png
            # Replace X Y Z : 'ABCD_EX_tau-Y_TpZ'
            baseStr = args.baseFileStr.replace( 'EX', 'E' + str(E),   1 )
            baseStr = baseStr.replace( 'tau-Y', 'tau' + str(tau),     1 )
            baseStr = baseStr.replace( 'TpZ',   'Tp'  + str(args.Tp), 1 )

            configFile = baseStr + '.cfg'
            csvFile    = baseStr + '.csv'
            pngFile    = baseStr + '.png'

            config['GMN']['dataOutCSV'] = csvFile
            config['GMN']['plotFile']   = pngFile

            configDir = './E' + str( E )

            WriteConfig( config, configDir, configFile )


#------------------------------------------------------------------------
#------------------------------------------------------------------------
def WriteConfig( config, configDir, configFile ):

    with open( configDir + '/' + configFile, 'w' ) as cf:
        config.write( cf )
    
#------------------------------------------------------------------------
#------------------------------------------------------------------------
def DefaultConfig():

    '''Default configuration file'''

    # Create ConfigParser object
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option # preserve case

    config['GMN'] = {}
    config['GMN']['predictionLength'] = '300'
    config['GMN']['predictionStart']  = '700'
    config['GMN']['outPath']          = '.'
    config['GMN']['dataOutCSV']       = 'ABCD_E3_tau-1_Tp1.csv'
    config['GMN']['showPlot']         = 'False'
    config['GMN']['plotFile']         = 'ABCD_E3_tau-1_Tp1.png'
    config['GMN']['plotType']         = 'state'
    config['GMN']['plotColumns']      = 'Out A B C D'

    config['Network'] = {}
    config['Network']['name']       = ''
    config['Network']['targetNode'] = 'Out'
    config['Network']['path']       = '../network/ABCD_Test/'
    config['Network']['file']       = 'ABCD_Network_E3_T0_tau-1_rhoDiff.pkl'
    config['Network']['data']       = '../data/TestData_ABCD.csv'

    config['Node'] = {}
    config['Node']['info']     = 'Node description'
    config['Node']['data']     = ''
    config['Node']['function'] = 'Simplex'

    config['EDM'] = {}
    config['EDM']['lib']             = ''
    config['EDM']['pred']            = ''
    config['EDM']['E']               = '3'
    config['EDM']['Tp']              = '1'
    config['EDM']['knn']             = '0'
    config['EDM']['tau']             = '-1'
    config['EDM']['theta']           = '3'
    config['EDM']['exclusionRadius'] = '0'
    config['EDM']['columns']         = ''
    config['EDM']['target']          = ''
    config['EDM']['solver']          = ''
    config['EDM']['embedded']        = 'False'
    config['EDM']['validLib']        = ''
    config['EDM']['generateSteps']   = '0'
    config['EDM']['libSizes']        = ''
    config['EDM']['sample']          = '0'
    config['EDM']['random']          = 'False'
    config['EDM']['includeData']     = 'False'
    config['EDM']['seed']            = '0'

    config['Scale'] = {}
    config['Scale']['factor'] = '1'
    config['Scale']['offset'] = '0'

    return config

#--------------------------------------------------------------
#--------------------------------------------------------------
def ParseCmdLine():

    parser = ArgumentParser( description = 'Write config' )

    parser.add_argument('-c', '--configFile',
                        dest    = 'configFile', type = str, 
                        action  = 'store',
                        default = 'ABCD_E3_tau-1_Tp1.cfg',
                        help    = 'Output config file.')

    parser.add_argument('-d', '--configDir',
                        dest    = 'configDir', type = str, 
                        action  = 'store',
                        default = './configTest',
                        help    = 'Directory of config files.')

    parser.add_argument('-PL', '--predLength',
                        dest    = 'predLength', type = str, 
                        action  = 'store',
                        default = '300',
                        help    = 'predLength')

    parser.add_argument('-PS', '--predStart',
                        dest    = 'predStart', type = str, 
                        action  = 'store',
                        default = '700',
                        help    = 'predStart')

    parser.add_argument('-OP', '--outPath',
                        dest    = 'outPath', type = str, 
                        action  = 'store',
                        default = './',
                        help    = 'outPath')

    parser.add_argument('-PC', '--plotColumns',
                        dest    = 'plotColumns', type = str, 
                        action  = 'store',
                        default = 'Out A B C D',
                        help    = 'plotColumns')

    parser.add_argument('-TN', '--targetNode',
                        dest    = 'targetNode', type = str, 
                        action  = 'store',
                        default = 'Out',
                        help    = 'targetNode')

    parser.add_argument('-NP', '--networkPath',
                        dest    = 'networkPath', type = str, 
                        action  = 'store',
                        default = '../network/ABCD_Test/',
                        help    = 'networkPath for networkFile')

    parser.add_argument('-NF', '--networkFile',
                        dest    = 'networkFile', type = str, 
                        action  = 'store',
                        default = 'ABCD_Network_E3_T0_tau-1_rhoDiff.pkl',
                        help    = 'networkFile (pkl)')

    parser.add_argument('-ND', '--networkData',
                        dest    = 'networkData', type = str, 
                        action  = 'store',
                        default = '../data/TestData_ABCD.csv',
                        help    = 'networkData file')

    parser.add_argument('-BF', '--baseFileStr',
                        dest    = 'baseFileStr', type = str, 
                        action  = 'store',
                        default = 'ABCD_EX_tau-Y_TpZ',
                        help    = 'base file string for .csv .png output')

    parser.add_argument('-Tp', '--Tp',
                        dest    = 'Tp', type = int, 
                        action  = 'store',
                        default = 1,
                        help    = 'Tp')

    parser.add_argument('-E', '--E', nargs = '+',
                        dest    = 'E', type = int, 
                        action  = 'store',
                        default = [3, 5, 7],
                        help    = 'List of E.')

    parser.add_argument('-t', '--tau', nargs = '+',
                        dest    = 'tau', type = int, 
                        action  = 'store',
                        default = [-1, -3, -5],
                        help    = 'List of tau.')

    parser.add_argument('-D', '--DEBUG',
                        dest   = 'DEBUG', # type = bool, 
                        action = 'store_true', default = False )

    args = parser.parse_args()

    return args

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
