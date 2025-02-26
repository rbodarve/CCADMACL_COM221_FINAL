import os, sys

import tkinter as tk
from tkinter import ttk

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Controllers.Controller import Controller
from Controllers.ServiceController import ServiceController

from Services import EventHandlers

class EventHandlerController(Controller):
	"""
	This class handles all user events in the application; binding the widgets
	to their respective events processes that are defined within this class.
	"""

	def selectImage(self, previewWidget: ttk.Widget | tk.Widget = None) -> str:
		"""
		Opens a file dialog to select an image file. The selected image file will be
		displayed in the application.

		:param previewWidget: The widget where the selected image will be displayed.
		:type previewWidget: ttk.Widget | tk.Widget

		:return: The selected image file.
		:rtype: str
		"""
		return EventHandlers.selectImage(previewWidget)

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