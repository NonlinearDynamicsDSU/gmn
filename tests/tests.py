
import gmn
import unittest
# import pkg_resources # Get data file names from GMN package

from pandas import read_csv

#----------------------------------------------------------------
# Suite of tests
#----------------------------------------------------------------
class test_GMN( unittest.TestCase ):

    # def __init__(self, *args, **kwargs):
    #              super( test_GMN, self ).__init__( *args, **kwargs )

    #------------------------------------------------------------
    # 
    #------------------------------------------------------------
    @classmethod
    def setUpClass( self ):
        self.GetDataFiles( self )

    #------------------------------------------------------------
    # 
    #------------------------------------------------------------
    def GetDataFiles( self ):
        self.Files = {}

        dataFiles = [ "DataOut_ABCD_CMI_E7_tau-3.csv" ]

        # self.Files map of DataFrames from dataFiles
        for fileName in dataFiles:
            self.Files[ fileName ] = read_csv( fileName )

    #------------------------------------------------------------
    # GMN Generate Read configFile
    #------------------------------------------------------------
    def test_read_config( self ):

        # print ( "--- GMN Run Read Config ---", flush = True )
        args = gmn.CLI_Parser.ParseCmdLine()
        args.configFile = 'gmn_test1.cfg'
        parameters = gmn.ConfigParser.ReadConfig( args )

        # Instantiate and initialize GMN
        GMN = gmn.GMN( args, parameters )

        GMN.Generate() # Run GMN forward in time

        df = self.Files[ "DataOut_ABCD_CMI_E7_tau-3.csv" ]
 
        self.assertTrue( df.equals( GMN.DataOut.round(4) ) )

    #------------------------------------------------------------
    # GMN Generate argument configFile
    #------------------------------------------------------------
    def test_constructor_config( self ):

        # print ( "--- GMN Run constructor configFile ---", flush = True )

        # Instantiate and initialize GMN
        GMN = gmn.GMN( configFile = 'gmn_test1.cfg' )

        GMN.Generate() # Run GMN forward in time

        df = self.Files[ "DataOut_ABCD_CMI_E7_tau-3.csv" ]
 
        self.assertTrue( df.equals( GMN.DataOut.round(4) ) )

#------------------------------------------------------------
#
#------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
