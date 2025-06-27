from ml.models import *

import pandas as pd
import numpy as np
import tqdm
import time
import sys


pd.set_option('display.max_columns', 10) 



def eval(df, model = None, n = 20, n_in = 5):
    rand_idxs = np.random.randint(0, df.shape[0], size=(n, n_in))

    start = time.time()
    _ = [model.predict(list(idx)) for idx in rand_idxs]
    end = time.time()

    return (end - start)/n






if __name__ == '__main__':
    print('loading')
    df = pd.read_csv('data/netflix_clean.csv')
    df['type'] = df['type'].map({'TV Show': 0, 'Movie': 1})
    df = df.drop(columns=['show_id', 'duration'])
    #print(df.head())
    #print(list(df.columns))

    selected =   ['type', 'title', 'director', 'cast', 'country', 'release_year', 'rating', 'listed_in', 'description']
    w = np.array([    .3,     0.2,        0.5,    0.5,       0.2,            0.5,        2,           4,            3])



    for model, m_name in zip([MLOVIE(), KNN()], ["MLOVIE", "KNN"]):
        model.load()
        print(f"average time {m_name}: \t{eval(df, model, n = 20)} \t s")
