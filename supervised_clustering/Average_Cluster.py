from unidecode import unidecode
from collections import defaultdict
import statistics
import numpy as np
import pandas as pd
import math
from common_functions import *

df = pd.read_csv(r"data.csv")


def identify_cluster(org_avg, pred):
  vec_name= calculate_vector(pred)
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
    if row['organization_id'] == identify_cluster(org_avg, row['meta_match_name']):
      count+=1
  acc= (count/len(df))*100
  return acc

if __name__ == '__main__':

    cluster_cen = calculate_average()
    # print(accuracy(cluster_cen))
    prediction_text= 'Community Nursing Homesvillage Retirement'
    print(identify_cluster(cluster_cen,prediction_text))