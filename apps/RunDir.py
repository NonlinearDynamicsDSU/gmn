#! /usr/bin/env python3

# Python distribution modules
from multiprocessing import set_start_method, Pool
from os import cpu_count, environ, listdir, sched_setaffinity, walk
from time import time

# Community modules

# Local modules
import gmn
from   gmn.CLI_Parser   import ParseCmdLine
from   gmn.ConfigParser import ReadConfig

# Reset core affinity to override BLAS, numpy binding to single core
sched_setaffinity( 0, range( cpu_count() ) )

#-------------------------------------------
def CallGenerate( args, param ):
    '''Wrapper for GMN.Generate() in multiprocessing Pool'''
    GMN = gmn.GMN( args, param )
    GMN.Generate()

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def main():
    '''GMN application command line interface
       Runs all config (.cfg) files found in args.configDir (-d).

       Note : The product of -c --cores and -t --threads should not
       exceed the cpu_count if using kedm.

       Thanks to Keichi Takahashi
       ---------------------------------------------------------------------
       Note : kedm : Kokkos using OpenMP is not compatible with
       multiprocessing.Pool using forked processes owing to a gcc library
       (libgomp) block in OpenMP. This requires Pool to use method = 'spawn'.
       See: https://github.com/pytorch/pytorch/issues/17199

       Note: OpenBLAS, used by pyEDM, kEDM etc., sets the core affinity
       when loaded and restricts the execution to one core only. When using
       separate spawned processes in Pool, must set the core affinity.
       See : https://stackoverflow.com/questions/15639779/
       ---------------------------------------------------------------------
    '''

    startTime = time()
    args      = ParseCmdLine()

    if not args.configDir :
        raise RuntimeError( "No config file directory (-d) specified." )

    # kedm : Kokkos : OpenMP
    environ[ 'OMP_NUM_THREADS' ] = str( args.threads )
    # gcc libgomp blocks multiprocess.Pool with default forked processes
    set_start_method( "spawn" )

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

    with Pool( processes = args.cores ) as pool:
        pool.starmap( CallGenerate,
                      [ ( args, param ) for param in params ] )

    print( 'Elapsed time', str( round( time() - startTime, 4 ) ) )

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
