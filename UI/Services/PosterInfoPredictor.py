import os, re, sys, warnings

import cv2
import joblib
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from tkinter import messagebox

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import AppInfo

warnings.filterwarnings("ignore")

class PosterInfoPredictor:
	"""
	`PosterInfoPredictor` class is responsible for predicting the rating, year, and
	genres of a movie based on the movie's poster. This class is responsible for
	loading the model, processing the image, and predicting the rating of the movie.

	Using `joblib`, the persisted model is loaded from the `model` directory. The
	model is a pre-trained model that is used to predict the rating of the movie
	based on the movie's poster. The model is trained using movie posters scraped
	from IMDb's website, based on the `title.episode.tsv` dataset. The said dataset
	contains 8.79 million rows and 4 columns; consisting of the `tconst`, `parentTconst`,
	`seasonNumber`, and `episodeNumber` columns.

	Among the said 8.79 million rows, only those with unique `parentTconst` values are
	considered. The `parentTconst` is the unique identifier for the TV series. 59k
	unique rows are then scraped and used to train the model.
	"""

	#########################
	### PRIVATE VARIABLES ###
	#########################

	__instance: "PosterInfoPredictor" = None
	"""
	Holds the instance of the `PosterInfoPredictor` class.
	"""

	__clusteringModel: any = None
	"""
	Holds the model that will be used to
	predict the rating of a movie poster.
	"""

	__pcaModel: any = None
	"""
	Holds the PCA model that will be used to
	transform the features of the movie poster.
	"""

	__scalerModel: any = None
	"""
	Holds the scalar model that will be used to
	scale the features of the movie poster.
	"""

	__ratingModel: any = None
	"""
	Holds the rating model that will predict the
	rating based on RGBW.
	"""

	__yearModel: any = None
	"""
	Holds the model that will predict the year
	based on RGBW.
	"""

	__ratingMap: pd.DataFrame = None
	"""
	Holds the mapping of the rating to the cluster.
	"""

	###########################
	### PROTECTED VARIABLES ###
	###########################

	###################
	### CONSTRUCTOR ###
	###################
	def __init__(self):
		"""
		The constructor of the `PosterInfoPredictor` class.
		"""
		raise RuntimeError("This class is a singleton! Use `getInstance()` instead.")

	#################################
	### SINGLETON RELATED METHODS ###
	#################################

	@classmethod
	def getInstance(cls) -> "PosterInfoPredictor":
		"""
		Returns the only instance of the `Controller` class that will be created throughout
		the application's lifecycle.

		:return: The only instance of the `Controller` class/subclass.
		:rtype: any
		"""
		if cls.__instance is None:
			cls.__instance = cls.__new__(cls)
			cls.__instance.__setup()
		return cls.__instance

	def test(self):
		print(f"Testing PosterInfoPredictor class | Class Name: {self.__class__.__name__}")

	#####################
	### CLASS METHODS ###
	#####################

	def __setup(self):
		"""
		Sets up the `PosterInfoPredictor` class.
		"""
		# Sets up the models
		self.__clusteringModel = joblib.load(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/pkl/best_cluster_model.pkl"))
		self.__pcaModel = joblib.load(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/pkl/pca_model.pkl"))
		self.__scalerModel = joblib.load(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/pkl/scaler.pkl"))

		self.__ratingModel = joblib.load(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/pkl/rating.pkl"))
		self.__yearModel = joblib.load(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/pkl/year.pkl"))

		# Load the rating map
		self.__ratingMap = pd.read_csv(AppInfo.resourcePath(f"{AppInfo.RESOURCE_PATH}/{AppInfo.RATING_CSV_SOURCE}"))

	def predict(self, poster: str, rating: float = None, year: int = None, parseOutput: bool = True) -> str:
		"""
		Predicts the rating of the movie based on the movie's poster. Two optional parameters,
		the `rating` and the `year`, can also be provided for a more accurate result,
		preventing the program from predicting the `rating` and `year` values respectively.

		When either the `rating` or `year` or both is missing, the method will
		use a regression model to predict the said values based on the `RGBW` of the
		poster and a built-in **`Rating Map`** of the application.

		:param poster: The path to the movie's poster.
		:type poster: str

		:param rating: The rating of the movie.
		:type rating: float

		:param year: The year the media of the poster was released xor aired.
		:type year: int

		:param parseOutput: By default, set to `True`. When `True`, the returned value 
		:type parseOutput: bool

		:return: The predicted genres of the movie. The genres are already parsed to also show the confidence level of each selected genres.
		:rtype: str
		"""
		assert isinstance(poster, str), f"Invalid poster path: {poster} | {type(poster)}"
		assert os.path.exists(poster), f"Poster does not exist: {poster}"

		# Extract the features from the image
		imageFeatures = self.__extractColorFeatures(poster)
		imageFeatures = pd.DataFrame(imageFeatures, index=[0])

		# Preprocess the features
		processedFeatures = self.__preprocessFeatures(imageFeatures)

		# Predict the rating of the movie
		clusterSection = self.__clusteringModel.predict(processedFeatures)
		clusterSection = clusterSection[0]

		# Predict rating
		if rating is None: rating = round(self.__ratingModel.predict(processedFeatures)[0], 1)

		# Predict which year it was released
		if year is None: year = int(round(self.__yearModel.predict(processedFeatures)[0]))

		# Predict the genres of the movie
		clusterData = self.__ratingMap[self.__ratingMap['cluster'] == clusterSection]
		genresColumns = [col for col in self.__ratingMap.columns if col.startswith("genre_")]
		genreDistrib = clusterData[genresColumns].mean()

		topGenres = genreDistrib.nlargest(3)
		genrePred = ", ".join([
			f"{genre.replace('genre_', '')} ({score:.1%})"
			for genre, score in topGenres.items()
		])

		return (rating, year, genrePred) if parseOutput else (rating, year, genreDistrib)

	#############################
	### IMAGE RELATED METHODS ###
	#############################

	def __extractColorFeatures(self, poster: str) -> dict:
		"""
		Extracts the color features from the image. Specifically,
		the color histogram features from the image which results
		to the RGBW values.

		:param poster: The path to the movie's poster.
		:type image: str

		:return: The extracted color features from the image.
		:rtype: dict
		"""
		# Load the image
		image = cv2.imread(poster)
		posterName = poster.split("/")[-1]
		print(posterName)
		if image is None:
			messagebox.showerror(
				f"Failed to load the image: {poster}",
				f"The file either do not exist or has special unicode characters."
			)

			raise FileNotFoundError(f"Failed to load the image: {poster}")

		# Resize the image
		image = cv2.resize(image, (224, 336))

		# Convert to RGB
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# Calculate RGBW values
		features = {}
		r, g, b = cv2.split(image)
		w = (r + g + b) / 3
		features = {
			"r_mean": r.mean(),
			"g_mean": g.mean(),
			"b_mean": b.mean(),
			"w_mean": w.mean(),
		}

		return features

	def __preprocessFeatures(self, features: pd.DataFrame) -> np.ndarray:
		"""
		Preprocesses the features of the movie poster; scaling, imputing,
		and transforming the features.

		:param features: The features of the movie poster.
		:type features: pd.DataFrame

		:return: The preprocessed features of the movie poster.
		:rtype: np.ndarray
		"""
		# Impute missing values (rating & year)
		if "rating" not in features.columns: features["rating"] = 5.0
		if "year" not in features.columns: features["year"] = year = int(np.mean(self.__ratingMap["year"]))

		# Scale features
		scaledFeatures = self.__scalerModel.transform(features)

		# Apply PCA
		pcaFeatures = self.__pcaModel.transform(scaledFeatures)
		pcaFeatures = pcaFeatures[:, :self.__clusteringModel.n_features_in_]

		return pcaFeatures

	@property
	def clusteringModel(self):
		return self.__clusteringModel

	@property
	def pcaModel(self):
		return self.__pcaModel

	@property
	def scalerModel(self):
		return self.__scalerModel

# Used for testing the `PosterInfoPredictor` class
if __name__ == "__main__":
	import os
	name = os.path.basename(__file__)[:-3]

	print(f"\n\n===== {name} START =====")
	predictor1 = PosterInfoPredictor.getInstance()
	predictor1.test()

	predictor2 = PosterInfoPredictor.getInstance()
	predictor2.test()

	print(f"\npredictor1 == predictor2: {predictor1 == predictor2}")
	print(f"predictor1 is predictor2: {predictor1 is predictor2}")
	print(f"id(predictor1) == id(predictor2): {id(predictor1) == id(predictor2)}")

	print(f"\nRater Model: {predictor1.rater}")
	print(f"PCA Model: {predictor1.pca}")
	print(f"Scaler Model: {predictor1.scaler}")
	print(f"===== {name} END =====\n\n")