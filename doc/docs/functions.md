## API Reference

### <function> GMN </function> 
** Description **  :   
Class object GMN.
Constructor:

| Parameter | Type | Default | Purpose |
| --------- | ---- | ------- | ------- |
| args        | argparse ArgumentParser |
| parameters  | gmn Parameter object    |
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
