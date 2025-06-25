import sys, os
import numpy as np
import pandas as pd
from utility_tools import DataScaler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../ml")))  # Adjust the path to import from the parent directory
from ..ml.models import KNN, MLOVIE

class model_recommendation:
    def __init__(self, model_type, film_list_titles):
        """
        This function takes a model type and a film list titles as input and returns a recommendation.

        model_type: KNN or MLOVIE [str]
        film_list_titles: list of titles in "netflix_titles.csv" [list[str]]
        """
        # https://www.kaggle.com/datasets/infamouscoder/dataset-netflix-shows
        # https://www.kaggle.com/code/samad0015/eda-on-netflix-shows
        path_encoded = "netflix_encoded.csv"
        path_exposition = "netflix_titles.csv"
        df = pd.read_csv(path_encoded)
        self.df_exposition = pd.read_csv(path_exposition)
        
        self.model_type = model_type
        self.film_list_id = [self.df_exposition[self.df_exposition['title'] == title]['show_id'].values[0] for title in film_list_titles]

        # KNN part
        if self.model_type == "KNN":
            path_weighted = "netflix_weighted.csv"
            # Check if exist the csv file netflix_weighted.csv
            if not os.path.exists(path_weighted):
                df_weighted = df.copy()
                # Call the DataScaler class to scale the features
                ds = DataScaler(df.weighted)
                df.weighted = ds.scale_feature_by_factor('duration_final', 0.03)
                df.weighted = ds.scale_feature_by_factor('release_year', 0.001)
                df.weighted = ds.scale_feature_by_factor('rating', 2)
                df.weighted = ds.scale_all_features_by_factor("cast", 1.5)
                df.weighted = ds.scale_all_features_by_factor("director", 1.5)
                df.weighted = ds.scale_all_features_by_factor("country", 1.5)
                df.weighted = ds.scale_all_features_by_factor("listed_in", 4)
            else:
                df_weighted = pd.read_csv(path_weighted)
                ds = DataScaler(df_weighted)
            X = ds.generate_X()
            # Call the KNN class to fit the model
            knn = KNN()
            knn.fit(X)
            # Predict the films based on the film list id
            film_idx_list = [np.where(df['show_id'] == film_id)[0].any() for film_id in self.film_list_id]
            self.suggested_film_list = knn.predict(film_idx_list)
        
        # MLOVIE part
        elif self.model_type == "MLOVIE":
            mlovie = MLOVIE()
            # mlovie.change_w(weight_dict)
            film_idx_list = [np.where(df['show_id'] == film_id)[0].any() for film_id in self.film_list_id]
            self.suggested_film_list = mlovie.predict(film_idx_list)
        
        self.suggested_film_list = [df.iloc[idx]['show_id'] for idx in self.suggested_film_list]

    def get_title(self):
        """
        This function returns the title of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['title'].values[0] for film_id in self.suggested_film_list]

    def get_description(self):
        """
        This function returns the description of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['description'].values[0] for film_id in self.suggested_film_list]
    
    def get_year(self):
        """
        This function returns the year of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['release_year'].values[0] for film_id in self.suggested_film_list]
    
    def get_listed_in(self):
        """
        This function returns the listed_in of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['listed_in'].values[0] for film_id in self.suggested_film_list]
    
    def get_director(self):
        """
        This function returns the director of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['director'].values[0] for film_id in self.suggested_film_list]
    
    def get_cast(self):
        """
        This function returns the cast of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['cast'].values[0] for film_id in self.suggested_film_list]
    
    def get_country(self):
        """
        This function returns the country of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['country'].values[0] for film_id in self.suggested_film_list]
    
    def get_rating(self):
        """
        This function returns the rating of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['rating'].values[0] for film_id in self.suggested_film_list]
    
    def get_duration(self):
        """
        This function returns the duration of the suggested films.
        """
        return [self.df_exposition[self.df_exposition['show_id'] == film_id]['duration'].values[0] for film_id in self.suggested_film_list]