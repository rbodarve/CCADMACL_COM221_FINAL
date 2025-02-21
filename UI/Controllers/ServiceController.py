from Controllers.Controller import Controller

class ServiceController(Controller):
	"""
	This class is responsible for handling the application's business logic, particularly,
	the prediction of the movie's rating based on the movie's poster. This class will
	interact with the `PosterRatePredictor` class to predict the movie's rating.
	"""

	def predict(self):
		"""
		Predicts the movie's rating based on the movie's poster.
		"""
		print("Predicting the movie's rating...")

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