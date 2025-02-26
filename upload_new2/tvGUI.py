import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class TVPosterAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load the clustering models and data
        self.scaler = joblib.load('scaler.pkl')
        self.pca_model = joblib.load('pca_model.pkl')
        self.cluster_model = joblib.load('best_cluster_model.pkl')
        self.data = pd.read_csv('combined_data.csv')

        # Train regression models for year and rating
        self.train_regression_models()

        # Setup UI
        self.title("TV Show Poster Analyzer")
        self.geometry("800x600")
        self.setup_ui()

    def train_regression_models(self):
        """Train regression models for year and rating prediction"""
        # Extract RGBW features from the original dataset
        feature_cols = ['PC1', 'PC2', 'PC3']  # Using PCA components as they contain RGBW information
        X = self.data[feature_cols].values
        
        # Train year prediction model
        y_year = self.data['year'].values
        self.year_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.year_model.fit(X, y_year)
        
        # Train rating prediction model
        y_rating = self.data['rating'].values
        self.rating_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rating_model.fit(X, y_rating)
        
        # Calculate and print model performance
        year_pred = self.year_model.predict(X)
        rating_pred = self.rating_model.predict(X)
        
        year_mae = np.mean(np.abs(y_year - year_pred))
        rating_mae = np.mean(np.abs(y_rating - rating_pred))

        joblib.dump(self.year_model, 'year_model.pkl')
        joblib.dump(self.rating_model, 'rating_model.pkl')
        
        print(f"Year prediction MAE: {year_mae:.2f} years")
        print(f"Rating prediction MAE: {rating_mae:.2f} points")

    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Image selection button
        self.select_btn = ttk.Button(main_frame, text="Select Poster Image", command=self.select_image)
        self.select_btn.grid(row=0, column=0, columnspan=2, pady=10)

        # Image display area
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Genre predictions
        self.genre_var = tk.StringVar()
        ttk.Label(results_frame, text="Predicted Genres:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(results_frame, textvariable=self.genre_var).grid(row=0, column=1, sticky=tk.W)

        # Rating prediction
        self.rating_var = tk.StringVar()
        ttk.Label(results_frame, text="Predicted Rating:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(results_frame, textvariable=self.rating_var).grid(row=1, column=1, sticky=tk.W)

        # Year prediction
        self.year_var = tk.StringVar()
        ttk.Label(results_frame, text="Predicted Year:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(results_frame, textvariable=self.year_var).grid(row=2, column=1, sticky=tk.W)

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff")]
        )
        if file_path:
            self.analyze_image(file_path)

    def extract_color_features(self, image_path):
        # Read and process image
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        # Resize for consistency
        img_resized = cv2.resize(img, (224, 336))
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Calculate RGBW values
        r, g, b = cv2.split(img_rgb)
        w = (r + g + b) / 3  # White component
        features = np.array([r.mean(), g.mean(), b.mean(), w.mean()])
        
        return features

    def analyze_image(self, image_path):
        try:
            # Extract color features
            color_features = self.extract_color_features(image_path)
            if color_features is None:
                return
            
            # Create initial feature vector with just RGBW values
            initial_features = np.array([
                color_features[0],  # R mean
                color_features[1],  # G mean
                color_features[2],  # B mean
                color_features[3],  # W mean
                0,  # Temporary placeholder for rating
                0   # Temporary placeholder for year
            ])

            # Scale and transform initial features
            initial_scaled = self.scaler.transform(initial_features.reshape(1, -1))
            initial_pca = self.pca_model.transform(initial_scaled)
            initial_pca = initial_pca[:, :3]

            # Get initial predictions
            initial_year = self.year_model.predict(initial_pca)[0]
            initial_rating = self.rating_model.predict(initial_pca)[0]

            # Create final feature vector using the predictions
            features = np.array([
                color_features[0],  # R mean
                color_features[1],  # G mean
                color_features[2],  # B mean
                color_features[3],  # W mean
                initial_rating,     # Use predicted rating
                initial_year       # Use predicted year
            ])

            # Scale features again with the predictions included
            features_scaled = self.scaler.transform(features.reshape(1, -1))

            # Apply PCA transformation
            features_pca = self.pca_model.transform(features_scaled)

            # Select only the first 3 PCA components
            features_pca = features_pca[:, :3]

            # Get final predictions using the updated feature vector
            predicted_year = int(round(self.year_model.predict(features_pca)[0]))
            predicted_rating = round(self.rating_model.predict(features_pca)[0], 1)

            # Get cluster prediction
            cluster = self.cluster_model.predict(features_pca)[0]

            # Get genre distribution for the predicted cluster
            cluster_data = self.data[self.data['cluster'] == cluster]
            genre_columns = [col for col in self.data.columns if col.startswith('genre_')]
            genre_dist = cluster_data[genre_columns].mean()
            
            # Get top 3 genres
            top_genres = genre_dist.nlargest(3)
            genre_predictions = ", ".join([
                f"{genre.replace('genre_', '')} ({score:.1%})"
                for genre, score in top_genres.items()
            ])

            # Display results
            self.genre_var.set(genre_predictions)
            self.rating_var.set(f"{predicted_rating:.1f}")
            self.year_var.set(str(predicted_year))

            # Display image
            self.display_image(image_path)
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            self.genre_var.set("Error during analysis")
            self.rating_var.set("N/A")
            self.year_var.set("N/A")

    def display_image(self, image_path):
        # Open and resize image for display
        image = Image.open(image_path)
        image.thumbnail((300, 450))  # Resize maintaining aspect ratio
        photo = ImageTk.PhotoImage(image)
        
        # Update image display
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference

if __name__ == "__main__":
    app = TVPosterAnalyzer()
    app.mainloop()