# Python distribution modules
from argparse import ArgumentParser

#--------------------------------------------------------------
#--------------------------------------------------------------
def ParseCmdLine():

    parser = ArgumentParser( description = 'Run GMN' )

    parser.add_argument('-i', '--configFile',
                        dest    = 'configFile', type = str, 
                        action  = 'store',
                        default = None,
                        help    = 'Input config file.')

    parser.add_argument('-d', '--configDir',
                        dest    = 'configDir', type = str, 
                        action  = 'store',
                        default = None,
                        help    = 'Directory of input config files.')

    parser.add_argument('-o', '--outputFile',
                        dest    = 'outputFile', type = str, 
                        action  = 'store',
                        default = None,
                        help    = 'Output file.')

    parser.add_argument('-r', '--round',
                        dest    = 'round', type = int, 
                        action  = 'store',
                        default = 6,
                        help    = 'DataOut output file precision.')

    parser.add_argument('-c', '--cores',
                        dest    = 'cores', type = int, 
                        action  = 'store',
                        default = 4,
                        help    = 'Multiprocessing cores.')

    parser.add_argument('-P', '--Plot',
                        dest    = 'Plot',
                        action  = 'store_true',
                        default = False,
                        help    = 'Plot.')

    parser.add_argument('-S', '--StatePlot',
                        dest   = 'StatePlot',
                        action = 'store_true', default = False,
                        help   = 'State-space Plot.')

    parser.add_argument('-C', '--PlotColumns', nargs = '+',
                        dest    = 'plotColumns', type = str, 
                        action  = 'store',
                        default = [],
                        help    = 'Plot columns.')
    
    parser.add_argument('-fs', '--FigureSize', nargs = 2,
                        dest    = 'FigureSize', type = float,
                        action  = 'store',
                        default = [8,8], # inches
                        help    = 'Figure Size.')

    parser.add_argument('-F', '--PlotFile',
                        dest   = 'PlotFile',
                        action = 'store', default = None,
                        help   = 'Write plot to PlotFile.')

    parser.add_argument('-D', '--DEBUG',
                        dest   = 'DEBUG', # type = bool, 
                        action = 'store_true', default = False )

    parser.add_argument('-DA', '--DEBUG_ALL',
                        dest   = 'DEBUG_ALL', # type = bool, 
                        action = 'store_true', default = False )

    args = parser.parse_args()

    return args
