import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from recomandation_models import  DataScaler, KNN, MLOVIE

def model_recommendation(model_type, film_list_id):
    """
    This function takes a model type and a film list as input and returns a recommendation.
    """

    # https://www.kaggle.com/datasets/infamouscoder/dataset-netflix-shows
    # https://www.kaggle.com/code/samad0015/eda-on-netflix-shows
    path_encoded = "netflix_encoded.csv"
    path_exposition = "netflix_titles.csv"
    df = pd.read_csv(path_encoded)
    df_exposition = pd.read_csv(path_exposition)
    
    film_and_distances = []

    # KNN part
    if model_type == "KNN":
        # Call the DataScaler class to scale the features
        ds = DataScaler(df)
        df = ds.scale_feature_by_factor('duration_final', 0.03)
        df = ds.scale_feature_by_factor('release_year', 0.001)
        df = ds.scale_feature_by_factor('rating', 2)

        df = ds.scale_all_features_by_factor("cast", 1.5)
        df = ds.scale_all_features_by_factor("director", 1.5)
        df = ds.scale_all_features_by_factor("country", 1.5)
        df = ds.scale_all_features_by_factor("listed_in", 4)
        X = ds.generate_X()
        # Call the KNN class to fit the model
        knn = KNN()
        knn.fit(X)
        # Predict the films based on the film list id
        for film_id in film_list_id:
            film_idx = np.where(df['show_id'] == film_id)[0].any()
            films, distances = knn.predict(film_idx)
            film_and_distances.append(list(zip(films, distances)))
    
    # MLOVIE part
    elif model_type == "MLOVIE":
        #### from here...
        model = SentenceTransformer('all-MiniLM-L6-v2')
        selected =   ['title', 'director', 'cast', 'country', 'release_year',  'listed_in']
        weight = np.array([ 2,       0.3,        0.5,    0.1,       0.5,             4])
        weight = weight/weight.sum()
        weight_dict = {}
        for name, weight in zip(selected, weight):
            weight_dict[name] = weight
        #### ...to here we can find a way to pack this information in a class
        mlovie = MLOVIE(model)
        mlovie.change_w(weight_dict)
        for film_id in film_list_id:
            film_idx = np.where(df['show_id'] == film_id)[0].any()
            films, scores = mlovie.predict(film_idx)
            film_and_distances.append(list(zip(films, -scores)))
    # Sort the film and distances list
    suggested_film_list = np.sort(film_and_distances, key=lambda x: x[1])[1:6]
    suggested_film_list = [item[0] for item in suggested_film_list]
    return suggested_film_list