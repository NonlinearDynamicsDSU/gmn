#! /usr/bin/env python3

# Python distribution modules
from multiprocessing import set_start_method, Pool
from os import cpu_count, listdir, sched_setaffinity, walk

# Community modules

# Local modules
import gmn
from   gmn.CLI_Parser   import ParseCmdLine
from   gmn.ConfigParser import ReadConfig

sched_setaffinity(0, range(cpu_count()))
#-------------------------------------------
def CallGenerate( args, param ):
    '''Wrapper for GMN.Generate() in multiprocessing Pool'''
    GMN =  gmn.GMN( args, param )
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

    # libgomp deadlocks when called in a forked process
    # c.f. https://github.com/pytorch/pytorch/issues/17199
    set_start_method( "spawn" )

    with Pool( processes = args.cores ) as pool:
        DataOuts = pool.starmap( CallGenerate, [ ( args, param ) for param in params ] )

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
