import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

from Controllers.Controller import Controller

class EventHandlerController(Controller):
	"""
	This class handles all user events in the application; binding the widgets
	to their respective events processes that are defined within this class.
	"""

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