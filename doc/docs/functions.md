## GMN Methods

### <function> GMN </function> 
**Description** :  
Class object for Generative Manifold Networks (GMN).

**Constructor Signature**
```python
class GMN:
    def __init__( self, args  = None,  parameters = None,
                  configFile  = None,  configDir  = None,
                  outputFile  = None,  cores      = 4,
                  plot        = False, plotType   = 'state',
                  plotColumns = [],    plotFile   = None,
                  figureSize  = [8,8], verbose    = False, debug = False ):
```

Full configuration is performed by instantiating GMN with `args` from [gmn.CLI_Parser.ParseCmdLine()](https://github.com/NonlinearDynamicsDSU/gmn/blob/master/gmn/CLI_Parser.py) and `parameters` from [gmn.ConfigParser.ReadConfig()](https://github.com/NonlinearDynamicsDSU/gmn/blob/master/gmn/ConfigParser.py). This is normally done in an application such as the command-line-interface (CLI) program [Run.py](https://github.com/NonlinearDynamicsDSU/gmn/blob/master/apps/Run.py).

If `args` is `None` `GMN.__init__` function arguments are used to populate args. 

If `parameters` is `None` the parameters object is created from `args`.

| Parameter | Type | Default | Purpose |
| --------- | ---- | ------- | ------- |
| args        | argparse ArgumentParser | None | command line arguments
| parameters  | gmn Parameter object    | None | GMN parameters
| configFile  | string | None | Configuration file for Network / Nodes |
| configDir   | string | None | Path to directory of configuration file(s) |
| dataOutFile | string | None | Generated data output file : .csv or .feather |
| cores       | int    | 4    | Number of CPU processor cores |
| plot        | bool   | False| Logical to plot time series results |
| statePlot   | bool   | False| Logical to plot time series and state results |
| plotColumns | []     | []   | List of columns to plot |
| plotFile    | string | None | File for plot results |
| debug       | bool   | False| Logical to print debug info |

**Returns**  :  
`GMN` class object.  The object is initialized to create the `GMN.Network` class object, all `Node` class objects of the network including input data, and the `GMN.DataOut` pandas DataFrame. 

**Example** :  
```python
# Initalize GMN object with default.cfg
import gmn
G = gmn.GMN( configFile = 'config/default.cfg' )
```

---

### <function> GMN.Generate </function> 
**Description**  :   
Execute GMN forecast loop for `predictionLength` steps calling the Generate() method of each Network Node. Parameters `mode` must be `Generate`.

**Returns**  :  
Populates the `GMN.DataOut` pandas DataFrame. 

**Notes** :
If `args.outputFile`, or `parameters.dataOutFile`: write `DataOut` as a .csv or .feather file according to the `dataOutFile` file extension.

if args.Plot or args.StatePlot or parameters.showPlot or parameters.plotFile: call GMN.Plot()

**Example** :  
```python
G.Generate()
```
---

### <function> GMN.Forecast </function> 
** Description **  :
Execute GMN `Forecast()` method of each Network Node. Parameters `mode` must not be `Generate`. Presumes Parameters `lib` and `pred` are specified in the config file. Does not generate data, but makes predictions over the `pred` indices based on the `lib` state-space.

**Returns**  :  
Populates the `GMN.DataOut` pandas DataFrame. 

**Notes** :  
If `args.outputFile`, or `parameters.dataOutFile`: write `DataOut` as a .csv or .feather file according to the `dataOutFile` file extension.

if args.Plot or args.StatePlot or parameters.showPlot or parameters.plotFile: call GMN.Plot()

**Example** :  
```python
G.Forecast()
```
---

### <function> GMN.Plot </function> 
** Description **  :   
Plot generated time series (args.plot = True, or Parameters.plotType is 'time') or time series and 2-D state-space plots (args.statePlot = True, or Parameters.plotType is 'state').

**Returns**  :  
pyplot image 

---

## GMN Attributes

### GMN.DataOut
**Description**  :  
pandas DataFrame of generated data.

### GMN.Parameters
**Description**  :  
Python object of Parameters class.
