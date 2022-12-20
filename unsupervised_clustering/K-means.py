
import json
import numpy as np
import os

import os.path as osp
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from tqdm import tqdm
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.gmeans import gmeans
from pyclustering.utils import read_sample


from preprocess import clean_org_name


def fit_KMeans(loc: str):
    df = pd.read_csv(osp.join(result_loc, 'train_data_20.csv'))
    with open(osp.join(result_loc, 'uq_words.json'), 'r') as fp:
        uq_words = json.load(fp)

    org_vecs = []
    org_names = df['organization_name'].values.tolist()
    weights_1 = [1, 0.8, 0.7, 0.6, 0.4, 0.3]
    weights_2= [1, 0.8]
    
    print('Generating vectors')
    for org_name in org_names:
        vec = np.zeros(len(uq_words))
        ws = clean_org_name(org_name).split(' ')
        # ws = org_name.split(' ')
        for idx, w in enumerate(ws):
            if ws[0].isnumeric():
                if w in uq_words.keys() and idx < len(weights_2):
                    vec[uq_words[w]] = weights_2[idx]
            else:
                if w in uq_words.keys() and idx < len(weights_1):
                    vec[uq_words[w]] = weights_1[idx]

        org_vecs.append(vec)    

    
    # print('Performing PCA')
    # pca = PCA(n_components=1000)
    # X = pca.fit_transform(np.array(org_vecs))
    

    print('performing LSA')
    lsa = make_pipeline(TruncatedSVD(n_components=400), Normalizer(copy=False))
    X_lsa = lsa.fit_transform(np.array(org_vecs))

    # print('finding out k')
    # 
    # gmeans_instance = gmeans(X_lsa, repeat=1).process()
    # clusters = gmeans_instance.get_clusters()
    # print(len(clusters))
    # 
    # 
    # minibatch_kmeans = MiniBatchKMeans(
    # n_clusters=10000,
    # batch_size= 1000,
    # random_state=0,
    # max_iter=10)
    # 
    # print('Fitting Model')
    # clusters= minibatch_kmeans.fit(X_lsa)
    #X = np.array(org_vecs)
    print('Fitting k-means')
    kmeans = KMeans(n_clusters=385)
    clusters = kmeans.fit(X_lsa)

   
    pred= []
    for vec in tqdm(X_lsa, desc='Making predictions: '):
        pred.append(clusters.predict(vec[np.newaxis, :]))
    
    if 'clean_organization_name' not in df.columns:
        clean_names = []
        for name_ in org_names:
            clean_names.append(clean_org_name(name_)) 

        df['clean_organization_name'] = clean_names

    df['Predicted Cluster'] = pred
    df.to_csv(osp.join(result_loc, 'pred_20.csv'), index=False)



if __name__ == "__main__":
    result_loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results"
    fit_KMeans(loc=result_loc)
