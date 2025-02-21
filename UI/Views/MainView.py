import os
import sys

import tkinter as tk

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import AppInfo
from Controllers import EventHandlerControllerClass, ServiceControllerClass, getEventHandlerController, getServiceController
from Views.View import View

class MainView(View):
	"""
	`MainView` class is responsible for creating the main view frame for the application,
	setting up the UI, and managing the application's widgets. This class is the main
	class that controls the entire application's UI since this application only has a
	single view.
	"""

	#######################
	# PROTECTED VARIABLES #
	#######################

	_serviceController: ServiceControllerClass = getServiceController()
	"""
	Holds the instance of the `ServiceController` class which handles
	the application's service logic. This controller is responsible for
	bridging the gap between the UI and the application's logic.

	Only a single instance of this controller is allowed to exist since its
	design pattern is a singleton.
	"""

	_eventHandlerController: EventHandlerControllerClass = getEventHandlerController()
	"""
	Holds the instance of the `EventHandlerController` class which handles
	the UI's event processes such as button clicks, text changes, etc.

	Only a single instance of this controller is allowed to exist since its
	design pattern is a singleton.
	"""

	###################
	### CONSTRUCTOR ###
	###################
	def __init__(self, root: tk.Tk, *args, **kwargs) -> None:
		super().__init__(root, *args, **kwargs)

		self.createWidgets()
		self.configureWidgets()

	#######################
	### SETUP FUNCTIONS ###
	#######################

	def createWidgets(self) -> None:
		print("Creating widgets for MainView")

		# Title Label
		self.addWidget(
			"title",
			tk.Label(
				self,
				text = AppInfo.NAME,
				font = ("Helvetica", 24),
				justify = tk.CENTER
			),
			{
				"strat": "pack",
				"args": {
					"ipady": 10,
					"side": tk.TOP,
					"fill": tk.X
				}
			}
		)

		# Image Preview
		self.addWidget(
			"imagePreview",
			tk.Label(
				self,
				relief = tk.GROOVE,
				borderwidth = 3
			),
			{
				"strat": "pack",
				"args": {
					"padx": 50,
					"pady": 25,
					"side": tk.TOP,
					"fill": tk.BOTH,
					"expand": True,
				}
			}
		)

		# Button Group
		self.addWidget(
			"buttonGroup",
			tk.Frame(self),
			{
				"strat": "pack",
				"args": {
					"side": tk.TOP,
					"ipady": 10
				}
			}
		)

		# > Select Image Button
		self.addWidget(
			"selectImgBtn",
			tk.Button(
				self.getWidget("buttonGroup"),
				text = "Select Image",
				command = lambda: self._eventHandlerController.selectImage(self.getWidget("imagePreview"))
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT
				}
			}
		)

		# > Predict Button
		self.addWidget(
			"predictBtn",
			tk.Button(
				self.getWidget("buttonGroup"),
				text = "Predict",
				command = self._serviceController.predict
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT
				}
			}
		)

		super().createWidgets()
		return

	def configureWidgets(self) -> None:
		"""
		Configures the widgets for the Converter section of the application, such as adding event handlers
		and setting default values.
		"""
		for name, widget in self._widgets.items():
			bindings = self._widgetBindings.get(name)
			
			if bindings:
				for bind in bindings:
					widget.bind(bind["event"], bind["handler"])
