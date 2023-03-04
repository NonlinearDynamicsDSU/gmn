# Python distribution modules
from enum import Enum

#-----------------------------------------------------------
#-----------------------------------------------------------
class FunctionType( Enum ):
    '''Enumeration for Function types in Node'''
    Simplex     = 1
    kedmSimplex = 2
    SMap        = 3
    kedmSMap    = 4
    Linear      = 5
    SVR         = 6
    knn         = 7
