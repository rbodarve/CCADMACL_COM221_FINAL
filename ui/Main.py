import sys
from typing import Tuple, List, Dict, Callable

import tkinter as tk
from tkinter import ttk

import AppInfo
from Controllers import EventHandlerControllerClass, getEventHandlerController
from Themes import Dark
from Views import MainViewClass as MainView

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

	#######################
	# PROTECTED VARIABLES #
	#######################

	_eventHandlerController: EventHandlerControllerClass = getEventHandlerController()
	"""
	Holds the instance of the `EventHandlerController` class which handles
	the UI's event processes such as button clicks, text changes, etc.

	Only a single instance of this controller is allowed to exist since its
	design pattern is a singleton.
	"""

	#########################
	### PRIVATE VARIABLES ###
	#########################

	__widgets: Dict[str, tk.Widget] = {}
	"""
	A dictionary that holds all the widgets in the view. The key is the name
	of the widget and the value is the widget itself.
 
	By default, it is an empty dictionary.
	"""

	__widgetStrategy: Dict[str, str|dict] = {}
	"""
	A dictionary that holds the strategy on how each widget will be placed in
	the view. When a widget from `widgets` is not added to this dictionary, it
	will use the default "pack" strategy for placement.

	The widget strategy also dictates whether the widget is a static widget that
	cannot be changed or a dynamic widget that can be changed during runtime. This
	allows widgets to be safe from accidental changes and to be easily identified
	as static or dynamic widgets. This is defined using the "static" key in the
	strategy dictionary, with a `bool` value. If not defined, the widget is considered
	dynamic. If the widget is considered static, the `getWidget` method will raise
	an exception when trying to access it. This also meant that the widget cannot be
	removed.

	By default, it is an empty dictionary.
	"""

	__widgetBindings: Dict[str, List[Dict[str, str|Callable]]] = {}
	"""
	A dictionary that holds the bindings for each widget in the view. The key is
	the name of the widget and the value is a list of dictionaries that contain
	the event (`event`) and the callback function (`handler`) for that event.

	An example entry of the dictionary would be:

	```python
	self._widgetBindings["wrappingLabel"] = (
		{
			"event": "<Configure>",
			"handler": lambda e: e.widget.config(wraplength = e.width - 10)
		}
	)
	```

	This entry binds the `<Configure>` event to the `wrappingLabel` widget and
	configures the `wraplength` of the widget based on the width of the widget.
	"""

	__appDimensions: Tuple[int, int] = (600, 800)
	"""
	Defines the dimensions of the application window.
	"""	

	__appIcon: str = "assets/icon.ico"
	"""
	Defines the application's icon path.
	"""

	###################
	### CONSTRUCTOR ###
	###################
 
	def __init__(self):
		super().__init__()

		# Sets up the UI
		self.__createWidgets()

		# Configures the widgets
		self.__configureWidgets()

		# Register custom themes
		self.__registerThemes()

		# Sets up some configurations
		self.__setup()

	#######################
	### SETUP FUNCTIONS ###
	#######################

	def __registerThemes(self) -> None:
		"""
		Registers the custom themes for the application.

		Currently, the application only supports the dark mode theme.
		"""
		Dark.registerDarkMode(ttk.Style(self))

	def __setup(self) -> None:
		"""
		Sets up the application's configuration.
		"""
		self.title(AppInfo.NAME)
		self.iconbitmap(f"{AppInfo.resourcePath(self.__appIcon)}")

		# Sets the application's theme
		ttk.Style(self).theme_use("dark" if AppInfo.isDarkMode() else "default")

		# Recalculate the dimensions of the application
		self.__appDimensions = (
			int(self.winfo_screenheight() * 0.75),
			# 29 is the missing height of the image preview widget
			# so that the image preview will be a square shape.
			int(self.winfo_screenheight() * 0.75) + 29
		)

		# Centers the window
		appWidth = self.__appDimensions[0]
		appHeight = self.__appDimensions[1]
		winWidth = self.winfo_screenwidth()
		winHeight = self.winfo_screenheight()
		x = (winWidth // 2) - (appWidth // 2)
		y = (winHeight // 2) - (appHeight // 2)

		self.geometry(f"{appWidth}x{appHeight}+{x}+{y}")
		self.resizable(False, False)
		self.update()

	def __createWidgets(self) -> None:
		"""
		Instantiates all the widgets needed by the application, then places
		them in the application's UI.
		"""

		# Frame
		self.addWidget(
			"mainFrame",
			MainView(self),
			{
				"strat": "pack",
				"args": {
					"fill": tk.BOTH,
					"expand": True
				}
			}
		)

		# Adds the widgets to the application
		for key, widget in self.__widgets.items():
			# If the widget has a strategy, use it
			if self.__widgetStrategy.keys().__contains__(key):
				strategy = self.__widgetStrategy[key]
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

	def __configureWidgets(self) -> None:
		"""
		Configures the widgets for the Converter section of the application, such as adding event handlers
		and setting default values.
		"""
		for name, widget in self.__widgets.items():
			bindings = self.__widgetBindings.get(name)
			
			if bindings:
				for bind in bindings:
					widget.bind(bind["event"], bind["handler"])

	###########################
	### GETTERS AND SETTERS ###
	###########################

	def addWidget(self, name: str, widget: tk.Widget, strategy: Dict[str, str|dict] = None, bindings: List[Dict[str, str|Callable]] = None) -> "App":
		"""
		Adds a widget to the view. It takes in the widget to add, the name of
		the widget, and an optional strategy on how the widget will be placed
		in the view.
		
		:param name: The name of the widget.
		:type name: str
		
		:param widget: The widget to add to the view.
		:type widget: tk.Widget
		
		:param strategy: The strategy on how the widget will be placed in the view.
		:type strategy: Dict[str, str|dict]

		:param bindings: The bindings for the widget.
		:type bindings: List[dict]

		:return: This instance of the `App` class.
		:rtype: App
		"""
		self.__widgets[name] = widget

		if strategy:
			self.__widgetStrategy[name] = strategy

		if bindings:
			self.__widgetBindings[name] = bindings

		return self

	def getWidget(self, name: str) -> tk.Widget:
		"""
		Returns the widget with the given name.
		
		:param name: The name of the widget.
		:type name: str

		:return: The widget with the given name.
		:rtype: tk.Widget
		"""
		widget = self.__widgets.get(name)

		if not widget:
			raise Exception(f"Widget with name '{name}' does not exist.")

		strat = self.__widgetStrategy.get(name)
		if strat and "static" in strat.keys() and strat["static"]:
				raise Exception(f"Widget with name '{name}' is a static widget and cannot be accessed.")

		return self.__widgets.get(name)

# Initializes the entire application
def main():
	if len(sys.argv) > 0:
		if "--version" in sys.argv or "-V" in sys.argv:
			print(f"{App.NAME} v{App.VERSION}")
			sys.exit(0)

	app = App()
	app.mainloop()
 
if __name__ == "__main__":
	main()