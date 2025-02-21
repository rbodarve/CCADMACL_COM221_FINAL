class Controller:
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

	__instance = None
	"""
	This variable will hold the only instance of the `Controller` class that will be
	created throughout the application's lifecycle.
	"""

	###################
	### CONSTRUCTOR ###
	###################
	def __init__(self):
		"""
		The constructor of the `Controller` class.

		:raises RuntimeError: This class is a singleton! Use `getInstance()` instead.
		"""
		raise RuntimeError("This class is a singleton! Use `getInstance()` instead.")

	@classmethod
	def getInstance(cls) -> any:
		"""
		Returns the only instance of the `Controller` class that will be created throughout
		the application's lifecycle.

		:return: The only instance of the `Controller` class/subclass.
		:rtype: any
		"""
		if cls.__instance is None:
			cls.__instance = cls.__new__(cls)
		return cls.__instance

	def test(self):
		print(f"Testing Controller class | Class Name: {self.__class__.__name__}")