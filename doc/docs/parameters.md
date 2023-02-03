## Parameters

The `GMN.Parameters` object is a mapping of configuration file parameters. A single configuration file can be provided in the `GMN` constructor or command line argument in which case each `Node` in the `Network` will inherit the same configuration file and parameters.

If a `Network` `Node` is named `node_1` and if a file named `node_1.cfg` is found in the `Network.path`, then `node_1` will load the `node_1.cfg` file defining the `Node` parameters. 

 `[EDM]` parameters are defined in [EDM Parameters](https://sugiharalab.github.io/EDM_Documentation/parameters/).

### Configuration File

```python
[GMN]
predictionLength = 300
predictionStart  = 700
outPath          = ../output
dataOutCSV       =
showPlot         = True
plotFile         =
plotType         = state
plotColumns      = Out A B C D

[Network]
name       = ABCD 4 Driver
targetNode = Out
path       = ../network/ABCD_Test/
file       = ABCD_Network_E3_T0_tau-1_rhoDiff.pkl
data       = ../data/TestData_ABCD.csv

[Node]
info       = Node description
# If node.cfg in Network.path, Node.data replaces Network.data
data       = ../data/TestData_ABCD.csv
function   = Simplex

[EDM]
# lib & pred are set to lib = [1, N-(E-1)tau]; pred = [N-1, N]
# where N = Network.predictionStart; unless overriden here:
lib             = 
pred            = 
E               = 7
Tp              = 1
knn             = 0
tau             = -3
theta           = 3
exclusionRadius = 0
# columns are set to node inputs plus the node itself
# target to the node itself; unless overriden here:
columns         = 
target          = 
solver          = 
embedded        = False
validLib        = 
generateSteps   = 0
libSizes        = 
sample          = 0
random          = False
includeData     = False
seed            = 0

[Scale]
factor          = 1
offset          = 0
```