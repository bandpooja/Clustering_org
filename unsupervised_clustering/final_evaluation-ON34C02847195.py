import argparse
from collections import defaultdict
from gettext import find
import json
from multiprocessing import Pool
import numpy as np
import os
import os.path as osp
import pandas as pd
from preprocess import clean_org_name
from sklearn.svm import SVC # "Support vector classifier" 
from sklearn.model_selection import train_test_split  
from tqdm import tqdm


def calculate_vectors(org_name):
    with open(osp.join(result_loc, 'uq_words.json'), 'r') as fp:
        uq_words = json.load(fp)
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


def calculate_std():
  organization_dictionary_std={}
  organization_dictionary = defaultdict(list)

  for _, row  in df.iterrows():
    if row['number'] in organization_dictionary:
      organization_dictionary[row['number']].append(calculate_vectors(row['organization_name']))
    else:
      #print('hi',row['organization_id'])
      organization_dictionary[row['number']].append(calculate_vectors(row['organization_name']))

  for id in organization_dictionary.keys():
    organization_dictionary_std[id]= 2*(np.std(organization_dictionary[id]))
  
  
  return organization_dictionary_std



def calculate_average():
  organization_dictionary={}
  organization_dictionary_avg={}
  org_id={}
  
  for _, row  in df.iterrows():
    if row['number'] in organization_dictionary:
      organization_dictionary[row['number']]+=calculate_vectors(row['organization_name'])
      org_id[row['number']]+=1
    else:
      organization_dictionary[row['number']]=calculate_vectors(row['organization_name'])
      org_id[row['number']] = 1
      
  for id in organization_dictionary:
    organization_dictionary_avg[id]= organization_dictionary[id]/org_id[id]

  return organization_dictionary_avg
        
def make_pickle_file():
    final_df = pd.DataFrame()
    std_dict = calculate_std()
    avg_dict = calculate_average()
    ids = []
    avg = []
    radius = []
    for i in std_dict.keys():
        ids.append(i)
        avg.append(avg_dict[i])
        radius.append(std_dict[i])

    final_df['group']=ids
    final_df['center']=avg
    final_df['radius']=radius

    final_df.to_pickle('data_result.pkl')

def make_predictions(org_name):
    suggestions = {}
    pred_list = []
    final_df = pd.read_pickle('data_result.pkl')
    point= calculate_vectors(org_name)


    for _, row  in final_df.iterrows():

        distance= np.linalg.norm(point - row['center'])
        if distance < (row['radius']):
            pred_list.append(df.loc[df.number == row['group'], 'organization_name'].values[0])

        else:
            suggestions[df.loc[df.number == row['group'], 'organization_name'].values[0]]=  distance - row['radius']

    sorted_suggestion_list= {k: v for k, v in sorted(suggestions.items(), key=lambda item: item[1])}
    
    
    if len(pred_list) == 0:
        result = list(sorted_suggestion_list.keys())[:3]
    elif len(pred_list) == 1:
        result = pred_list+list(sorted_suggestion_list.keys())[:2]
    elif len(pred_list) == 2:
        result = pred_list+list(sorted_suggestion_list.keys())[:1]
    else:
        result = pred_list

    return result

def make_group_predictions(organizationID: str, result_file: str) -> None:
    # region get names from the ID
    url_path = f'http://on34c02847195.cihs.ad.gov.on.ca:8080/api/employee_group/{id}/names'
    response = requests.get(url_path)
    data = response.json()
    print(data)
    names =[]
    for org_name in data:
        names.append(org_name['Organization_name'])
    # endregion

    # region vectorize and make predictions
    org_name_vec = []
    for n in names:
        org_name_vec.append(calculate_vectors(n))
    group_pred= np.array(org_name_vec)

    final_df = pd.read_pickle('data_result.pkl')
    center= np.array(final_df['center'].values.tolist())
    radius= np.array(final_df['radius'].values.tolist())
    c_splits = np.array_split(center, 2)
    r_split= np.array_split(radius, 2)
    A_list= []
    pred = []
    for idx,mat in enumerate(c_splits):
        A= (np.sum((group_pred[:,None] - mat)**2, axis=-1)**.5)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        r= A-r_split[idx]
        result= np.argsort(r)
        for res in list(result):
            A_list=A_list+ list(res[:3])
            
    dic= {x:A_list.count(x) for x in A_list}
    suggestions = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1],reverse=True)}       
    suggestions_keys = list(suggestions.keys())
   
    for i in suggestions_keys:
        pred.append(df.loc[df.number == final_df._get_value(i, 'group'), 'organization_name'].values[0])
    # endregion

    # region write results to a text file
    with open(result_file, "w") as file:
        for p in pred:
            file.write(p)
    # endregion
    return


def accuracy_measure():
    count=0
    for _, row  in tqdm(df.iterrows(),desc='making predictions'):
        pred=make_predictions(row['organization_name'])
        if row['number'] in pred:
            count+=1
        else:
            print(row['organization_name'],pred)
    acc= (count/len(df))*100
    return acc
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--organizationID", "-orgID", type=str,\
        help="organization IDs to make predictions on")
    parser.add_argument("--result_file", "-f", type=str,\
        help=".txt file to save the result in")    

    args = parser.parse_args()
    # global varibles
    result_loc = r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results"
    df= pd.read_csv(osp.join(result_loc, 'final.csv'))

    # final_df = pd.read_pickle('data_result.pkl')
    make_group_predictions(args.organizationID, args.result_file)

       
   
    









    
    
    





