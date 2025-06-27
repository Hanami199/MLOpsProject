from ml.models import *
# from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

def training(df_clean, selected, w):
    model = 0#SentenceTransformer('all-MiniLM-L6-v2')
    mlovie = MLOVIE(model)
    mlovie.fit(df_clean, selected, w)

    mlovie.save()






if __name__ == '__main__':
    selected =   ['title', 'director', 'cast', 'country', 'release_year',  'listed_in', 'description']
    w = np.array([ .1,       0.4,        1,    0.1,       0.1,             2,            2])
    df = pd.read_csv('data/netflix_clean.csv')
    df = df.drop(columns=['show_id', 'duration'])
    print(list(df.columns))
    
    # training(selected, w)