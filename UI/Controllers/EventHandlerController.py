import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

from Controllers.Controller import Controller
from Controllers.ServiceController import ServiceController

class EventHandlerController(Controller):
	"""
	This class handles all user events in the application; binding the widgets
	to their respective events processes that are defined within this class.
	"""

	_serviceController: ServiceController = ServiceController.getInstance()
	"""
	Holds the instance of the `ServiceController` class which handles
	the application's service logic. This controller is responsible for
	bridging the gap between the UI and the application's logic.

	Only a single instance of this controller is allowed to exist since its
	design pattern is a singleton.
	"""

	__lastDir = "~/Downloads"
	"""
	Holds the last directory where the user opened a file dialog. This is used
	to remember the last directory the user opened a file dialog to make it easier
	for the user to navigate to the last directory they opened.
	"""

	def selectImage(self, previewWidget: tk.Widget = None) -> str:
		"""
		Opens a file dialog to select an image file. The selected image file will be
		displayed in the application.

		:param previewWidget: The widget where the selected image will be displayed.
		:type previewWidget: tk.Widget

		:return: The selected image file.
		:rtype: str
		"""
		file = filedialog.askopenfilename(
			title="Select an image file",
			filetypes = [("Image files", "*.png *.jpg *.jpeg")],
			initialdir = self.__lastDir
		)
		if file:
			print(f"Selected file: {file}")

			# Update the last directory
			self.__lastDir = file

			if previewWidget:
				self.showImage(previewWidget, file)


	def showImage(self, widget: tk.Label, image: str) -> str:
		"""
		Displays the selected image in the application.

		:param image: The image file to be displayed.
		:type image: str

		:return: The displayed image file.
		:rtype: str
		"""

		if image:
			# Open the image file and some variable preparation
			img = Image.open(image)
			size = img.size
			maxSize = (widget.winfo_width(), widget.winfo_height())
			indexToCompare = 0 if size[0] > size[1] else 1
			aspectRatio = None

			if indexToCompare == 0:
				aspectRatio = size[0] / maxSize[0] if maxSize[0] > size[0] else maxSize[0] / size[0]
			else:
				aspectRatio = size[1] / maxSize[1] if maxSize[1] > size[1] else maxSize[1] / size[1]

			# Resize the image to fit the widget
			newSize = (
				int(size[0] * aspectRatio),
				int(size[1] * aspectRatio)
			)
			img = img.resize(newSize, Image.Resampling.LANCZOS)

			# Calculate the x and y position of the image
			x = abs(int((maxSize[0] - newSize[0]) / 2))
			y = abs(int((maxSize[1] - newSize[1]) / 2))

			print(f"\nMax size: {maxSize}")
			print(f"Image size: {size}")
			print(f"New size: {newSize}")
			print(f"Aspect ratio: {aspectRatio}")
			print(f"Position: ({x}, {y})")
			# Create a new image with a transparent background in a square shape
			newImg = Image.new("RGBA", maxSize, (255, 255, 255, 0))
			newImg.paste(img, (x, y))

			image = ImageTk.PhotoImage(image = newImg)
			widget.configure(image = image)
			widget.image = image
			widget.update()
		
		return image

# Used for testing the `EventHandlerController` class
if __name__ == "__main__":
	import os
	name = os.path.basename(__file__)[:-3]
	print(f"\n\n===== {name} START =====")
	controller1 = EventHandlerController.getInstance()
	controller1.test()

	controller2 = EventHandlerController.getInstance()
	controller2.test()

	print(f"\ncontroller1 == controller2: {controller1 == controller2}")
	print(f"controller1 is controller2: {controller1 is controller2}")
	print(f"id(controller1) == id(controller2): {id(controller1) == id(controller2)}")
	print(f"===== {name} END =====\n\n")

__all__ = ["EventHandlerController"]