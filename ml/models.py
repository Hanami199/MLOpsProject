import numpy as np
import pandas as pd
from tqdm.notebook import tqdm

class KNN:
    def __init__(self, k=10):
        self.k   = k
        self.res = k


    def fit(self, X):
        self.X = X
        self.n, self.d = X.shape


    def predict(self, X):
        n_movies = X.shape[0]
        idxs, distances = np.zeros((n_movies, self.res)), np.zeros((n_movies, self.res))
        
        for i, x in enumerate(X):
            idxs[i] , distances[i] = self._predict(x)
        
        distances, idxs = distances.flatten(), idxs.flatten()
        
        idx_sort = np.argsort(distances)                                       # compute where the score is higher
        idxs_sorted = idxs[idx_sort]                                           # movie indexes with the higher score overall

        filter = ~np.isin(idxs_sorted, X)                                      # remove searched indexes
        _, unique_idx = np.unique(idxs_sorted[filter], return_index=True)      # get where there is the first new number

        return idxs_sorted[filter][np.sort(unique_idx)][:self.k]               # return the first k movie index
           

    def _predict(self, idx):
        x = self.X[idx]
        difference = (x - self.X)
        distances = np.sqrt(np.sum( difference*difference, axis=1))/self.n
        idx = np.argsort(distances)[1:self.res + 1]
        return idx, distances[idx]
    





class MLOVIE:
    def __init__(self, model = None, k = 10):
        self.model      = model
        self.k          = k
        self.res        = k
        self.folder     = "data/"

        self.col_names  = None
        self.n, self.d  = None, None
        self.embeddings = {}
        self.numeric    = {}
        self.w          = {}
        self.type       = {}
        
        self.file_names = ['embeddings.npz', 'numeric.npz', 'w.npz', 'type.npz']


    def fit(self, df, col_names, w = None):
        assert self.model is not None, "model is None"

        self.n, self.d = df.shape
        w = np.ones(n)/n if w is None else w/np.sum(w)
        self.col_names = col_names

        for column, w in tqdm(zip(col_names, w), total=len(col_names)):
            if pd.api.types.is_numeric_dtype(df[column]):
                self.numeric[column] = df[column].to_numpy()
                self.type[column]    = 'numeric'
            else:
                self.embeddings[column] = self.model.encode(df[column], normalize_embeddings=True)
                self.type[column]       = 'str'

            self.w[column] = w


    def _predict(self, x):
        """x is the index of a movie"""
        assert self.col_names is not None, "model not fitted yet"
        scores = np.zeros((self.n, self.d))
        
        for i, name in enumerate(self.col_names):
            if self.type[name] == 'str':
                z = self.embeddings[name][x]  #z = self.model.encode(x[name])
                scores[:, i] = (self.CosineSimilarity(z, self.embeddings[name]))*self.w[name]
            else:
                z = self.numeric[name][x]
                scores[:, i] = self.NumericScore(self.numeric[name], z)*self.w[name]
                
        scores = np.sum(scores, axis=1)
        idx = np.argsort(-scores)[1:self.res+1]
        return idx, scores[idx] 
    
    
    def predict(self, X):
        n_movies = X.shape[0]
        idxs, scores = np.zeros((n_movies, self.res)), np.zeros((n_movies, self.res))
        
        for i, x in enumerate(X):
            idxs[i] , scores[i] = self._predict(x)
        
        scores, idxs = scores.flatten(), idxs.flatten()
        
        idx_sort = np.argsort(-scores)                                         # compute where the score is higher
        idxs_sorted = idxs[idx_sort]                                           # movie indexes with the higher score overall

        filter = ~np.isin(idxs_sorted, X)                                      # remove searched indexes
        _, unique_idx = np.unique(idxs_sorted[filter], return_index=True)      # get where there is the first new number

        return idxs_sorted[filter][np.sort(unique_idx)][:self.k]               # return the first k movie index
                

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
        for i, name in enumerate(self.col_names):
            self.w[name] = w[name] if isinstance(w, dict) else w[i]

    def CosineSimilarity(self, z, X, sort_idx = False):
        z = np.reshape(z, (1, -1))
        norm = (np.linalg.norm(z) * np.linalg.norm(X, axis=1, keepdims=True))
        cosine_similarity = ((X @ z.T) / norm).squeeze()

        return cosine_similarity