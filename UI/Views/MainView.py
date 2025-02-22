import os
import sys

import tkinter as tk
from tkinter import ttk

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
		# Assertion Tests
		assert isinstance(root, tk.Tk), "The root must be a `tk.Tk` object."

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
			ttk.Label(
				self,
				text = AppInfo.NAME,
				font = ("Helvetica", 24),
				anchor = tk.CENTER
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
			ttk.Label(
				self,
				text = "No image selected",
				relief = tk.GROOVE,
				borderwidth = 3,
				anchor = tk.CENTER
			),
			{
				"strat": "pack",
				"args": {
					"padx": 50,
					"side": tk.TOP,
					"fill": tk.BOTH,
					"expand": True,
				}
			}
		)

		# Image Label
		self.addWidget(
			"imageLabel",
			ttk.Label(
				self,
				font = ("Helvetica", 12),
				anchor = tk.CENTER
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.TOP
				}
			}
		)

		# Button Group
		self.addWidget(
			"buttonGroup",
			ttk.Frame(self),
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
			ttk.Button(
				self.getWidget("buttonGroup"),
				text = "Select Image",
				command = lambda: self.getWidget("imageLabel").configure(text = self._eventHandlerController.selectImage(self.getWidget("imagePreview")).split("/")[-1])
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
			ttk.Button(
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
