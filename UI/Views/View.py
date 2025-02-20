from typing import List, Dict, Callable

import tkinter as tk
from tkinter import ttk

__all__ = ["View"]

class View(ttk.Frame):
	"""
	The base class for all views in the application. It inherits from the
	`tk.Frame` class, which is a container widget that is used to organize
	other widgets in the application. It provides a common interface for
	creating and managing widgets in the application.
 
	Furthermore, since it is an abstract class, it contains abstract methods
	that must be implemented by its subclasses. These methods define the
	behavior of the view, such as creating the widgets and arranging them.
	"""

	_widgets: Dict[str, tk.Widget] = {}
	"""
	A dictionary that holds all the widgets in the view. The key is the name
	of the widget and the value is the widget itself.
 
	By default, it is an empty dictionary.
	"""

	_widgetStrategy: Dict[str, str|dict] = {}
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

	_widgetBindings: Dict[str, List[Dict[str, str|Callable]]] = {}
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

	###################
	### CONSTRUCTOR ###
	###################
	def __init__(self, root: tk.Tk|tk.Widget, fillSpace: bool = True, *args, **kwargs) -> None:
		"""
		Initializes the View class. It takes in the parent widget where the
		view will be placed.
		
		:param root: The parent widget where the view will be placed.
		:type root: tk.Tk | tk.Widget

		:param fillSpace: A flag that indicates whether the view should fill the space of the parent widget. Optional.
		:type fillSpace: bool
		"""
		super().__init__(root, *args, **kwargs)
  
		if fillSpace:
			self.bind(
				"<Configure>",
				lambda e: e.widget.config(
					width = e.widget.winfo_toplevel().winfo_width(),
					height = e.widget.winfo_toplevel().winfo_height()
				)
			)

	#######################
	### SETUP FUNCTIONS ###
	#######################
	def createWidgets(self) -> None:
		"""
		Creates the widgets for the view and arranges them in the view.

		This method is an abstract method that must be implemented by the
		subclasses of the `View` class.
		"""
		print(self._widgets.keys())

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

	######################
	### HELPER METHODS ###
	######################

	# Widgets
	def addWidget(self, name: str, widget: tk.Widget, strategy: Dict[str, str|dict] = None, bindings: List[Dict[str, str|Callable]] = None) -> "View":
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

		:return: This instance of the `View` class.
		:rtype: View
		"""
		self._widgets[name] = widget
		if strategy:
			self._widgetStrategy[name] = strategy

		return self

	def getWidget(self, name: str) -> tk.Widget:
		"""
		Returns the widget with the given name.
		
		:param name: The name of the widget.
		:type name: str

		:return: The widget with the given name.
		:rtype: tk.Widget
		"""
		widget = self._widgets.get(name)

		if not widget:
			raise Exception(f"Widget with name '{name}' does not exist.")

		strat = self._widgetStrategy.get(name)
		if strat and strat["static"]:
				raise Exception(f"Widget with name '{name}' is a static widget and cannot be accessed.")

		return self._widgets.get(name)

	def removeWidget(self, name: str) -> "View":
		"""
		Removes the widget with the given name from the view.
		
		:param name: The name of the widget to remove.
		:type name: str

		:return: This instance of the `View` class.
		:rtype: View
		"""
		widget = self._widgets.get(name)

		if not widget:
			raise Exception(f"Widget with name '{name}' does not exist.")

		strat = self._widgetStrategy.get(name)
		if strat and strat["static"]:
			raise Exception(f"Widget with name '{name}' is a static widget and cannot be removed.")
		
		self._widgets.pop(name, None)
		self._widgetStrategy.pop(name, None)

		return self