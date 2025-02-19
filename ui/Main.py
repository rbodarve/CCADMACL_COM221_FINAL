import os
import sys
import traceback

import tkinter as tk

from Controller import Controller

from custom_widgets.ScrollableFrame import ScrollableFrame

class App(tk.Tk):
	"""
	`App` class is the main entrypoint of the application, allowing the entire program
	to run. This class is responsible for creating the application's window, setting
	up the UI, and managing the application's widgets. It is the main class that
	controls the entire application.

	For its logic and processes, it delegates that particular task to the `Controller`
	class, which is responsible for managing the application's logic while interacting
	with the UI.
	"""
	NAME: str = "Poster Analysis"
	"""
	Defines the name of the application.
	"""
	
	VERSION: str = "1.0.0"
	"""
	Defines the current version of the application.
	
	:type: str
	"""

	_controller: Controller = None
	"""
	Holds the only instance of the `Controller` class that will be created throughout
	the application's lifecycle.
	"""

	_widgetStrategy: dict = {}
	"""
	Defines the strategy on how each widgets will be placed in the application.
	When a widget from `widgets` is not added to this dictionary, it will use the
	default "pack" strategy for placement.
	"""
	
	_widgets: dict = {}
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

	_appDimensions: tuple = (800, 600)
	
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

		self.title(self.NAME)
		self.iconbitmap(f"{self.resourcePath('assets/icon.ico')}")

		# Centers the window
		appWidth = self._appDimensions[0]
		appHeight = self._appDimensions[1]
		winWidth = self.winfo_screenwidth()
		winHeight = self.winfo_screenheight()
		x = (winWidth // 2) - (appWidth // 2)
		y = (winHeight // 2) - (appHeight // 2)

		self.geometry(f"{appWidth}x{appHeight}+{x}+{y}")
		self.resizable(False, False)

		# Instantiates the controller
		self._controller = Controller.getInstance()

		# Sets up the UI
		self._createWidgets()

	#######################
	### SETUP FUNCTIONS ###
	#######################

	def _createWidgets(self):
		"""
		Instantiates all the widgets needed by the application, then places
		them in the application's UI.
		"""

		# Scrollable Frame
		self.setWidget(
			"scrollableFrame",
			tk.Frame(
				self,
				borderwidth = 2, 
				relief = tk.SUNKEN
			),
			{
				"strat": "pack",
				"args": {
					"fill": tk.BOTH,
					"expand": True
				}
			}
		)
  
		# > Title Label
		self.setWidget(
			"title",
			tk.Label(
				self.getWidget("scrollableFrame"),
				text = self.NAME,
				font = ("Arial", 24, "bold"),
				justify = tk.CENTER
			),
			{
				"strat": "pack",
				"args": {
					"fill": tk.X,
					"expand": True
				}
			}
		)
  
		# > Button Group
		self.setWidget(
			"buttonGroup",
			tk.Frame(
				self.getWidget("scrollableFrame")
			),
			{
				"strat": "pack",
				"args": {
					"fill": tk.X,
					"expand": True
				}
			}
		)
  
		# > > Select Image Button
		self.setWidget(
			"selectImageButton",
			tk.Button(
				self.getWidget("buttonGroup"),
				text = "Select Image",
				command = lambda: setattr(self, "file", self._controller.showImage(self.getWidget("imagePreview"), self._controller.selectImage()))
			)
		)
  
		# > Image Preview
		self.setWidget(
			"imagePreview",
			tk.Label(
				self.getWidget("scrollableFrame"),
				text = "No image selected",
				font = ("Arial", 12, "italic"),
				border = 2,
				relief = 'solid'
			),
			{
				"strat": "pack",
				"args": {
					"fill": tk.BOTH,
					"expand": True
				}
			}
		)

		# Adds the widgets to the application
		for key, widget in self._widgets.items():
			# If the widget has a strategy, use it
			if self._widgetStrategy.keys().__contains__(key):
				strategy = self._widgetStrategy[key]
				print(f"Using {strategy['strat']} strategy")
	
				# Check if the strategy is a valid function
				if (strategy["strat"] in ["pack", "grid", "place"]):
					getattr(widget, strategy["strat"])(**strategy["args"])
				# Else, fallback to the pack strategy
				else:
					widget.pack(pady = 10)
			# Otherwise, just use the pack strategy
			else:
				widget.pack(pady = 10)

	########################
	### HELPER FUNCTIONS ###
	########################
 
	def resourcePath(self, relative_path: str) -> str:
		"""
		Returns the absolute path of the resource file.
  		"""
		base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
		return os.path.join(base_path, relative_path)

	###########################
	### GETTERS AND SETTERS ###
	###########################

	def setWidget(self, name: str, widget: tk.Widget, strategy: dict = None):
		"""
		Sets the widget with the given name.

		:param name: The name of the widget.
		:type name: str

		:param widget: The widget to be set.
		:type widget: tk.Widget

		:param strategy: The strategy to be used when placing the widget.
		:type strategy: dict
		"""
		self._widgets[name] = widget
		if strategy:
			self._widgetStrategy[name] = strategy

	def getWidget(self, name: str) -> tk.Widget:
		"""
		Returns the widget with the given name.
		"""
		return self._widgets[name]

# Initializes the entire application
def main():
	if len(sys.argv) > 0:
		if "--version" in sys.argv:
			print(f"{App.NAME} v{App.VERSION}")
			sys.exit(0)
	
	app = App()
	app.mainloop()
 
if __name__ == "__main__":
	main()