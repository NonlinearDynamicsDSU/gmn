#! /usr/bin/env python3

# Python distribution modules
from multiprocessing import Pool
from os import listdir, walk

# Community modules

# Local modules
import gmn
from   gmn.CLI_Parser   import ParseCmdLine
from   gmn.ConfigParser import ReadConfig

#-------------------------------------------
def CallGenerate( GMN ):
    '''Wrapper for GMN.Generate() in multiprocessing Pool'''
    GMN.Generate()

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def main():
    '''GMN application command line interface
       Runs all config (.cfg) files found in args.configDir (-d).'''

    args = ParseCmdLine()

    if not args.configDir :
        raise RuntimeError( "No config file directory (-d) specified." )

    # List of config files in configDir
    configFiles = []

    # walk yields a 3-tuple (dirpath, dirnames, filenames)
    for root, dirs, files in walk( args.configDir ):
        for f in files :
            if f.endswith( '.cfg' ) :
                configFiles.append( root + '/' + f ) 

    if args.DEBUG:
        print( "RunDir config files:", configFiles )

    # Iterable of parameters for each configFile
    params = [ ReadConfig( args, configurationFile = f ) for f in configFiles ]

    # Iterable of GMN objects
    gmns = [ gmn.GMN( args, param ) for param in params ]

    with Pool( processes = args.cores ) as pool:
        DataOuts = pool.map( CallGenerate, gmns )

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
