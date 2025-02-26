import os, sys
from typing import List, Tuple

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Controllers.Controller import Controller

from UI.Services.PosterInfoPredictor import PosterInfoPredictor

class ServiceController(Controller):
	"""
	This class is responsible for handling the application's business logic, particularly,
	the prediction of the movie's rating based on the movie's poster. This class will
	interact with the `PosterRatePredictor` class to predict the movie's rating.
	"""

	__posterInfoPredictor: "PosterInfoPredictor" = PosterInfoPredictor.getInstance()
	"""
	Holds the instance of the `PosterRatePredictor` class which handles the prediction
	of the movie's rating based on the movie's poster.

	The instance in this object could be replaced anytime during runtime.
	"""

	def predict(self, poster: str) -> Tuple[float, int, str]:
		"""
		Predicts the movie's rating based on the movie's poster.
		The information that will be returned is a tuple containing
		the predicted rating, the predicted year, and the predicted genre(s).

		:param poster: The path to the movie's poster.
		:type poster: str

		:return: The predicted info of the movie.
		:rtype: Tuple[float, int, str]
		"""
		print("\nPredicting the movie's info...")
		return self.__posterInfoPredictor.predict(poster)

	def validateVarType(self, value: any, varTypes: List[type]) -> bool:
		"""
		Validates the given value if it is an instance of the given types.

		:param value: The value to validate.
		:type value: any

		:param varTypes: A list consisting of the types to validate the value.
		:type varTypes: List[type]

		:return: `True` if the value is an instance of any of the given types, `False` otherwise.
		:rtype: bool
		"""
		assert varTypes, "No variable types provided."

		for varType in varTypes:
			if not isinstance(varType, type):
				varType = type(varType) 

			if isinstance(value, varType):
				return True
		return False

# Used for testing the `ServiceController` class
if __name__ == "__main__":
	import os
	name = os.path.basename(__file__)[:-3]
	print(f"\n\n===== {name} START =====")
	controller1 = ServiceController.getInstance()
	controller1.test()

	controller2 = ServiceController.getInstance()
	controller2.test()

	print(f"\ncontroller1 == controller2: {controller1 == controller2}")
	print(f"controller1 is controller2: {controller1 is controller2}")
	print(f"id(controller1) == id(controller2): {id(controller1) == id(controller2)}")
	print(f"===== {name} END =====\n\n")

__all__ = ["ServiceController"]