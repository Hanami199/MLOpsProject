import os
import numpy as np
import pandas as pd
from ml.models import KNN, MLOVIE

class ModelRecommendation:
    def __init__(self, model_type = "MLOVIE", film_list_titles = []):
        """
        This function takes a model type and a film list titles as input and returns a recommendation.

        model_type: KNN or MLOVIE [str]
        film_list_titles: list of titles in "netflix_titles.csv" [list[str]]
        """
        # https://www.kaggle.com/datasets/infamouscoder/dataset-netflix-shows
        # https://www.kaggle.com/code/samad0015/eda-on-netflix-shows
        path_encoded = "./data/netflix_encoded.csv"
        path_exposition = "./data/netflix_titles.csv"
        df = pd.read_csv(path_encoded)
        self.df_exposition = pd.read_csv(path_exposition)
        
        self.film_list_id = [self.df_exposition[self.df_exposition['title'] == title]['show_id'].values[0] for title in film_list_titles]
        
        if model_type == "KNN":
            model = KNN()
            # Check if exist the csv file matrix_weighted.npz
            if not os.path.exists("./data/matrix_weighted.npz"):
                model.save(df)
        elif model_type == "MLOVIE":
            model = MLOVIE()

        # load the model    
        model.load()
        # Predict the films based on the film list id
        film_idx_list = [np.where(df['show_id'] == film_id)[0].item() for film_id in self.film_list_id]
        self.suggested_film_list = model.predict(film_idx_list)
        self.suggested_film_list = [df.iloc[int(idx)]['show_id'] for idx in self.suggested_film_list]

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
    
    def _tune_df(self, df):
        pass