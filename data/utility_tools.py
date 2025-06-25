import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os
import json
from tqdm.notebook import tqdm

class DataScaler:
    """This class is used to scale the features of a DataFrame.
    It provides methods to scale individual features
    and all features by a given factor. It also provides methods to generate the feature matrix for model training."""

    def __init__(self, df):
        self.df = df

    def scale_feature_by_factor(self, feature, factor):
        self.df[feature] = self.df[feature] * factor
        return self.df

    def scale_all_features_by_factor(self, feature, factor):
        if feature is "cast":
            self.df = self._scale_cast_features(factor)
        elif feature is "director":
            self.df = self._scale_director_features(factor)
        elif feature is "country":
            self.df = self._scale_country_features(factor)
        elif feature is "listed_in":
            self.df = self._scale_listed_in_features(factor)
        return self.df
    
    def generate_X(self):
        return self.df.drop(columns=['show_id', 'title', 'description']).to_numpy(dtype='float32')

    def _scale_cast_features(self, factor):
        # Seleziona tutte le colonne che iniziano con "cast_"
        cast_cols = [col for col in self.df.columns if col.startswith('cast_')]
        # Moltiplica ogni colonna per il fattore
        self.df[cast_cols] = self.df[cast_cols] * factor
        return self.df

    def _scale_director_features(self, factor):
        # Seleziona tutte le colonne che iniziano con "director_"
        director_cols = [col for col in self.df.columns if col.startswith('director_')]
        # Moltiplica ogni colonna per il fattore
        self.df[director_cols] = self.df[director_cols] * factor
        return self.df

    def _scale_country_features(self, factor):
        # Seleziona tutte le colonne che iniziano con "country_"
        country_cols = [col for col in self.df.columns if col.startswith('country_')]
        # Moltiplica ogni colonna per il fattore
        self.df[country_cols] = self.df[country_cols] * factor
        return self.df

    def _scale_listed_in_features(self, factor):
        # Seleziona tutte le colonne che iniziano con "listed_in_"
        listed_in_cols = [col for col in self.df.columns if col.startswith('listed_in_')]
        # Moltiplica ogni colonna per il fattore
        self.df[listed_in_cols] = self.df[listed_in_cols] * factor
        return self.df    