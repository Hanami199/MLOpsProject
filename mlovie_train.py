from ml.models import *
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 10) 



def training(df, selected, w, model = None):
    print('\r \ntraining...')
    mlovie = MLOVIE(model)
    mlovie.fit(df, selected, w)
    mlovie.save()






if __name__ == '__main__':
    print('loading')
    model = SentenceTransformer('all-MiniLM-L6-v2')



    selected =   ['type', 'title', 'director', 'cast', 'country', 'release_year', 'rating', 'listed_in', 'description']
    w = np.array([    .3,     0.2,        0.5,    0.5,       0.2,            0.5,        2,           4,            3])


    df = pd.read_csv('data/netflix_clean.csv')

    df['type'] = df['type'].map({'TV Show': 0, 'Movie': 1})
    df = df.drop(columns=['show_id', 'duration'])
    print(df.head())
    print(list(df.columns))
    
    #training(df, selected, w, model)