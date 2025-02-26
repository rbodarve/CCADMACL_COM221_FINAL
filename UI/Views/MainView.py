import os, sys

import tkinter as tk
from tkinter import ttk, messagebox

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

	#####################
	# PRIVATE VARIABLES #
	#####################

	__selectedImg: str = None
	"""
	Holds the path of the selected image file. This is used to keep track of the
	selected image file for the application to use when predicting the image's rating
	down the line.
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

		# Label Group
		self.addWidget(
			"labelGroup",
			ttk.Frame(self),
			{
				"strat": "pack",
				"args": {
					"side": tk.TOP,
					"ipady": 10,
					"fill": tk.X
				}
			}
		)

		# > Image Label Group
		self.addWidget(
			"imageLabelGroup",
			ttk.Frame(self.getWidget("labelGroup")),
			{
				"strat": "pack",
				"args": {
					"side": tk.TOP,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > Image "Image" Label
		self.addWidget(
			"imageImageLabel",
			ttk.Label(
				self.getWidget("imageLabelGroup"),
				text = "Image: ",
				font = ("Helvetica", 12),
				anchor = tk.E
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > Image Label
		self.addWidget(
			"imageLabel",
			ttk.Label(
				self.getWidget("imageLabelGroup"),
				text = "No image selected",
				font = ("Helvetica", 12),
				anchor = tk.W
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > Prediction Label Group
		self.addWidget(
			"predictionLabelGroup",
			ttk.Frame(self.getWidget("labelGroup")),
			{
				"strat": "pack",
				"args": {
					"side": tk.TOP,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > Rating Label Group
		self.addWidget(
			"ratingLabelGroup",
			ttk.Frame(self.getWidget("predictionLabelGroup")),
			{
				"strat": "pack",
				"args": {
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > > Rating "Rating" Label
		self.addWidget(
			"ratingRatingLabel",
			ttk.Label(
				self.getWidget("ratingLabelGroup"),
				text = "Rating:",
				font = ("Helvetica", 12),
				anchor = tk.E
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > > Rating Input
		self.addWidget(
			"ratingInput",
			ttk.Entry(
				self.getWidget("ratingLabelGroup"),
				font = ("Helvetica", 12),
				justify = tk.CENTER,
				foreground = "black"
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			},
			additionalData = {
				"textVar": tk.DoubleVar(self, value = None)
			}
		)

		# > > Year Label Group
		self.addWidget(
			"yearLabelGroup",
			ttk.Frame(self.getWidget("predictionLabelGroup")),
			{
				"strat": "pack",
				"args": {
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > > Year "Year" Label
		self.addWidget(
			"yearYearLabel",
			ttk.Label(
				self.getWidget("yearLabelGroup"),
				text = "Year:",
				font = ("Helvetica", 12),
				anchor = tk.E
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > > Year Input
		self.addWidget(
			"yearInput",
			ttk.Entry(
				self.getWidget("yearLabelGroup"),
				font = ("Helvetica", 12),
				justify = tk.CENTER,
				foreground = "black"
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			},
			additionalData = {
				"textVar": tk.IntVar(self, value = None)
			}
		)

		# > Genre Label Group
		self.addWidget(
			"genreLabelGroup",
			ttk.Frame(self.getWidget("labelGroup")),
			{
				"strat": "pack",
				"args": {
					"side": tk.TOP,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > Genre "Genre" Label
		self.addWidget(
			"genreGenreLabel",
			ttk.Label(
				self.getWidget("genreLabelGroup"),
				text = "Genre:",
				font = ("Helvetica", 12),
				anchor = tk.E
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
				}
			}
		)

		# > > Genre Label
		self.addWidget(
			"genreLabel",
			ttk.Label(
				self.getWidget("genreLabelGroup"),
				text = "No prediction yet",
				font = ("Helvetica", 12),
				anchor = tk.W
			),
			{
				"strat": "pack",
				"args": {
					"padx": 5,
					"side": tk.LEFT,
					"fill": tk.X,
					"expand": True
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
				command = self.__selectImgBtnProcess
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
				command = self.__predictBtnProcess
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

	#########################
	### PRIVATE FUNCTIONS ###
	#########################

	def __selectImgBtnProcess(self) -> None:
		"""
		Processes the `Select Image` button click event. This function will open a file dialog
		to select an image file. If an image file is selected, it will be displayed in the application.
		"""
		self.__selectedImg = self._eventHandlerController.selectImage(self.getWidget("imagePreview"))
		self.getWidget("imageLabel").configure(text = self.__selectedImg.split("/")[-1])

	def __predictBtnProcess(self) -> None:
		"""
		Processes the `Predict` button click event. This function will predict the rating of the selected
		image file. If no image file is selected, it will not predict anything.
		"""
		if self.__selectedImg:
			# Fetch the widgets first
			forDisabling = [
				self.getWidget("ratingInput"),
				self.getWidget("yearInput"),
				self.getWidget("selectImgBtn"),
				self.getWidget("predictBtn")
			]

			# Fetch the provided rating and year
			rating = self.getWidgetAdditionalData("ratingInput", "textVar").get()
			year = self.getWidgetAdditionalData("yearInput", "textVar").get()

			# Validate the rating and year
			print(f"\n Rating: {rating} ({type(rating)}) | Year: {year} ({type(year)})")
			validated = (
				self._serviceController.validateVarType(rating, [type(None), float])
				and self._serviceController.validateVarType(year, [type(None), int])
			)

			if not validated:
				messagebox.showwarning("Invalid Input", "Please provide a valid rating and year.")
				return

			# Disable the inputs
			for widget in forDisabling:
				widget.configure(state = "readonly")

			# Predict the genres and display them
			rating, year, genres = self._serviceController.predict(self.__selectedImg)
			self.getWidget("genreLabel").configure(text = genres)
			self.getWidget("ratingInput").configure(text = rating)
			self.getWidget("yearInput").configure(text = year)

			self.getWidgetAdditionalData("ratingInput", "textVar").set(rating)
			self.getWidgetAdditionalData("yearInput", "textVar").set(year)

			# Enable the inputs
			for widget in forDisabling:
				widget.configure(state = "normal")
			# TODO: Implement the new prediction process (including the new input widgets).
		else:
			messagebox.showwarning("No Image Selected", "Please select an image first.")