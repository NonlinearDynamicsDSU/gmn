### #! /usr/bin/env python3

'''
Functions
1. TimeExtension() for DataFrame time column. Needs refactor.
'''

# Python distribution modules
from datetime import date, datetime, time

# Community modules
from pandas import Series

#-----------------------------------------------------------
#-----------------------------------------------------------
def TimeExtension( times, length = 1, verbose = False ) :
    '''Try to create length time values past times[-1]
       times must be at least length 2
       Classes probed : datetime.datetime, datetime.date
                        datetime.time, int, float
       If times are not recognized (str) return int sequence
    '''

    if len( times ) < 2 :
        raise RuntimeError( "times must have at least 2 elements." )

    if isinstance( times, Series ):
        times = times.array

    lastValue = None
    deltaTime = None

    # Classify time, get lastValue, compute deltaTime
    isDateTime = False
    isDate     = False
    isTime     = False
    isInt      = False
    isFloat    = False

    # datetime.date 
    isDate = isinstance( times[-1], date ) # True / False
    if isDate:
        lastValue = times[-1] # is date class
        deltaTime = times[-1] - times[-2]
    else:
        try:               d = date.fromisoformat( str( times[-1] ) )
        except ValueError: pass
        else:
            isDate    = True;
            lastValue = d
            deltaTime = d - date.fromisoformat( str( times[-2] ) )

    # datetime.date time 
    if not isDate:
        isDateTime = isinstance( times[-1], datetime )
        if isDateTime:
            lastValue = times[-1] # is datetime class
            deltaTime = times[-1] - times[-2]
        else:
            try:               dt = datetime.fromisoformat( str( times[-1] ) )
            except ValueError: pass
            else:
                isDateTime = True
                lastValue  = dt
                deltaTime  = dt - datetime.fromisoformat( str( times[-2] ) )

    # int
    if not isDate and not isDateTime:
        isInt = isinstance( times[-1], int )
        if isInt:
            lastValue = times[-1] # int
            deltaTime = times[-1] - times[-2]
        else:
            try:               int( str( times[-1] ) )
            except ValueError: pass
            else:
                isInt     = True
                lastValue = int( str( times[-1] ) )
                deltaTime = int( str( times[-1] ) ) - int( str( times[-2] ) )

    # float
    if not isDate and not isDateTime and not isInt:
        isFloat = isinstance( times[-1], float )
        if isFloat:
            lastValue = times[-1] # float
            deltaTime = times[-1] - times[-2]
        else:
            try:               float( str( times[-1] ) )
            except ValueError: pass
            else:
                isFloat   = True
                lastValue = float( str(times[-1]) )
                deltaTime = float( str(times[-1]) ) - float( str(times[-2]) )

    # time is last since 10, 12 will be converted to valid time objects
    # time is PITA since can't add, subtract time (midnight rollover issue)
    # and can't add/subtract timedelta. 
    if not isDate and not isDateTime and not isInt and not isFloat:
        isTime = isinstance( times[-1], time )
        if isTime:
            # Can't subtract two time objects... convert to datetime
            date_     = date.fromisoformat( '2000-01-01' )
            dtime     = datetime( 2000, 1, 1 )
            dtime1    = dtime.combine( date_, times[-1] )
            dtime2    = dtime.combine( date_, times[-2] )
            deltaTime = dtime1 - dtime2
            lastValue = dtime1 # set to datetime instead of time for +timedelta

        else:
            try:
                t1 = time.fromisoformat( str( times[-1] ) )
                t2 = time.fromisoformat( str( times[-2] ) )
            except ValueError: pass
            else:
                isTime    = True
                # Can't subtract two time objects... convert to datetime
                date_     = date.fromisoformat( '2000-01-01' )
                dtime     = datetime( 2000, 1, 1 )
                dtime1    = dtime.combine( date_, t1 )
                dtime2    = dtime.combine( date_, t2 )
                deltaTime = dtime1 - dtime2
                lastValue = dtime1 # datetime instead of time for +timedelta
            
    if not isDate and not isDateTime and not isInt \
       and not isFloat and not isTime:
        # Failed to convert
        lastValue = 0
        deltaTime = 1

    if verbose:
        print( 'TimeExtension()', isDateTime, isDate, isTime, isInt, isFloat,
               str( lastValue ) )

    # New vector of length
    newTime = [lastValue] * length

    for i in range( length ):
        if isTime:
            # time (lastValue) was converted to a datetime for timedelta
            # Ignore the bogus date, just take the time
            newTime_     = lastValue + deltaTime
            newTime[ i ] = time( hour   = newTime_.hour,
                                 minute = newTime_.minute,
                                 second = newTime_.second )
            lastValue    = newTime_
        else :
            newTime[ i ] = lastValue + deltaTime
            lastValue    = newTime[ i ]

    if verbose:
        print( "   newTime:", str( newTime ) )

    return newTime

#-----------------------------------------------------------
#
#-----------------------------------------------------------
def TestTimeExtension( length = 3 ) :
    ''' '''

    dt  = datetime.fromisoformat( '2000-01-31 12:00:30' )
    dt2 = datetime.fromisoformat( '2000-02-01 12:00:30' )
    d   = date.fromisoformat( '2000-01-31' )
    d2  = date.fromisoformat( '2000-02-02' )
    t   = time.fromisoformat( '12:00:30' )
    t2  = time.fromisoformat( '12:00:35' )
    i   = 122
    i2  = 123
    f   = 10.1
    f2  = 10.6

    TimeExtension( [ dt, dt2 ], length, True ) # why date object ? subclass ?
    TimeExtension( [ d, d2 ], length, True )
    TimeExtension( [ t, t2 ], length, True )
    TimeExtension( [ i, i2 ], length, True )
    TimeExtension( [ f, f2 ], length, True )

    print()

    TimeExtension( ['2000-01-31 12:00:30','2000-01-31 12:00:35'], length, True )
    TimeExtension( ['2000-01-31','2000-02-01'], length, True )
    TimeExtension( ['12:00:30','12:00:31'], length, True )
    TimeExtension( ['12','13','14'], length, True )
    TimeExtension( ['1.0','1.1','1.2'], length, True )
    TimeExtension( ['X','Y'], length, True )

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#if __name__ == "__main__":
#    TestTimeExtension()
