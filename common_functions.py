

from unidecode import unidecode
from collections import defaultdict
import statistics
import numpy as np
import pandas as pd
import math
from stopwords import stopwords as company_shorts
import string
import re
from cleanco import cleanco
from plot_cluster import *

df = pd.read_csv(r"data.csv")
def calculate_vector(org_name_):
        ## a b c d e f g h i j k l m n o p q r s t u v w x y z D 
  b_list= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  org_name= clean_org_name(org_name_)
 # print(org_name)
  t= unidecode(org_name)
  t=t.lower().replace(" ", '')
  print(t)
  weight=0
  for i,c in enumerate(t):
    if c.isalnum():
      if c.isdigit():
        weight+= fun_val(i)
        b_list[26]+= fun_val(i)
      else:
        weight+= fun_val(i)
        b_list[int(ord(c)-ord('a'))] += fun_val(i)
    else:
       pass
  b_list=np.array(b_list)
  b_list=b_list/weight
  return b_list
  

def calculate_average():
  organization_dictionary={}
  organization_dictionary_avg={}
  org_id={}
  
  for _, row  in df.iterrows():
    if row['organization_id'] in organization_dictionary:
      organization_dictionary[row['organization_id']]+=calculate_vector(row['meta_match_name'])
      org_id[row['organization_id']]+=1
    else:
      organization_dictionary[row['organization_id']]=calculate_vector(row['meta_match_name'])
      org_id[row['organization_id']] = 1
      
  for id in organization_dictionary:
    organization_dictionary_avg[id]= organization_dictionary[id]/org_id[id]

  return organization_dictionary_avg



def calculate_average_plot():
  organization_dictionary={}
  organization_dictionary_avg={}
  org_id={}
  
  for _, row  in df.iterrows():
    if row['organization_id'] in organization_dictionary:
      organization_dictionary[row['organization_id']]+=calculate_vector(row['meta_match_name'])
      org_id[row['organization_id']]+=1
    else:
      organization_dictionary[row['organization_id']]=calculate_vector(row['meta_match_name'])
      org_id[row['organization_id']] = 1
      
  for id in organization_dictionary:
    organization_dictionary_avg[id]= organization_dictionary[id]/org_id[id]

  return org_id,organization_dictionary_avg


def count_duplicate_records():
  
  dup_id= defaultdict(list)
  for _, row  in df.iterrows():
    for _, row_i in df.iterrows():
      if row['organization_id'] != row_i['organization_id'] and row['meta_match_name']== row_i['meta_match_name']:
        i=0
        if i==0:
          dup_id[row['meta_match_name']].append(row['organization_id'])
        dup_id[row['meta_match_name']].append(row_i['organization_id'])
        i+=1
  return dup_id


def clean_org_name(text):
    """Cleans two organization names for comparison

    - Makes string Lower Case
    - Strips Punctuation
    - Removes Company Short Forms (Ltd, lp, inc, corp)
    - Strips any whitespace from the beginning and end of a string

    Arguments:
        text {Str} -- A string to compare

    Returns:
        Str -- Cleaned String for comparison
    """

    original_text = text
    text = str(text).lower()

    # If the text contains parenthesis and not contains "formally" word then also clean the text inside parenthesis

    if("formally" not in text):
        text = text + str([' '+clean_org_name(j) for j in [i[1:-1] for i in re.findall('\([^)]*\)', text)]])

    # Else remove all the content in the parenthesis
    text = re.sub(r'\([^)]*\)', '', text)

    # Removing all the punctuation from the string
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.split(' ')

    # Removing company suffix(stopwords) from the string
    text = ' '.join([word for word in text if word not in company_shorts])

    # Strip any whitespace
    text = text.strip()

    # last layer of cleaning with cleanco library
    text = cleanco(text).clean_name().title()

    # if it removes all the words from the original string then returning the original word itself
    # else returning the clean text

    return original_text if text == '' else text




if __name__ == '__main__':
  print(count_duplicate_records())



