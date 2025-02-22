from os.path import dirname, basename, isfile, join
import glob

# Excluded files
__excluded = [
	"__init__"
]

# Fetch all the view files
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and basename(f)[:-3] not in __excluded]
