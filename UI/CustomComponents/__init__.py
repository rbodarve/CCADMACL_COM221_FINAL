from os.path import dirname, basename, isfile, join
import glob
from importlib import import_module

# Excluded files
__excluded = [
	"__init__"
]

# Fetch all the view files
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and basename(f)[:-3] not in __excluded]

# Import the underlying names from the modules
for module in __all__:
	clss = getattr(import_module(f"CustomComponents.{module}"), module, None)
	if not clss: raise RuntimeError(f"Class '{module}' does not exist in module '{module}'.")
	setattr(__import__(__name__), f"{module}Class", clss)