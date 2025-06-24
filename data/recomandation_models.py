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


class KNN:
    """A simple K-Nearest Neighbors implementation for finding similar items in a dataset.
    It calculates the Euclidean distance between a given point and all points in the training set,
    returning the indices and distances of the k nearest neighbors."""

    def __init__(self, k=10):
        self.k = k

    def fit(self, X):
        self.X_train = X
        self.n, self.d = X.shape

    def predict(self, x):
        difference = (x - self.X_train)
        distances = np.sqrt(np.sum( difference*difference, axis=1))/self.n
        idxs = np.argsort(distances)[1:self.k + 1]
        distances = np.sort(distances)[1:self.k + 1]
        return idxs, distances
    

class MLOVIE:
    """A recommendation model that uses a pre-trained SentenceTransformer to encode text data
    and compute similarity scores for recommendations based on multiple features."""

    def __init__(self,  model, k = 10):
        self.model = model
        self.k = k
        self.folder = "data/"

        self.col_names = None
        self.n, self.d = None, None
        self.embeddings = {}
        self.numeric = {}
        self.w = {}
        self.type = {}
        
        self.file_names = ['embeddings.npz', 'numeric.npz', 'w.npz', 'type.npz']

    def fit(self, df, selected, w = None):
        self.n, self.d = df.shape
        w = np.ones(self.n)/self.n if w is None else w/np.sum(w)  # ATTENTION: changed n in self.n, becouse give me an error in the code
        self.col_names = selected

        for column, w in tqdm(zip(selected, w), total=len(selected)):
            if pd.api.types.is_numeric_dtype(df[column]):
                self.numeric[column]    = df[column].to_numpy()
                self.type[column] = 'numeric'
            else:
                self.embeddings[column] = self.model.encode(df[column], normalize_embeddings=True)
                self.type[column] = 'str'

            self.w[column] = w

    def predict(self, x):
        """"x should be a dictionary"""
        scores = np.zeros((self.n, self.d))

        for i, name in enumerate(self.col_names):
            if self.type[name] == 'str':
                z = self.model.encode(x[name])
                scores[:, i] = (self.CosineSimilarity(z, self.embeddings[name]))*self.w[name]
            else:
                scores[:, i] = self.NumericScore(self.numeric[name], x[name])*self.w[name]
        
        scores = np.sum(scores, axis=1)
        idx = np.argsort(-scores)[1:self.k + 1]  # Exclude the first one (itself)
        return idx, scores[idx]
    
    def save(self):
        assert self.col_names is not None, "model not fitted yet"
        print("Saving into:", os.getcwd())
        
        arg = [self.embeddings, self.numeric, self.w, self.type]
        
        for name, file in zip(self.file_names, arg):
            print(self.folder + name)
            np.savez_compressed(self.folder + name, **file)
        
        with open(self.folder + "db_info.json", "w") as file:
            json.dump([self.col_names, [self.n, self.d]], file)

    def load(self):
        arg = []
        
        for name in self.file_names:
            try:
                with np.load(self.folder + name, allow_pickle=True) as npz_file:
                    arg.append({key: npz_file[key] for key in npz_file.files})
            except Exception as e:
                raise IOError(f"Error loading {self.folder + name}: {str(e)}")

        self.embeddings, self.numeric, self.w, self.type = arg

        with open(self.folder + "db_info.json", "r") as file:
            info = json.load(file)
            self.col_names, (self.n, self.d) = info

    def NumericScore(self, x, X):
        dif = x - X
        return 1 / (np.sqrt(dif * dif) + 1)
    
    def change_w(self, w):
        for name in self.col_names:
            self.w[name] = w[name]

    def CosineSimilarity(self, z, X, sort_idx = False):
        z = np.reshape(z, (1, -1))
        norm = (np.linalg.norm(z) * np.linalg.norm(X, axis=1, keepdims=True))
        cosine_similarity = ((X @ z.T) / norm).squeeze()

        return cosine_similarity