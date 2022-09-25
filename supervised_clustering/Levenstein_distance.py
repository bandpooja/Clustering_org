# standard libraries
import numpy as np
import pandas as pd
import math
import distance



def levenshtein(texts):
    '''
    Levenshtein Distance
    '''
    texts = np.asarray(texts, dtype=object)
    _similarity = np.array([[distance.levenshtein(list(w1),list(w2)) for w1 in texts] for w2 in texts])
    _similarity = -1*_similarity
    return _similarity

if __name__ == '__main__':
    text= ['Halton Healthcare', 'Halton Healthcare Georgetown Hospitalmilton District Hospitaloakville Trafalgar Memorial Hospital']
    text = ['Halton Healthcare', 'Linamar']
    print(levenshtein(text))