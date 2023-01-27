'''gmn package'''

# import gmn modules

from gmn.GMN          import *
from gmn.Auxiliary    import TimeExtension
from gmn.CLI_Parser   import *
from gmn.ConfigParser import *
from gmn.Network      import *
from gmn.Node         import *
from gmn.Parameters   import *
from gmn.Plot         import *

# Craziness to set __version__ from .toml : gmn must already be installed!
# Perhaps just use a .toml parser and read the file?
import importlib.metadata
__version__ = importlib.metadata.version("gmn")
