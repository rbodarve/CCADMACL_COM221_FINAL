import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image

#########################
### PRIVATE VARIABLES ###
#########################

__lastDir: str = "~/Downloads"
"""
Holds the last directory where the user opened a file dialog. This is used
to remember the last directory the user opened a file dialog to make it easier
for the user to navigate to the last directory they opened.
"""

#########################
### HANDLER PROCESSES ###
#########################

def selectImage(previewWidget: ttk.Widget | tk.Widget = None) -> str:
	"""
	Opens a file dialog to select an image file. If the `previewWidget` is
	provided, the selected image file will be displayed in the application.

	:param previewWidget: The widget where the selected image will be displayed.
	:type previewWidget: ttk.Widget | tk.Widget

	:return: The selected image file's path.
	:rtype: str
	"""
	# Type check the parameters
	assert isinstance(previewWidget, tk.Widget) or isinstance(previewWidget, ttk.Widget) or previewWidget is None, "The preview widget must be a `tk.Widget` object, `ttk.Widget` object, or `None`."

	# Get access to the global variable(s)
	global __lastDir

	# Open a file dialog to select an image file
	file = filedialog.askopenfilename(
		title="Select an image file",
		filetypes = [("Image files", "*.png *.jpg *.jpeg")],
		initialdir = __lastDir
	)

	# Check if a file was selected. If so, show the image in the application
	if file:
		print(f"Selected file: {file}")

		# Update the last directory
		__lastDir = file

		if previewWidget:
			showImage(previewWidget, file)

	# Return the selected file
	return file

def showImage(widget: ttk.Label | tk.Label, image: str) -> str:
	"""
	Displays the selected image in the application.

	:param widget: The widget where the image will be displayed.
	:type widget: tk.Label

	:param image: The image file to be displayed.
	:type image: str

	:return: The displayed image file.
	:rtype: str
	"""
	# Type check the parameters
	assert isinstance(widget, tk.Label) or isinstance(widget, ttk.Label), "The widget must be a `tk.Label` object or `ttk.Label` object."
	assert isinstance(image, str), "The image must be a string."

	# Check if required parameters are provided
	assert widget, "The widget is required."
	assert image, "The image is required."

	if image:
		# Open the image file and some variable preparation
		img = Image.open(image)
		imgName = image.split("/")[-1]
		size = img.size
		maxSize = (
			widget.winfo_width() - 6,
			widget.winfo_height() - 6
		)

		indexToCompare = 0 if size[0] > size[1] else 1
		aspectRatio = None

		if indexToCompare == 0:
			aspectRatio = maxSize[0] / size[0]
		else:
			aspectRatio = maxSize[1] / size[1]

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
		print(f"Image: {image}")
		print(f"Image name: {imgName}")
		# Create a new image with a transparent background in a square shape
		newImg = Image.new("RGBA", maxSize, (255, 255, 255, 0))
		newImg.paste(img, (x, y))

		photo = ImageTk.PhotoImage(image = newImg)
		widget.configure(text = image, image = photo)
		# widget.image = photo
		widget.update()
	
	return image