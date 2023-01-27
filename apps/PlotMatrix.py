#! /usr/bin/env python3

import time, argparse, pickle

import matplotlib.pyplot as plt
from   pandas import read_csv, DataFrame

#----------------------------------------------------------------------------
# Main module
#----------------------------------------------------------------------------
def main():
    '''Plot result of InteractionMatrix.py.
       Input is a pickled dictionary of pandas dataFrames or a csv

       args.plot selects the dataFrame to plot

       if args.csvFile (-oc) save the dataFrame to args.csvFile'''

    startTime = time.time()

    args = ParseCmdLine()

    if args.verbose: print( args )

    #-----------------------------------------
    if args.CSV :
        df = read_csv( args.file, index_col = 0 )
    else:
        with open( args.file, 'rb') as f:
            D = pickle.load( f )

            if args.verbose: print( D.keys() )

            df = D[ args.plot ] # get pandas DataFrame

    if args.verbose: print( args.plot, '\n', df )

    if args.csvFile :
        df.round(4).to_csv( args.csvFile, na_rep = 'nan' )

    N = len( df.columns )

    #-----------------------------------------
    # Default title
    if args.title :
        title = args.title
    elif args.CSV :
        title = args.file
    else :
        if ( args.plot == 'SMap' ) :
            title = "SMap Non Linearity"
        elif ( args.plot == 'NonLinear' ) :
            title = "MI Non Linearity"
        elif ( args.plot == 'rhoDiff' ) :
            title = "CrossMap Correlation Difference"
        elif ( args.plot == 'CrossMap' ) :
            title = "Simplex Cross Map"
        elif ( args.plot == 'Correlation' ) :
            title = "Cross Correlation |ρ|"
        elif ( args.plot == 'CCM' ) :
            title = "CCM   row = column : col = target"
        elif ( args.plot == 'MutualInfo' ) :
            title = "Mutual Information"
        elif ( args.plot == 'CMI' ) :
            title = "CMI"

    plt.figure( figsize = args.size )
    plt.matshow( df, fignum = 1 ) # fignum = 1 is plt.figure above
    plt.title( title )
    plt.xticks( range(N), labels = df.columns[range(0,N)],
                rotation = 'vertical' )
    plt.yticks( range(N), labels = df.columns[range(0,N)] )
    plt.colorbar()
    plt.show()

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def ParseCmdLine():
    
    parser = argparse.ArgumentParser( description = 'Plot Matrix' )
    
    parser.add_argument('-f', '--file',
                        dest   = 'file',   type = str,  required = True,
                        action = 'store',  default = None,
                        help = 'Pickle of dict or csv from InteractionMatrix.py')

    parser.add_argument('-p', '--plot',
                        dest   = 'plot', type = str,
                        action = 'store',  default = None,
                        help = 'Plot (SMap CCM CrossMap MutualInfo NonLinear ' +\
                               'Correlation rhoDiff CMI)')

    parser.add_argument('-oc', '--csvFile',
                        dest   = 'csvFile', type = str,
                        action = 'store',   default = None,
                        help = 'Output .csv of matrix.')

    parser.add_argument('-t', '--title',
                        dest   = 'title', type = str,
                        action = 'store',  default = None,
                        help = 'Figure title.')

    parser.add_argument('-s', '--size',
                        dest   = 'size', type = int, nargs = 2,
                        action = 'store',  default = [5,5],
                        help = 'Figure size x, y')

    parser.add_argument('-v', '--verbose',
                        dest   = 'verbose',
                        action = 'store_true', default = False,
                        help = 'verbose.')

    args = parser.parse_args()

    if args.file :
        if args.file.lower().endswith( '.csv' ) :
            args.CSV = True
        else :
            args.CSV = False

    return args

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
if __name__ == "__main__":
    main()
