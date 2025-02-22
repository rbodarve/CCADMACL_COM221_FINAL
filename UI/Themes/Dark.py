from typing import Dict, List

import tkinter as tk
from tkinter import ttk

#######################
### THEME VARIABLES ###
#######################

__COLORS: Dict[str, str] = {
    "fg": "#DEE2E6",
	"bg": "#212529",
	"disabledfg": "#B2B3B4",
}

#########################
### PRIVATE FUNCTIONS ###
#########################

def __modifyStyle(style: ttk.Style) -> None:
	"""
	Modifies the layout of the dark mode style.

	:param style: The style object for the application.
	:type style: ttk.Style
	"""
	assert style is not None, "The style object must be provided."
	assert isinstance(style, ttk.Style), "The style object must be a `ttk.Style` object."

	components: List[str] = [
		".",
		"TFrame",
		"TLabel",
		"TButton",
	]

	for component in components:
		additionalParams: Dict[str, any] = {}

		if "button" in component.lower():
			additionalParams["padding"] = (8, 4, 8, 4)
			additionalParams["anchor"] = tk.CENTER

			if component == "TButton":
				additionalParams["borderwidth"] = 1
				additionalParams["relief"] = tk.RAISED

		style.configure(
			component,
			foreground = __COLORS["fg"],
			background = __COLORS["bg"],
			**additionalParams
		)

def __buildDarkModeStyle(style: ttk.Style) -> ttk.Style:
	"""
	Returns the dark mode style.

	:return: The style object for the application.
	:rtype: ttk.Style
	"""
	assert style is not None, "The style object must be provided."
	assert isinstance(style, ttk.Style), "The style object must be a `ttk.Style` object."

	style.theme_create("dark", "default")
	style.theme_use("dark")

	__modifyStyle(style)

	return ttk.Style()

########################
### GLOBAL VARIABLES ###
########################

DARK_MODE_STYLE: ttk.Style = None

########################
### GLOBAL FUNCTIONS ###
########################

def registerDarkMode(style: ttk.Style) -> None:
	"""
	Registers the dark mode style.

	:param style: The style object for the application.
	:type style: ttk.Style
	"""
	assert style is not None, "The style object must be provided."
	assert isinstance(style, ttk.Style), "The style object must be a `ttk.Style` object."

	# Get access to the global variable(s)
	global DARK_MODE_STYLE

	DARK_MODE_STYLE = __buildDarkModeStyle(style)