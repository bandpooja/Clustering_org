import threading
import pandas as pd
import numpy as np
import os as osp


final_df = pd.read_pickle('C://Users//BandalPo//OneDrive - Government of Ontario//Documents//Clustering_org//data_result.pkl')
df= pd.read_csv(osp.path.join(r"C:\\Users\\BandalPo\\OneDrive - Government of Ontario\\Documents\\cluster_results", 'final.csv'))
point= final_df['center'][70]
pred_list=[]
suggestions={}


matrix= np.array_split(final_df,3)

#matrix = [[1, 2],[3, 4],[5, 6]]

def min(n, **total):
    if n==0:
        l=0
    else:
        l=len(matrix[n-1])-1

    for i in range(l,len(matrix[n])):
        distance= np.linalg.norm(point - matrix[n]['center'][i])
        if distance < matrix[n]['radius'][i]:
            pred_list.append(df.loc[df.number == matrix[n]['group'][i], 'organization_name'].values[0])
        elif minThreads["minThreads"] > distance - matrix[n]['radius'][i]:
            minThreads['minThreads'] = distance - matrix[n]['radius'][i]
            suggestions[df.loc[df.number == matrix[n]['group'][i], 'organization_name'].values[0]]= minThreads["minThreads"]

        


minThreads ={"minThreads":max(0, np.linalg.norm(point - matrix[0]['center'][0]) -matrix[0]['radius'][0])}

for i in range(len(matrix)):
    t = threading.Thread(target=min, args=(i,), kwargs=minThreads)
    print('thread ',i)
    t.start()
print(minThreads['minThreads'])
        
