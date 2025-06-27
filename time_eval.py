from ml.models import *

import pandas as pd
import numpy as np
import tqdm
import time
import sys
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 10) 
plt.style.use('ggplot')
plt.rcParams['axes.facecolor'] = '#FEFEFE'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['grid.color'] = '#000000'
plt.rcParams['grid.alpha'] = 0.05





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

    # selected =   ['type', 'title', 'director', 'cast', 'country', 'release_year', 'rating', 'listed_in', 'description']
    # w = np.array([    .3,     0.2,        0.5,    0.5,       0.2,            0.5,        2,           4,            3])


    n_idx = 20
    results = np.zeros((2, n_idx))
    x = np.arange(n_idx) + 1

    for i, (model, m_name) in enumerate(zip([MLOVIE(), KNN()], ["MLOVIE", "KNN"])):
        model.load()
        for j in tqdm.tqdm(range(n_idx)):
            results[i, j] = eval(df, model, n = 20, n_in = j+1)
    
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_title("Average time inference KNN vs MLOVIE")
    ax.plot(x, results[1], label = 'KNN', color = '#FBE735', linewidth=3)
    ax.plot(x, results[0], label = 'MLOVIE', color = '#440154', linewidth=3)
    ax.legend()
    ax.set_xlabel('number of movie indexes')
    ax.set_ylabel('time (s)')
    plt.show()

    print(f"average time MLOVIE: \t{results[0]} \t s")
    print(f"average time KNN:    \t{results[1]} \t s")
