from unidecode import unidecode
from collections import defaultdict
import statistics
import numpy as np
import pandas as pd
import math
from common_functions import *



def calculate_std():
  organization_dictionary_std={}
  organization_dictionary = defaultdict(list)
  df = pd.read_csv(r"data.csv")
  for _, row  in df.iterrows():
    if row['organization_id'] in organization_dictionary:
      organization_dictionary[row['organization_id']].append(calculate_vector(row['meta_match_name']))
    else:
      #print('hi',row['organization_id'])
      organization_dictionary[row['organization_id']].append(calculate_vector(row['meta_match_name']))

  for id in organization_dictionary.keys():
    organization_dictionary_std[id]= np.std(organization_dictionary[id])
  return organization_dictionary_std


def identify_cluster(org_std, org_avg, pred):
  vec_name= calculate_vector(pred)
  pred_list=[]
  
  item_0 = list(org_avg.items())[0]
  first_item = item_0[1]
  min_outside_cluster = item_0[0]
  min_dist = max(0, np.linalg.norm(vec_name - first_item) - 2*org_std[min_outside_cluster])

  for id in org_std.keys():
    distance= np.linalg.norm(vec_name - org_avg[id])
    if distance < (2*org_std[id]):
      pred_list.append(id)
    elif min_dist > distance - 2*org_std[id]:
      min_dist = distance - 2*org_std[id]
      min_outside_cluster= id
  return pred_list, min_outside_cluster



if __name__ == '__main__':
    cluster_cen = calculate_average()
    cluster_std = calculate_std()

    text= 'Extendicare York'

    print(identify_cluster(cluster_std,cluster_cen,text))