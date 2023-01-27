#! /usr/bin/env python3

# Python distribution modules

# Community modules

# Local modules
import gmn
from   gmn.CLI_Parser   import ParseCmdLine
from   gmn.ConfigParser import ReadConfig

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
def main():
    '''GMN application command line interface
       Runs a single GMN instance. See RunDir.py for parallel.'''

    args       = ParseCmdLine()
    parameters = ReadConfig( args )

    # Instantiate and initialize GMN
    GMN = gmn.GMN( args, parameters )

    GMN.Generate() # Run GMN forward in time

#----------------------------------------------------------------------------
# Provide for cmd line invocation and clean module loading
#----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
