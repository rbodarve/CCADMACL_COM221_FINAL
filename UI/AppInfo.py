import os
import sys

import darkdetect

#####################
### APP CONSTANTS ###
#####################

NAME: str = "Poster Analysis"
"""
Defines the name of the application.
"""

VERSION: str = "1.0.0"
"""
Defines the current version of the application.

:type: str
"""

RESOURCE_PATH: str = "assets"
"""
Defines the path to the application's resources/assets folder
that contains the images, icons, and other resources needed.
"""

RATING_CSV_SOURCE: str = "map/rating-map.csv"
"""
Defines where the rating map CSV file is located.
"""


#########################
### PRIVATE VARIABLES ###
#########################

__isDarkMode: bool = darkdetect.isDark()
"""
Holds the current mode of the application. This variable is used
to determine the application's color scheme in accordance to the
system's color scheme.
"""

########################
### HELPER FUNCTIONS ###
########################

#===================
# RESOURCE FUNCTIONS
#===================

def resourcePath(target: str) -> str:
	"""
	Returns the absolute path of the resource file after the provided
	`target` file has been appended to the base path.

	:param target: The target resource file.
	:type target: str

	:returns: The absolute path of the resource file.
	:rtype: str
	"""

	base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_path, target)

#====================
# DARK MODE FUNCTIONS
#====================

def isDarkMode() -> bool:
	"""
	Returns whether the application is in dark mode or not.

	:returns: True if the application is in dark mode, False otherwise.
	:rtype: bool
	"""
	# Get access to the global variable(s)
	global __isDarkMode

	return __isDarkMode