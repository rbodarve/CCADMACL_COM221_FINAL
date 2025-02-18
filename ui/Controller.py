import os

import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class Controller():
	"""
	`Controller` class controls what process will be done in the application. This class
	will be filled with methods that will be called by the widgets in the application,
	allowing the application to be interactive. Furthermore, it serves to separate the
	logic of the application from the UI, allowing a more organized, structured, readable,
	and maintainable code.

	This class is the heart of the application, and it is responsible for managing the
	application's logic while interacting with the UI. All UI related widget setups

	This class will be a singleton class, meaning that only one instance of this class
	will be created throughout the application's lifecycle. This is to ensure that the
	application's logic is consistent and that all widgets are interacting with the same
	instance of this class.
	"""

	_instance = None
	"""
	This variable will hold the only instance of the `Controller` class that will be
	created throughout the application's lifecycle.
	"""

	@staticmethod
	def getInstance() -> 'Controller':
		"""
		Returns the only instance of the `Controller` class that will be created throughout
		the application's lifecycle.

		:return: The only instance of the `Controller` class.
		:rtype: Controller
		"""
		if Controller._instance is None:
			Controller._instance = Controller()
		return Controller._instance

	def selectImage(self) -> str:
		"""
		Opens a file dialog to select an image file. The selected image file will be
		displayed in the application.

		:return: The selected image file.
		:rtype: str
		"""
		file = filedialog.askopenfilename(
			title="Select an image file",
			filetypes = [("Image files", "*.png *.jpg *.jpeg")],
			initialdir = "~/Desktop"
		)
		if file:
			print(f"Selected file: {file}")

	def showImage(self, widget: tk.Label, image: str) -> str:
		"""
		Displays the selected image in the application.

		:param image: The image file to be displayed.
		:type image: str

		:return: The displayed image file.
		:rtype: str
		"""

		if image:
			image = Image.open(image)
			image = ImageTk.PhotoImage(image)
			widget.configure(image=image)
			widget.image = image
			widget.pack()

			# TODO: Continue implementing image loading
		
		return image