from ml.models import *
from sentence_transformers import SentenceTransformer


def training(df_clean, selected, w):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    mlovie = MLOVIE(model)
    mlovie.fit(df_clean, selected, w)

    mlovie.save()






if __name__ == 'main':
    selected =   ['title', 'director', 'cast', 'country', 'release_year',  'listed_in', 'description']
    w = np.array([ .1,       0.4,        1,    0.1,       0.1,             2,            2])
    df_clean = 0
    training(selected, w)