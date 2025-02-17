import os
import sys
import traceback

import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox

class App(tk.Tk):
	VERSION: str = "1.0.0"
	"""
	Defines the current version of the application.
	
	:type: str
	"""
	
	_widgetStrategy: dict = {}
	"""
	Defines the strategy on how each widgets will be placed in the application.
	When a widget from `widgets` is not added to this dictionary, it will use the
	default "pack" strategy for placement.
	"""
	
	widgets: dict = {}
	"""
	A dictionary that holds all the widgets in the application. By default, it is an
 	empty dictionary.
  
	All widgets that are created in the application are stored in this dictionary for easy
	access and to easily add them to the application. The key is the name of the widget and
	the value is the widget itself.
 
	When being added, their position in the dictionary dictates their position in the
	application.
  
	:type: dict
 	"""
	
	file: str = None
	"""
	Holds the selected file by the user. By default, it is an empty list.
 
	:type: str
	"""

	###################
	### CONSTRUCTOR ###
	###################
 
	def __init__(self):
		super().__init__()
  
		self.title("Poster Analysis")
		# self.iconbitmap(f"{self.resource_path('assets/icon.ico)})

		# Centers the window
		appWidth = 800
		appHeight = 600
		winWidth = self.winfo_screenwidth()
		winHeight = self.winfo_screenheight()
		x = (winWidth // 2) - (appWidth // 2)
		y = (winHeight // 2) - (appHeight // 2)

		self.geometry(f"{appWidth}x{appHeight}+{x}+{y}")
		self.resizable(False, False)

		self._createWidgets()

	#######################
	### SETUP FUNCTIONS ###
	#######################

	def _createWidgets(self):
		"""
		Instantiates all the widgets needed by the application, then places
		them in the application's UI.
		"""