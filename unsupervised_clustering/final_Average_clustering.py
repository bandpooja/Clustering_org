from collections import defaultdict
import statistics
import numpy as np
import pandas as pd
import math
import string
import re
#from cleanco import cleanco
import pandas as pd
import glob
import json
import os as osp
from preprocess import clean_org_name
from skmultilearn.adapt import MLkNN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import warnings


result_loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results"

def concate_csv():

    # setting the path for joining multiple files
    files = osp.path.join("C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results","pred_*.csv")
    print(files)

    # list of merged files returned
    files = glob.glob(files)
    print(len(files))
    print("Resultant CSV after joining all CSV files at a particular location...");

    # joining files with concat and read_csv
    df = pd.concat(map(pd.read_csv, files), ignore_index=True)
    #df.to_csv(osp.path.join(result_loc, 'final.csv'), index=False)


df= pd.read_csv(osp.path.join(result_loc, 'final.csv'))
with open(osp.path.join(result_loc, 'uq_words.json'), 'r') as fp:
    uq_words = json.load(fp)

def calculate_vectors(org_name):
    weights_1 = [1, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    weights_2= [1, 0.8]

    vec = np.zeros(len(uq_words))
    ws = clean_org_name(org_name).split(' ')
    # ws = org_name.split(' ')
    for idx, w in enumerate(ws):
        if ws[0].isnumeric() and len(ws[0])>2 :
            if w in uq_words.keys() and idx < len(weights_2):
                vec[uq_words[w]] = weights_2[idx]
        else:
            if w in uq_words.keys() and idx < len(weights_1):
                vec[uq_words[w]] = weights_1[idx]
    return vec


# def calculate_average():
#     organization_dictionary={}
#     organization_dictionary_avg={}
#     org_id={}
    
#     for _, row  in df.iterrows():
#         if row['number'] in organization_dictionary:
#             organization_dictionary[row['number']]+=calculate_vectors(row['organization_name'])
#             org_id[row['number']]+=1
#         else:
#             organization_dictionary[row['number']]=calculate_vectors(row['organization_name'])
#             org_id[row['number']] = 1
        
#     for id in organization_dictionary:
#         organization_dictionary_avg[id]= organization_dictionary[id]/org_id[id]

#     return organization_dictionary_avg


def identify_cluster(org_avg, pred):
  vec_name= calculate_vectors(pred)
  item_0 = list(org_avg.items())[0]
  first_item = item_0[1]
  min_outside_cluster = item_0[0]
  min_dist = np.linalg.norm(vec_name - first_item)
  for id in org_avg.keys():
     distance= np.linalg.norm(vec_name - org_avg[id])
     if min_dist > distance:
        min_dist = distance 
        min_outside_cluster= id
  return min_outside_cluster

def accuracy(org_avg):
  count=0
  for _, row  in df.iterrows():
    pred= identify_cluster(org_avg, row['organization_name'])
    if row['number'] == pred:
        count+=1
    else:
        print(row['organization_name'],row['number'], pred)
  acc= (count/len(df))*100
  return acc

def KNN_org():
    df_target=[]
    df_org= []
    df_test_data=[]
    df_test_target=[]
    df_test= pd.read_csv(osp.path.join(result_loc, 'test_set.csv'))
    for _, row  in df.iterrows():
        df_org.append(calculate_vectors(row['organization_name']))
        df_target.append(row['number'])

    # for _, row  in df_test.iterrows():
    #     df_test_data.append(calculate_vectors(row['organization_name']))
    #     df_test_target.append(row['number'])


    #Create KNN Object
    knn = KNeighborsClassifier(n_neighbors=3)
    #Create x and y variable
    x = df_org
    y = df_target

    # x1=df_test_data
    # y1=df_test_target

    knn.fit(x, y)

    # #Predict testing set
    #y_pred = knn.predict(x)
    #Check performance using accuracy
    #print(accuracy_score(y, y_pred))

    # count=0
    # for _, row  in df.iterrows():
    #     pred= knn.predict([calculate_vectors(row['organization_name'])])
    #     if row['number'] == pred:
    #         count+=1
    #     else:
    #         print(row['organization_name'],row['number'], pred)
    # acc= (count/len(df))*100
    
    # return acc

    pred= knn.predict([calculate_vectors('A.C. Masonry')])

    return pred


def multilabel_knn_apply():

    classifier = MLkNN(k=3)
    df_target=[]
    df_org= []

    for _, row  in df.iterrows():
        df_org.append(calculate_vectors(row['organization_name']))
        df_target.append(row['number'])
    
    x = np.array(df_org)
    y = np.array(df_target)
    classifier.fit(x, y)
    predictions = classifier.predict([calculate_vectors('A.C. Masonry')])

    return predictions



if __name__ == '__main__':

    # cluster_cen = calculate_average()
    # print('Calculated average')
    # #print(accuracy(cluster_cen))
    # prediction_text= 'A.C. Masonry'
    # #print(prediction_text ,identify_cluster(cluster_cen,prediction_text))
    
    # result= KNN_org()
    # print(result)

    result= multilabel_knn_apply()
    print(result)



