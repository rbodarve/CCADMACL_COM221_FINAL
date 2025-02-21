import os
import traceback

import joblib

class PosterRatePredictor:
	"""
	`PosterRatePredictor` class is responsible for predicting the rating of a movie
	based on the movie's poster. This class is responsible for loading the model,
	processing the image, and predicting the rating of the movie.

	Using `joblib`, the model is loaded from the `model` directory. The model is a
	"""