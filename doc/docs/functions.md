## API Reference

### <function> GMN </function> 
** Description **  :   
Class object for Generative Manifold Networks (GMN).

** Constructor Signature **
```python
    def __init__( self, args  = None,  parameters = None,
                  configFile  = None,  configDir  = None,
                  outputFile  = None,  cores      = 4, 
                  plot        = False, statePlot  = False, 
                  plotColumns = [],    plotFile   = None,
                  debug       = False )
```

Full configuration is performed by instantiating GMN with `args` from gmn.CLI_Parser.ParseCmdLine() and `parameters` from gmn.ConfigParser.ReadConfig().

If `args` is `None` `GMN.__init__` function arguments are used to populate args. If `parameters` is `None` the parameters object is created from the `args`.

| Parameter | Type | Default | Purpose |
| --------- | ---- | ------- | ------- |
| args        | argparse ArgumentParser | None | command line arguments
| parameters  | gmn Parameter object    | None | GMN parameters
| configFile  | string | None | Configuration file for Network / Nodes |
| configDir   | string | None | Path to directory of configuration file(s) |
| outputFile  | string | None | CSV output file |
| cores       | int    | 4    | Number of CPU processor cores |
| plot        | bool   | False| Logical to plot time series results |
| statePlot   | bool   | False| Logical to plot time series and state results |
| plotColumns | []     | []   | List of columns to plot |
| plotFile    | string | None | File for plot results |
| debug       | bool   | False| Logical to print debug info |

** Returns **  :   
`GMN` class object.  The object is initialized to create the `GMN.Network` class object, all `Node` class objects of the network including input data, and the `GMN.DataOut` pandas DataFrame. 

** Example ** :   
```python
import gmn
G = gmn.GMN( configFile = 'config/default.cfg' )
```

---

### <function> GMN.Generate </function> 
** Description **  :   
Execute GMN forecast loop for predictionLength steps calling the Generate() method of each Network Node.

** Returns **  :   
Populates the `GMN.DataOut` pandas DataFrame. 

** Notes ** :   
If `args.outputFile`, or `parameters.dataOutCSV`: write `DataOut` as a .csv file.

if args.Plot or args.StatePlot or parameters.showPlot or parameters.plotFile: call GMN.Plot()

** Example ** :   
```python
G.Generate()
```
---

### <function> GMN.Plot </function> 
** Description **  :   
Plot generated time series (args.plot = True, or Parameters.plotType is 'time') or time series and 2-D state-space plots (args.statePlot = True, or Parameters.plotType is 'state').

** Returns **  :   
pyplot image 

---

### GMN.DataOut
** Description **  :   
pandas DataFrame of generated data.
