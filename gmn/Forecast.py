
# Community modules

# Local modules
from .Common import *

#----------------------------------------------------------------------
#----------------------------------------------------------------------
def Forecast( self ):
    '''Node method
       Called from GMN Forecast() in the Network Node loop'''

    if self.args.DEBUG :
        print( '-----> Node:Forecast() : ',self.FunctionType.name, self.name)
        print( self.data.tail( 2 ), flush = True );

    # Local References for convenience and readability
    Parameters = self.Parameters
    data       = self.data

    if self.args.DEBUG :
        print( '  data : shape: ', data.shape );
        print( data.tail( 3 ) ); print('', flush = True)

    #--------------------------------------------------------------------
    if self.FunctionType.value == FunctionType.Simplex.value :

        # If lib or pred are set in Parameters, use them
        # otherwise lib = [1, libEnd_i], pred = [N-1, N] N = data.shape[0]
        if len( Parameters.lib ) and not Parameters.lib.isspace():
            lib = Parameters.lib
        else:
            lib = "1 %d" % self.libEnd_i # Constant... for now

        if len( Parameters.pred ) and not Parameters.pred.isspace():
            pred = Parameters.pred
        else:
            pred = "%d %d" % ( data.shape[0] - 1, data.shape[0] )

        S = self.Function( dataFrame       = data,
                           lib             = lib,
                           pred            = pred,
                           E               = Parameters.E,
                           Tp              = Parameters.Tp,
                           knn             = Parameters.knn,
                           tau             = Parameters.tau,
                           exclusionRadius = Parameters.exclusionRadius,
                           columns         = Parameters.columns,
                           target          = Parameters.target,
                           embedded        = Parameters.embedded,
                           validLib        = Parameters.validLib,
                           generateSteps   = Parameters.generateSteps )

        # Return tuple of time and Predictions
        val = ( S.iloc[:,0], S['Predictions'] )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.SMap.value :

        # SMap multivariate requires embedded = True
        # Embed data to E, tau
        df = Embed( dataFrame = data, E = Parameters.E,
                    tau = Parameters.tau, columns = Parameters.columns )

        # Remove leading NaN from the time shift
        df = df.dropna()

        # Insert time column for SMap dataFrame
        df.insert( 0, data.columns[0], data.iloc[:,0] )

        # If lib or pred are set in Parameters, use them
        # otherwise lib = [1, libEnd_i], pred = [N-1, N] N = df.shape[0]
        if len( Parameters.lib ) and not Parameters.lib.isspace():
            lib = Parameters.lib
        else :
            lib  = "1 %d" % self.libEnd_i # Constant... for now

        if len( Parameters.pred ) and not Parameters.pred.isspace():
            pred = Parameters.pred
        else:
            pred = "%d %d" % ( df.shape[0] - 1, df.shape[0] )

        # Note: dataFrame = df, columns, target from embedding
        S = self.Function( dataFrame       = df,
                           lib             = lib,
                           pred            = pred,
                           E               = Parameters.E,
                           Tp              = Parameters.Tp,
                           knn             = Parameters.knn,
                           tau             = Parameters.tau,
                           theta           = Parameters.theta,
                           exclusionRadius = Parameters.exclusionRadius,
                           columns         = df.columns[1:-1],
                           target          = Parameters.target + '(t-0)',
                           solver          = None, # Parameters.solver,
                           embedded        = Parameters.embedded,
                           validLib        = Parameters.validLib,
                           generateSteps   = Parameters.generateSteps )

        # Return tuple of time and Predictions
        val = ( S['predictions'].iloc[:,0], S['predictions']['Predictions'] )

        # SMap can diverge if E, tau are not appropriate
        if val.max() > 1E15 :
            raise RuntimeError( "Forecast:SMap() Node: " + self.name +\
                                "   Divergence detected (>1E15)" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.kedmSimplex.value :
        raise RuntimeError( "Forecast kedmSimplex function not available" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.kedmSMap.value :
        raise RuntimeError( "Forecast kedmSMap function not available" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.Linear.value :
        raise RuntimeError( "Forecast Linear function not available" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.SVR.value :
        raise RuntimeError( "Forecast SVR function not available" )

    #--------------------------------------------------------------------
    elif self.FunctionType.value == FunctionType.knn.value :
        raise RuntimeError( "Forecast knn function not available" )

    if self.args.DEBUG :
        print( self.name, "val:", val )
        print( '<----- Node:Forecast() : ',self.FunctionType.name,self.name )
        print('', flush = True)

    return val
